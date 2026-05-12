"""
Centralized API exception handlers.

This module keeps API error responses consistent and request-ID aware.
"""

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Return structured validation errors with request ID context."""

    request_id = getattr(request.state, "request_id", None)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "validation_error",
            "message": "Request validation failed.",
            "request_id": request_id,
            "details": exc.errors(),
        },
    )
