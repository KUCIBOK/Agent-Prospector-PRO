"""
Artist contact model — tracks artist onboarding via Instagram.
"""

import enum
from datetime import datetime

from sqlmodel import Field

from app.models.base import BaseModel


class EnrollmentStatus(str, enum.Enum):
    """Artist enrollment status."""

    INVITED = "INVITED"  # Invitation generated, awaiting contact
    CONTACTED = "CONTACTED"  # Artist initiated contact
    ENROLLED = "ENROLLED"  # Artist account created


class ArtistContact(BaseModel, table=True):
    """
    Artist contact model — tracks Instagram onboarding.

    CRITICAL: first_contact_initiated_at is the gatekeeper.
    - NULL = no auto-send allowed (artist hasn't contacted us yet)
    - NOT NULL = auto-send unlocked (artist reached out first)

    Fields:
        prospect_id: FK to Prospect (type=ARTIST)
        instagram_handle: Artist's Instagram handle
        invitation_sent_at: When we generated the invitation
        first_contact_initiated_at: CRITICAL — when artist first contacted us
        first_contact_channel: How they contacted (story_reply, message, link_click)
        enrollment_status: INVITED → CONTACTED → ENROLLED
        enrolled_at: When account was created
    """

    id: int | None = Field(default=None, primary_key=True)
    prospect_id: int = Field(foreign_key="prospect.id", unique=True, index=True)
    instagram_handle: str = Field(index=True)
    invitation_sent_at: datetime | None = None

    # CRITICAL FIELD: Gatekeeper for auto-send
    first_contact_initiated_at: datetime | None = Field(default=None, index=True)

    first_contact_channel: str | None = None  # story_reply, message, link_click
    enrollment_status: EnrollmentStatus = Field(default=EnrollmentStatus.INVITED, index=True)
    enrolled_at: datetime | None = None
