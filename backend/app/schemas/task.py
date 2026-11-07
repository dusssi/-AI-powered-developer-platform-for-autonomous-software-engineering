from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    repository_id: UUID
    instruction: str = Field(min_length=1, max_length=20_000)
    engine: Literal["fake"] = "fake"
    read_only: bool = True


class TaskEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    sequence: int
    correlation_id: UUID
    engine: str
    event_type: str
    message: str | None
    payload: dict[str, Any]
    occurred_at: datetime


class TaskAttemptResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    attempt_number: int
    engine: str
    status: str
    started_at: datetime | None
    finished_at: datetime | None
    created_at: datetime
    events: list[TaskEventResponse]


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    workspace_id: UUID
    repository_id: UUID
    created_by_id: UUID
    instruction: str
    engine: str
    status: str
    read_only: bool
    created_at: datetime
    updated_at: datetime


class TaskDetailResponse(TaskResponse):
    attempts: list[TaskAttemptResponse]
