"""
Prospect model — artists and clients (curators, advisors, galleries).
"""

import enum
from datetime import datetime

from sqlmodel import Field

from app.models.base import BaseModel


class ProspectType(str, enum.Enum):
    """Type of prospect."""

    ARTIST = "ARTIST"
    ART_ADVISOR = "ART_ADVISOR"
    CURATOR = "CURATOR"
    GALLERY = "GALLERY"
    OTHER = "OTHER"


class ProspectStatus(str, enum.Enum):
    """Status of prospect discovery/qualification."""

    IDENTIFIED = "IDENTIFIED"  # Newly discovered
    PREQUALIFIED = "PREQUALIFIED"  # Auto-qualified by system
    DOCUMENTATION_REQUESTED = "DOCUMENTATION_REQUESTED"  # For artists
    VERIFICATION_IN_PROGRESS = "VERIFICATION_IN_PROGRESS"
    VERIFIED_KUCIBOK = "VERIFIED_KUCIBOK"  # Only human can set this
    ENROLLED = "ENROLLED"  # For artists on platform


class Priority(str, enum.Enum):
    """Contact priority."""

    P1 = "P1"  # Contact immediately
    P2 = "P2"  # Contact this week
    P3 = "P3"  # Nurturing / watchlist
    P4 = "P4"  # Archive


class ConfidenceLevel(str, enum.Enum):
    """Confidence in data quality."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class RecommendedAngle(str, enum.Enum):
    """Recommended outreach angle."""

    SOURCING = "SOURCING"
    LOGISTICS = "LOGISTICS"
    SOURCING_AND_LOGISTICS = "SOURCING_AND_LOGISTICS"
    DISCOVERY = "DISCOVERY"
    INTERNATIONAL_ACCESS = "INTERNATIONAL_ACCESS"


class Prospect(BaseModel, table=True):
    """
    Prospect model — artist or client.

    Fields:
        type: ARTIST, ART_ADVISOR, CURATOR, GALLERY, OTHER
        name: Full name
        country: ISO country code or name
        city: City (optional)
        website: Website URL (optional)
        email: Email address (optional)
        linkedin: LinkedIn profile URL (optional)
        instagram: Instagram handle (optional)
        description: Bio / description
        specialty: Professional specialty
        africa_interest: Detected interest in African art
        international_activity: International activity level
        digital_maturity: How tech-savvy they are
        status: IDENTIFIED → PREQUALIFIED → VERIFIED_KUCIBOK
        score: Current fit score (/100)
        confidence: LOW / MEDIUM / HIGH
        priority: P1–P4
        recommended_angle: SOURCING, LOGISTICS, etc.
        reason_to_contact: Why we should reach out (JSON structure)
        last_verified_at: Last time data was verified/updated
    """

    id: int | None = Field(default=None, primary_key=True)
    type: ProspectType = Field(index=True)
    name: str = Field(index=True)
    country: str = Field(index=True)
    city: str | None = None
    website: str | None = Field(default=None, unique=True, index=True)
    email: str | None = Field(default=None, unique=True, index=True)
    linkedin: str | None = Field(default=None, unique=True)
    instagram: str | None = Field(default=None, unique=True)
    description: str | None = None
    specialty: str | None = None

    # Data quality & interest signals
    africa_interest: str | None = None  # "HIGH", "MEDIUM", "LOW", "UNKNOWN"
    international_activity: str | None = None
    digital_maturity: str | None = None

    # Status & classification
    status: ProspectStatus = Field(default=ProspectStatus.IDENTIFIED, index=True)
    score: float = Field(default=0.0, ge=0.0, le=100.0)
    confidence: ConfidenceLevel = Field(default=ConfidenceLevel.LOW, index=True)
    priority: Priority | None = Field(default=None, index=True)

    # Outreach
    recommended_angle: RecommendedAngle | None = None
    reason_to_contact: str | None = None  # JSON: {why, why_now, what}

    # Audit
    last_verified_at: datetime | None = None

    # Timestamps (from TimestampMixin)
    # created_at: datetime
    # updated_at: datetime
