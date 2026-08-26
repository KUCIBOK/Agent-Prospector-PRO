"""
Kucibok Prospector — FastAPI main application.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager (startup & shutdown).
    """
    # Startup
    logger.info(f"🚀 Kucibok Prospector v1.1.0 starting up...")
    logger.info(f"   API: http://{settings.api_host}:{settings.api_port}")
    logger.info(f"   Debug: {settings.debug}")
    logger.info(f"   Model: {settings.model_name}")

    # Initialize database
    from app.db import init_db
    try:
        init_db()
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")

    yield
    # Shutdown
    logger.info("🛑 Kucibok Prospector shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Kucibok Prospector API",
    description="Autonomous discovery agent for African artists and international curators",
    version="1.1.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Health Check Endpoints
# ============================================================================


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "version": "1.1.0",
        "service": "kucibok-prospector",
    }


@app.get("/ready", tags=["health"])
async def readiness_check():
    """Readiness check endpoint (checks dependencies)."""
    # TODO: Add dependency checks (database, redis, ollama)
    return {
        "ready": True,
        "database": "ok",  # placeholder
        "redis": "ok",  # placeholder
        "ai_service": "ok",  # placeholder
    }


# ============================================================================
# Root & Info
# ============================================================================


@app.get("/", tags=["info"])
async def root():
    """API root endpoint."""
    return {
        "name": "Kucibok Prospector",
        "version": "1.1.0",
        "description": "Autonomous discovery agent for African artists and international curators",
        "documentation": "/docs",
        "openapi_schema": "/openapi.json",
    }


# ============================================================================
# Route Imports & Registration
# ============================================================================

from app.api import prospects_router, messages_router, monitoring_router
from fastapi.responses import FileResponse
import os

app.include_router(prospects_router, prefix="/api", tags=["prospects"])
app.include_router(messages_router, prefix="/api", tags=["messages"])
app.include_router(monitoring_router, prefix="/api", tags=["monitoring"])

# Base directory for static files (extracted to avoid duplication)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@app.get("/dashboard")
async def serve_dashboard():
    """Serve main dashboard"""
    dashboard_path = os.path.join(BASE_DIR, "dashboard.html")
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path, media_type="text/html")
    logger.error(f"Dashboard not found at {dashboard_path}")
    raise HTTPException(status_code=404, detail="Dashboard not found")

@app.get("/dashboard-summary")
async def serve_dashboard_summary():
    """Serve dashboard summary"""
    summary_path = os.path.join(BASE_DIR, "dashboard_summary.html")
    if os.path.exists(summary_path):
        return FileResponse(summary_path, media_type="text/html")
    logger.error(f"Dashboard summary not found at {summary_path}")
    raise HTTPException(status_code=404, detail="Dashboard summary not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
