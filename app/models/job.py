"""
Job model — tracks async job execution.
"""

import enum
from datetime import datetime

from sqlmodel import Field

from app.models.base import BaseModel


class JobType(str, enum.Enum):
    """Type of background job."""

    DISCOVERY = "DISCOVERY"
    INTENT_DETECTION = "INTENT_DETECTION"  # NEW: Detect signals for existing prospects
    CRAWLING = "CRAWLING"
    ENRICHMENT = "ENRICHMENT"
    ANALYSIS = "ANALYSIS"
    SCORING = "SCORING"
    OUTREACH_GENERATION = "OUTREACH_GENERATION"
    ARTIST_ONBOARDING = "ARTIST_ONBOARDING"
    BACKUP = "BACKUP"
    MAINTENANCE = "MAINTENANCE"


class JobStatus(str, enum.Enum):
    """Job execution status."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    RETRYING = "RETRYING"


class Job(BaseModel, table=True):
    """
    Job model — tracks background job execution.

    Fields:
        job_type: Type of job
        status: PENDING → RUNNING → SUCCESS/FAILED
        attempts: Number of attempts (max 3)
        started_at: When job started
        completed_at: When job finished
        error_message: Error message if FAILED
        result_count: Number of items processed
    """

    id: int | None = Field(default=None, primary_key=True)
    job_type: JobType = Field(index=True)
    status: JobStatus = Field(default=JobStatus.PENDING, index=True)
    attempts: int = Field(default=0, ge=0, le=3)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None
    result_count: int = Field(default=0)
