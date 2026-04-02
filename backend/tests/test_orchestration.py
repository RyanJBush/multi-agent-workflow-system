"""Tests for the orchestration pipeline and agent outputs."""

from __future__ import annotations

import pytest

from app.agents.base import AgentInput
from app.agents.planner import PlannerAgent
from app.agents.research import ResearchAgent
from app.agents.summarizer import SummarizerAgent
from app.orchestration.orchestrator import WorkflowOrchestrator
from app.schemas.workflow import WorkflowRequest


@pytest.mark.asyncio
async def test_research_agent_returns_findings():
    agent = ResearchAgent()
    output = await agent.run(AgentInput(task="Evaluate the state of quantum computing"))
    assert output.status == "success"
    assert output.data is not None
    findings = output.data
    assert len(findings.key_facts) >= 1


@pytest.mark.asyncio
async def test_summarizer_agent_requires_research():
    agent = SummarizerAgent()
    output = await agent.run(AgentInput(task="anything", context={}))
    assert output.status == "failed"
    assert output.error is not None


@pytest.mark.asyncio
async def test_summarizer_agent_with_research():
    from app.schemas.workflow import ResearchFindings

    research = ResearchFindings(
        key_facts=["AI is growing", "Healthcare adoption is rising"],
        gaps=["Long-term safety unknown"],
        sources=["WHO", "Nature"],
    )
    agent = SummarizerAgent()
    output = await agent.run(AgentInput(task="AI in healthcare", context={"research": research}))
    assert output.status == "success"
    assert output.data.summary != ""


@pytest.mark.asyncio
async def test_planner_agent_produces_steps():
    from app.schemas.workflow import SummaryOutput

    summary = SummaryOutput(summary="AI is transforming healthcare delivery.", word_count=7)
    agent = PlannerAgent()
    output = await agent.run(AgentInput(task="AI in healthcare", context={"summary": summary}))
    assert output.status == "success"
    assert len(output.data.steps) >= 3


@pytest.mark.asyncio
async def test_orchestrator_full_pipeline():
    orchestrator = WorkflowOrchestrator()
    response = await orchestrator.run(
        WorkflowRequest(task="Build a roadmap for adopting microservices architecture")
    )
    assert response.status == "completed"
    assert len(response.agent_results) == 3
    assert all(r.status == "success" for r in response.agent_results)
    assert isinstance(response.summary, str) and len(response.summary) > 0
    assert len(response.action_plan) >= 3
    assert response.id is not None
    assert response.completed_at is not None


@pytest.mark.asyncio
async def test_orchestrator_propagates_agent_status_failure(monkeypatch):
    """An agent returning status='failed' without raising must stop the pipeline
    and cause the run to be marked as failed — not completed."""
    from app.agents.base import AgentOutput

    async def _failing_summarizer(self, inp: AgentInput) -> AgentOutput:
        return AgentOutput(
            agent_name="summarizer",
            status="failed",
            error="Injected failure for testing",
        )

    monkeypatch.setattr(SummarizerAgent, "run", _failing_summarizer)

    orchestrator = WorkflowOrchestrator()
    response = await orchestrator.run(
        WorkflowRequest(task="Test that a failed agent stops the pipeline")
    )

    # The whole run must be marked failed
    assert response.status == "failed"
    assert response.error is not None

    # Pipeline must have stopped after the summarizer — planner must NOT have run
    assert len(response.agent_results) == 2
    assert response.agent_results[0].agent_name == "research"
    assert response.agent_results[0].status == "success"
    assert response.agent_results[1].agent_name == "summarizer"
    assert response.agent_results[1].status == "failed"


@pytest.mark.asyncio
async def test_orchestrator_response_structure():
    orchestrator = WorkflowOrchestrator()
    response = await orchestrator.run(
        WorkflowRequest(task="Research the future of electric vehicles in Europe")
    )
    # Verify field names/types
    assert hasattr(response, "id")
    assert hasattr(response, "summary")
    assert hasattr(response, "action_plan")
    assert hasattr(response, "agent_results")
    # All action steps have required fields
    for step in response.action_plan:
        assert step.step >= 1
        assert len(step.action) > 0
