from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.dependencies import get_current_user
from app.db.session import get_db_session
from app.models.repository import Repository
from app.models.task import Task
from app.models.task_attempt import TaskAttempt
from app.models.user import User
from app.models.workspace import Workspace
from app.schemas.task import TaskCreate, TaskDetailResponse, TaskResponse

router = APIRouter(prefix="/workspaces", tags=["tasks"])
SessionDep = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


async def owned_workspace(workspace_id: UUID, session: AsyncSession, user: User) -> Workspace:
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
    "/{workspace_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    workspace_id: UUID,
    payload: TaskCreate,
    session: SessionDep,
    current_user: CurrentUser,
):
    await owned_workspace(workspace_id, session, current_user)
    repository = await session.scalar(
        select(Repository).where(
            Repository.id == payload.repository_id,
            Repository.workspace_id == workspace_id,
        )
    )
    if repository is None:
        raise HTTPException(status_code=404, detail="Repository not found in this workspace")

    instruction = payload.instruction.strip()
    if not instruction:
        raise HTTPException(status_code=422, detail="Task instruction cannot be blank")

    task = Task(
        workspace_id=workspace_id,
        repository_id=repository.id,
        created_by_id=current_user.id,
        instruction=instruction,
        engine=payload.engine,
        status="queued",
        read_only=payload.read_only,
    )
    session.add(task)
    await session.flush()
    session.add(
        TaskAttempt(
            task_id=task.id,
            attempt_number=1,
            engine=payload.engine,
            status="queued",
        )
    )
    await session.commit()
    await session.refresh(task)
    return task


@router.get("/{workspace_id}/tasks", response_model=list[TaskResponse])
async def list_tasks(
    workspace_id: UUID,
    session: SessionDep,
    current_user: CurrentUser,
):
    await owned_workspace(workspace_id, session, current_user)
    result = await session.scalars(
        select(Task)
        .where(Task.workspace_id == workspace_id)
        .order_by(Task.created_at.desc())
    )
    return list(result.all())


@router.get("/{workspace_id}/tasks/{task_id}", response_model=TaskDetailResponse)
async def get_task(
    workspace_id: UUID,
    task_id: UUID,
    session: SessionDep,
    current_user: CurrentUser,
):
    await owned_workspace(workspace_id, session, current_user)
    task = await session.scalar(
        select(Task)
        .where(Task.id == task_id, Task.workspace_id == workspace_id)
        .options(selectinload(Task.attempts).selectinload(TaskAttempt.events))
    )
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
