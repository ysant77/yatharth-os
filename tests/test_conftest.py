import pytest_asyncio

from yatharth_os.db.session import engine


@pytest_asyncio.fixture(scope="session", autouse=True)
async def dispose_async_engine():
    yield
    await engine.dispose()
