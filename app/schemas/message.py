"""
Message schemas for outreach.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models import MessageChannel, MessageStatus, MessageOutcome


class MessageCreate(BaseModel):
    """Create message request."""

    prospect_id: int
    persona: str
    variant_label: str
    content: str
    channel: MessageChannel = MessageChannel.LINKEDIN


class MessageUpdate(BaseModel):
    """Update message request."""

    status: Optional[MessageStatus] = None
    outcome: Optional[MessageOutcome] = None


class MessageResponse(BaseModel):
    """Message response."""

    id: int
    prospect_id: int
    persona: str
    variant_label: str
    channel: MessageChannel
    content: str
    status: MessageStatus
    outcome: MessageOutcome
    generated_at: datetime
    sent_at: Optional[datetime]
    model_version: str

    class Config:
        from_attributes = True


class MessagesQueueResponse(BaseModel):
    """Outreach queue response (sorted by priority)."""

    total: int
    pending: int  # DRAFT messages
    sent: int  # SENT messages
    replied: int  # Outcome = REPLIED
    items: list[MessageResponse]
