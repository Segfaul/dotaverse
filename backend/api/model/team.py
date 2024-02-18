from typing import AsyncIterator

from sqlalchemy import String, DateTime, func, select
from sqlalchemy.orm import DeclarativeBase as Base, Mapped, relationship, mapped_column, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .base import Base
from .mixin import CRUDMixin
from .player import Player


class Team(Base, CRUDMixin):
    '''
    Dota2 pro-team

    Attributes
    ----------
    name : str
        name of the team
    dotabuff_link : str
        link to the team's profile on dotabuff
    modified_at : datetime
        date the team's data was last modified
    '''
    __tablename__ = "team"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    name: Mapped[str] = mapped_column("name", String(length=32), nullable=False, unique=True)
    dotabuff_link: Mapped[str] = mapped_column("dotabuff_link", String(length=128), nullable=False)
    modified_at: Mapped[DateTime] = mapped_column(
        "modified_at", DateTime("Europe/Moscow"), nullable=False, 
        server_default=func.now, onupdate=func.now
    )

    players: Mapped[list[Player]] = relationship('Player', back_populates='team')

    @classmethod
    async def read_all(cls, session: AsyncSession, **kwargs) -> AsyncIterator:
        stmt = select(cls)
        include_players = kwargs.get('include_players', None)
        if include_players:
            stmt = stmt.options(selectinload(cls.players))
        stream = await session.stream_scalars(stmt.order_by(cls.id))
        async for row in stream:
            yield row
        
    @classmethod
    async def read_by_id(cls, session: AsyncSession, item_id: int, **kwargs):
        stmt = select(cls).where(cls.id == item_id)
        include_players = kwargs.get('include_players', None)
        if include_players:
            stmt = stmt.options(selectinload(cls.players))
        return await session.scalar(stmt.order_by(cls.id))
