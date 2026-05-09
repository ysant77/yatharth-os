"""
Database initialization utilities.
"""

from sqlalchemy.ext.asyncio import AsyncEngine

from yatharth_os.db.base import Base
from yatharth_os.db.session import engine


async def init_db(db_engine: AsyncEngine = engine) -> None:
    """
    Initialize database tables.

    Creates all SQLAlchemy ORM tables defined in metadata.
    """

    async with db_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
