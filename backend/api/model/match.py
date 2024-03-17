from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.api.model.base import Base
from backend.api.model.mixin import CRUDMixin

if TYPE_CHECKING:
    from backend.api.model.matchteam import MatchTeam
else:
    MatchTeam = "MatchTeam"

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
    created_at: Mapped[DateTime] = mapped_column(
        "created_at", DateTime("Europe/Moscow"), 
        default=func.now()
    )

    match_teams: Mapped[List[MatchTeam]] = relationship('MatchTeam', back_populates='match')
