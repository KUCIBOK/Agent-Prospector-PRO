"""
Prospect routes — CRUD operations and discovery.
"""

import logging

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlmodel import Session, col, func, select

from app.db import get_session
from app.models import Priority, Prospect, ProspectStatus, ProspectType
from app.schemas import (
    ProspectCreate,
    ProspectResponse,
    ProspectsListResponse,
    ProspectUpdate,
)
from app.services.deep_google_source import DeepGoogleSource

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/prospects", tags=["prospects"])


@router.get("", response_model=ProspectsListResponse)
def list_prospects(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    prospect_type: ProspectType | None = None,
    status: ProspectStatus | None = None,
    priority: Priority | None = None,
    country: str | None = None,
    search: str | None = None,
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
        query = query.where(col(Prospect.country).ilike(f"%{country}%"))
    if search:
        query = query.where(
            (col(Prospect.name).ilike(f"%{search}%")) | (col(Prospect.email).ilike(f"%{search}%"))
        )

    # Count total
    if query.whereclause is not None:
        count_query = select(func.count()).select_from(Prospect).where(query.whereclause)
    else:
        count_query = select(func.count()).select_from(Prospect)
    total = session.execute(count_query).scalar() or 0

    # Paginate
    offset = (page - 1) * page_size
    result = session.execute(query.offset(offset).limit(page_size))
    prospects = result.scalars().all()

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
    try:
        # Check for duplicates by email
        if prospect_in.email:
            existing = session.exec(
                select(Prospect).where(Prospect.email == prospect_in.email)
            ).first()
            if existing:
                raise HTTPException(
                    status_code=409, detail="Prospect with this email already exists"
                )

        # Create prospect
        prospect = Prospect(**prospect_in.model_dump())
        session.add(prospect)
        session.commit()
        session.refresh(prospect)

        logger.info(f"✅ Created prospect: {prospect.name} ({prospect.id})")
        return ProspectResponse.model_validate(prospect)

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.exception("❌ Error creating prospect")
        # Server errors (DB, validation) should return 500, not 400
        raise HTTPException(status_code=500, detail="Internal server error") from e


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
        select(Prospect.type, func.count(col(Prospect.id))).group_by(Prospect.type)
    ).all()

    return {"by_type": {str(t): count for t, count in types}}


@router.get("/stats/by-priority")
def stats_by_priority(session: Session = Depends(get_session)):
    """Get prospect counts by priority."""
    priorities = session.exec(
        select(Prospect.priority, func.count(col(Prospect.id))).group_by(Prospect.priority)
    ).all()

    return {"by_priority": {str(p): count for p, count in priorities if p}}


@router.post("/deep-source")
def deep_source_curators(
    target_count: int = Query(50, ge=1, le=200),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    session: Session = Depends(get_session),
):
    """
    🔥 Deep Source Hot Curator Prospects from Google

    This endpoint:
    1. Searches Google for independent curators
    2. Extracts emails, websites, names
    3. Creates hot prospects in database
    4. Returns summary + list of created prospects

    Query parameters:
    - target_count: Number of prospects to find (default: 50, max: 200)

    Response:
    {
        "created": 50,
        "duplicates": 2,
        "errors": 0,
        "total": 52,
        "prospects": [
            {
                "id": 1,
                "name": "Marie Dubois",
                "type": "CURATOR",
                "email": "marie@galerie.fr",
                "website": "https://galerie.fr",
                "description": "African contemporary art curator"
            },
            ...
        ]
    }
    """
    try:
        logger.info(f"🔥 Starting deep source for {target_count} curator prospects...")

        # Create deep source engine
        source_engine = DeepGoogleSource(session)

        # Run deep sourcing
        results = source_engine.deep_source_curators(target_count=target_count)

        # Convert prospects to response format
        prospects_response = []
        for prospect in results.get("prospects", []):
            prospects_response.append(
                {
                    "id": prospect.id,
                    "name": prospect.name,
                    "type": str(prospect.type),
                    "email": prospect.email,
                    "website": prospect.website,
                    "description": prospect.description,
                    "country": prospect.country,
                }
            )

        response = {
            "created": results["created"],
            "duplicates": results["duplicates"],
            "errors": results["errors"],
            "total": results["total"],
            "prospects": prospects_response,
            "message": f"✅ Deep sourced {results['created']} hot curator prospects!",
            "next_steps": [
                "1. Prospects are now in database (Status: IDENTIFIED)",
                "2. System will auto-enrich profiles (24h)",
                "3. Auto-score prospects (SaaS Fit, Priority P1-P4)",
                "4. Auto-send 'Sourcing & Vetting' emails to P1-P2",
                "5. Follow-ups scheduled (days 3, 7, 14)",
            ],
        }

        logger.info(
            f"✅ Deep source complete: {results['created']} created, {results['duplicates']} duplicates"
        )

        return response

    except Exception as e:
        logger.exception("❌ Deep sourcing failed")
        raise HTTPException(status_code=500, detail="Deep sourcing failed") from e
