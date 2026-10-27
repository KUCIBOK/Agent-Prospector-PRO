"""
Celery tasks — background jobs for discovery, enrichment, scoring, etc.
"""

import logging
from datetime import datetime, timezone

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


@app.task(bind=True, max_retries=2)
def rescore_artists_advanced(self) -> dict:
    """
    Weekly task: Re-score all artists with advanced scoring.

    Advanced bonuses:
    - Major fair participation (+8-10)
    - Instagram growth trajectory (+5-7)
    - Prestigious gallery representation (+10)
    - International awards/residencies (+8)
    - Media mentions/press (+5)

    Result: Better identification of professional, market-ready artists.
    """
    session = SessionLocal()
    job = None

    try:
        from app.services.advanced_artist_scoring import AdvancedArtistScorer

        # Create job record
        job = Job(
            job_type=JobType.SCORING,
            status=JobStatus.RUNNING,
            started_at=datetime.now(timezone.utc),
        )
        session.add(job)
        session.commit()
        session.refresh(job)

        logger.info(f"📊 Advanced artist re-scoring (Job #{job.id})...")

        scorer = AdvancedArtistScorer(session)
        results = scorer.bulk_rescore_artists()

        # Mark job as success
        job.status = JobStatus.SUCCESS
        job.completed_at = datetime.now(timezone.utc)
        job.result_count = len(results)
        session.add(job)
        session.commit()

        logger.info(f"✅ Advanced re-scoring complete: {len(results)} artists updated")
        return {
            "job_id": job.id,
            "status": "SUCCESS",
            "artists_rescored": len(results),
        }

    except Exception as exc:
        logger.error(f"❌ Advanced re-scoring failed: {str(exc)}", exc_info=True)

        if job:
            job.attempts += 1
            if job.attempts < 3:
                job.status = JobStatus.RETRYING
            else:
                job.status = JobStatus.FAILED
            job.error_message = str(exc)
            session.add(job)
            session.commit()

        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))

    finally:
        session.close()


@app.task(bind=True, max_retries=2)
def detect_intent_signals(self) -> dict:
    """
    Daily task: Detect intent signals for all prospects.

    Signals:
    - LinkedIn changes (title, hires)
    - Africa exhibitions
    - New curator/advisor jobs
    - Gallery expansion/relocation
    """
    session = SessionLocal()
    job = None

    try:
        from app.services.intent_signals import IntentSignalDetector

        # Create job record
        job = Job(
            job_type=JobType.INTENT_DETECTION,
            status=JobStatus.RUNNING,
            started_at=datetime.now(timezone.utc),
        )
        session.add(job)
        session.commit()
        session.refresh(job)

        logger.info(f"🔍 Detecting intent signals (Job #{job.id})...")

        detector = IntentSignalDetector(session)
        signal_count = detector.detect_all_signals()

        # Mark job as success
        job.status = JobStatus.SUCCESS
        job.completed_at = datetime.now(timezone.utc)
        job.result_count = signal_count
        session.add(job)
        session.commit()

        logger.info(f"✅ Intent detection complete: {signal_count} signals found")
        return {
            "job_id": job.id,
            "status": "SUCCESS",
            "signal_count": signal_count,
        }

    except Exception as exc:
        logger.error(f"❌ Intent detection failed: {str(exc)}", exc_info=True)

        if job:
            job.attempts += 1
            if job.attempts < 3:
                job.status = JobStatus.RETRYING
            else:
                job.status = JobStatus.FAILED
            job.error_message = str(exc)
            session.add(job)
            session.commit()

        # Retry exponentially
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))

    finally:
        session.close()


@app.task(bind=True, max_retries=2)
def analyze_instagram_artists(self) -> dict:
    """
    Daily task: Analyze all artists' Instagram profiles.

    Detects:
    - EMERGING vs ESTABLISHED (follower count, engagement)
    - Quality score (engagement rate, post frequency, bio)
    - Signals for high-quality profiles
    """
    session = SessionLocal()
    job = None

    try:
        from app.services.instagram_artist_analyzer import InstagramArtistAnalyzer

        # Create job record
        job = Job(
            job_type=JobType.ENRICHMENT,
            status=JobStatus.RUNNING,
            started_at=datetime.now(timezone.utc),
        )
        session.add(job)
        session.commit()
        session.refresh(job)

        logger.info(f"📱 Analyzing Instagram artists (Job #{job.id})...")

        analyzer = InstagramArtistAnalyzer(session)
        results = analyzer.bulk_analyze_artists()

        # Mark job as success
        job.status = JobStatus.SUCCESS
        job.completed_at = datetime.now(timezone.utc)
        job.result_count = len(results)
        session.add(job)
        session.commit()

        logger.info(f"✅ Instagram analysis complete: {len(results)} artists analyzed")
        return {
            "job_id": job.id,
            "status": "SUCCESS",
            "artists_analyzed": len(results),
        }

    except Exception as exc:
        logger.error(f"❌ Instagram analysis failed: {str(exc)}", exc_info=True)

        if job:
            job.attempts += 1
            if job.attempts < 3:
                job.status = JobStatus.RETRYING
            else:
                job.status = JobStatus.FAILED
            job.error_message = str(exc)
            session.add(job)
            session.commit()

        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))

    finally:
        session.close()


@app.task(bind=True, max_retries=2)
def monitor_linkedin_curators(self) -> dict:
    """
    Daily task: Monitor LinkedIn curator profiles for changes.

    Detects:
    - Title changes
    - Company changes
    - New activity signals
    """
    session = SessionLocal()
    job = None

    try:
        from app.services.linkedin_curator_finder import LinkedInCuratorFinder

        # Create job record
        job = Job(
            job_type=JobType.ENRICHMENT,
            status=JobStatus.RUNNING,
            started_at=datetime.now(timezone.utc),
        )
        session.add(job)
        session.commit()
        session.refresh(job)

        logger.info(f"💼 Monitoring LinkedIn curators (Job #{job.id})...")

        curator_finder = LinkedInCuratorFinder(session)
        signals = curator_finder.monitor_linkedin_changes()

        # Mark job as success
        job.status = JobStatus.SUCCESS
        job.completed_at = datetime.now(timezone.utc)
        job.result_count = len(signals)
        session.add(job)
        session.commit()

        logger.info(f"✅ LinkedIn monitoring complete: {len(signals)} changes detected")
        return {
            "job_id": job.id,
            "status": "SUCCESS",
            "signals_detected": len(signals),
        }

    except Exception as exc:
        logger.error(f"❌ LinkedIn monitoring failed: {str(exc)}", exc_info=True)

        if job:
            job.attempts += 1
            if job.attempts < 3:
                job.status = JobStatus.RETRYING
            else:
                job.status = JobStatus.FAILED
            job.error_message = str(exc)
            session.add(job)
            session.commit()

        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))

    finally:
        session.close()


@app.task(bind=True, max_retries=3)
def run_discovery(self) -> dict:
    """
    Run Client & Artist Discovery.

    Discovers:
    1. Artists (emerging & established)
    2. Clients (advisors, curators, galleries)
    """
    session = SessionLocal()
    job = None

    try:
        from app.services.discovery import DiscoveryEngine

        # Create job record
        job = Job(
            job_type=JobType.DISCOVERY,
            status=JobStatus.RUNNING,
            started_at=datetime.now(timezone.utc),
        )
        session.add(job)
        session.commit()
        session.refresh(job)

        logger.info(f"🔍 Running Discovery (Job #{job.id})...")

        engine = DiscoveryEngine(session)

        # Discover artists
        artist_results = engine.discover_artists(limit=50)
        artist_count = artist_results["discovered"]

        # Discover clients
        client_results = engine.discover_clients(limit=50)
        client_count = client_results["discovered"]

        total = artist_count + client_count

        # Mark job as success
        job.status = JobStatus.SUCCESS
        job.completed_at = datetime.now(timezone.utc)
        job.result_count = total
        session.add(job)
        session.commit()

        logger.info(f"✅ Discovery complete: {total} prospects found ({artist_count} artists, {client_count} clients)")
        return {
            "job_id": job.id,
            "status": "SUCCESS",
            "result_count": total,
            "artists": artist_count,
            "clients": client_count,
        }

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

        raise self.retry(exc=exc, countdown=60)

    finally:
        session.close()


@app.task(bind=True, max_retries=3)
def run_crawling(self) -> dict:
    """
    Run web crawling for identified prospects.

    Crawls:
    1. Prospect websites
    2. Extract data (emails, social links, content)
    3. Update source tracking
    """
    session = SessionLocal()
    job = None

    try:
        from app.services.crawler import Crawler
        from app.models import Prospect, ProspectStatus
        from sqlmodel import select

        job = Job(
            job_type=JobType.CRAWLING,
            status=JobStatus.RUNNING,
            started_at=datetime.now(timezone.utc),
        )
        session.add(job)
        session.commit()
        session.refresh(job)

        logger.info(f"🕷️  Running Crawling (Job #{job.id})...")

        crawler = Crawler()

        # Get prospects with websites to crawl
        prospects = session.exec(
            select(Prospect)
            .where(Prospect.website.isnot(None))
            .where(Prospect.status == ProspectStatus.IDENTIFIED)
            .limit(50)
        ).all()

        result_count = 0
        for prospect in prospects:
            try:
                if prospect.website:
                    crawl_result = crawler.crawl_website(prospect.website)

                    if crawl_result.status == "SUCCESS":
                        # Update prospect with crawled data
                        if crawler.update_prospect_from_crawl(prospect, crawl_result):
                            session.add(prospect)
                            result_count += 1

                    session.commit()

            except Exception as e:
                logger.error(f"Error crawling {prospect.name}: {str(e)}")

        job.status = JobStatus.SUCCESS
        job.completed_at = datetime.now(timezone.utc)
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

    Enriches:
    1. Normalize country, email, URL, name
    2. Detect intent signals
    3. Fill missing data
    """
    session = SessionLocal()
    job = None

    try:
        from app.services.enrichment import Enrichment

        job = Job(
            job_type=JobType.ENRICHMENT,
            status=JobStatus.RUNNING,
            started_at=datetime.now(timezone.utc),
        )
        session.add(job)
        session.commit()
        session.refresh(job)

        logger.info(f"🔄 Running Enrichment (Job #{job.id})...")

        enricher = Enrichment(session)
        results = enricher.bulk_enrich_prospects(limit=100)

        job.status = JobStatus.SUCCESS
        job.completed_at = datetime.now(timezone.utc)
        job.result_count = results["enriched"]
        session.add(job)
        session.commit()

        logger.info(f"✅ Enrichment complete: {results['enriched']} prospects enriched")
        return {"job_id": job.id, "status": "SUCCESS", "result_count": results["enriched"]}

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

    Scores:
    1. Analyze prospects (AI-powered)
    2. Calculate Artist Fit / SaaS Fit scores
    3. Determine Priority (P1–P4)
    4. Generate outreach messages
    """
    session = SessionLocal()
    job = None

    try:
        from app.services.analysis import AnalysisService
        from app.services.scoring import (
            calculate_artist_fit_score,
            calculate_saas_fit_score,
            calculate_confidence_score,
            calculate_priority,
        )
        from app.services.outreach import generate_message_variants
        from app.models import (
            Prospect,
            ProspectType,
            ProspectStatus,
            Score,
            ScoreType,
            Message,
        )
        from app.ai.providers import get_ai_provider
        from sqlmodel import select

        job = Job(
            job_type=JobType.SCORING,
            status=JobStatus.RUNNING,
            started_at=datetime.now(timezone.utc),
        )
        session.add(job)
        session.commit()
        session.refresh(job)

        logger.info(f"📊 Running Scoring (Job #{job.id})...")

        ai_provider = get_ai_provider()
        analyzer = AnalysisService(session, ai_provider)

        # Batch analyze prospects
        analyzer.batch_analyze_prospects(limit=100)

        # Score and generate messages
        prospects = session.exec(
            select(Prospect)
            .where(Prospect.status == ProspectStatus.IDENTIFIED)
            .limit(100)
        ).all()

        result_count = 0
        for prospect in prospects:
            try:
                # Analyze prospect
                analysis = analyzer.analyze_prospect(prospect)

                # Calculate scores
                if prospect.type == ProspectType.ARTIST:
                    score, breakdown = calculate_artist_fit_score(prospect)
                    score_type = ScoreType.ARTIST_FIT
                else:
                    score, breakdown = calculate_saas_fit_score(prospect)
                    score_type = ScoreType.SAAS_FIT

                # Confidence
                confidence = calculate_confidence_score(prospect)
                priority = calculate_priority(score, confidence)

                # Update prospect
                prospect.score = score
                prospect.confidence = confidence
                prospect.priority = priority
                prospect.status = ProspectStatus.PREQUALIFIED

                # Store score
                score_record = Score(
                    prospect_id=prospect.id,
                    score_type=score_type,
                    score=score,
                    breakdown=breakdown,
                )
                session.add(score_record)

                # Generate outreach messages if P1-P2
                if priority and priority.value in ["P1", "P2"]:
                    variants = generate_message_variants(
                        prospect,
                        analysis.get("reason_to_contact"),
                        count=3,
                    )

                    for variant in variants:
                        message = Message(
                            prospect_id=prospect.id,
                            persona=variant["persona"],
                            variant_label=variant["variant_label"],
                            content=variant["content"],
                            status=variant["status"],
                        )
                        session.add(message)

                session.add(prospect)
                result_count += 1

            except Exception as e:
                logger.error(f"Error scoring {prospect.name}: {str(e)}")

        session.commit()

        job.status = JobStatus.SUCCESS
        job.completed_at = datetime.now(timezone.utc)
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
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}
