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


def test_workflow_request_too_long():
    with pytest.raises(ValidationError):
        WorkflowRequest(task="x" * 2001)


def test_workflow_request_max_length():
    req = WorkflowRequest(task="x" * 2000)
    assert len(req.task) == 2000


def test_workflow_request_min_length():
    req = WorkflowRequest(task="hello")
    assert len(req.task) == 5


def test_action_step_defaults():
    step = ActionStep(step=2, action="Do something")
    assert step.step == 2
    assert step.rationale == ""


def test_plan_output_defaults():
    plan = PlanOutput()
    assert plan.steps == []
    assert plan.estimated_duration == ""


def test_research_findings_with_values():
    findings = ResearchFindings(
        key_facts=["fact1", "fact2"],
        gaps=["gap1"],
        sources=["src1"],
        raw="raw text",
    )
    assert len(findings.key_facts) == 2
    assert findings.raw == "raw text"


def test_agent_result_duration_default():
    r = AgentResult(agent_name="planner", status="success")
    assert r.duration_ms == 0
    assert r.output is None
