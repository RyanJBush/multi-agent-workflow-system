"""Research Agent — gathers structured findings about a task."""

from __future__ import annotations

from app.agents.base import AgentInput, AgentOutput, BaseAgent
from app.schemas.workflow import ResearchFindings
from app.services.llm import LLMService

_PROMPT_TEMPLATE = """\
You are a research analyst.

Given the following task, extract:
1. Key facts (3-5 bullet points)
2. Knowledge gaps or open questions (1-3)
3. Potential reference sources or domains

Task: {task}

Respond in this exact format:
KEY_FACTS: <fact1> | <fact2> | <fact3>
GAPS: <gap1> | <gap2>
SOURCES: <source1> | <source2>
"""


class ResearchAgent(BaseAgent):
    name = "research"
    description = "Gathers structured facts, gaps, and sources for a given task."

    def __init__(self, llm: LLMService | None = None) -> None:
        self._llm = llm or LLMService()

    async def run(self, input: AgentInput) -> AgentOutput:
        prompt = _PROMPT_TEMPLATE.format(task=input.task)
        raw = await self._llm.complete(prompt)
        findings = self._parse(raw, input.task)
        return AgentOutput(agent_name=self.name, status="success", data=findings)

    # ------------------------------------------------------------------

    def _parse(self, raw: str, task: str) -> ResearchFindings:
        key_facts: list[str] = []
        gaps: list[str] = []
        sources: list[str] = []

        for line in raw.splitlines():
            line = line.strip()
            if line.upper().startswith("KEY_FACTS:"):
                key_facts = [f.strip() for f in line.split(":", 1)[1].split("|") if f.strip()]
            elif line.upper().startswith("GAPS:"):
                gaps = [g.strip() for g in line.split(":", 1)[1].split("|") if g.strip()]
            elif line.upper().startswith("SOURCES:"):
                sources = [s.strip() for s in line.split(":", 1)[1].split("|") if s.strip()]

        # Fall back: extract pipe-delimited tokens from stub response
        if not key_facts:
            parts = [p.strip() for p in raw.split("|") if p.strip()]
            key_facts = parts[1:4] if len(parts) >= 4 else [task[:80]]

        return ResearchFindings(
            key_facts=key_facts,
            gaps=gaps or ["Further research needed"],
            sources=sources or ["General knowledge"],
            raw=raw,
        )
