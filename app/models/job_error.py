"""
Job error model — detailed error logging.
"""

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, ForeignKey

from app.models.base import BaseModel


class JobError(BaseModel, table=True):
    """
    Job error model — detailed error tracking.

    Fields:
        job_id: FK to Job that failed
        error_message: Error message
        stack_trace: Full stack trace
        timestamp: When error occurred
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: int = Field(foreign_key="job.id", index=True)
    error_message: str
    stack_trace: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)
