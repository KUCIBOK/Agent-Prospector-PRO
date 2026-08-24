"""
Signal model — intent signals (expositions, opportunities, etc.).
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, ForeignKey
import enum

from app.models.base import BaseModel


class SignalType(str, enum.Enum):
    """Type of intent signal."""

    # Gallery/Curator activity
    NEW_EXHIBITION = "NEW_EXHIBITION"
    AFRICA_EXHIBITION = "AFRICA_EXHIBITION"  # NEW: Exhibition featuring African art
    CALL_FOR_ARTISTS = "CALL_FOR_ARTISTS"
    FAIR_PARTICIPATION = "FAIR_PARTICIPATION"
    GALLERY_EXPANSION = "GALLERY_EXPANSION"  # NEW: Gallery expansion, new location, etc.

    # Career/Hiring signals
    CAREER_CHANGE = "CAREER_CHANGE"  # NEW: Title change, promotion, etc.
    HIRING_CURATOR = "HIRING_CURATOR"  # NEW: Open position for curator/advisor
    HIRING_SPREE = "HIRING_SPREE"  # NEW: Multiple hires in company

    # Other signals
    PROGRAM_LAUNCH = "PROGRAM_LAUNCH"
    INTERNATIONAL_ACTIVITY = "INTERNATIONAL_ACTIVITY"
    NEW_PUBLICATION = "NEW_PUBLICATION"
    PARTNERSHIP = "PARTNERSHIP"
    ACQUISITION = "ACQUISITION"
    OTHER = "OTHER"


class Importance(str, enum.Enum):
    """Signal importance."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Confidence(str, enum.Enum):
    """Signal confidence."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Signal(BaseModel, table=True):
    """
    Signal model — public events indicating potential need.

    Examples:
    - New exhibition featuring African art
    - Call for artists from Africa
    - Participation in African art fair
    - Launching international program
    - Recent publication about African art

    Fields:
        prospect_id: FK to Prospect
        signal_type: Type of signal
        description: What happened
        source_url: Where we found this
        signal_date: When it happened
        importance: LOW/MEDIUM/HIGH
        confidence: Data confidence
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    prospect_id: int = Field(foreign_key="prospect.id", index=True)
    signal_type: SignalType = Field(index=True)
    description: str
    source_url: Optional[str] = None
    signal_date: datetime = Field(index=True)
    importance: Importance = Field(default=Importance.MEDIUM)
    confidence: Confidence = Field(default=Confidence.MEDIUM)
