"""
Tests for async database initialization.
"""

import pytest
from sqlalchemy import inspect

from yatharth_os.db.base import Base
from yatharth_os.db.init_db import init_db
from yatharth_os.db.session import engine


@pytest.mark.asyncio
async def test_database_tables_created() -> None:
    """
    Ensure database tables are initialized correctly.
    """

    await init_db()

    async with engine.begin() as connection:
        tables = await connection.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )

    expected_tables = {
        "users",
        "contact_requests",
    }

    assert expected_tables.issubset(set(tables))

    metadata_tables = set(Base.metadata.tables.keys())

    assert expected_tables.issubset(metadata_tables)
