"""
Job monitoring schemas.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models import JobType, JobStatus


class JobResponse(BaseModel):
    """Job response."""

    id: int
    job_type: JobType
    status: JobStatus
    attempts: int
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error_message: Optional[str]
    result_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class JobsListResponse(BaseModel):
    """List jobs response."""

    total: int
    pending: int
    running: int
    success: int
    failed: int
    items: list[JobResponse]


class MonitoringResponse(BaseModel):
    """System monitoring response."""

    status: str  # "ok", "warning", "error"
    uptime_seconds: int
    total_prospects: int
    total_artists: int
    total_clients: int
    jobs: JobsListResponse
    last_discovery: Optional[datetime]
    last_scoring: Optional[datetime]
    last_outreach_generation: Optional[datetime]
    database_size_mb: float
    cache_size_mb: float
