"""Tests for enrichment service."""

from sqlmodel import Session

from app.models import Prospect, ProspectType
from app.services.enrichment import Enrichment


def test_normalize_country():
    """Test country normalization."""
    assert Enrichment.normalize_country("Senegal") == "SN"
    assert Enrichment.normalize_country("senegal") == "SN"
    assert Enrichment.normalize_country("SN") == "SN"
    assert Enrichment.normalize_country("South Africa") == "ZA"
    assert Enrichment.normalize_country("Nigeria") == "NG"
    assert Enrichment.normalize_country("UNKNOWN") is None


def test_normalize_email():
    """Test email normalization."""
    assert Enrichment.normalize_email("Test@EXAMPLE.COM") == "test@example.com"
    assert Enrichment.normalize_email("  test@example.com  ") == "test@example.com"
    assert Enrichment.normalize_email("invalid.email") is None
    assert Enrichment.normalize_email("") is None


def test_normalize_url():
    """Test URL normalization."""
    assert Enrichment.normalize_url("example.com") == "https://example.com"
    assert Enrichment.normalize_url("https://example.com/") == "https://example.com"
    assert Enrichment.normalize_url("http://example.com") == "http://example.com"


def test_normalize_name():
    """Test name normalization."""
    assert Enrichment.normalize_name("jean dupont") == "Jean Dupont"
    assert Enrichment.normalize_name("  john doe  ") == "John Doe"
    assert Enrichment.normalize_name("") is None


def test_enrich_prospect(session: Session):
    """Test prospect enrichment."""
    prospect = Prospect(
        type=ProspectType.ARTIST,
        name="jean dupont",
        country="senegal",
        email="Jean@EXAMPLE.COM",
        website="example.com",
    )
    session.add(prospect)
    session.commit()
    session.refresh(prospect)

    enricher = Enrichment(session)
    enriched = enricher.enrich_prospect(prospect)

    # Should normalize all fields
    assert enriched.name == "Jean Dupont"
    assert enriched.country == "SN"
    assert enriched.email == "jean@example.com"
    assert enriched.website == "https://example.com"


def test_detect_signals(session: Session):
    """Test intent signal detection."""
    prospect = Prospect(
        type=ProspectType.CURATOR,
        name="Test Curator",
        country="FR",
        description="Specializes in African contemporary art exhibitions and international fairs",
    )
    session.add(prospect)
    session.commit()
    session.refresh(prospect)

    enricher = Enrichment(session)
    signals = enricher.detect_intent_signals(prospect)

    # Should detect exhibition and international activity signals
    assert len(signals) > 0
    signal_types = [s.signal_type for s in signals]
    assert any("EXHIBITION" in str(t) for t in signal_types)
