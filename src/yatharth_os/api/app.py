"""
FastAPI application entrypoint for Yatharth OS.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from yatharth_os.api.auth_routes import router as auth_router
from yatharth_os.api.contact_routes import router as contact_router
from yatharth_os.api.exception_handlers import validation_exception_handler
from yatharth_os.api.routes import router as portfolio_router
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

app.add_middleware(RequestLoggingMiddleware)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(portfolio_router)
app.include_router(auth_router)
app.include_router(contact_router)
