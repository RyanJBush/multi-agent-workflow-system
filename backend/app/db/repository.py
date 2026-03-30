import json
from datetime import datetime
from uuid import UUID

from app.db.sqlite import get_connection
from app.schemas.workflow import WorkflowRunRecord


def create_workflow_run(
    run_id: UUID,
    created_at: datetime,
    status: str,
    request_payload: dict,
    response_payload: dict,
    error_message: str | None = None,
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO workflow_runs (run_id, created_at, status, request_payload, response_payload, error_message)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                str(run_id),
                created_at.isoformat(),
                status,
                json.dumps(request_payload),
                json.dumps(response_payload),
                error_message,
            ),
        )
        conn.commit()


def list_workflow_runs(limit: int = 20) -> list[WorkflowRunRecord]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT run_id, status, created_at, response_payload
            FROM workflow_runs
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    results: list[WorkflowRunRecord] = []
    for row in rows:
        response_payload = json.loads(row["response_payload"])
        results.append(
            WorkflowRunRecord(
                run_id=UUID(row["run_id"]),
                status=row["status"],
                created_at=datetime.fromisoformat(row["created_at"]),
                summary=response_payload.get("summary", ""),
            )
        )
    return results


def get_workflow_run(run_id: UUID) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT run_id, status, created_at, request_payload, response_payload, error_message
            FROM workflow_runs
            WHERE run_id = ?
            """,
            (str(run_id),),
        ).fetchone()

    if row is None:
        return None

    return {
        "run_id": row["run_id"],
        "status": row["status"],
        "created_at": row["created_at"],
        "request_payload": json.loads(row["request_payload"]),
        "response_payload": json.loads(row["response_payload"]),
        "error_message": row["error_message"],
    }
