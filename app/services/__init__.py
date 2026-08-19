"""
Business logic services.
"""

from app.services.scoring import (
    calculate_artist_fit_score,
    calculate_saas_fit_score,
    calculate_confidence_score,
    calculate_priority,
)
from app.services.outreach import (
    detect_persona,
    generate_message_variant,
    generate_message_variants,
)

__all__ = [
    # Scoring
    "calculate_artist_fit_score",
    "calculate_saas_fit_score",
    "calculate_confidence_score",
    "calculate_priority",
    # Outreach
    "detect_persona",
    "generate_message_variant",
    "generate_message_variants",
]
