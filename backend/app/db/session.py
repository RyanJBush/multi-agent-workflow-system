"""Async SQLite session and table initialisation."""

from __future__ import annotations

import aiosqlite

from app.core.config import settings

# Strip the SQLAlchemy-style prefix for direct aiosqlite usage
_DB_PATH = settings.database_url.replace("sqlite+aiosqlite:///", "")


async def get_db() -> aiosqlite.Connection:
    """Yield an open DB connection (caller must close)."""
    return await aiosqlite.connect(_DB_PATH)


async def init_db() -> None:
    """Create tables if they do not exist."""
    async with aiosqlite.connect(_DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS workflow_runs (
                id          TEXT PRIMARY KEY,
                task        TEXT NOT NULL,
                status      TEXT NOT NULL,
                summary     TEXT,
                action_plan TEXT,
                agent_results TEXT,
                error       TEXT,
                created_at  TEXT NOT NULL,
                completed_at TEXT
            )
            """
        )
        await db.commit()
