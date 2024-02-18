from typing import AsyncIterator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDMixin:
    '''
    CRUD mixin class

    Methods
    ----------
    create(session: AsyncSession, **kwargs):
        returns a new object in Table
    read_all(session: AsyncSession, **kwargs):
        returns all the objects in Table
    read_by_id(session: AsyncSession, item_id: int, **kwargs):
        returns an object by its id
    update(session: AsyncSession, **kwargs):
        updates an object by its instance
    delete(session: AsyncSession, item):
        deletes an object by its instance
    '''

    @classmethod
    async def read_all(cls, session: AsyncSession, **kwargs) -> AsyncIterator:
        stmt = select(cls)
        if kwargs:
            stmt = stmt.filter_by(**kwargs)
        stream = await session.stream_scalars(stmt.order_by(cls.id))
        async for row in stream:
            yield row

    @classmethod
    async def read_by_id(cls, session: AsyncSession, item_id: int, **kwargs):
        stmt = select(cls).where(cls.id == item_id)
        # Fiction added for the implementation of selectinload
        if kwargs:
            stmt = stmt.filter_by(**kwargs)
        return await session.scalar(stmt.order_by(cls.id))

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs):
        item = cls(**kwargs)
        session.add(item)
        await session.flush()
        new_item = await cls.read_by_id(session, item.id)
        return new_item if new_item else RuntimeError()

    async def update(self, session: AsyncSession, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
        await session.flush()

    @classmethod
    async def delete(cls, session: AsyncSession, item) -> None:
        await session.delete(item)
        await session.flush()
