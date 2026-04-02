from __future__ import annotations

from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Request
# ---------------------------------------------------------------------------


class WorkflowRequest(BaseModel):
    task: str = Field(
        ..., min_length=5, max_length=2000, description="The research or planning task."
    )


# ---------------------------------------------------------------------------
# Per-agent typed outputs
# ---------------------------------------------------------------------------


class ResearchFindings(BaseModel):
    key_facts: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    raw: str = ""


class SummaryOutput(BaseModel):
    summary: str = ""
    word_count: int = 0


class ActionStep(BaseModel):
    step: int
    action: str
    rationale: str = ""


class PlanOutput(BaseModel):
    steps: list[ActionStep] = Field(default_factory=list)
    estimated_duration: str = ""


# ---------------------------------------------------------------------------
# Aggregated agent result stored per-run
# ---------------------------------------------------------------------------


class AgentResult(BaseModel):
    agent_name: str
    status: Literal["success", "failed"]
    output: Any = None
    error: str | None = None
    duration_ms: int = 0


# ---------------------------------------------------------------------------
# Response
# ---------------------------------------------------------------------------


class WorkflowResponse(BaseModel):
    id: UUID
    task: str
    status: Literal["completed", "failed"]
    summary: str = ""
    action_plan: list[ActionStep] = Field(default_factory=list)
    agent_results: list[AgentResult] = Field(default_factory=list)
    created_at: datetime
    completed_at: datetime | None = None
    error: str | None = None


# ---------------------------------------------------------------------------
# History list item (lighter)
# ---------------------------------------------------------------------------


class WorkflowSummary(BaseModel):
    id: UUID
    task: str
    status: Literal["completed", "failed"]
    created_at: datetime
    completed_at: datetime | None = None
