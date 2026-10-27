"""
Base models and utilities for SQLModel.
"""

from datetime import datetime, timezone
from typing import Optional, Protocol

from sqlmodel import Field, SQLModel


class TimestampMixin:
    """Mixin adding created_at and updated_at timestamps."""

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BaseModel(SQLModel, TimestampMixin):
    """Base model for all database models."""


class _HasId(Protocol):
    id: Optional[int]


def require_id(obj: _HasId) -> int:
    """Return obj.id, failing loudly if the row has not been saved yet."""
    if obj.id is None:
        raise ValueError(f"{type(obj).__name__} has no id: add and flush it to the session first")
    return obj.id
