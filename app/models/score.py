"""
Score model — stores fit scores and breakdowns.
"""

from typing import Optional

from sqlmodel import Field, ForeignKey, JSON
import enum

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

    id: Optional[int] = Field(default=None, primary_key=True)
    prospect_id: int = Field(foreign_key="prospect.id", index=True)
    score_type: ScoreType = Field(index=True)
    score: float = Field(ge=0.0, le=100.0)
    breakdown: Optional[dict] = Field(default=None, sa_column_kwargs={"type": JSON})
    model_version: str = Field(default="1.0")
