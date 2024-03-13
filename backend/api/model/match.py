from typing import TYPE_CHECKING

from sqlalchemy import Float, DateTime, func, select
from sqlalchemy.orm import DeclarativeBase as Base, Mapped, mapped_column, relationship, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.model.base import Base
from backend.api.model.mixin import CRUDMixin

if TYPE_CHECKING:
    from backend.api.model.matchplayer import MatchPlayer
else:
    MatchPlayer = "MatchPlayer"

class Match(Base, CRUDMixin):
    '''
    Dota2 Match

    Attributes
    ----------
    win_percentage : float
        percentage of wins in the match
    created_at : datetime
        date the match was created
    '''
    __tablename__ = "match"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    win_percentage: Mapped[Float] = mapped_column(
        "win_percentage", Float(precision=3), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(
        "created_at", DateTime("Europe/Moscow"), 
        default=func.now()
    )

    match_players: Mapped[list[MatchPlayer]] = relationship('MatchPlayer', back_populates='match')

    @classmethod
    async def read_by_id(cls, session: AsyncSession, item_id: int, **kwargs):
        stmt = select(cls).where(cls.id == item_id)
        include_players = kwargs.get('include_players', None)
        if include_players:
            stmt = stmt.options(selectinload(cls.match_players))
        return await session.scalar(stmt.order_by(cls.id))
