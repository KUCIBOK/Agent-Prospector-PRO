"""
Outreach service — generate LinkedIn messages for prospects.

Based on LOGIC.md section 16:
- Persona detection (ART_ADVISOR vs CURATOR)
- Message generation (multiple variants, no markdown)
- Respect guardrails (no invented data, LOW confidence = generic)
"""

from app.models import ConfidenceLevel, MessageStatus, Prospect


def detect_persona(prospect: Prospect) -> str:
    """
    Detect persona type: ART_ADVISOR or CURATOR.

    Uses: specialty, description, type, organization clues.
    """
    if not prospect.specialty:
        return "ART_ADVISOR"  # Default

    specialty_lower = prospect.specialty.lower()

    if any(word in specialty_lower for word in ["curator", "curatorial", "curating"]):
        return "CURATOR"
    elif any(word in specialty_lower for word in ["advisor", "advise", "advising", "consultant"]):
        return "ART_ADVISOR"
    else:
        return "ART_ADVISOR"  # Default


def generate_message_variant(
    prospect: Prospect,
    persona: str,
    variant_label: str,
    reason_to_contact: dict | None = None,
) -> str:
    """
    Generate a single message variant.

    Important guardrails:
    - If confidence is LOW, message is generic (no specific claims)
    - All details must come from prospect data or reason_to_contact
    - Never invent: exhibitions, activities, relationships, emails
    - Plain text only (no markdown)
    - Professional but direct tone

    Args:
        prospect: The prospect to message
        persona: ART_ADVISOR or CURATOR
        variant_label: e.g., "variant_1_short", "variant_2_medium"
        reason_to_contact: dict with {why, why_now, what}

    Returns:
        Message text (plain, no markdown)
    """
    name = prospect.name.split()[0] if prospect.name else "there"

    if prospect.confidence == ConfidenceLevel.LOW:
        # Generic message (no specific claims)
        if persona == "CURATOR":
            return f"""Hi {name},

I'm reaching out because we work with contemporary artists across Africa and noticed your work in curatorial practice.

We help international art professionals source and manage relationships with African artists directly. Given your background, I thought it might be relevant.

Happy to chat if you're interested.

Best,
Kucibok Team"""
        else:  # ART_ADVISOR
            return f"""Hi {name},

Quick note: we connect international art advisors with contemporary African artists and manage the logistics between continents.

Thought it might be useful for your practice. Open to a conversation if you think so too.

Best,
Kucibok Team"""
    else:
        # Personalized message with specific context
        why = reason_to_contact.get("why", "") if reason_to_contact else ""

        if persona == "CURATOR":
            return f"""Hi {name},

{why}

We've built infrastructure to connect curators like you directly with vetted contemporary African artists. Everything from sourcing to logistics to customs handling.

Worth 15 min to explore?

Best,
Kucibok Team"""
        else:  # ART_ADVISOR
            return f"""Hi {name},

{why}

Kucibok simplifies sourcing African artists and managing the Africa-to-international logistics. No intermediaries, direct relationships.

Curious if it fits your work?

Best,
Kucibok Team"""


def generate_message_variants(
    prospect: Prospect,
    reason_to_contact: dict | None = None,
    count: int = 3,
) -> list[dict]:
    """
    Generate multiple message variants for a prospect.

    Returns:
        List of dicts: {persona, variant_label, content}
    """
    persona = detect_persona(prospect)
    variants = []

    labels = ["variant_1_short", "variant_2_medium", "variant_3_long"][:count]

    for label in labels:
        content = generate_message_variant(prospect, persona, label, reason_to_contact)
        variants.append(
            {
                "persona": persona,
                "variant_label": label,
                "content": content,
                "status": MessageStatus.DRAFT,
            }
        )

    return variants
