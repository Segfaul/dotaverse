from typing import AsyncIterator, AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from backend.api.main import app
from backend.api.model import Base

async_engine = create_async_engine(
    'sqlite+aiosqlite:///test.db',
    pool_pre_ping=True,
    echo=False,
)

AsyncSessionFactory = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    expire_on_commit=False,
    future=True,
)

async def get_session() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        yield session

@pytest.fixture(
    scope="session",
    params=[
        pytest.param(("asyncio", {"use_uvloop": True}), id="asyncio+uvloop"),
    ],
)
def anyio_backend(request):
    return request.param


@pytest.fixture(scope="function", autouse=True)
def replace_get_session(monkeypatch):
    monkeypatch.setattr('backend.api.service.db_service.get_session', get_session)


@pytest.fixture(scope="session", autouse=True)
async def start_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await async_engine.dispose()


@pytest.fixture(scope="session", autouse=True)
async def client(start_db) -> AsyncClient:
    transport = ASGITransport(
        app=app,
    )
    async with AsyncClient(
        # app=app,
        base_url="http://127.0.0.1:8000/api/v1",
        headers={"Content-Type": "application/json"},
        transport=transport,
    ) as test_client:
        yield test_client
