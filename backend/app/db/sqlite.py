import sqlite3
from pathlib import Path

from app.core.config import get_settings


def get_connection() -> sqlite3.Connection:
    settings = get_settings()
    db_path = Path(settings.sqlite_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS workflow_runs (
                run_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                status TEXT NOT NULL,
                request_payload TEXT NOT NULL,
                response_payload TEXT NOT NULL,
                error_message TEXT
            )
            """
        )
        conn.commit()
