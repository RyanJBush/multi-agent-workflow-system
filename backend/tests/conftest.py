"""Shared fixtures for the test suite."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

import app.db.session as session_module
from app.db.session import init_db


@pytest.fixture(autouse=True)
async def _setup_test_db(tmp_path, monkeypatch):
    """Use an isolated temp DB for every test."""
    db_file = str(tmp_path / "test_workflows.db")
    monkeypatch.setattr(session_module, "_DB_PATH", db_file)
    await init_db()


@pytest.fixture
async def client(_setup_test_db):
    from app.main import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
