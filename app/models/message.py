"""
Message model — outreach messages for LinkedIn.
"""

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, ForeignKey
import enum

from app.models.base import BaseModel


class MessageChannel(str, enum.Enum):
    """Outreach channel."""

    LINKEDIN = "LINKEDIN"
    EMAIL = "EMAIL"
    INSTAGRAM = "INSTAGRAM"


class MessageStatus(str, enum.Enum):
    """Message status in workflow."""

    DRAFT = "DRAFT"  # Generated, not sent
    SENT = "SENT"  # Manually sent
    OPENED = "OPENED"
    REPLIED = "REPLIED"


class MessageOutcome(str, enum.Enum):
    """Outcome after contact."""

    NONE = "NONE"
    REPLIED = "REPLIED"
    MEETING = "MEETING"
    CUSTOMER = "CUSTOMER"
    LOST = "LOST"
    NOT_RELEVANT = "NOT_RELEVANT"


class Message(BaseModel, table=True):
    """
    Message model — outreach messages.

    Generated automatically for prospects, sent manually on LinkedIn.
    No approval step before manual send (guardrail: accuracy check).

    Fields:
        prospect_id: FK to Prospect
        persona: ART_ADVISOR or CURATOR
        variant_label: Short label (e.g., "variant_1_short")
        channel: LINKEDIN (only for V1.1)
        content: Message text (no markdown, plain)
        status: DRAFT → SENT
        outcome: REPLIED, MEETING, CUSTOMER, LOST, NOT_RELEVANT
        generated_at: When system generated this
        sent_at: When human sent it
        model_version: AI model that generated it
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    prospect_id: int = Field(foreign_key="prospect.id", index=True)
    persona: str = Field(index=True)  # ART_ADVISOR or CURATOR
    variant_label: str
    channel: MessageChannel = Field(default=MessageChannel.LINKEDIN)
    content: str
    status: MessageStatus = Field(default=MessageStatus.DRAFT, index=True)
    outcome: MessageOutcome = Field(default=MessageOutcome.NONE, index=True)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    sent_at: Optional[datetime] = None
    model_version: str = Field(default="1.0")
