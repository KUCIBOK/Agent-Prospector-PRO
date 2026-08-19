"""
Celery application configuration.
"""

import logging
from celery import Celery

from app.config import settings

logger = logging.getLogger(__name__)

# Create Celery app
app = Celery(
    "kucibok",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

# Configure Celery
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minute hard limit
    task_soft_time_limit=25 * 60,  # 25 minute soft limit
    worker_prefetch_multiplier=1,  # Process one task at a time
    worker_max_tasks_per_child=1000,
)

logger.info("✅ Celery app initialized")
