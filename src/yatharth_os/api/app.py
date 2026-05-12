"""
FastAPI application entrypoint for Yatharth OS.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from yatharth_os.api.auth_routes import router as auth_router
from yatharth_os.api.contact_routes import router as contact_router
from yatharth_os.api.exception_handlers import (
    rate_limit_exception_handler,
    validation_exception_handler,
)
from yatharth_os.api.routes import router as portfolio_router
from yatharth_os.core.limiter import limiter
from yatharth_os.core.logging import configure_logging
from yatharth_os.db.init_db import init_db
from yatharth_os.middleware.request_logging import RequestLoggingMiddleware

configure_logging()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Initialize application resources during startup."""

    await init_db()
    yield


app = FastAPI(
    title="Yatharth OS API",
    version="0.1.0",
    lifespan=lifespan,
)

app.state.limiter = limiter

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(SlowAPIMiddleware)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)

app.include_router(portfolio_router)
app.include_router(auth_router)
app.include_router(contact_router)
