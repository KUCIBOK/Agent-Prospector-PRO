"""Tests for outreach service."""

import pytest
from app.models import Prospect, ProspectType, ConfidenceLevel
from app.services.outreach import (
    detect_persona,
    generate_message_variant,
    generate_message_variants,
)


def test_detect_persona_curator():
    """Test persona detection for curator."""
    prospect = Prospect(
        type=ProspectType.CURATOR,
        name="Test Curator",
        country="FR",
        specialty="Curatorial Practice",
    )
    persona = detect_persona(prospect)
    assert persona == "CURATOR"


def test_detect_persona_advisor():
    """Test persona detection for advisor."""
    prospect = Prospect(
        type=ProspectType.ART_ADVISOR,
        name="Test Advisor",
        country="US",
        specialty="Art Advisory & Consulting",
    )
    persona = detect_persona(prospect)
    assert persona == "ART_ADVISOR"


def test_generate_message_low_confidence():
    """Test message generation with LOW confidence (should be generic)."""
    prospect = Prospect(
        type=ProspectType.CURATOR,
        name="Test",
        country="FR",
        specialty="Curation",
        confidence=ConfidenceLevel.LOW,
    )
    message = generate_message_variant(prospect, "CURATOR", "variant_1_short")
    assert message
    assert len(message) > 0
    # Should not contain specific claims
    assert "exhibition" not in message.lower() or "exhibition" in prospect.specialty.lower()


def test_generate_message_high_confidence():
    """Test message generation with HIGH confidence (can be specific)."""
    prospect = Prospect(
        type=ProspectType.ART_ADVISOR,
        name="John Doe",
        country="US",
        specialty="Art Advisory",
        confidence=ConfidenceLevel.HIGH,
    )
    message = generate_message_variant(prospect, "ART_ADVISOR", "variant_1_short")
    assert message
    assert "John" in message  # Should include personalization


def test_generate_variants():
    """Test generating multiple message variants."""
    prospect = Prospect(
        type=ProspectType.CURATOR,
        name="Test",
        country="FR",
        specialty="Curation",
        confidence=ConfidenceLevel.MEDIUM,
    )
    variants = generate_message_variants(prospect, count=3)
    assert len(variants) == 3
    # All variants should have a persona (CURATOR or similar)
    assert all("persona" in v for v in variants)
    assert all(v["status"] == "DRAFT" for v in variants)
    # Variants should have different labels
    assert len(set(v["variant_label"] for v in variants)) == 3
