"""
Database models (SQLModel) — all models for export.
"""

from app.models.ai_analysis import AIAnalysis
from app.models.artist_contact import ArtistContact, EnrollmentStatus
from app.models.base import BaseModel, TimestampMixin
from app.models.job import Job, JobStatus, JobType
from app.models.job_error import JobError
from app.models.message import Message, MessageChannel, MessageOutcome, MessageStatus
from app.models.prospect import (
    ConfidenceLevel,
    Priority,
    Prospect,
    ProspectStatus,
    ProspectType,
    RecommendedAngle,
)
from app.models.score import Score, ScoreType
from app.models.signal import Confidence, Importance, Signal, SignalType
from app.models.source import Source, SourceType

__all__ = [
    # Base
    "BaseModel",
    "TimestampMixin",
    # Prospect
    "Prospect",
    "ProspectType",
    "ProspectStatus",
    "Priority",
    "ConfidenceLevel",
    "RecommendedAngle",
    # Source
    "Source",
    "SourceType",
    # Signal
    "Signal",
    "SignalType",
    "Importance",
    "Confidence",
    # Score
    "Score",
    "ScoreType",
    # Message
    "Message",
    "MessageChannel",
    "MessageStatus",
    "MessageOutcome",
    # Artist Contact
    "ArtistContact",
    "EnrollmentStatus",
    # Job
    "Job",
    "JobType",
    "JobStatus",
    # Error
    "JobError",
    # AI Analysis
    "AIAnalysis",
]
