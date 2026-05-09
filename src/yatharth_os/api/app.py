"""
FastAPI application entrypoint for Yatharth OS.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from yatharth_os.api.routes import router
from yatharth_os.db.init_db import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Initialize application resources during startup.
    """

    await init_db()
    yield


app = FastAPI(
    title="Yatharth OS API",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router)
