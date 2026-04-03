from app.agents.base import Agent


class PlannerAgent(Agent):
    name = "planner_agent"

    def run(self, payload: dict) -> dict:
        summary: str = payload["summary"]

        plan = [
            {
                "task": "Define target user segment and interview script",
                "priority": "high",
                "rationale": "Reduces risk by validating demand before build-out",
            },
            {
                "task": "Run 5-10 lightweight discovery interviews",
                "priority": "high",
                "rationale": "Generates evidence for highest-value workflow direction",
            },
            {
                "task": "Draft 2-week execution plan from validated insights",
                "priority": "medium",
                "rationale": f"Converts strategy into execution using summary context: {summary[:80]}",
            },
        ]

        return {"action_plan": plan}
