"""API-key authentication."""

from fastapi.testclient import TestClient

from app.config import settings
from app.main import app


def test_api_requires_key(monkeypatch):
    monkeypatch.setattr(settings, "api_key", "secret")
    client = TestClient(app)
    assert client.get("/api/prospects").status_code == 401
    assert client.get("/api/prospects", headers={"X-API-Key": "wrong"}).status_code == 401


def test_api_refuses_when_unconfigured(monkeypatch):
    monkeypatch.setattr(settings, "api_key", "")
    monkeypatch.setattr(settings, "debug", False)
    assert TestClient(app).get("/api/prospects").status_code == 503


def test_health_stays_public():
    assert TestClient(app).get("/health").status_code == 200
