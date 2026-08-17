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
# Module Imports (placeholder for future routes)
# ============================================================================

# TODO: Import & include routers as they're implemented
# from app.api.prospects import router as prospects_router
# from app.api.messages import router as messages_router
# from app.api.monitoring import router as monitoring_router
# from app.api.admin import router as admin_router

# app.include_router(prospects_router, prefix="/api/prospects", tags=["prospects"])
# app.include_router(messages_router, prefix="/api/messages", tags=["messages"])
# app.include_router(monitoring_router, prefix="/api/monitoring", tags=["monitoring"])
# app.include_router(admin_router, prefix="/api/admin", tags=["admin"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
