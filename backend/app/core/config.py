from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    llm_provider: str = Field(default="stub", pattern="^(stub|openai)$")
    openai_api_key: str = ""

    log_level: str = "INFO"
    request_id_header: str = "X-Request-ID"

    database_url: str = "sqlite+aiosqlite:///./workflows.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
