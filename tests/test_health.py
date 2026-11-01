from fastapi.testclient import TestClient

from app.main import main_app


def test_liveness():
    with TestClient(main_app) as client:
        response = client.get("/api/v1/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}