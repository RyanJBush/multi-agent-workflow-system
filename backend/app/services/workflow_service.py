from datetime import datetime, UTC
from uuid import UUID, uuid4

from app.core.exceptions import WorkflowError
from app.db.repository import create_workflow_run, get_workflow_run, list_workflow_runs
from app.orchestration.workflow_orchestrator import WorkflowOrchestrator
from app.schemas.workflow import ActionItem, WorkflowHistoryResponse, WorkflowRequest, WorkflowResult


class WorkflowService:
    def __init__(self, orchestrator: WorkflowOrchestrator | None = None) -> None:
        self.orchestrator = orchestrator or WorkflowOrchestrator()

    def run_workflow(self, request: WorkflowRequest) -> WorkflowResult:
        run_id = uuid4()
        created_at = datetime.now(UTC)

        try:
            summary, action_plan_payload, agent_results = self.orchestrator.run(request)
            action_plan = [ActionItem(**item) for item in action_plan_payload]
            result = WorkflowResult(
                run_id=run_id,
                status="completed",
                created_at=created_at,
                summary=summary,
                action_plan=action_plan,
                agent_results=agent_results,
            )
            create_workflow_run(
                run_id=run_id,
                created_at=created_at,
                status=result.status,
                request_payload=request.model_dump(),
                response_payload=result.model_dump(mode="json"),
            )
            return result
        except Exception as exc:
            failed = WorkflowResult(
                run_id=run_id,
                status="failed",
                created_at=created_at,
                summary="",
                action_plan=[],
                agent_results=[],
                error_message=str(exc),
            )
            create_workflow_run(
                run_id=run_id,
                created_at=created_at,
                status=failed.status,
                request_payload=request.model_dump(),
                response_payload=failed.model_dump(mode="json"),
                error_message=str(exc),
            )
            raise WorkflowError(str(exc)) from exc

    def get_history(self, limit: int = 20) -> WorkflowHistoryResponse:
        return WorkflowHistoryResponse(items=list_workflow_runs(limit=limit))

    def get_run_detail(self, run_id: UUID) -> dict:
        record = get_workflow_run(run_id)
        if not record:
            raise WorkflowError(f"Workflow run not found: {run_id}")
        return record
