from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase as Base, Mapped, relationship, mapped_column

from backend.api.model.base import Base
from backend.api.model.mixin import CRUDMixin

if TYPE_CHECKING:
    from backend.api.model.team import Team
else:
    Team = "Team"


class Player(Base, CRUDMixin):
    '''
    Dota2 pro-player

    Attributes
    ----------
    name : str
        name of the player
    dotabuff_link : str
        link to the player's Dotabuff profile
    team_id : int
        id of the team the player belongs to
    created_at : datetime
        date the player's profile was created
    '''
    __tablename__ = "player"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    name: Mapped[str] = mapped_column("name", String(length=32), nullable=False)
    dotabuff_link: Mapped[str] = mapped_column("dotabuff_link", String(length=128), nullable=False)
    team_id: Mapped[int] = mapped_column("team_id", ForeignKey('team.id'), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        "created_at", DateTime("Europe/Moscow"), 
        default=func.now
    )

    team: Mapped[Team] = relationship('Team', back_populates='players')
