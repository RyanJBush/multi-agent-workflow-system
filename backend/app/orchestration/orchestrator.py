"""Workflow orchestrator — runs the Research → Summarizer → Planner pipeline."""

from __future__ import annotations

import time
from datetime import UTC, datetime
from uuid import uuid4

from app.agents.base import AgentInput
from app.agents.planner import PlannerAgent
from app.agents.research import ResearchAgent
from app.agents.summarizer import SummarizerAgent
from app.schemas.workflow import (
    ActionStep,
    AgentResult,
    PlanOutput,
    ResearchFindings,
    SummaryOutput,
    WorkflowRequest,
    WorkflowResponse,
)
from app.services.llm import LLMService


class WorkflowOrchestrator:
    def __init__(self, llm: LLMService | None = None) -> None:
        _llm = llm or LLMService()
        self._research = ResearchAgent(llm=_llm)
        self._summarizer = SummarizerAgent(llm=_llm)
        self._planner = PlannerAgent(llm=_llm)

    async def run(self, request: WorkflowRequest) -> WorkflowResponse:
        run_id = uuid4()
        created_at = datetime.now(UTC)
        agent_results: list[AgentResult] = []
        task = request.task

        # -------------------------------------------------------------------
        # Stage 1 — Research
        # -------------------------------------------------------------------
        research_findings: ResearchFindings | None = None
        t0 = time.monotonic()
        try:
            research_out = await self._research.run(AgentInput(task=task))
            research_findings = (
                ResearchFindings.model_validate(research_out.data) if research_out.data else None
            )
            agent_results.append(
                AgentResult(
                    agent_name="research",
                    status=research_out.status,
                    output=research_findings.model_dump() if research_findings else None,
                    duration_ms=int((time.monotonic() - t0) * 1000),
                )
            )
        except Exception as exc:
            agent_results.append(
                AgentResult(
                    agent_name="research",
                    status="failed",
                    error=str(exc),
                    duration_ms=int((time.monotonic() - t0) * 1000),
                )
            )
            return self._failed_response(run_id, task, created_at, agent_results, str(exc))

        # -------------------------------------------------------------------
        # Stage 2 — Summarizer
        # -------------------------------------------------------------------
        summary_output: SummaryOutput | None = None
        t0 = time.monotonic()
        try:
            summarizer_out = await self._summarizer.run(
                AgentInput(task=task, context={"research": research_findings})
            )
            summary_output = (
                SummaryOutput.model_validate(summarizer_out.data) if summarizer_out.data else None
            )
            agent_results.append(
                AgentResult(
                    agent_name="summarizer",
                    status=summarizer_out.status,
                    output=summary_output.model_dump() if summary_output else None,
                    duration_ms=int((time.monotonic() - t0) * 1000),
                )
            )
        except Exception as exc:
            agent_results.append(
                AgentResult(
                    agent_name="summarizer",
                    status="failed",
                    error=str(exc),
                    duration_ms=int((time.monotonic() - t0) * 1000),
                )
            )
            return self._failed_response(run_id, task, created_at, agent_results, str(exc))

        # -------------------------------------------------------------------
        # Stage 3 — Planner
        # -------------------------------------------------------------------
        plan_output: PlanOutput | None = None
        t0 = time.monotonic()
        try:
            planner_out = await self._planner.run(
                AgentInput(task=task, context={"summary": summary_output})
            )
            plan_output = PlanOutput.model_validate(planner_out.data) if planner_out.data else None
            agent_results.append(
                AgentResult(
                    agent_name="planner",
                    status=planner_out.status,
                    output=plan_output.model_dump() if plan_output else None,
                    duration_ms=int((time.monotonic() - t0) * 1000),
                )
            )
        except Exception as exc:
            agent_results.append(
                AgentResult(
                    agent_name="planner",
                    status="failed",
                    error=str(exc),
                    duration_ms=int((time.monotonic() - t0) * 1000),
                )
            )
            return self._failed_response(run_id, task, created_at, agent_results, str(exc))

        # -------------------------------------------------------------------
        # Aggregate
        # -------------------------------------------------------------------
        summary_text = summary_output.summary if summary_output else ""
        action_plan: list[ActionStep] = plan_output.steps if plan_output else []

        return WorkflowResponse(
            id=run_id,
            task=task,
            status="completed",
            summary=summary_text,
            action_plan=action_plan,
            agent_results=agent_results,
            created_at=created_at,
            completed_at=datetime.now(UTC),
        )

    # ------------------------------------------------------------------

    @staticmethod
    def _failed_response(
        run_id,
        task: str,
        created_at: datetime,
        agent_results: list[AgentResult],
        error: str,
    ) -> WorkflowResponse:
        return WorkflowResponse(
            id=run_id,
            task=task,
            status="failed",
            agent_results=agent_results,
            created_at=created_at,
            completed_at=datetime.now(UTC),
            error=error,
        )
