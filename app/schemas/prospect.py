"""
Prospect schemas for request/response validation.
"""

from datetime import datetime

from pydantic import BaseModel

from app.models import (
    ConfidenceLevel,
    Priority,
    ProspectStatus,
    ProspectType,
    RecommendedAngle,
)


class ProspectCreate(BaseModel):
    """Create prospect request."""

    type: ProspectType
    name: str
    country: str
    city: str | None = None
    website: str | None = None  # Accepte string simple (pas validation stricte URL)
    email: str | None = None  # Accepte string simple (pas validation stricte Email)
    linkedin: str | None = None
    instagram: str | None = None
    description: str | None = None
    specialty: str | None = None


class ProspectUpdate(BaseModel):
    """Update prospect request."""

    name: str | None = None
    city: str | None = None
    website: str | None = None  # Match ProspectCreate - use plain string
    email: str | None = None  # Match ProspectCreate - use plain string
    linkedin: str | None = None
    instagram: str | None = None
    description: str | None = None
    specialty: str | None = None
    africa_interest: str | None = None
    international_activity: str | None = None
    digital_maturity: str | None = None
    status: ProspectStatus | None = None
    score: float | None = None
    confidence: ConfidenceLevel | None = None
    priority: Priority | None = None
    recommended_angle: RecommendedAngle | None = None
    reason_to_contact: str | None = None


class ProspectResponse(BaseModel):
    """Prospect response."""

    id: int
    type: ProspectType
    name: str
    country: str
    city: str | None
    website: str | None
    email: str | None
    linkedin: str | None
    instagram: str | None
    description: str | None
    specialty: str | None
    africa_interest: str | None
    international_activity: str | None
    digital_maturity: str | None
    status: ProspectStatus
    score: float
    confidence: ConfidenceLevel
    priority: Priority | None
    recommended_angle: RecommendedAngle | None
    reason_to_contact: str | None
    last_verified_at: datetime | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProspectsListResponse(BaseModel):
    """List prospects response."""

    total: int
    page: int
    page_size: int
    items: list[ProspectResponse]
