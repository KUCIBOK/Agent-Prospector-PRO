"""
Pydantic schemas for request/response validation.
"""

from app.schemas.job import JobResponse, JobsListResponse, MonitoringResponse
from app.schemas.message import (
    MessageCreate,
    MessageResponse,
    MessagesQueueResponse,
    MessageUpdate,
)
from app.schemas.prospect import (
    ProspectCreate,
    ProspectResponse,
    ProspectsListResponse,
    ProspectUpdate,
)

__all__ = [
    # Prospect
    "ProspectCreate",
    "ProspectUpdate",
    "ProspectResponse",
    "ProspectsListResponse",
    # Message
    "MessageCreate",
    "MessageUpdate",
    "MessageResponse",
    "MessagesQueueResponse",
    # Job & Monitoring
    "JobResponse",
    "JobsListResponse",
    "MonitoringResponse",
]
