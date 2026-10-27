"""
Source model — tracks data origins for every claim.
"""

import enum
from datetime import datetime, timezone

from sqlmodel import Field

from app.models.base import BaseModel


class SourceType(str, enum.Enum):
    """Type of data source."""

    WEBSITE = "WEBSITE"
    SOCIAL_MEDIA = "SOCIAL_MEDIA"
    PUBLIC_PROFILE = "PUBLIC_PROFILE"
    EXHIBITION = "EXHIBITION"
    NEWS_ARTICLE = "NEWS_ARTICLE"
    DIRECTORY = "DIRECTORY"
    API = "API"
    OTHER = "OTHER"


class Source(BaseModel, table=True):
    """
    Source model — tracks where data comes from.

    Rule: Every important claim must link to a source.

    Fields:
        prospect_id: FK to Prospect
        url: Source URL
        source_type: WEBSITE, SOCIAL_MEDIA, etc.
        title: Title of page/article
        captured_text_hash: Hash of captured text (for dedup)
        captured_at: When we fetched this
    """

    id: int | None = Field(default=None, primary_key=True)
    prospect_id: int = Field(foreign_key="prospect.id", index=True)
    url: str = Field(index=True)
    source_type: SourceType
    title: str | None = None
    captured_text_hash: str | None = Field(default=None, unique=True)
    captured_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
