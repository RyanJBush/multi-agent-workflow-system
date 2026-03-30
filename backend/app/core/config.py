from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    llm_provider: str = "stub"
    openai_api_key: str = ""

    database_url: str = "sqlite+aiosqlite:///./workflows.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
