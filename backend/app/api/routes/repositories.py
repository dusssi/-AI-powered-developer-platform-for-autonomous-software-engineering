import re
from typing import Annotated
from urllib.parse import urlsplit
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_db_session
from app.models.repository import Repository
from app.models.user import User
from app.models.workspace import Workspace
from app.schemas.repository import RepositoryCreate, RepositoryResponse

router = APIRouter(prefix="/workspaces", tags=["repositories"])
SessionDep = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
_REPO_PART = re.compile(r"^[A-Za-z0-9_.-]+$")


def normalize_github_url(value: str) -> tuple[str, str]:
    """Accept only canonical HTTPS GitHub repository URLs; never fetch the URL here."""
    parsed = urlsplit(value.strip())
    try:
        port = parsed.port
    except ValueError:
        raise HTTPException(status_code=422, detail="Repository URL has an invalid port") from None
    if (
        parsed.scheme != "https"
        or parsed.hostname != "github.com"
        or parsed.username is not None
        or parsed.password is not None
        or port not in (None, 443)
        or parsed.query
        or parsed.fragment
    ):
        raise HTTPException(
            status_code=422,
            detail="Only HTTPS github.com repository URLs are supported",
        )

    parts = [part for part in parsed.path.strip("/").split("/") if part]
    if len(parts) != 2:
        raise HTTPException(status_code=422, detail="URL must have the form https://github.com/owner/repository")
    owner, repository = parts
    if repository.endswith(".git"):
        repository = repository[:-4]
    if not _REPO_PART.fullmatch(owner) or not _REPO_PART.fullmatch(repository):
        raise HTTPException(status_code=422, detail="Repository URL contains invalid characters")
    full_name = f"{owner}/{repository}"
    return full_name, f"https://github.com/{full_name}.git"


async def get_owned_workspace(
    workspace_id: UUID, session: AsyncSession, user: User
) -> Workspace:
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
    "/{workspace_id}/repositories",
    response_model=RepositoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_repository(
    workspace_id: UUID,
    payload: RepositoryCreate,
    session: SessionDep,
    current_user: CurrentUser,
):
    await get_owned_workspace(workspace_id, session, current_user)
    full_name, clone_url = normalize_github_url(payload.url)
    default_branch = payload.default_branch.strip() if payload.default_branch else None
    if payload.default_branch is not None and not default_branch:
        raise HTTPException(status_code=422, detail="Default branch cannot be blank")
    repository = Repository(
        workspace_id=workspace_id,
        provider="github",
        full_name=full_name,
        clone_url=clone_url,
        default_branch=default_branch,
        connection_status="pending_connection",
    )
    session.add(repository)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=409, detail="This repository is already registered in the workspace"
        ) from None
    await session.refresh(repository)
    return repository


@router.get("/{workspace_id}/repositories", response_model=list[RepositoryResponse])
async def list_repositories(
    workspace_id: UUID, session: SessionDep, current_user: CurrentUser
):
    await get_owned_workspace(workspace_id, session, current_user)
    result = await session.scalars(
        select(Repository)
        .where(Repository.workspace_id == workspace_id)
        .order_by(Repository.created_at.desc())
    )
    return list(result.all())


@router.delete(
    "/{workspace_id}/repositories/{repository_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def unregister_repository(
    workspace_id: UUID,
    repository_id: UUID,
    session: SessionDep,
    current_user: CurrentUser,
):
    await get_owned_workspace(workspace_id, session, current_user)
    repository = await session.scalar(
        select(Repository).where(
            Repository.id == repository_id,
            Repository.workspace_id == workspace_id,
        )
    )
    if repository is None:
        raise HTTPException(status_code=404, detail="Repository not found")
    await session.delete(repository)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
