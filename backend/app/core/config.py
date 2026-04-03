from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Multi-Agent Workflow Automation System"
    app_env: str = "local"
    api_prefix: str = "/api/v1"
    sqlite_path: str = "./workflows.db"
    frontend_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173"]
    )
    llm_mode: str = "mock"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="", case_sensitive=False)

    @field_validator("frontend_origins", mode="before")
    @classmethod
    def _parse_frontend_origins(cls, value: object) -> list[str]:
        if isinstance(value, str):
            return [origin.strip().rstrip("/") for origin in value.split(",") if origin.strip()]
        if isinstance(value, list):
            return [str(origin).strip().rstrip("/") for origin in value if str(origin).strip()]
        return ["http://localhost:5173", "http://127.0.0.1:5173"]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
