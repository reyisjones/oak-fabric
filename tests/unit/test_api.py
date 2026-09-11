import pytest
from fastapi.testclient import TestClient

from src.api.main import create_app
from src.common.config import Settings


def test_health_contract(monkeypatch):
    monkeypatch.setenv("APP_ENV", "test")
    with TestClient(create_app()) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok", "service": "oak-fabric"}
        assert client.post("/health").status_code == 405
        assert client.get("/ingest/document").status_code == 404


def test_production_hides_interactive_docs(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    with TestClient(create_app()) as client:
        assert client.get("/docs").status_code == 404
        assert client.get("/openapi.json").status_code == 404
        assert client.get("/health").status_code == 200


def test_development_publishes_health_schema(monkeypatch):
    monkeypatch.delenv("APP_ENV", raising=False)
    with TestClient(create_app()) as client:
        assert "/health" in client.get("/openapi.json").json()["paths"]


@pytest.mark.parametrize("value", ["", "prod", "DEVELOPMENT"])
def test_invalid_environment_fails_before_serving(monkeypatch, value):
    monkeypatch.setenv("APP_ENV", value)
    with pytest.raises(ValueError, match="APP_ENV"):
        create_app()


@pytest.mark.parametrize("value", ["development", "test", "production"])
def test_valid_environment(monkeypatch, value):
    monkeypatch.setenv("APP_ENV", value)
    assert Settings.from_env().environment == value
