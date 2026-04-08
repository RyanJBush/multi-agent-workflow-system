"""Phase 6 focused API and deterministic workflow tests."""

from __future__ import annotations

import pytest

from app.agents.base import AgentOutput
from app.api.routes import _orchestrator


@pytest.mark.asyncio
async def test_health_returns_provider_and_request_id(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.headers.get("X-Request-ID")
    payload = resp.json()
    assert payload["status"] == "ok"
    assert payload["llm_provider"] in {"stub", "openai"}


@pytest.mark.asyncio
async def test_run_then_history_then_detail_roundtrip(client):
    run_resp = await client.post(
        "/api/v1/workflows/run",
        json={"task": "Create a product launch plan for an AI assistant"},
    )
    assert run_resp.status_code == 200
    run_payload = run_resp.json()

    history_resp = await client.get("/api/v1/workflows/history?limit=5")
    assert history_resp.status_code == 200
    history_payload = history_resp.json()
    assert any(item["id"] == run_payload["id"] for item in history_payload)

    detail_resp = await client.get(f"/api/v1/workflows/{run_payload['id']}")
    assert detail_resp.status_code == 200
    detail_payload = detail_resp.json()
    assert detail_payload["id"] == run_payload["id"]
    assert detail_payload["task"] == run_payload["task"]


@pytest.mark.asyncio
async def test_history_limit_validation_failure(client):
    resp = await client.get("/api/v1/workflows/history?limit=0")
    assert resp.status_code == 422
    body = resp.json()
    assert "request_id" in body


@pytest.mark.asyncio
async def test_workflow_failure_surface_from_agent(monkeypatch, client):
    async def _forced_failure(_input):
        return AgentOutput(
            agent_name="summarizer",
            status="failed",
            error="forced failure for API test",
        )

    monkeypatch.setattr(_orchestrator._summarizer, "run", _forced_failure)

    resp = await client.post(
        "/api/v1/workflows/run",
        json={"task": "Trigger summarizer failure and verify API failed state"},
    )
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["status"] == "failed"
    assert payload["error"] == "forced failure for API test"
    assert payload["agent_results"][1]["agent_name"] == "summarizer"


@pytest.mark.asyncio
async def test_stub_outputs_are_deterministic_for_same_task(client):
    task = "Assess opportunities for AI-powered customer support automation"

    first = await client.post("/api/v1/workflows/run", json={"task": task})
    second = await client.post("/api/v1/workflows/run", json={"task": task})

    assert first.status_code == 200
    assert second.status_code == 200

    first_payload = first.json()
    second_payload = second.json()

    assert first_payload["summary"] == second_payload["summary"]
    assert first_payload["action_plan"] == second_payload["action_plan"]
    assert (
        first_payload["agent_results"][0]["output"] == second_payload["agent_results"][0]["output"]
    )
