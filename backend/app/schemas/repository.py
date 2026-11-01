from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RepositoryCreate(BaseModel):
    url: str = Field(min_length=1, max_length=500)
    default_branch: str | None = Field(default=None, min_length=1, max_length=120)


class RepositoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    workspace_id: UUID
    provider: str
    full_name: str
    clone_url: str
    default_branch: str | None
    connection_status: str
    created_at: datetime
