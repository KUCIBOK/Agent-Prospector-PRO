"""Tests for discovery service."""

from sqlmodel import Session

from app.models import ProspectType
from app.services.discovery import DiscoveryEngine, SearchQuery


def test_search_query_artists():
    """Test artist search query building."""
    query = SearchQuery(ProspectType.ARTIST, ["contemporary artist"], ["Senegal", "Nigeria"])
    google_queries = query.build_google_queries()
    assert len(google_queries) > 0
    assert any("Senegal" in q or "Nigeria" in q for q in google_queries)


def test_search_query_clients():
    """Test client search query building."""
    query = SearchQuery(ProspectType.ART_ADVISOR, ["art advisor"])
    linkedin_queries = query.build_linkedin_queries()
    assert len(linkedin_queries) > 0


def test_generate_artist_searches(session: Session):
    """Test artist discovery query generation."""
    engine = DiscoveryEngine(session)
    searches = engine.generate_artist_searches(countries=["SN", "NG"])
    assert len(searches) > 0


def test_generate_client_searches(session: Session):
    """Test client discovery query generation."""
    engine = DiscoveryEngine(session)
    searches = engine.generate_client_searches()
    assert len(searches) > 0
    # Should have advisors, curators, galleries
    types = [s.target_type for s in searches]
    assert ProspectType.ART_ADVISOR in types
    assert ProspectType.CURATOR in types
    assert ProspectType.GALLERY in types


def test_create_prospect_from_result(session: Session):
    """Test creating prospect from search result."""
    engine = DiscoveryEngine(session)
    prospect = engine.create_prospect_from_result(
        name="Test Artist",
        prospect_type=ProspectType.ARTIST,
        country="SN",
        website="https://example.com",
        source_url="https://discovery.com/artist",
    )
    assert prospect is not None
    assert prospect.name == "Test Artist"
    assert prospect.type == ProspectType.ARTIST
    assert prospect.country == "SN"


def test_duplicate_detection(session: Session):
    """Test duplicate detection in discovery."""
    engine = DiscoveryEngine(session)

    # Create first prospect
    prospect1 = engine.create_prospect_from_result(
        name="Test Artist",
        prospect_type=ProspectType.ARTIST,
        country="SN",
        website="https://example.com",
        source_url="https://discovery.com/artist1",
    )
    assert prospect1 is not None

    # Try to create duplicate (same website)
    prospect2 = engine.create_prospect_from_result(
        name="Test Artist",
        prospect_type=ProspectType.ARTIST,
        country="SN",
        website="https://example.com",
        source_url="https://discovery.com/artist2",
    )
    assert prospect2 is None  # Should return None (duplicate)
