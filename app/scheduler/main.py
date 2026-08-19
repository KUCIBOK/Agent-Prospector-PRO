"""
Job scheduler — runs pipelines on a daily schedule.

Configurable via .env:
- DISCOVERY_SCHEDULE_HOUR (default: 8)
- CRAWLING_SCHEDULE_HOUR (default: 9)
- ENRICHMENT_SCHEDULE_HOUR (default: 10)
- ANALYSIS_SCHEDULE_HOUR (default: 11)
- SCORING_SCHEDULE_HOUR (default: 12)
"""

import logging
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.config import settings
from app.workers.tasks import (
    run_discovery,
    run_crawling,
    run_enrichment,
    run_scoring,
)

logger = logging.getLogger(__name__)


def start_scheduler() -> BackgroundScheduler:
    """Initialize and start the job scheduler."""
    if not settings.scheduler_enabled:
        logger.info("⏰ Scheduler is disabled (SCHEDULER_ENABLED=false)")
        return None

    scheduler = BackgroundScheduler()

    # Discovery
    scheduler.add_job(
        func=run_discovery.delay,
        trigger=CronTrigger(hour=settings.discovery_schedule_hour, minute=0),
        id="discovery",
        name="Client & Artist Discovery",
        replace_existing=True,
    )
    logger.info(f"📍 Scheduled Discovery at {settings.discovery_schedule_hour}:00")

    # Crawling
    scheduler.add_job(
        func=run_crawling.delay,
        trigger=CronTrigger(hour=settings.crawling_schedule_hour, minute=0),
        id="crawling",
        name="Web Crawling",
        replace_existing=True,
    )
    logger.info(f"🕷️  Scheduled Crawling at {settings.crawling_schedule_hour}:00")

    # Enrichment
    scheduler.add_job(
        func=run_enrichment.delay,
        trigger=CronTrigger(hour=settings.enrichment_schedule_hour, minute=0),
        id="enrichment",
        name="Data Enrichment",
        replace_existing=True,
    )
    logger.info(f"🔄 Scheduled Enrichment at {settings.enrichment_schedule_hour}:00")

    # Scoring
    scheduler.add_job(
        func=run_scoring.delay,
        trigger=CronTrigger(hour=settings.scoring_schedule_hour, minute=0),
        id="scoring",
        name="Scoring & Outreach Generation",
        replace_existing=True,
    )
    logger.info(f"📊 Scheduled Scoring at {settings.scoring_schedule_hour}:00")

    scheduler.start()
    logger.info("✅ Scheduler started!")

    return scheduler


if __name__ == "__main__":
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    logger.info("🚀 Starting APScheduler...")
    scheduler = start_scheduler()

    try:
        # Keep scheduler running
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("⏹️  Stopping scheduler...")
        scheduler.shutdown()
        logger.info("✅ Scheduler stopped")
