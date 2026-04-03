from app.orchestration.workflow_orchestrator import WorkflowOrchestrator
from app.schemas.workflow import WorkflowRequest


def test_orchestrator_returns_structured_response() -> None:
    orchestrator = WorkflowOrchestrator()
    request = WorkflowRequest(
        title='US campus productivity app research',
        objective='Identify a practical go-to-market approach for first 90 days',
        constraints=['low budget', 'small team'],
        output_format='both',
    )

    summary, action_plan, agent_results = orchestrator.run(request)

    assert isinstance(summary, str)
    assert len(summary) > 0
    assert isinstance(action_plan, list)
    assert len(action_plan) >= 1

    assert len(agent_results) == 3
    assert [result.agent_name for result in agent_results] == [
        'research_agent',
        'summarizer_agent',
        'planner_agent',
    ]
    assert all(result.status == 'completed' for result in agent_results)
