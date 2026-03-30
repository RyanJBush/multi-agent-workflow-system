from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Multi-Agent Workflow Automation System"
    app_env: str = "local"
    api_prefix: str = "/api/v1"
    sqlite_path: str = "./workflows.db"
    frontend_origin: str = "http://localhost:5173"
    llm_mode: str = "mock"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="", case_sensitive=False)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
