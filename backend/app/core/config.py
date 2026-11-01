from functools import lru_cache

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    app_name: str = "BuckLabs Dev API"
    environment: str = "development"
    log_level: str = "INFO"
    api_prefix: str = "/api/v1"
    cors_origins: list[str] = Field(default_factory=list)
    expose_docs: bool = True
    database_url: str = "sqlite+aiosqlite:///./bucklabs_dev.db"
    jwt_secret: SecretStr = SecretStr("dev-only-change-this-secret-before-deploying")
    access_token_minutes: int = Field(default=30, ge=5, le=1440)

    @model_validator(mode="after")
    def validate_production_secrets(self):
        if self.environment.lower() == "production":
            if self.jwt_secret.get_secret_value() == "dev-only-change-this-secret-before-deploying":
                raise ValueError("JWT_SECRET must be configured in production")
            if self.expose_docs:
                raise ValueError("EXPOSE_DOCS must be false in production")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
