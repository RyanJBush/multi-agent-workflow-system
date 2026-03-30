from uuid import UUID

from fastapi import APIRouter, Query

from app.schemas.workflow import WorkflowHistoryResponse, WorkflowRequest, WorkflowResult
from app.services.workflow_service import WorkflowService

router = APIRouter(prefix="/workflows", tags=["workflows"])
service = WorkflowService()


@router.post("/run", response_model=WorkflowResult)
def run_workflow(request: WorkflowRequest) -> WorkflowResult:
    return service.run_workflow(request)


@router.get("/history", response_model=WorkflowHistoryResponse)
def get_history(limit: int = Query(default=20, ge=1, le=100)) -> WorkflowHistoryResponse:
    return service.get_history(limit=limit)


@router.get("/{run_id}")
def get_run_detail(run_id: UUID) -> dict:
    return service.get_run_detail(run_id)
