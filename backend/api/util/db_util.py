from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.util.endpoint_util import create_object_or_raise_400

async def get_or_create(db_session: AsyncSession, item, **kwargs):
    """
    Response pattern for db models if item already exists
    """
    stmt = select(item).filter_by(**kwargs)
    instance = (await db_session.execute(stmt)).scalar_one_or_none()
    if instance:
        return instance

    return await create_object_or_raise_400(db_session, item, **kwargs)
