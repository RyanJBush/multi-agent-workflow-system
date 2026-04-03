from app.core.config import Settings


def test_frontend_origins_accepts_comma_separated_env_value() -> None:
    settings = Settings(frontend_origins="http://localhost:5173,http://127.0.0.1:5173/")

    assert settings.frontend_origins == ["http://localhost:5173", "http://127.0.0.1:5173"]
