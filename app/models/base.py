"""
Base models and utilities for SQLModel.
"""

from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class TimestampMixin:
    """Mixin adding created_at and updated_at timestamps."""

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class BaseModel(SQLModel, TimestampMixin):
    """Base model for all database models."""

    pass
