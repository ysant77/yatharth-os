"""
FastAPI application entrypoint for Yatharth OS.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from yatharth_os.api.auth_routes import router as auth_router
from yatharth_os.api.routes import router as portfolio_router
from yatharth_os.db.init_db import init_db


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

app.include_router(portfolio_router)
app.include_router(auth_router)
