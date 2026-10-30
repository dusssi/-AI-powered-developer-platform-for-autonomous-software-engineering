from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class WorkspaceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)

class WorkspaceUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=120)

class WorkspaceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    created_at: datetime
