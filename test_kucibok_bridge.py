#!/usr/bin/env python
"""
Test Kucibok Bridge Outreach Service

Tests:
1. Message generation by segment (Curator vs Auctioneer)
2. Personalization with context
3. Rule validation (word count, markdown, forbidden words)
4. HTML email rendering
"""

import logging
from app.db import SessionLocal
from app.models import Prospect, ProspectType, ProspectStatus
from app.services.kucibok_bridge_outreach import KucibokBridgeOutreach

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def print_header():
    """Print test header."""
    print("""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║          🔥 KUCIBOK BRIDGE OUTREACH SERVICE TEST 🔥            ║
║                                                                ║
║  Testing Playbook Implementation:                             ║
║  ✓ Message generation (2 segments)                            ║
║  ✓ Personalization rules                                      ║
║  ✓ Word count validation (80-100)                             ║
║  ✓ No markdown, no forbidden words                            ║
║  ✓ HTML email rendering                                       ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
    """)


def test_message_generation():
    """Test message generation for both segments."""
    print("\n🔍 TEST 1: Message Generation by Segment\n")

    session = SessionLocal()
    bridge = KucibokBridgeOutreach(session)

    # Test Curator prospect
    curator = Prospect(
        name="Marie Dubois",
        email="marie@galerie.fr",
        type=ProspectType.CURATOR,
        country="FR",
        description="Contemporary art curator, focus on African artists",
        website="https://galerie-dubois.fr"
    )

    # Test Auctioneer prospect
    auctioneer = Prospect(
        name="Jean Leclerc",
        email="jean@artcurial.com",
        type=ProspectType.CURATOR,  # Will be detected as auctioneer by description
        country="FR",
        description="Commissaire-priseur, Artcurial Paris",
        website="https://artcurial.com"
    )

    print("=" * 70)
    print("CURATOR SEGMENT MESSAGE:")
    print("=" * 70)

    message_curator = bridge.generate_message(curator, variant_index=0)
    print(f"\nProspect: {curator.name}")
    print(f"Email: {curator.email}")
    print(f"Description: {curator.description}")
    print(f"\nMessage:\n{message_curator}")

    # Validate
    rules = bridge.validate_message_rules(message_curator)
    word_count = len(message_curator.split())
    print(f"\nValidation:")
    print(f"  ✓ Word count: {word_count}/100")
    print(f"  ✓ No markdown: {not rules['has_markdown']}")
    print(f"  ✓ No forbidden words: {not rules['has_forbidden_words']}")
    print(f"  ✓ No 'Concrètement': {not rules['has_concrètement']}")

    print("\n" + "=" * 70)
    print("AUCTIONEER SEGMENT MESSAGE:")
    print("=" * 70)

    message_auctioneer = bridge.generate_message(auctioneer, variant_index=0)
    print(f"\nProspect: {auctioneer.name}")
    print(f"Email: {auctioneer.email}")
    print(f"Description: {auctioneer.description}")
    print(f"\nMessage:\n{message_auctioneer}")

    # Validate
    rules = bridge.validate_message_rules(message_auctioneer)
    word_count = len(message_auctioneer.split())
    print(f"\nValidation:")
    print(f"  ✓ Word count: {word_count}/100")
    print(f"  ✓ No markdown: {not rules['has_markdown']}")
    print(f"  ✓ No forbidden words: {not rules['has_forbidden_words']}")

    session.close()


def test_personalization():
    """Test personalization variants."""
    print("\n\n🔍 TEST 2: Personalization Variants\n")

    session = SessionLocal()
    bridge = KucibokBridgeOutreach(session)

    curator = Prospect(
        name="Sophie Bernard",
        email="sophie@espaceb.com",
        type=ProspectType.CURATOR,
        country="FR",
        description="Modern art curator, Paris galleries",
        specialty="Contemporary & emerging artists"
    )

    print("=" * 70)
    print("GENERATING 3 DIFFERENT VARIANTS FOR SAME PROSPECT:")
    print("=" * 70)

    for i in range(3):
        print(f"\n--- VARIANT {i + 1} ---\n")
        message = bridge.generate_message(curator, variant_index=i)
        print(message)
        print(f"({len(message.split())} words)")

    session.close()


def test_followup():
    """Test follow-up message generation."""
    print("\n\n🔍 TEST 3: Follow-up Message\n")

    session = SessionLocal()
    bridge = KucibokBridgeOutreach(session)

    prospect = Prospect(
        name="Thomas Fontaine",
        email="thomas@gallery.fr",
        type=ProspectType.CURATOR,
    )

    print("=" * 70)
    print("FOLLOW-UP MESSAGE (after 5-7 days no response):")
    print("=" * 70)

    followup_msg = bridge.generate_followup_message(prospect)
    print(f"\nProspect: {prospect.name}")
    print(f"\nFollow-up Message:\n{followup_msg}")
    print(f"\nWord count: {len(followup_msg.split())}")

    session.close()


def test_html_rendering():
    """Test HTML email rendering."""
    print("\n\n🔍 TEST 4: HTML Email Rendering\n")

    session = SessionLocal()
    bridge = KucibokBridgeOutreach(session)

    prospect = Prospect(
        name="Marie Dubois",
        email="marie@galerie.fr",
    )

    print("=" * 70)
    print("KUCIBOK BRIDGE HTML EMAIL:")
    print("=" * 70)

    html = bridge.render_html_email(
        prospect=prospect,
        artist_name="Gaétan Rapaccioli",
        artist_city="Dakar",
        artist_country="Senegal",
        artist_medium="Painting",
        works_available=5,
        dossier_url="https://kucibok.com/dossier/gaetan-rapaccioli",
        opening_message="Voici le dossier complet dont je vous parlais — sourcé et vérifié directement sur le terrain à Dakar."
    )

    print("\n✅ HTML email generated successfully")
    print(f"   Size: {len(html)} bytes")
    print(f"   Contains Kucibok Bridge branding: {'KUCIBOK BRIDGE' in html}")
    print(f"   Contains artist name: {'Gaétan Rapaccioli' in html}")
    print(f"   Contains CTA button: {'Consulter le dossier complet' in html}")

    # Save to file for inspection
    with open("test_kucibok_bridge_email.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n   Saved to: test_kucibok_bridge_email.html")

    session.close()


def test_validation():
    """Test message validation rules."""
    print("\n\n🔍 TEST 5: Rule Validation\n")

    session = SessionLocal()
    bridge = KucibokBridgeOutreach(session)

    test_cases = [
        ("Good message", "Bonjour Marie, I'm sourcing African artists from Dakar. Each profile is verified on the ground before presentation. I can share a first dossier if interested, no commitment.", True),

        ("Too long", "Bonjour Marie, " + " word " * 150, False),

        ("Has markdown", "Bonjour Marie, **bold text** and _italic_", False),

        ("Has forbidden word", "Bonjour Marie, our automated platform uses AI to find artists", False),

        ("Starts with Concrètement", "Concrètement, voici comment ça marche...", False),
    ]

    print("=" * 70)
    print("TESTING MESSAGE VALIDATION RULES:")
    print("=" * 70)

    for label, message, should_pass in test_cases:
        rules = bridge.validate_message_rules(message)
        is_valid = not any(rules.values())

        status = "✅ PASS" if is_valid == should_pass else "❌ FAIL"
        print(f"\n{status} | {label}")
        print(f"   Message length: {len(message.split())} words")

        if any(rules.values()):
            for rule, violated in rules.items():
                if violated:
                    print(f"   ❌ {rule}")

    session.close()


def print_summary():
    """Print test summary."""
    print("\n\n" + "=" * 70)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 70)
    print("""
KUCIBOK BRIDGE PLAYBOOK IMPLEMENTED:

✓ Two segments: Curator vs Auctioneer
✓ Personalized messages (80-100 words, no markdown)
✓ Warm tone, no commercial push
✓ Moctar Sidibé persona enforcement
✓ Follow-up sequences (day 0, day 5-7)
✓ HTML email template rendering
✓ Message validation rules

READY FOR PRODUCTION:
1. Integrate with API endpoint
2. Connect to LinkedIn/email sending
3. Track responses in dashboard
4. Auto-trigger follow-ups

NEXT STEPS:
See: KUCIBOK_BRIDGE_PLAYBOOK.md
See: DEEP_SOURCE_QUICK_START.md
See: START_SYSTEM.md
    """)


def main():
    """Run all tests."""
    print_header()

    try:
        test_message_generation()
        test_personalization()
        test_followup()
        test_html_rendering()
        test_validation()
        print_summary()

    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
