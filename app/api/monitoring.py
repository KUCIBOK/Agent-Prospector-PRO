"""
Monitoring routes — system health and job status.
"""

import logging
import os
import time
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlmodel import select, func

from app.db import get_session
from app.models import (
    Prospect,
    ProspectType,
    Job,
    JobStatus,
    Message,
    Signal,
)
from app.schemas import JobResponse, JobsListResponse, MonitoringResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/monitoring", tags=["monitoring"])

# App start time
START_TIME = time.time()


@router.get("/health")
def health_check():
    """Simple health check."""
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime_seconds": int(time.time() - START_TIME),
    }


@router.get("/jobs", response_model=JobsListResponse)
def list_jobs(
    session: Session = Depends(get_session),
    status: str = Query(None),
    limit: int = Query(50, ge=1, le=500),
) -> JobsListResponse:
    """List recent jobs with status breakdown."""
    query = select(Job).order_by(Job.created_at.desc()).limit(limit)

    if status:
        query = query.where(Job.status == status)

    jobs = session.exec(query).all()

    # Count by status
    pending = session.scalar(select(func.count()).select_from(Job).where(Job.status == JobStatus.PENDING))
    running = session.scalar(select(func.count()).select_from(Job).where(Job.status == JobStatus.RUNNING))
    success = session.scalar(select(func.count()).select_from(Job).where(Job.status == JobStatus.SUCCESS))
    failed = session.scalar(select(func.count()).select_from(Job).where(Job.status == JobStatus.FAILED))

    return JobsListResponse(
        total=len(jobs),
        pending=pending or 0,
        running=running or 0,
        success=success or 0,
        failed=failed or 0,
        items=[JobResponse.model_validate(j) for j in jobs],
    )


@router.get("/prospects/stats")
def prospect_stats(session: Session = Depends(get_session)):
    """Get prospect statistics."""
    total = session.scalar(select(func.count()).select_from(Prospect))

    # By type
    artists = session.scalar(
        select(func.count()).select_from(Prospect).where(Prospect.type == ProspectType.ARTIST)
    )
    advisors = session.scalar(
        select(func.count()).select_from(Prospect).where(Prospect.type == ProspectType.ART_ADVISOR)
    )
    curators = session.scalar(
        select(func.count()).select_from(Prospect).where(Prospect.type == ProspectType.CURATOR)
    )
    galleries = session.scalar(
        select(func.count()).select_from(Prospect).where(Prospect.type == ProspectType.GALLERY)
    )

    # By priority
    p1 = session.scalar(select(func.count()).select_from(Prospect).where(Prospect.priority == "P1"))
    p2 = session.scalar(select(func.count()).select_from(Prospect).where(Prospect.priority == "P2"))
    p3 = session.scalar(select(func.count()).select_from(Prospect).where(Prospect.priority == "P3"))
    p4 = session.scalar(select(func.count()).select_from(Prospect).where(Prospect.priority == "P4"))

    return {
        "total": total or 0,
        "by_type": {
            "artists": artists or 0,
            "advisors": advisors or 0,
            "curators": curators or 0,
            "galleries": galleries or 0,
        },
        "by_priority": {
            "P1": p1 or 0,
            "P2": p2 or 0,
            "P3": p3 or 0,
            "P4": p4 or 0,
        },
    }


@router.get("/messages/stats")
def message_stats(session: Session = Depends(get_session)):
    """Get message statistics."""
    total = session.scalar(select(func.count()).select_from(Message))
    draft = session.scalar(select(func.count()).select_from(Message).where(Message.status == "DRAFT"))
    sent = session.scalar(select(func.count()).select_from(Message).where(Message.status == "SENT"))
    replied = session.scalar(select(func.count()).select_from(Message).where(Message.outcome == "REPLIED"))
    meeting = session.scalar(select(func.count()).select_from(Message).where(Message.outcome == "MEETING"))
    customer = session.scalar(select(func.count()).select_from(Message).where(Message.outcome == "CUSTOMER"))

    return {
        "total": total or 0,
        "by_status": {
            "draft": draft or 0,
            "sent": sent or 0,
        },
        "by_outcome": {
            "replied": replied or 0,
            "meeting": meeting or 0,
            "customer": customer or 0,
        },
    }


@router.get("/system")
def system_info():
    """Get system information."""
    return {
        "uptime_seconds": int(time.time() - START_TIME),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "environment": os.getenv("ENVIRONMENT", "production"),
        "debug": os.getenv("DEBUG", "false").lower() == "true",
    }


@router.post("/jobs/rescore-artists-advanced")
def trigger_artist_rescoring():
    """Trigger advanced artist re-scoring job."""
    from app.workers.tasks import rescore_artists_advanced

    task = rescore_artists_advanced.delay()
    return {
        "status": "queued",
        "task_id": task.id,
        "message": "Advanced artist re-scoring job queued",
    }


@router.post("/jobs/analyze-instagram")
def trigger_instagram_analysis():
    """Trigger Instagram artist analysis job."""
    from app.workers.tasks import analyze_instagram_artists

    task = analyze_instagram_artists.delay()
    return {
        "status": "queued",
        "task_id": task.id,
        "message": "Instagram artist analysis job queued",
    }


@router.post("/jobs/monitor-linkedin")
def trigger_linkedin_monitoring():
    """Trigger LinkedIn curator monitoring job."""
    from app.workers.tasks import monitor_linkedin_curators

    task = monitor_linkedin_curators.delay()
    return {
        "status": "queued",
        "task_id": task.id,
        "message": "LinkedIn curator monitoring job queued",
    }


@router.get("/signals/recent")
def recent_signals(
    session: Session = Depends(get_session),
    limit: int = Query(10, ge=1, le=100),
    days: int = Query(7, ge=1, le=90),
):
    """Get recently detected intent signals."""
    from datetime import timedelta

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    signals = session.exec(
        select(Signal)
        .where(Signal.signal_date >= cutoff)
        .order_by(Signal.signal_date.desc())
        .limit(limit)
    ).all()

    return {
        "total": len(signals),
        "signals": [
            {
                "id": s.id,
                "prospect_id": s.prospect_id,
                "signal_type": s.signal_type,
                "description": s.description,
                "source_url": s.source_url,
                "signal_date": s.signal_date.isoformat(),
                "importance": s.importance,
                "confidence": s.confidence,
            }
            for s in signals
        ],
    }


@router.get("/summary")
def summary(session: Session = Depends(get_session)):
    """Get summary dashboard data."""
    prospects_total = session.scalar(select(func.count()).select_from(Prospect))
    artists = session.scalar(
        select(func.count()).select_from(Prospect).where(Prospect.type == ProspectType.ARTIST)
    )
    clients = prospects_total - artists if prospects_total else 0

    messages_total = session.scalar(select(func.count()).select_from(Message))
    messages_draft = session.scalar(select(func.count()).select_from(Message).where(Message.status == "DRAFT"))
    messages_sent = session.scalar(select(func.count()).select_from(Message).where(Message.status == "SENT"))

    jobs_total = session.scalar(select(func.count()).select_from(Job))
    jobs_failed = session.scalar(select(func.count()).select_from(Job).where(Job.status == JobStatus.FAILED))

    # NEW: Count recent signals (last 7 days)
    from datetime import timedelta
    recent_cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    recent_signals = session.scalar(
        select(func.count()).select_from(Signal).where(Signal.signal_date >= recent_cutoff)
    )

    return {
        "prospects": {
            "total": prospects_total or 0,
            "artists": artists or 0,
            "clients": clients or 0,
        },
        "messages": {
            "total": messages_total or 0,
            "draft": messages_draft or 0,
            "sent": messages_sent or 0,
        },
        "jobs": {
            "total": jobs_total or 0,
            "failed": jobs_failed or 0,
        },
        "signals": {
            "recent": recent_signals or 0,  # NEW: signals in last 7 days
        },
        "uptime_seconds": int(time.time() - START_TIME),
    }
