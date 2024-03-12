import os
from typing import Annotated, AsyncIterator

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from dotenv import load_dotenv

from backend.config import log, logger

env = os.environ.get
load_dotenv('./.env')

DEBUG = (env('DEBUG').lower()=="true")
POSTGRE_CON = f"postgres://{env('POSTGRES_USER')}:{env('POSTGRES_PASSWORD')}" \
              f"@{env('POSTGRES_HOST')}:{env('POSTGRES_PORT')}/{env('POSTGRES_DB')}"

async_engine = create_async_engine(
    'sqlite+aiosqlite:///test.db' if DEBUG else POSTGRE_CON,
    pool_pre_ping=True,
    echo=False,
)
AsyncSessionFactory = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    future=True,
)

@log(logger)
async def get_session() -> AsyncIterator[async_sessionmaker]:
    try:
        yield AsyncSessionFactory
    except SQLAlchemyError as e:
        logger.exception(e)


# AsyncSession = Annotated[async_sessionmaker, Depends(get_session)]
