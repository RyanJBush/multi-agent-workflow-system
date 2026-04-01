"""Summarizer Agent — condenses research findings into a paragraph."""

from __future__ import annotations

from app.agents.base import AgentInput, AgentOutput, BaseAgent
from app.schemas.workflow import ResearchFindings, SummaryOutput
from app.services.llm import LLMService

_PROMPT_TEMPLATE = """\
You are a professional summarizer.

Condense the following research findings into a single, coherent paragraph
(50-100 words). Be precise and factual.

Task: {task}

Key facts:
{facts}

Gaps:
{gaps}

Respond with only the summary paragraph — no labels or headers.
"""


class SummarizerAgent(BaseAgent):
    name = "summarizer"
    description = "Condenses research findings into a concise summary paragraph."

    def __init__(self, llm: LLMService | None = None) -> None:
        self._llm = llm or LLMService()

    async def run(self, input: AgentInput) -> AgentOutput:
        findings: ResearchFindings | None = input.context.get("research")
        if findings is None:
            return AgentOutput(
                agent_name=self.name,
                status="failed",
                error="Missing research findings in context.",
            )

        facts_text = "\n".join(f"- {f}" for f in findings.key_facts)
        gaps_text = "\n".join(f"- {g}" for g in findings.gaps)

        prompt = _PROMPT_TEMPLATE.format(
            task=input.task,
            facts=facts_text or "No specific facts extracted.",
            gaps=gaps_text or "No gaps identified.",
        )
        raw = await self._llm.complete(prompt)
        summary = self._parse(raw, findings)
        return AgentOutput(agent_name=self.name, status="success", data=summary)

    # ------------------------------------------------------------------

    def _parse(self, raw: str, findings: ResearchFindings) -> SummaryOutput:
        # Strip stub prefix
        text = raw.replace("STUB_RESPONSE | ", "").strip()
        # Clean up pipe-delimited tokens from stub
        if "|" in text:
            parts = [p.strip() for p in text.split("|")]
            text = parts[0] if parts[0] else " ".join(parts)
        if not text:
            text = " ".join(findings.key_facts[:3])
        return SummaryOutput(summary=text, word_count=len(text.split()))
