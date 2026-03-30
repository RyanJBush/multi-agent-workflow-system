"""LLM service abstraction.

In stub mode (LLM_PROVIDER=stub) all completions return deterministic
templated text so the system runs fully offline without any API key.
"""

from __future__ import annotations

from app.core.config import settings


class LLMService:
    def __init__(self) -> None:
        self._provider = settings.llm_provider

    async def complete(self, prompt: str) -> str:
        if self._provider == "openai":
            return await self._openai_complete(prompt)
        return self._stub_complete(prompt)

    # ------------------------------------------------------------------
    # Stub
    # ------------------------------------------------------------------

    def _stub_complete(self, prompt: str) -> str:
        """Return a deterministic placeholder that is structured enough
        for agents to parse without any external API call."""
        return (
            "STUB_RESPONSE | "
            + prompt[:120].replace("\n", " ")
            + " | key_fact_1 | key_fact_2 | key_fact_3"
        )

    # ------------------------------------------------------------------
    # OpenAI
    # ------------------------------------------------------------------

    async def _openai_complete(self, prompt: str) -> str:  # pragma: no cover
        try:
            import openai  # type: ignore[import]
        except ImportError as exc:
            raise RuntimeError("Install 'openai' to use LLM_PROVIDER=openai") from exc

        client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return response.choices[0].message.content or ""
