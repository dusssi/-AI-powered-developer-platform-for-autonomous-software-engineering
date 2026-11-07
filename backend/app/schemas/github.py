from pydantic import BaseModel, ConfigDict
from uuid import UUID


class GitHubInstallStartResponse(BaseModel):
    install_url: str


class GitHubInstallationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    workspace_id: UUID
    installation_id: int
    account_login: str | None
    status: str
