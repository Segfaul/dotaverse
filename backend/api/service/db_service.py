import os
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from dotenv import load_dotenv

env = os.environ.get
load_dotenv('./.env')

TEST = (env('TEST').lower()=="true")
DEBUG = (env('DEBUG').lower()=="true")
POSTGRE_CON = f"postgresql+asyncpg://{env('POSTGRES_USER')}:{env('POSTGRES_PASSWORD')}" \
              f"@{env('POSTGRES_HOST')}:{env('POSTGRES_PORT')}/{env('POSTGRES_DB')}"

async_engine = create_async_engine(
    f'sqlite+aiosqlite:///{"test" if TEST else "dotaverse"}.db' if DEBUG else POSTGRE_CON,
    pool_pre_ping=True,
    echo=False,
)
AsyncSessionFactory = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    expire_on_commit=False,
    future=True,
)

async def get_session() -> AsyncIterator[async_sessionmaker]:
    async with AsyncSessionFactory() as session:
        yield session
