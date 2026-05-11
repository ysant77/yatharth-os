"""
Async database session configuration.

This module configures:
- async SQLAlchemy engine
- async session factory
- FastAPI-compatible session dependency
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

DATABASE_URL = "sqlite+aiosqlite:///./yatharth_os.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Yield an async SQLAlchemy database session.

    This function is intended to be used as a FastAPI dependency.
    """

    async with AsyncSessionLocal() as session:
        yield session
