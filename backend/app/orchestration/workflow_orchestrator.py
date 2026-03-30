from app.agents.planner_agent import PlannerAgent
from app.agents.research_agent import ResearchAgent
from app.agents.summarizer_agent import SummarizerAgent
from app.core.exceptions import AgentExecutionError
from app.schemas.workflow import AgentResult, WorkflowRequest


class WorkflowOrchestrator:
    def __init__(self) -> None:
        self.research_agent = ResearchAgent()
        self.summarizer_agent = SummarizerAgent()
        self.planner_agent = PlannerAgent()

    def run(self, request: WorkflowRequest) -> tuple[str, list[dict], list[AgentResult]]:
        agent_results: list[AgentResult] = []

        try:
            research = self.research_agent.run(
                {
                    "title": request.title,
                    "objective": request.objective,
                    "constraints": request.constraints,
                    "audience": request.audience,
                }
            )
            agent_results.append(
                AgentResult(agent_name=self.research_agent.name, status="completed", output=research)
            )

            summary_payload = self.summarizer_agent.run(
                {"title": request.title, "objective": request.objective, "research": research}
            )
            agent_results.append(
                AgentResult(
                    agent_name=self.summarizer_agent.name,
                    status="completed",
                    output=summary_payload,
                )
            )

            summary_text = summary_payload["summary"]
            planner_payload = self.planner_agent.run({"summary": summary_text, "research": research})
            agent_results.append(
                AgentResult(agent_name=self.planner_agent.name, status="completed", output=planner_payload)
            )
        except Exception as exc:
            raise AgentExecutionError(f"Agent execution failed: {exc}") from exc

        return summary_text, planner_payload["action_plan"], agent_results
