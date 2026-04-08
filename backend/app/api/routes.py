"""API router — workflow endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.db.repository import get_run, list_runs, save_run
from app.db.session import get_db
from app.orchestration.orchestrator import WorkflowOrchestrator
from app.schemas.workflow import WorkflowRequest, WorkflowResponse, WorkflowSummary

router = APIRouter(prefix="/api/v1/workflows", tags=["workflows"])
_orchestrator = WorkflowOrchestrator()


@router.post("/run", response_model=WorkflowResponse, status_code=200)
async def run_workflow(request: WorkflowRequest) -> WorkflowResponse:
    """Submit a task and get back a fully-orchestrated workflow result."""
    result = await _orchestrator.run(request)
    db = await get_db()
    try:
        await save_run(db, result)
    finally:
        await db.close()
    return result


@router.get("/history", response_model=list[WorkflowSummary])
async def get_history(
    limit: int = Query(default=50, ge=1, le=200, description="Maximum number of runs to return."),
) -> list[WorkflowSummary]:
    """Return a list of past workflow run summaries."""
    db = await get_db()
    try:
        return await list_runs(db, limit=limit)
    finally:
        await db.close()


@router.get("/{run_id}", response_model=WorkflowResponse)
async def get_workflow(run_id: str) -> WorkflowResponse:
    """Return full details for a single workflow run."""
    db = await get_db()
    try:
        run = await get_run(db, run_id)
    finally:
        await db.close()
    if run is None:
        raise HTTPException(status_code=404, detail="Workflow run not found.")
    return run
