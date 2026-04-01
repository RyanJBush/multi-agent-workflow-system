"""Tests for /health and workflow endpoints."""

from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_health(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_run_workflow_success(client):
    resp = await client.post(
        "/api/v1/workflows/run",
        json={"task": "Research the impact of AI on healthcare in 2024"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "completed"
    assert data["task"] == "Research the impact of AI on healthcare in 2024"
    assert isinstance(data["summary"], str) and len(data["summary"]) > 0
    assert isinstance(data["action_plan"], list) and len(data["action_plan"]) > 0
    assert len(data["agent_results"]) == 3


@pytest.mark.asyncio
async def test_run_workflow_validation_error(client):
    resp = await client.post("/api/v1/workflows/run", json={"task": "ab"})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_history_endpoint(client):
    # First, run a workflow to ensure history is not empty
    await client.post(
        "/api/v1/workflows/run",
        json={"task": "Plan a product launch for a SaaS startup"},
    )
    resp = await client.get("/api/v1/workflows/history")
    assert resp.status_code == 200
    history = resp.json()
    assert isinstance(history, list)
    assert len(history) >= 1
    item = history[0]
    assert "id" in item
    assert "task" in item
    assert "status" in item


@pytest.mark.asyncio
async def test_get_workflow_not_found(client):
    resp = await client.get("/api/v1/workflows/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_workflow_by_id(client):
    run_resp = await client.post(
        "/api/v1/workflows/run",
        json={"task": "Evaluate renewable energy trends for 2025"},
    )
    run_id = run_resp.json()["id"]
    resp = await client.get(f"/api/v1/workflows/{run_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == run_id
