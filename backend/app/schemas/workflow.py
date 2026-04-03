from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class WorkflowRequest(BaseModel):
    title: str = Field(min_length=5, max_length=120)
    objective: str = Field(min_length=10, max_length=1000)
    constraints: list[str] = Field(default_factory=list)
    audience: str | None = Field(default=None, max_length=120)
    output_format: Literal["action_plan", "brief", "both"] = "both"


class ActionItem(BaseModel):
    task: str
    priority: Literal["high", "medium", "low"]
    rationale: str


class AgentResult(BaseModel):
    agent_name: str
    status: Literal["completed", "failed"]
    output: dict


class WorkflowResult(BaseModel):
    run_id: UUID
    status: Literal["completed", "failed"]
    created_at: datetime
    summary: str
    action_plan: list[ActionItem]
    agent_results: list[AgentResult]
    error_message: str | None = None


class WorkflowRunRecord(BaseModel):
    run_id: UUID
    status: str
    created_at: datetime
    summary: str


class WorkflowHistoryResponse(BaseModel):
    items: list[WorkflowRunRecord]


class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    run_id: UUID | None = None
    details: dict | None = None
