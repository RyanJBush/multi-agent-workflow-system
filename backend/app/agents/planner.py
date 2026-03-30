"""Planner Agent — converts a summary into a numbered action plan."""

from __future__ import annotations

from app.agents.base import AgentInput, AgentOutput, BaseAgent
from app.schemas.workflow import ActionStep, PlanOutput, SummaryOutput
from app.services.llm import LLMService

_PROMPT_TEMPLATE = """\
You are a strategic planner.

Based on the summary below, produce a numbered action plan with 3-5 concrete
steps. Each step must include a short action title and a one-sentence rationale.

Task: {task}

Summary:
{summary}

Respond in this exact format (one step per line):
STEP 1: <action> | RATIONALE: <rationale>
STEP 2: <action> | RATIONALE: <rationale>
...
"""

_DEFAULT_STEPS = [
    ("Define scope and objectives", "Ensures alignment before any work begins."),
    ("Conduct in-depth research", "Builds the knowledge base needed for informed decisions."),
    ("Synthesise findings and identify priorities", "Focuses effort on highest-impact areas."),
    ("Develop and test a pilot solution", "Validates the approach with minimal risk."),
    ("Review, refine, and document outcomes", "Captures learnings for future reference."),
]


class PlannerAgent(BaseAgent):
    name = "planner"
    description = "Produces a structured, prioritised action plan from a summary."

    def __init__(self, llm: LLMService | None = None) -> None:
        self._llm = llm or LLMService()

    async def run(self, input: AgentInput) -> AgentOutput:
        summary_output: SummaryOutput | None = input.context.get("summary")
        summary_text = summary_output.summary if summary_output else input.task

        prompt = _PROMPT_TEMPLATE.format(task=input.task, summary=summary_text)
        raw = await self._llm.complete(prompt)
        plan = self._parse(raw)
        return AgentOutput(agent_name=self.name, status="success", data=plan)

    # ------------------------------------------------------------------

    def _parse(self, raw: str) -> PlanOutput:
        steps: list[ActionStep] = []
        for line in raw.splitlines():
            line = line.strip()
            upper = line.upper()
            if not upper.startswith("STEP"):
                continue
            # Format: "STEP N: action | RATIONALE: rationale"
            try:
                after_colon = line.split(":", 1)[1]
                if "|" in after_colon:
                    action_part, rationale_part = after_colon.split("|", 1)
                    action = action_part.strip()
                    rationale = rationale_part.replace("RATIONALE:", "").strip()
                else:
                    action = after_colon.strip()
                    rationale = ""
                steps.append(ActionStep(step=len(steps) + 1, action=action, rationale=rationale))
            except (IndexError, ValueError):
                continue

        if not steps:
            steps = [
                ActionStep(step=i + 1, action=a, rationale=r)
                for i, (a, r) in enumerate(_DEFAULT_STEPS)
            ]

        return PlanOutput(steps=steps, estimated_duration="2-4 weeks")
