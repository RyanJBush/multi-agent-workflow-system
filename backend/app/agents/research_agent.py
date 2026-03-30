from app.agents.base import Agent


class ResearchAgent(Agent):
    name = "research_agent"

    def run(self, payload: dict) -> dict:
        objective: str = payload["objective"]
        constraints: list[str] = payload.get("constraints", [])

        key_themes = [
            f"Market context for: {objective}",
            "Target audience pain points and alternatives",
            "Competitive positioning opportunities",
        ]

        risks = [
            "Insufficient user validation before execution",
            "Overly broad initial scope may reduce impact",
        ]

        if constraints:
            risks.append(f"Must operate within constraints: {', '.join(constraints[:3])}")

        return {
            "key_themes": key_themes,
            "assumptions": ["Limited time and budget", "One-user MVP first"],
            "risks": risks,
        }
