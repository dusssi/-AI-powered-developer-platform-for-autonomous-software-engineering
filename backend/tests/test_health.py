from fastapi.testclient import TestClient

from app.main import create_app


def test_health_endpoint_reports_liveness() -> None:
    client = TestClient(create_app())
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_reports_service_configuration() -> None:
    client = TestClient(create_app())
    response = client.get("/ready")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["service"] == "BuckLabs Dev API"
    assert body["environment"] == "development"


def test_openapi_is_available_in_development() -> None:
    client = TestClient(create_app())

    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"]["title"] == "BuckLabs Dev API"
