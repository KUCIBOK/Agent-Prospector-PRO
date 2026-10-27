"""
API-key authentication for all /api routes.

Clients send the key in the `X-API-Key` header. The key is set with the
`API_KEY` environment variable. Without a configured key the API refuses
requests, unless DEBUG=true (local development only).
"""

import hmac

from fastapi import Header, HTTPException, status

from app.config import settings


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if not settings.api_key:
        if settings.debug:
            return
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="API_KEY is not configured on the server",
        )
    if not x_api_key or not hmac.compare_digest(x_api_key, settings.api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
