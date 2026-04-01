"""Tests for Pydantic schema validation."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.schemas.workflow import (
    ActionStep,
    AgentResult,
    PlanOutput,
    ResearchFindings,
    SummaryOutput,
    WorkflowRequest,
)


def test_workflow_request_valid():
    req = WorkflowRequest(task="Analyse market trends in fintech")
    assert req.task == "Analyse market trends in fintech"


def test_workflow_request_too_short():
    with pytest.raises(ValidationError):
        WorkflowRequest(task="hi")


def test_research_findings_defaults():
    findings = ResearchFindings()
    assert findings.key_facts == []
    assert findings.gaps == []
    assert findings.sources == []


def test_summary_output():
    s = SummaryOutput(summary="This is a test summary.", word_count=5)
    assert s.word_count == 5


def test_plan_output():
    plan = PlanOutput(
        steps=[ActionStep(step=1, action="Define scope", rationale="Clarity first.")],
        estimated_duration="1 week",
    )
    assert len(plan.steps) == 1
    assert plan.steps[0].step == 1


def test_agent_result_success():
    r = AgentResult(agent_name="research", status="success", output={"key_facts": []})
    assert r.status == "success"
    assert r.error is None


def test_agent_result_failed():
    r = AgentResult(agent_name="research", status="failed", error="timeout")
    assert r.error == "timeout"
