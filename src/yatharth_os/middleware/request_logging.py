"""
Request ID and structured request logging middleware.

Every incoming HTTP request receives an `X-Request-ID`.

If the caller already provides `X-Request-ID`, the application preserves it.
Otherwise, the application generates a new UUID-based request ID.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from time import perf_counter
from uuid import uuid4

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

REQUEST_ID_HEADER = "X-Request-ID"

logger = structlog.get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Attach request IDs and emit structured request logs."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """Process an HTTP request and log its lifecycle."""

        request_id = request.headers.get(REQUEST_ID_HEADER) or str(uuid4())
        request.state.request_id = request_id

        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)

        start_time = perf_counter()

        logger.info(
            "http_request_started",
            method=request.method,
            path=request.url.path,
            client_host=request.client.host if request.client else None,
        )

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = round((perf_counter() - start_time) * 1000, 2)

            logger.exception(
                "http_request_failed",
                method=request.method,
                path=request.url.path,
                duration_ms=duration_ms,
            )

            raise

        duration_ms = round((perf_counter() - start_time) * 1000, 2)
        response.headers[REQUEST_ID_HEADER] = request_id

        logger.info(
            "http_request_completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
        )

        structlog.contextvars.clear_contextvars()

        return response
