"""
Score model — stores fit scores and breakdowns.
"""

import enum
from typing import Any

from sqlalchemy import JSON
from sqlmodel import Field

from app.models.base import BaseModel


class ScoreType(str, enum.Enum):
    """Type of score."""

    ARTIST_FIT = "ARTIST_FIT"
    SAAS_FIT = "SAAS_FIT"
    CONFIDENCE = "CONFIDENCE"
    PRIORITY = "PRIORITY"


class Score(BaseModel, table=True):
    """
    Score model — stores calculated fit scores.

    Fields:
        prospect_id: FK to Prospect
        score_type: ARTIST_FIT, SAAS_FIT, CONFIDENCE, PRIORITY
        score: Numeric score (0-100)
        breakdown: JSON with component breakdown
        model_version: Which AI model computed this
    """

    id: int | None = Field(default=None, primary_key=True)
    prospect_id: int = Field(foreign_key="prospect.id", index=True)
    score_type: ScoreType = Field(index=True)
    score: float = Field(ge=0.0, le=100.0)
    breakdown: Any | None = Field(default=None, sa_type=JSON)
    model_version: str = Field(default="1.0")
