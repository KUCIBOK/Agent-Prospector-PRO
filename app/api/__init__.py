"""
API routers — all API endpoints.
"""

from app.api.messages import router as messages_router
from app.api.monitoring import router as monitoring_router
from app.api.prospects import router as prospects_router

__all__ = [
    "messages_router",
    "monitoring_router",
    "prospects_router",
]
