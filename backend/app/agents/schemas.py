from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class AgentEventType(StrEnum):
    TASK_STARTED = "task.started"
    PLAN_CREATED = "plan.created"
    MESSAGE = "message"
    TOOL_REQUESTED = "tool.requested"
    APPROVAL_REQUIRED = "approval.required"
    TOOL_COMPLETED = "tool.completed"
    FILE_CHANGED = "file.changed"
    VERIFICATION_STARTED = "verification.started"
    VERIFICATION_COMPLETED = "verification.completed"
    TASK_COMPLETED = "task.completed"
    TASK_FAILED = "task.failed"
    TASK_CANCELLED = "task.cancelled"


class EngineCapabilities(BaseModel):
    """Features an adapter can safely expose to the platform."""

    model_config = ConfigDict(extra="forbid")

    engine: str = Field(min_length=1, max_length=80)
    version: str | None = Field(default=None, max_length=80)
    streaming: bool = True
    cancellation: bool = True
    structured_tool_events: bool = False
    supports_read_only: bool = True


class AgentTaskContext(BaseModel):
    """Minimum task-scoped context passed from the control plane to an adapter."""

    model_config = ConfigDict(extra="forbid")

    task_id: UUID
    attempt_id: UUID
    actor_id: UUID
    workspace_id: UUID
    repository_id: UUID
    workspace_path: str = Field(min_length=1, max_length=2048)
    instruction: str = Field(min_length=1, max_length=20_000)
    read_only: bool = True
    correlation_id: UUID = Field(default_factory=uuid4)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentEvent(BaseModel):
    """Normalized event emitted by any engine adapter."""

    model_config = ConfigDict(extra="forbid")

    id: UUID = Field(default_factory=uuid4)
    task_id: UUID
    attempt_id: UUID
    correlation_id: UUID
    engine: str = Field(min_length=1, max_length=80)
    type: AgentEventType
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    message: str | None = Field(default=None, max_length=20_000)
    payload: dict[str, Any] = Field(default_factory=dict)
