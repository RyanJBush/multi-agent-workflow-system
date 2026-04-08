"""Tests for individual agent parsing logic and edge cases."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.agents.base import AgentInput
from app.agents.planner import PlannerAgent
from app.agents.research import ResearchAgent
from app.agents.summarizer import SummarizerAgent
from app.schemas.workflow import ResearchFindings, SummaryOutput

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_llm(return_value: str) -> MagicMock:
    """Return a mock LLMService whose `complete` coroutine returns *return_value*."""
    mock = MagicMock()
    mock.complete = AsyncMock(return_value=return_value)
    return mock


# ---------------------------------------------------------------------------
# ResearchAgent — structured response parsing (lines 49, 51, 53)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_research_parse_key_facts_branch():
    """LLM response with KEY_FACTS: prefix must populate key_facts list."""
    llm = _make_llm("KEY_FACTS: fact one | fact two | fact three")
    agent = ResearchAgent(llm=llm)
    output = await agent.run(AgentInput(task="test task"))
    assert output.status == "success"
    assert "fact one" in output.data.key_facts
    assert "fact two" in output.data.key_facts
    assert "fact three" in output.data.key_facts


@pytest.mark.asyncio
async def test_research_parse_gaps_branch():
    """LLM response with GAPS: prefix must populate gaps list."""
    llm = _make_llm("KEY_FACTS: some fact\nGAPS: open question one | open question two")
    agent = ResearchAgent(llm=llm)
    output = await agent.run(AgentInput(task="test task"))
    assert output.status == "success"
    assert "open question one" in output.data.gaps
    assert "open question two" in output.data.gaps


@pytest.mark.asyncio
async def test_research_parse_sources_branch():
    """LLM response with SOURCES: prefix must populate sources list."""
    llm = _make_llm("KEY_FACTS: some fact\nGAPS: some gap\nSOURCES: Wikipedia | Nature")
    agent = ResearchAgent(llm=llm)
    output = await agent.run(AgentInput(task="test task"))
    assert output.status == "success"
    assert "Wikipedia" in output.data.sources
    assert "Nature" in output.data.sources


@pytest.mark.asyncio
async def test_research_parse_full_structured_response():
    """All three sections are parsed correctly from a well-formed LLM response."""
    raw = "KEY_FACTS: AI is advancing | Costs are falling\nGAPS: Safety unknown\nSOURCES: arXiv"
    llm = _make_llm(raw)
    agent = ResearchAgent(llm=llm)
    output = await agent.run(AgentInput(task="AI trends"))
    assert output.status == "success"
    findings = output.data
    assert "AI is advancing" in findings.key_facts
    assert "Costs are falling" in findings.key_facts
    assert "Safety unknown" in findings.gaps
    assert "arXiv" in findings.sources


@pytest.mark.asyncio
async def test_research_parse_fallback_when_no_key_facts():
    """When the response has no KEY_FACTS: prefix, the fallback extracts pipe tokens."""
    # Stub-like response — no KEY_FACTS prefix
    llm = _make_llm("STUB_RESPONSE | token1 | token2 | token3 | token4")
    agent = ResearchAgent(llm=llm)
    output = await agent.run(AgentInput(task="fallback task"))
    assert output.status == "success"
    # Fallback uses pipe-split tokens from index 1 onward (max 3)
    assert len(output.data.key_facts) >= 1


@pytest.mark.asyncio
async def test_research_parse_uses_task_when_empty_response():
    """When the response is empty, key_facts falls back to the task string."""
    llm = _make_llm("")
    agent = ResearchAgent(llm=llm)
    output = await agent.run(AgentInput(task="my specific task"))
    assert output.status == "success"
    # key_facts should contain the task (truncated to 80 chars)
    assert any("my specific task" in f for f in output.data.key_facts)


# ---------------------------------------------------------------------------
# SummarizerAgent — empty-text fallback (line 65)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_summarizer_parse_empty_text_uses_key_facts():
    """When the LLM returns an empty string, summary falls back to key_facts."""
    findings = ResearchFindings(
        key_facts=["Quantum computing is maturing", "Error rates are dropping", "IBM leads"],
        gaps=["Practical timescales unclear"],
        sources=["Nature"],
    )
    llm = _make_llm("")  # empty response → text will be empty after processing
    agent = SummarizerAgent(llm=llm)
    output = await agent.run(AgentInput(task="Quantum computing", context={"research": findings}))
    assert output.status == "success"
    # Fallback joins first 3 key_facts
    assert "Quantum computing is maturing" in output.data.summary


@pytest.mark.asyncio
async def test_summarizer_parse_stub_prefix_stripped():
    """The 'STUB_RESPONSE | ' prefix is stripped from the summary text."""
    findings = ResearchFindings(key_facts=["Fact A"], gaps=[], sources=[])
    llm = _make_llm("STUB_RESPONSE | This is the actual summary text.")
    agent = SummarizerAgent(llm=llm)
    output = await agent.run(AgentInput(task="test", context={"research": findings}))
    assert output.status == "success"
    assert "STUB_RESPONSE" not in output.data.summary


@pytest.mark.asyncio
async def test_summarizer_requires_research_context():
    """SummarizerAgent returns 'failed' when research context is absent."""
    agent = SummarizerAgent()
    output = await agent.run(AgentInput(task="no research", context={}))
    assert output.status == "failed"
    assert output.error is not None
    assert "research" in output.error.lower()


@pytest.mark.asyncio
async def test_summarizer_pipe_delimited_response():
    """Pipe-delimited stub response uses the first non-empty token as summary."""
    findings = ResearchFindings(key_facts=["fact"], gaps=[], sources=[])
    llm = _make_llm("First part | second part | third part")
    agent = SummarizerAgent(llm=llm)
    output = await agent.run(AgentInput(task="test", context={"research": findings}))
    assert output.status == "success"
    assert output.data.summary == "First part"


@pytest.mark.asyncio
async def test_summarizer_word_count_calculated():
    """word_count matches the number of whitespace-separated tokens in the summary."""
    findings = ResearchFindings(key_facts=["fact"], gaps=[], sources=[])
    llm = _make_llm("one two three four five")
    agent = SummarizerAgent(llm=llm)
    output = await agent.run(AgentInput(task="test", context={"research": findings}))
    assert output.status == "success"
    assert output.data.word_count == 5


# ---------------------------------------------------------------------------
# PlannerAgent — STEP parsing branches (lines 61-72)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_planner_parse_step_with_rationale():
    """STEP lines containing '| RATIONALE:' are parsed into action + rationale."""
    raw = "STEP 1: Define objectives | RATIONALE: Ensures focus\nSTEP 2: Build prototype | RATIONALE: De-risks early"
    llm = _make_llm(raw)
    agent = PlannerAgent(llm=llm)
    output = await agent.run(
        AgentInput(
            task="build a product", context={"summary": SummaryOutput(summary="test", word_count=1)}
        )
    )
    assert output.status == "success"
    steps = output.data.steps
    assert len(steps) == 2
    assert steps[0].action == "Define objectives"
    assert steps[0].rationale == "Ensures focus"
    assert steps[1].action == "Build prototype"
    assert steps[1].rationale == "De-risks early"


@pytest.mark.asyncio
async def test_planner_parse_step_without_rationale():
    """STEP lines without '|' produce a step with an empty rationale."""
    raw = "STEP 1: Just do the thing"
    llm = _make_llm(raw)
    agent = PlannerAgent(llm=llm)
    output = await agent.run(AgentInput(task="simple task"))
    assert output.status == "success"
    assert len(output.data.steps) == 1
    assert output.data.steps[0].action == "Just do the thing"
    assert output.data.steps[0].rationale == ""


@pytest.mark.asyncio
async def test_planner_parse_skips_malformed_step():
    """A 'STEP' line with no colon raises IndexError which is silently skipped."""
    # "STEP" alone has no colon — split(":", 1)[1] raises IndexError
    raw = "STEP\nSTEP 1: Valid action | RATIONALE: Good reason"
    llm = _make_llm(raw)
    agent = PlannerAgent(llm=llm)
    output = await agent.run(AgentInput(task="test"))
    assert output.status == "success"
    # The malformed line is skipped; only the valid step is parsed
    assert len(output.data.steps) == 1
    assert output.data.steps[0].action == "Valid action"


@pytest.mark.asyncio
async def test_planner_parse_no_steps_uses_defaults():
    """When no STEP lines are found, the default 5-step plan is returned."""
    llm = _make_llm("No steps here at all")
    agent = PlannerAgent(llm=llm)
    output = await agent.run(AgentInput(task="no steps task"))
    assert output.status == "success"
    assert len(output.data.steps) == 5
    assert output.data.estimated_duration == "2-4 weeks"


@pytest.mark.asyncio
async def test_planner_uses_task_as_summary_when_context_missing():
    """When no summary context is provided, the planner uses the raw task string."""
    llm = _make_llm("STEP 1: Act on task | RATIONALE: Direct approach")
    agent = PlannerAgent(llm=llm)
    output = await agent.run(AgentInput(task="task without summary"))
    assert output.status == "success"
    # Verify the prompt was constructed (LLM was called once)
    llm.complete.assert_awaited_once()
    call_args = llm.complete.call_args[0][0]
    assert "task without summary" in call_args


# ---------------------------------------------------------------------------
# LLMService — stub behaviour
# ---------------------------------------------------------------------------


def test_llm_stub_returns_string():
    """In stub mode, complete() returns a non-empty deterministic string."""
    import asyncio

    from app.services.llm import LLMService

    llm = LLMService()
    result = asyncio.run(llm.complete("hello"))
    assert isinstance(result, str)
    assert len(result) > 0
    assert "STUB_RESPONSE" in result


@pytest.mark.asyncio
async def test_llm_stub_contains_prompt_excerpt():
    """Stub response embeds the first 120 characters of the prompt."""
    from app.services.llm import LLMService

    llm = LLMService()
    prompt = "A" * 200
    result = await llm.complete(prompt)
    assert "A" * 120 in result
