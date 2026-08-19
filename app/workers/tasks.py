"""
Celery tasks — background jobs for discovery, enrichment, scoring, etc.
"""

import logging
from datetime import datetime

from sqlmodel import Session

from app.db import SessionLocal
from app.models import Job, JobType, JobStatus, JobError, Prospect
from app.workers.celery_app import app

logger = logging.getLogger(__name__)


def log_job_error(job_id: int, error_msg: str, stack_trace: str = None) -> None:
    """Helper to log job errors."""
    session = SessionLocal()
    try:
        error = JobError(
            job_id=job_id,
            error_message=error_msg,
            stack_trace=stack_trace,
        )
        session.add(error)
        session.commit()
    finally:
        session.close()


@app.task(bind=True, max_retries=3)
def run_discovery(self) -> dict:
    """
    Run Client & Artist Discovery.

    Should:
    1. Generate discovery queries
    2. Execute searches
    3. Parse results
    4. Create/update prospects
    """
    session = SessionLocal()
    job = None

    try:
        # Create job record
        job = Job(
            job_type=JobType.DISCOVERY,
            status=JobStatus.RUNNING,
            started_at=datetime.utcnow(),
        )
        session.add(job)
        session.commit()
        session.refresh(job)

        logger.info(f"🔍 Running Discovery (Job #{job.id})...")

        # TODO: Implement actual discovery logic
        result_count = 0

        # Mark job as success
        job.status = JobStatus.SUCCESS
        job.completed_at = datetime.utcnow()
        job.result_count = result_count
        session.add(job)
        session.commit()

        logger.info(f"✅ Discovery complete: {result_count} prospects found")
        return {"job_id": job.id, "status": "SUCCESS", "result_count": result_count}

    except Exception as exc:
        logger.error(f"❌ Discovery failed: {str(exc)}", exc_info=True)

        if job:
            job.attempts += 1
            if job.attempts < 3:
                job.status = JobStatus.RETRYING
            else:
                job.status = JobStatus.FAILED
            job.error_message = str(exc)
            session.add(job)
            session.commit()
            log_job_error(job.id, str(exc))

        # Retry
        raise self.retry(exc=exc, countdown=60)

    finally:
        session.close()


@app.task(bind=True, max_retries=3)
def run_crawling(self) -> dict:
    """
    Run web crawling for identified prospects.

    Should:
    1. Get prospects needing crawling
    2. Crawl their websites/profiles
    3. Extract data
    4. Update sources
    """
    session = SessionLocal()
    job = None

    try:
        job = Job(
            job_type=JobType.CRAWLING,
            status=JobStatus.RUNNING,
            started_at=datetime.utcnow(),
        )
        session.add(job)
        session.commit()
        session.refresh(job)

        logger.info(f"🕷️  Running Crawling (Job #{job.id})...")

        # TODO: Implement actual crawling logic
        result_count = 0

        job.status = JobStatus.SUCCESS
        job.completed_at = datetime.utcnow()
        job.result_count = result_count
        session.add(job)
        session.commit()

        logger.info(f"✅ Crawling complete: {result_count} prospects crawled")
        return {"job_id": job.id, "status": "SUCCESS", "result_count": result_count}

    except Exception as exc:
        logger.error(f"❌ Crawling failed: {str(exc)}", exc_info=True)

        if job:
            job.attempts += 1
            if job.attempts < 3:
                job.status = JobStatus.RETRYING
            else:
                job.status = JobStatus.FAILED
            job.error_message = str(exc)
            session.add(job)
            session.commit()
            log_job_error(job.id, str(exc))

        raise self.retry(exc=exc, countdown=60)

    finally:
        session.close()


@app.task(bind=True, max_retries=3)
def run_enrichment(self) -> dict:
    """
    Run data enrichment for prospects.

    Should:
    1. Get prospects needing enrichment
    2. Fill missing data
    3. Normalize values
    4. Update records
    """
    session = SessionLocal()
    job = None

    try:
        job = Job(
            job_type=JobType.ENRICHMENT,
            status=JobStatus.RUNNING,
            started_at=datetime.utcnow(),
        )
        session.add(job)
        session.commit()
        session.refresh(job)

        logger.info(f"🔄 Running Enrichment (Job #{job.id})...")

        # TODO: Implement actual enrichment logic
        result_count = 0

        job.status = JobStatus.SUCCESS
        job.completed_at = datetime.utcnow()
        job.result_count = result_count
        session.add(job)
        session.commit()

        logger.info(f"✅ Enrichment complete: {result_count} prospects enriched")
        return {"job_id": job.id, "status": "SUCCESS", "result_count": result_count}

    except Exception as exc:
        logger.error(f"❌ Enrichment failed: {str(exc)}", exc_info=True)

        if job:
            job.attempts += 1
            if job.attempts < 3:
                job.status = JobStatus.RETRYING
            else:
                job.status = JobStatus.FAILED
            job.error_message = str(exc)
            session.add(job)
            session.commit()
            log_job_error(job.id, str(exc))

        raise self.retry(exc=exc, countdown=60)

    finally:
        session.close()


@app.task(bind=True, max_retries=3)
def run_scoring(self) -> dict:
    """
    Run scoring for all prospects.

    Should:
    1. Get prospects needing scoring
    2. Calculate fit scores
    3. Update priority
    4. Generate outreach messages if P1-P3
    """
    session = SessionLocal()
    job = None

    try:
        job = Job(
            job_type=JobType.SCORING,
            status=JobStatus.RUNNING,
            started_at=datetime.utcnow(),
        )
        session.add(job)
        session.commit()
        session.refresh(job)

        logger.info(f"📊 Running Scoring (Job #{job.id})...")

        # TODO: Implement actual scoring logic
        result_count = 0

        job.status = JobStatus.SUCCESS
        job.completed_at = datetime.utcnow()
        job.result_count = result_count
        session.add(job)
        session.commit()

        logger.info(f"✅ Scoring complete: {result_count} prospects scored")
        return {"job_id": job.id, "status": "SUCCESS", "result_count": result_count}

    except Exception as exc:
        logger.error(f"❌ Scoring failed: {str(exc)}", exc_info=True)

        if job:
            job.attempts += 1
            if job.attempts < 3:
                job.status = JobStatus.RETRYING
            else:
                job.status = JobStatus.FAILED
            job.error_message = str(exc)
            session.add(job)
            session.commit()
            log_job_error(job.id, str(exc))

        raise self.retry(exc=exc, countdown=60)

    finally:
        session.close()


@app.task
def health_check() -> dict:
    """Health check task."""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}
