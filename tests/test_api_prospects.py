"""Tests for prospects API."""

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import Prospect, ProspectType


def test_create_prospect(client: TestClient):
    """Test creating a prospect."""
    response = client.post(
        "/api/prospects",
        json={
            "type": "ARTIST",
            "name": "Test Artist",
            "country": "SN",
            "city": "Dakar",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Artist"
    assert data["type"] == "ARTIST"


def test_list_prospects(client: TestClient, session: Session):
    """Test listing prospects."""
    # Create test prospects directly in DB
    for i in range(3):
        prospect = Prospect(
            type=ProspectType.ARTIST,
            name=f"Artist {i}",
            country="SN",
        )
        session.add(prospect)
    session.commit()

    response = client.get("/api/prospects")
    assert response.status_code == 200
    data = response.json()
    # Should have at least 3 prospects
    assert data.get("total", 0) >= 3 or len(data.get("items", [])) >= 3


def test_get_prospect(client: TestClient, session: Session):
    """Test getting a specific prospect."""
    prospect = Prospect(
        type=ProspectType.ARTIST,
        name="Test Artist",
        country="SN",
    )
    session.add(prospect)
    session.commit()
    session.refresh(prospect)

    response = client.get(f"/api/prospects/{prospect.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == prospect.id
    assert data["name"] == "Test Artist"


def test_get_prospect_not_found(client: TestClient):
    """Test getting non-existent prospect."""
    response = client.get("/api/prospects/9999")
    assert response.status_code == 404


def test_update_prospect(client: TestClient, session: Session):
    """Test updating a prospect."""
    prospect = Prospect(
        type=ProspectType.ARTIST,
        name="Test Artist",
        country="SN",
    )
    session.add(prospect)
    session.commit()
    session.refresh(prospect)

    response = client.patch(
        f"/api/prospects/{prospect.id}",
        json={"city": "Dakar", "score": 75.5},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Dakar"
    assert data["score"] == 75.5


def test_filter_prospects_by_type(client: TestClient, session: Session):
    """Test filtering prospects by type."""
    # Create mixed prospects
    for type_ in [ProspectType.ARTIST, ProspectType.CURATOR]:
        prospect = Prospect(type=type_, name=f"Prospect {type_}", country="SN")
        session.add(prospect)
    session.commit()

    response = client.get("/api/prospects?prospect_type=ARTIST")
    assert response.status_code == 200
    data = response.json()
    assert all(p["type"] == "ARTIST" for p in data["items"])


def test_server_errors_do_not_leak_details(client: TestClient, session: Session, monkeypatch):
    """A failing commit must return a generic 500, not the exception text."""

    def boom():
        raise RuntimeError("postgresql://user:s3cret@db/internal")

    monkeypatch.setattr(session, "commit", boom)
    response = client.post(
        "/api/prospects",
        json={"type": "ARTIST", "name": "Leak Test", "country": "SN"},
    )
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error"
    assert "s3cret" not in response.text
