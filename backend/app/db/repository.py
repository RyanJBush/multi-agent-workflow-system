"""Repository — thin persistence layer for workflow runs."""

from __future__ import annotations

import json

import aiosqlite

from app.schemas.workflow import WorkflowResponse, WorkflowSummary


async def save_run(db: aiosqlite.Connection, run: WorkflowResponse) -> None:
    await db.execute(
        """
        INSERT INTO workflow_runs
            (id, task, status, summary, action_plan, agent_results, error, created_at, completed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            str(run.id),
            run.task,
            run.status,
            run.summary,
            json.dumps([step.model_dump() for step in run.action_plan]),
            json.dumps([r.model_dump() for r in run.agent_results]),
            run.error,
            run.created_at.isoformat(),
            run.completed_at.isoformat() if run.completed_at else None,
        ),
    )
    await db.commit()


async def list_runs(db: aiosqlite.Connection, limit: int = 50) -> list[WorkflowSummary]:
    cursor = await db.execute(
        "SELECT id, task, status, created_at, completed_at FROM workflow_runs "
        "ORDER BY created_at DESC LIMIT ?",
        (limit,),
    )
    rows = await cursor.fetchall()
    return [
        WorkflowSummary(
            id=row[0],
            task=row[1],
            status=row[2],
            created_at=row[3],
            completed_at=row[4],
        )
        for row in rows
    ]


async def get_run(db: aiosqlite.Connection, run_id: str) -> WorkflowResponse | None:
    cursor = await db.execute("SELECT * FROM workflow_runs WHERE id = ?", (run_id,))
    row = await cursor.fetchone()
    if row is None:
        return None
    return WorkflowResponse(
        id=row[0],
        task=row[1],
        status=row[2],
        summary=row[3] or "",
        action_plan=json.loads(row[4]) if row[4] else [],
        agent_results=json.loads(row[5]) if row[5] else [],
        error=row[6],
        created_at=row[7],
        completed_at=row[8],
    )
