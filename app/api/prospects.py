"""
Prospect routes — CRUD operations and discovery.
"""

from typing import Optional
import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlmodel import select, func

from app.db import get_session
from app.models import Prospect, ProspectType, ProspectStatus, Priority
from app.schemas import (
    ProspectCreate,
    ProspectUpdate,
    ProspectResponse,
    ProspectsListResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/prospects", tags=["prospects"])


@router.get("", response_model=ProspectsListResponse)
def list_prospects(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    prospect_type: Optional[ProspectType] = None,
    status: Optional[ProspectStatus] = None,
    priority: Optional[Priority] = None,
    country: Optional[str] = None,
    search: Optional[str] = None,
) -> ProspectsListResponse:
    """
    List prospects with filtering and pagination.

    Query parameters:
    - page: Page number (default: 1)
    - page_size: Items per page (default: 20, max: 100)
    - prospect_type: Filter by type (ARTIST, ART_ADVISOR, CURATOR, etc.)
    - status: Filter by status (IDENTIFIED, PREQUALIFIED, etc.)
    - priority: Filter by priority (P1, P2, P3, P4)
    - country: Filter by country
    - search: Search by name or email
    """
    query = select(Prospect)

    # Apply filters
    if prospect_type:
        query = query.where(Prospect.type == prospect_type)
    if status:
        query = query.where(Prospect.status == status)
    if priority:
        query = query.where(Prospect.priority == priority)
    if country:
        query = query.where(Prospect.country.ilike(f"%{country}%"))
    if search:
        query = query.where(
            (Prospect.name.ilike(f"%{search}%")) | (Prospect.email.ilike(f"%{search}%"))
        )

    # Count total
    total = session.scalar(select(func.count()).select_from(Prospect).where(query.whereclause))

    # Paginate
    offset = (page - 1) * page_size
    prospects = session.exec(query.offset(offset).limit(page_size)).all()

    return ProspectsListResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=[ProspectResponse.model_validate(p) for p in prospects],
    )


@router.get("/{prospect_id}", response_model=ProspectResponse)
def get_prospect(prospect_id: int, session: Session = Depends(get_session)) -> ProspectResponse:
    """Get a specific prospect by ID."""
    prospect = session.get(Prospect, prospect_id)
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect not found")
    return ProspectResponse.model_validate(prospect)


@router.post("", response_model=ProspectResponse, status_code=201)
def create_prospect(
    prospect_in: ProspectCreate,
    session: Session = Depends(get_session),
) -> ProspectResponse:
    """Create a new prospect."""
    # Check for duplicates
    existing = session.exec(
        select(Prospect).where(
            (Prospect.email == prospect_in.email) if prospect_in.email else False
        )
    ).first()

    if existing:
        raise HTTPException(status_code=409, detail="Prospect with this email already exists")

    prospect = Prospect(**prospect_in.model_dump())
    session.add(prospect)
    session.commit()
    session.refresh(prospect)

    logger.info(f"✅ Created prospect: {prospect.name} ({prospect.id})")
    return ProspectResponse.model_validate(prospect)


@router.patch("/{prospect_id}", response_model=ProspectResponse)
def update_prospect(
    prospect_id: int,
    prospect_in: ProspectUpdate,
    session: Session = Depends(get_session),
) -> ProspectResponse:
    """Update a prospect."""
    prospect = session.get(Prospect, prospect_id)
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect not found")

    update_data = prospect_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(prospect, key, value)

    session.add(prospect)
    session.commit()
    session.refresh(prospect)

    logger.info(f"✅ Updated prospect: {prospect.name} ({prospect_id})")
    return ProspectResponse.model_validate(prospect)


@router.delete("/{prospect_id}", status_code=204)
def delete_prospect(prospect_id: int, session: Session = Depends(get_session)) -> None:
    """Delete a prospect (hard delete)."""
    prospect = session.get(Prospect, prospect_id)
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect not found")

    session.delete(prospect)
    session.commit()

    logger.info(f"✅ Deleted prospect: {prospect_id}")


@router.get("/stats/by-type")
def stats_by_type(session: Session = Depends(get_session)):
    """Get prospect counts by type."""
    types = session.exec(
        select(Prospect.type, func.count(Prospect.id)).group_by(Prospect.type)
    ).all()

    return {"by_type": {str(t): count for t, count in types}}


@router.get("/stats/by-priority")
def stats_by_priority(session: Session = Depends(get_session)):
    """Get prospect counts by priority."""
    priorities = session.exec(
        select(Prospect.priority, func.count(Prospect.id)).group_by(Prospect.priority)
    ).all()

    return {"by_priority": {str(p): count for p, count in priorities if p}}
