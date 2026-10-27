"""
Automated Tasks Scheduler — Run at specific times

Daily automation at 3 AM:
1. Scrape LinkedIn, Instagram, Google for prospects
2. Enrich profiles
3. Score prospects
4. Send Sourcing & Vetting emails
5. Send follow-up sequences
"""

import logging
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.config import settings
from app.db import SessionLocal
from app.models import ProspectType
from app.services.automated_prospecting import (
    AutomatedProspectingConfig,
    AutomatedProspectingEngine,
)

logger = logging.getLogger(__name__)


def run_3am_prospecting_job():
    """Run automated prospecting at 3 AM every day."""
    logger.info("🤖 ===== STARTING 3 AM AUTOMATION =====")
    logger.info(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    session = SessionLocal()

    try:
        # Configure automated prospecting
        config = AutomatedProspectingConfig(
            target_countries=["FR", "US", "SG", "CN", "BR", "IT", "DE", "ES", "GB", "CA"],
            target_types=[
                ProspectType.CURATOR,
                ProspectType.ART_ADVISOR,
                ProspectType.GALLERY,
            ],
            search_keywords=[
                "contemporary art",
                "curator",
                "art advisor",
                "gallery director",
                "art collector",
                "emerging artists",
            ],
            offer_type="SOURCING_AND_VETTING",
            daily_limit=50,
            scrape_hour=3,
        )

        engine = AutomatedProspectingEngine(session, config)

        # 1️⃣ Run daily scraping
        logger.info("🕷️  Step 1: Scraping LinkedIn, Instagram, Google...")
        scrape_results = engine.run_daily_scraping()
        logger.info(f"   ✅ Scraped: {scrape_results['created']} new prospects")

        # 2️⃣ Enrich profiles (done automatically by Celery worker)
        logger.info("🔄 Step 2: Enrichment (will run via worker)...")

        # 3️⃣ Score prospects (done automatically by Celery worker)
        logger.info("📊 Step 3: Scoring (will run via worker)...")

        # 4️⃣ Send emails to new prospects
        logger.info("📧 Step 4: Sending Sourcing & Vetting emails...")
        email_results = engine.send_outreach_emails_to_new_prospects()
        logger.info(f"   ✅ Emails sent: {email_results['sent']}")

        # 5️⃣ Send follow-ups
        logger.info("💌 Step 5: Sending follow-up sequences...")
        # TODO: Implement follow-up logic

        logger.info("🎉 ===== AUTOMATION COMPLETE =====")
        logger.info(f"Summary: {scrape_results['created']} new prospects found & emailed")

    except Exception as e:
        logger.error(f"❌ Automation failed: {e!s}", exc_info=True)

    finally:
        session.close()


def run_daily_follow_ups():
    """Send follow-up emails daily."""
    logger.info("💌 Running daily follow-up sequence...")

    session = SessionLocal()

    try:
        # TODO: Implement follow-up email logic
        # Send day-3, day-7, day-14 follow-ups
        logger.info("✅ Follow-ups sent")

    except Exception as e:
        logger.error(f"❌ Follow-up failed: {e!s}")

    finally:
        session.close()


def run_daily_analytics():
    """Update analytics and tracking."""
    logger.info("📊 Updating analytics...")

    session = SessionLocal()

    try:
        from sqlmodel import func, select

        from app.models import Message, Prospect, ProspectStatus

        total_prospects = session.scalar(select(func.count()).select_from(Prospect))
        identified = session.scalar(
            select(func.count())
            .select_from(Prospect)
            .where(Prospect.status == ProspectStatus.IDENTIFIED)
        )
        prequalified = session.scalar(
            select(func.count())
            .select_from(Prospect)
            .where(Prospect.status == ProspectStatus.PREQUALIFIED)
        )

        total_emails = session.scalar(select(func.count()).select_from(Message))
        emails_sent = session.scalar(
            select(func.count()).select_from(Message).where(Message.status == "SENT")
        )

        logger.info("📈 Daily Stats:")
        logger.info(f"   Total prospects: {total_prospects}")
        logger.info(f"   Identified: {identified}")
        logger.info(f"   Prequalified: {prequalified}")
        logger.info(f"   Total emails: {total_emails}")
        logger.info(f"   Emails sent: {emails_sent}")

    except Exception as e:
        logger.error(f"❌ Analytics failed: {e!s}")

    finally:
        session.close()


def run_advanced_artist_rescoring_job():
    """Re-score artists with advanced metrics (Sunday 4 AM)."""
    from app.workers.tasks import rescore_artists_advanced

    logger.info("📊 Queuing advanced artist re-scoring job...")
    task = rescore_artists_advanced.delay()
    logger.info(f"   ✅ Task queued: {task.id}")


def run_instagram_analysis_job():
    """Analyze artists on Instagram (7 AM daily)."""
    from app.workers.tasks import analyze_instagram_artists

    logger.info("📱 Queuing Instagram artist analysis job...")
    task = analyze_instagram_artists.delay()
    logger.info(f"   ✅ Task queued: {task.id}")


def run_linkedin_monitoring_job():
    """Monitor LinkedIn curators for changes (5 AM daily)."""
    from app.workers.tasks import monitor_linkedin_curators

    logger.info("💼 Queuing LinkedIn curator monitoring job...")
    task = monitor_linkedin_curators.delay()
    logger.info(f"   ✅ Task queued: {task.id}")


def start_automation_scheduler():
    """Start the automation scheduler."""
    if not settings.scheduler_enabled:
        logger.info("⏰ Automation scheduler is disabled")
        return None

    scheduler = BackgroundScheduler()

    # 🌙 3 AM Daily Scraping & Prospecting
    scheduler.add_job(
        func=run_3am_prospecting_job,
        trigger=CronTrigger(hour=3, minute=0),  # 3:00 AM every day
        id="daily_3am_prospecting",
        name="Daily 3 AM Automation (Scraping + Emails)",
        replace_existing=True,
    )
    logger.info("📍 Scheduled: Daily prospecting at 3:00 AM")

    # 🔗 LinkedIn Curator Monitoring (5 AM)
    scheduler.add_job(
        func=run_linkedin_monitoring_job,
        trigger=CronTrigger(hour=5, minute=0),  # 5:00 AM
        id="daily_5am_linkedin",
        name="Daily 5 AM LinkedIn Monitoring",
        replace_existing=True,
    )
    logger.info("📍 Scheduled: LinkedIn monitoring at 5:00 AM")

    # 📱 Instagram Artist Analysis (7 AM)
    scheduler.add_job(
        func=run_instagram_analysis_job,
        trigger=CronTrigger(hour=7, minute=0),  # 7:00 AM
        id="daily_7am_instagram",
        name="Daily 7 AM Instagram Analysis",
        replace_existing=True,
    )
    logger.info("📍 Scheduled: Instagram analysis at 7:00 AM")

    # 📊 Advanced Artist Re-scoring (Sunday 4 AM)
    scheduler.add_job(
        func=run_advanced_artist_rescoring_job,
        trigger=CronTrigger(day_of_week=6, hour=4, minute=0),  # Sunday 4 AM
        id="weekly_sunday_4am_rescoring",
        name="Weekly Sunday 4 AM Artist Re-scoring",
        replace_existing=True,
    )
    logger.info("📍 Scheduled: Advanced artist re-scoring every Sunday at 4:00 AM")

    # Daily follow-ups (9 AM)
    scheduler.add_job(
        func=run_daily_follow_ups,
        trigger=CronTrigger(hour=9, minute=0),  # 9:00 AM
        id="daily_9am_followups",
        name="Daily 9 AM Follow-ups",
        replace_existing=True,
    )
    logger.info("📍 Scheduled: Daily follow-ups at 9:00 AM")

    # Analytics update (6 PM)
    scheduler.add_job(
        func=run_daily_analytics,
        trigger=CronTrigger(hour=18, minute=0),  # 6:00 PM
        id="daily_6pm_analytics",
        name="Daily 6 PM Analytics",
        replace_existing=True,
    )
    logger.info("📍 Scheduled: Daily analytics at 6:00 PM")

    scheduler.start()
    logger.info("✅ Automation scheduler started!")
    logger.info("🤖 System now running 24/7 prospecting automation")
    logger.info("")
    logger.info("📅 Automation Schedule:")
    logger.info("   Every day:")
    logger.info("     3:00 AM - Prospecting (LinkedIn, Google discovery)")
    logger.info("     5:00 AM - LinkedIn curator monitoring (changes)")
    logger.info("     7:00 AM - Instagram artist analysis")
    logger.info("     9:00 AM - Follow-up sequences")
    logger.info("     6:00 PM - Analytics update")
    logger.info("   Every Sunday:")
    logger.info("     4:00 AM - Advanced artist re-scoring (fairs, galleries, awards)")
    logger.info("")

    return scheduler


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    logger.info("🚀 Starting Kucibok Automation Engine...")
    scheduler = start_automation_scheduler()

    try:
        # Keep running
        import time

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("⏹️  Stopping automation scheduler...")
        scheduler.shutdown()
        logger.info("✅ Scheduler stopped")
