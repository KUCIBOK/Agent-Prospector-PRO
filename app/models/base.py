"""
Base models and utilities for SQLModel.
"""

from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class TimestampMixin:
    """Mixin adding created_at and updated_at timestamps."""

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BaseModel(SQLModel, TimestampMixin):
    """Base model for all database models."""
