"""
Application configuration — loaded from environment variables.
"""

import os
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings, loaded from .env.
    """

    # ========================================================================
    # API & Server
    # ========================================================================
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", 8000))
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    secret_key: str = os.getenv("SECRET_KEY", "change-me-in-production")

    # ========================================================================
    # Database (PostgreSQL)
    # ========================================================================
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://kucibok:changeme@localhost:5432/kucibok_prospector",
    )

    # ========================================================================
    # Redis (Cache & Job Queue)
    # ========================================================================
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    # ========================================================================
    # AI / LLM (Ollama)
    # ========================================================================
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    model_name: str = os.getenv("MODEL_NAME", "llama2")
    model_temperature: float = float(os.getenv("MODEL_TEMPERATURE", 0.7))
    model_max_tokens: int = int(os.getenv("MODEL_MAX_TOKENS", 2048))

    # ========================================================================
    # Celery (Job Queue)
    # ========================================================================
    celery_broker_url: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    celery_result_backend: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

    # ========================================================================
    # Scheduler
    # ========================================================================
    scheduler_enabled: bool = os.getenv("SCHEDULER_ENABLED", "true").lower() == "true"
    discovery_schedule_hour: int = int(os.getenv("DISCOVERY_SCHEDULE_HOUR", 8))
    crawling_schedule_hour: int = int(os.getenv("CRAWLING_SCHEDULE_HOUR", 9))
    enrichment_schedule_hour: int = int(os.getenv("ENRICHMENT_SCHEDULE_HOUR", 10))
    analysis_schedule_hour: int = int(os.getenv("ANALYSIS_SCHEDULE_HOUR", 11))
    scoring_schedule_hour: int = int(os.getenv("SCORING_SCHEDULE_HOUR", 12))

    # ========================================================================
    # Crawler & Discovery
    # ========================================================================
    crawler_timeout: int = int(os.getenv("CRAWLER_TIMEOUT", 30))
    crawler_retry_attempts: int = int(os.getenv("CRAWLER_RETRY_ATTEMPTS", 3))
    crawler_user_agent: str = os.getenv(
        "CRAWLER_USER_AGENT", "Kucibok-Prospector/1.1 (+http://kucibok.com/bot)"
    )
    crawler_respect_robots_txt: bool = (
        os.getenv("CRAWLER_RESPECT_ROBOTS_TXT", "true").lower() == "true"
    )
    crawler_follow_redirects: bool = (
        os.getenv("CRAWLER_FOLLOW_REDIRECTS", "true").lower() == "true"
    )

    # ========================================================================
    # Outreach Engine
    # ========================================================================
    outreach_enabled: bool = os.getenv("OUTREACH_ENABLED", "true").lower() == "true"
    outreach_min_priority: str = os.getenv("OUTREACH_MIN_PRIORITY", "P2")
    outreach_min_confidence: str = os.getenv("OUTREACH_MIN_CONFIDENCE", "MEDIUM")
    linkedin_account_url: Optional[str] = os.getenv("LINKEDIN_ACCOUNT_URL")

    # ========================================================================
    # Artist Onboarding (Instagram)
    # ========================================================================
    artist_onboarding_enabled: bool = (
        os.getenv("ARTIST_ONBOARDING_ENABLED", "true").lower() == "true"
    )
    instagram_business_account_id: Optional[str] = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")
    instagram_access_token: Optional[str] = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    instagram_webhook_verify_token: Optional[str] = os.getenv("INSTAGRAM_WEBHOOK_VERIFY_TOKEN")
    instagram_api_version: str = os.getenv("INSTAGRAM_API_VERSION", "v18.0")

    # ========================================================================
    # Backup & Maintenance
    # ========================================================================
    backup_enabled: bool = os.getenv("BACKUP_ENABLED", "true").lower() == "true"
    backup_schedule: str = os.getenv("BACKUP_SCHEDULE", "daily")
    backup_retention_days: int = int(os.getenv("BACKUP_RETENTION_DAYS", 30))
    backup_location: str = os.getenv("BACKUP_LOCATION", "/app/backups")

    # ========================================================================
    # Logging
    # ========================================================================
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = os.getenv("LOG_FILE", "/app/logs/kucibok.log")
    log_max_bytes: int = int(os.getenv("LOG_MAX_BYTES", 10485760))
    log_backup_count: int = int(os.getenv("LOG_BACKUP_COUNT", 5))

    # ========================================================================
    # Security
    # ========================================================================
    api_key: str = os.getenv("API_KEY", "")
    cors_origins_str: str = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000")
    allowed_hosts_str: str = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1")

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins_str.split(",")]

    @property
    def allowed_hosts(self) -> list[str]:
        return [host.strip() for host in self.allowed_hosts_str.split(",")]

    class Config:
        case_sensitive = False
        env_file = ".env"
        extra = 'ignore'  # Ignore extra fields from .env


# Global settings instance
settings = Settings()
