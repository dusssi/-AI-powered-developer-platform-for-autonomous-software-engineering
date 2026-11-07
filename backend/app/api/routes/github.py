import hashlib
import hmac
import json
import secrets
from datetime import UTC, datetime, timedelta
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.config import get_settings
from app.db.session import get_db_session
from app.models.github_installation import GitHubInstallation, GitHubInstallState
from app.models.user import User
from app.models.workspace import Workspace
from app.schemas.github import GitHubInstallStartResponse, GitHubInstallationResponse

router = APIRouter(tags=["github"])
SessionDep = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


async def owned_workspace(workspace_id: UUID, session: AsyncSession, user: User):
    workspace = await session.scalar(
        select(Workspace).where(
            Workspace.id == workspace_id,
            Workspace.owner_id == user.id,
        )
    )
    if workspace is None:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace


@router.post(
    "/workspaces/{workspace_id}/github/install",
    response_model=GitHubInstallStartResponse,
)
async def start_github_installation(
    workspace_id: UUID, session: SessionDep, current_user: CurrentUser
):
    await owned_workspace(workspace_id, session, current_user)
    settings = get_settings()
    if not settings.github_app_slug:
        raise HTTPException(status_code=503, detail="GitHub App integration is not configured")
    raw_state = secrets.token_urlsafe(32)
    state_hash = hashlib.sha256(raw_state.encode()).hexdigest()
    session.add(
        GitHubInstallState(
            workspace_id=workspace_id,
            state_hash=state_hash,
            expires_at=datetime.now(UTC) + timedelta(minutes=10),
        )
    )
    await session.commit()
    install_url = (
        f"https://github.com/apps/{settings.github_app_slug}/installations/new"
        f"?state={raw_state}"
    )
    return GitHubInstallStartResponse(install_url=install_url)


@router.get("/github/setup/callback", response_model=GitHubInstallationResponse)
async def complete_github_installation(
    installation_id: int = Query(gt=0),
    state: str = Query(min_length=32, max_length=200),
    setup_action: str = Query(default="install"),
    session: SessionDep = None,
):
    if setup_action not in {"install", "update"}:
        raise HTTPException(status_code=400, detail="Unsupported GitHub setup action")
    state_hash = hashlib.sha256(state.encode()).hexdigest()
    pending = await session.scalar(
        select(GitHubInstallState).where(GitHubInstallState.state_hash == state_hash)
    )
    now = datetime.now(UTC)
    if pending is None or pending.used_at is not None or pending.expires_at <= now:
        raise HTTPException(status_code=400, detail="Invalid or expired installation state")
    existing = await session.scalar(
        select(GitHubInstallation).where(
            GitHubInstallation.installation_id == installation_id
        )
    )
    if existing is not None and existing.workspace_id != pending.workspace_id:
        raise HTTPException(status_code=409, detail="Installation is already linked elsewhere")
    if existing is None:
        existing = GitHubInstallation(
            workspace_id=pending.workspace_id,
            installation_id=installation_id,
            status="active",
        )
        session.add(existing)
    pending.used_at = now
    await session.commit()
    await session.refresh(existing)
    return existing


@router.get(
    "/workspaces/{workspace_id}/github/installations",
    response_model=list[GitHubInstallationResponse],
)
async def list_github_installations(
    workspace_id: UUID, session: SessionDep, current_user: CurrentUser
):
    await owned_workspace(workspace_id, session, current_user)
    result = await session.scalars(
        select(GitHubInstallation)
        .where(GitHubInstallation.workspace_id == workspace_id)
        .order_by(GitHubInstallation.created_at.desc())
    )
    return list(result.all())


@router.post("/github/webhook", status_code=status.HTTP_202_ACCEPTED)
async def github_webhook(
    request: Request,
    session: SessionDep,
    signature: Annotated[str | None, Header(alias="X-Hub-Signature-256")] = None,
    event: Annotated[str | None, Header(alias="X-GitHub-Event")] = None,
):
    secret = get_settings().github_webhook_secret
    if not secret or not signature or not signature.startswith("sha256="):
        raise HTTPException(status_code=401, detail="Webhook signature is required")
    body = await request.body()
    expected = "sha256=" + hmac.new(
        secret.get_secret_value().encode(), body, hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid webhook JSON") from None

    if event == "installation":
        action = payload.get("action")
        installation_id = payload.get("installation", {}).get("id")
        account_login = payload.get("installation", {}).get("account", {}).get("login")
        if isinstance(installation_id, int):
            installation = await session.scalar(
                select(GitHubInstallation).where(
                    GitHubInstallation.installation_id == installation_id
                )
            )
            if installation is not None:
                if action == "deleted":
                    installation.status = "deleted"
                elif action == "suspend":
                    installation.status = "suspended"
                elif action == "unsuspend":
                    installation.status = "active"
                if account_login:
                    installation.account_login = str(account_login)[:200]
                await session.commit()
    return {"status": "accepted"}
