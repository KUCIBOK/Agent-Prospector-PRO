"""
Database connection and session management.
"""

import logging
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel

from app.config import settings

logger = logging.getLogger(__name__)

# Create engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
    pool_pre_ping=True,  # Verify connections before using
)

# Session factory
SessionLocal = sessionmaker(
    engine,
    class_=Session,
    expire_on_commit=False,
)


def init_db() -> None:
    """
    Initialize database — create all tables.

    Call this once on startup.
    """
    logger.info("🗂️  Initializing database...")
    SQLModel.metadata.create_all(engine)
    logger.info("✅ Database initialized!")


def get_session() -> Generator[Session, None, None]:
    """
    Dependency — get database session for requests.

    Usage in FastAPI:
        @app.get("/items")
        def get_items(session: Session = Depends(get_session)):
            ...
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


async def get_session_async() -> Generator[Session, None, None]:
    """Async version of get_session (for async endpoints)."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
