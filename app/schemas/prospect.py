"""
Prospect schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl

from app.models import (
    ProspectType,
    ProspectStatus,
    Priority,
    ConfidenceLevel,
    RecommendedAngle,
)


class ProspectCreate(BaseModel):
    """Create prospect request."""

    type: ProspectType
    name: str
    country: str
    city: Optional[str] = None
    website: Optional[str] = None  # Accepte string simple (pas validation stricte URL)
    email: Optional[str] = None    # Accepte string simple (pas validation stricte Email)
    linkedin: Optional[str] = None
    instagram: Optional[str] = None
    description: Optional[str] = None
    specialty: Optional[str] = None


class ProspectUpdate(BaseModel):
    """Update prospect request."""

    name: Optional[str] = None
    city: Optional[str] = None
    website: Optional[str] = None  # Match ProspectCreate - use plain string
    email: Optional[str] = None    # Match ProspectCreate - use plain string
    linkedin: Optional[str] = None
    instagram: Optional[str] = None
    description: Optional[str] = None
    specialty: Optional[str] = None
    africa_interest: Optional[str] = None
    international_activity: Optional[str] = None
    digital_maturity: Optional[str] = None
    status: Optional[ProspectStatus] = None
    score: Optional[float] = None
    confidence: Optional[ConfidenceLevel] = None
    priority: Optional[Priority] = None
    recommended_angle: Optional[RecommendedAngle] = None
    reason_to_contact: Optional[str] = None


class ProspectResponse(BaseModel):
    """Prospect response."""

    id: int
    type: ProspectType
    name: str
    country: str
    city: Optional[str]
    website: Optional[str]
    email: Optional[str]
    linkedin: Optional[str]
    instagram: Optional[str]
    description: Optional[str]
    specialty: Optional[str]
    africa_interest: Optional[str]
    international_activity: Optional[str]
    digital_maturity: Optional[str]
    status: ProspectStatus
    score: float
    confidence: ConfidenceLevel
    priority: Optional[Priority]
    recommended_angle: Optional[RecommendedAngle]
    reason_to_contact: Optional[str]
    last_verified_at: Optional[datetime]
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
