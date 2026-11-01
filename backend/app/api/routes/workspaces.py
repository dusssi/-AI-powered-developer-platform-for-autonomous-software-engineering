from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_db_session
from app.models.user import User
from app.models.workspace import Workspace
from app.schemas.workspace import WorkspaceCreate, WorkspaceResponse, WorkspaceUpdate

router = APIRouter(prefix="/workspaces", tags=["workspaces"])
SessionDep = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

@router.post("", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    payload: WorkspaceCreate, session: SessionDep, current_user: CurrentUser
):
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=422, detail="Workspace name cannot be blank")
    workspace = Workspace(owner_id=current_user.id, name=name)
    session.add(workspace)
    await session.commit()
    await session.refresh(workspace)
    return workspace

@router.get("", response_model=list[WorkspaceResponse])
async def list_workspaces(session: SessionDep, current_user: CurrentUser):
    result = await session.scalars(
        select(Workspace).where(Workspace.owner_id == current_user.id)
        .order_by(Workspace.created_at.desc())
    )
    return list(result.all())

async def owned_workspace(workspace_id: UUID, session: AsyncSession, user: User) -> Workspace:
    workspace = await session.scalar(select(Workspace).where(
        Workspace.id == workspace_id, Workspace.owner_id == user.id
    ))
    if workspace is None:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace

@router.get("/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(workspace_id: UUID, session: SessionDep, current_user: CurrentUser):
    return await owned_workspace(workspace_id, session, current_user)

@router.patch("/{workspace_id}", response_model=WorkspaceResponse)
async def update_workspace(
    workspace_id: UUID, payload: WorkspaceUpdate, session: SessionDep, current_user: CurrentUser
):
    workspace = await owned_workspace(workspace_id, session, current_user)
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=422, detail="Workspace name cannot be blank")
    workspace.name = name
    await session.commit()
    await session.refresh(workspace)
    return workspace

@router.delete("/{workspace_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workspace(workspace_id: UUID, session: SessionDep, current_user: CurrentUser):
    workspace = await owned_workspace(workspace_id, session, current_user)
    await session.delete(workspace)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
