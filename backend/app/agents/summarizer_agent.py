from app.agents.base import Agent


class SummarizerAgent(Agent):
    name = "summarizer_agent"

    def run(self, payload: dict) -> dict:
        title: str = payload["title"]
        research = payload["research"]
        themes = research.get("key_themes", [])
        risks = research.get("risks", [])

        summary = (
            f"{title}: Focus on {themes[0].lower()} and validate demand quickly. "
            f"Primary execution risk is {risks[0].lower() if risks else 'unclear scope'}"
        )

        return {"summary": summary}
