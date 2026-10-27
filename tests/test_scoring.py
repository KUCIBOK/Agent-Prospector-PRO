"""Tests for scoring service."""

from app.models import ConfidenceLevel, Priority, Prospect, ProspectType
from app.services.scoring import (
    calculate_artist_fit_score,
    calculate_confidence_score,
    calculate_priority,
    calculate_saas_fit_score,
)


def test_artist_fit_score_minimal():
    """Test artist fit score with minimal data."""
    prospect = Prospect(
        type=ProspectType.ARTIST,
        name="Test Artist",
        country="SN",
    )
    score, breakdown = calculate_artist_fit_score(prospect)
    assert 0 <= score <= 100
    assert "profile_quality" in breakdown


def test_artist_fit_score_rich():
    """Test artist fit score with rich data."""
    prospect = Prospect(
        type=ProspectType.ARTIST,
        name="Test Artist",
        country="SN",
        city="Dakar",
        website="https://example.com",
        instagram="@testartist",
        linkedin="https://linkedin.com/in/test",
        description="Talented contemporary artist specializing in sculpture",
        specialty="Sculpture",
        africa_interest="HIGH",
    )
    score, breakdown = calculate_artist_fit_score(prospect)
    assert score > 50  # Should score higher with more data


def test_saas_fit_score():
    """Test SaaS fit score for curator."""
    prospect = Prospect(
        type=ProspectType.CURATOR,
        name="Test Curator",
        country="FR",
        website="https://example.com",
        linkedin="https://linkedin.com/in/test",
        africa_interest="HIGH",
        international_activity="HIGH",
    )
    score, breakdown = calculate_saas_fit_score(prospect)
    assert 0 <= score <= 100
    assert score > 20  # Should have decent score with Africa interest


def test_confidence_score_high():
    """Test confidence score with complete data."""
    prospect = Prospect(
        type=ProspectType.ARTIST,
        name="Test",
        country="SN",
        city="Dakar",
        email="test@example.com",
        website="https://example.com",
        linkedin="https://linkedin.com",
        instagram="@test",
        description="Bio",
        specialty="Art",
        digital_maturity="HIGH",
    )
    confidence = calculate_confidence_score(prospect)
    assert confidence == ConfidenceLevel.HIGH


def test_confidence_score_low():
    """Test confidence score with minimal data."""
    prospect = Prospect(
        type=ProspectType.ARTIST,
        name="Test",
        country="SN",
    )
    confidence = calculate_confidence_score(prospect)
    assert confidence == ConfidenceLevel.LOW


def test_priority_p1():
    """Test P1 priority calculation."""
    priority = calculate_priority(85, ConfidenceLevel.HIGH)
    assert priority == Priority.P1


def test_priority_p2():
    """Test P2 priority calculation."""
    priority = calculate_priority(70, ConfidenceLevel.MEDIUM)
    assert priority == Priority.P2


def test_priority_p3():
    """Test P3 priority calculation."""
    priority = calculate_priority(55, ConfidenceLevel.LOW)
    assert priority == Priority.P3


def test_priority_p4():
    """Test P4 priority calculation."""
    priority = calculate_priority(30, ConfidenceLevel.LOW)
    assert priority == Priority.P4
