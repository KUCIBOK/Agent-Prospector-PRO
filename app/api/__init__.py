"""
API routers — all API endpoints.
"""

from app.api.prospects import router as prospects_router
from app.api.messages import router as messages_router
from app.api.monitoring import router as monitoring_router

__all__ = [
    "prospects_router",
    "messages_router",
    "monitoring_router",
]
