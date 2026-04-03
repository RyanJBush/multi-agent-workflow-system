from fastapi.testclient import TestClient

from app.main import app


def test_run_workflow_and_history() -> None:
    with TestClient(app) as client:

        payload = {
            "title": "US campus productivity app research",
            "objective": "Identify a practical go-to-market approach for first 90 days",
            "constraints": ["low budget", "small team"],
            "output_format": "both",
        }

        run_resp = client.post("/api/v1/workflows/run", json=payload)
        assert run_resp.status_code == 200

        run_data = run_resp.json()
        assert run_data["status"] == "completed"
        assert len(run_data["agent_results"]) == 3
        assert len(run_data["action_plan"]) >= 1

        history_resp = client.get("/api/v1/workflows/history")
        assert history_resp.status_code == 200
        assert len(history_resp.json()["items"]) >= 1
