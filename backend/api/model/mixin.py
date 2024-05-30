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
                        if stmt.__dict__.get('_where_criteria', None) is not None:
                            stmt = stmt.options(selectinload(related_attr))
                else:
                    related_attr = getattr(cls, key, None)
                    if related_attr:
                        if len(str(value)) > 0:
                            stmt = stmt.filter(related_attr==value)
                        else:
                            stmt = stmt.order_by(related_attr)

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
        limit = int(kwargs.get('limit')) if str(kwargs.get('limit')).isdigit() else None
        offset = int(kwargs.get('offset')) if str(kwargs.get('offset')).isdigit() else 0
        stream = await session.stream_scalars(
            stmt.order_by(cls.id).limit(limit).offset(offset)
        )
        async for row in stream.unique():
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
        new_item = await cls.read_by_id(session, item_id=item.id)
        return new_item if new_item else RuntimeError()

    @classmethod
    async def update(cls, session: AsyncSession, item, **kwargs):
        if item:
            for key, value in kwargs.items():
                if hasattr(item, key) and value is not None:
                    setattr(item, key, value)
            await session.commit()
        return item

    @classmethod
    async def delete(cls, session: AsyncSession, item) -> None:
        await session.delete(item)
        await session.commit()
