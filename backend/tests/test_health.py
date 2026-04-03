from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_cors_allows_localhost_frontend_origin() -> None:
    with TestClient(app) as client:
        response = client.options(
            "/api/v1/workflows/history",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "GET",
            },
        )

    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"


def test_cors_allows_loopback_frontend_origin() -> None:
    with TestClient(app) as client:
        response = client.options(
            "/api/v1/workflows/history",
            headers={
                "Origin": "http://127.0.0.1:5173",
                "Access-Control-Request-Method": "GET",
            },
        )

    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://127.0.0.1:5173"
