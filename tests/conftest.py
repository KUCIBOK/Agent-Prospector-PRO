"""Pytest configuration and fixtures."""

import pytest
from sqlmodel import create_engine, Session, SQLModel
from sqlmodel.pool import StaticPool

from app.config import settings
from app.db import get_session
from app.main import app


@pytest.fixture(name="session")
def session_fixture():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session, monkeypatch):
    """FastAPI test client with mocked database."""

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    monkeypatch.setattr(settings, "api_key", "test-key")
    from fastapi.testclient import TestClient

    client = TestClient(app, headers={"X-API-Key": "test-key"})
    yield client
    app.dependency_overrides.clear()
