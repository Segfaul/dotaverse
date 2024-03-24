from typing import AsyncIterator

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.strategy_options import Load
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
    def apply_includes(cls, stmt, *args, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if key.startswith('include_'):
                    related_attr = getattr(cls, key[8:], None)
                    if related_attr and int(value):
                        stmt = stmt.options(selectinload(related_attr))
                else:
                    related_attr = getattr(cls, key, None)
                    stmt = stmt.filter_by(related_attr==value)
        if args:
            for arg in args:
                if isinstance(arg, Load):
                    stmt = stmt.options(arg)
                related_attr = getattr(cls, arg, None) if isinstance(arg, str) else None
                if related_attr:
                    stmt = stmt.order_by(related_attr)
        return stmt

    @classmethod
    async def read_all(cls, session: AsyncSession, *args, **kwargs) -> AsyncIterator:
        stmt = select(cls)
        stmt = cls.apply_includes(stmt, *args, **kwargs)
        stream = await session.stream_scalars(stmt.order_by(cls.id))
        async for row in stream:
            yield row

    @classmethod
    async def read_by_id(cls, session: AsyncSession, item_id: int, *args, **kwargs):
        stmt = select(cls).where(cls.id == item_id)
        # Fiction added for the implementation of selectinload
        stmt = cls.apply_includes(stmt, *args, **kwargs)
        return await session.scalar(stmt.order_by(cls.id))

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs):
        item = cls(**kwargs)
        session.add(item)
        await session.commit()
        new_item = await cls.read_by_id(session, item.id)
        return new_item if new_item else RuntimeError()

    @classmethod
    async def update(cls, session: AsyncSession, item, **kwargs):
        if item:
            for key, value in kwargs.items():
                if hasattr(item, key) and value:
                    setattr(item, key, value)
            await session.commit()
        return item

    @classmethod
    async def delete(cls, session: AsyncSession, item) -> None:
        await session.delete(item)
        await session.commit()
