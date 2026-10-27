"""
AI analysis model — stores raw LLM analysis results.
"""

from typing import Any

from sqlalchemy import JSON
from sqlmodel import Field

from app.models.base import BaseModel


class AIAnalysis(BaseModel, table=True):
    """
    AI analysis model — stores structured LLM output.

    Every important AI decision should have an audit trail:
    - What prompt was sent?
    - What model analyzed it?
    - What was the raw output?
    - When did this happen?

    Fields:
        prospect_id: FK to Prospect
        analysis_type: What we analyzed (e.g., "artist_fit", "saas_fit", "intent_signals")
        raw_output: JSON — the structured LLM response
        model_version: Which model computed this
    """

    id: int | None = Field(default=None, primary_key=True)
    prospect_id: int = Field(foreign_key="prospect.id", index=True)
    analysis_type: str = Field(index=True)  # artist_fit, saas_fit, intent_signals
    raw_output: Any = Field(sa_type=JSON)
    model_version: str = Field(default="1.0")
