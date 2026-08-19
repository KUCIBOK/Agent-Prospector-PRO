"""
Pydantic schemas for request/response validation.
"""

from app.schemas.prospect import (
    ProspectCreate,
    ProspectUpdate,
    ProspectResponse,
    ProspectsListResponse,
)
from app.schemas.message import (
    MessageCreate,
    MessageUpdate,
    MessageResponse,
    MessagesQueueResponse,
)
from app.schemas.job import JobResponse, JobsListResponse, MonitoringResponse

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
