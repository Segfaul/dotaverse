from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, relationship, mapped_column

from backend.api.model.base import Base
from backend.api.model.mixin import CRUDMixin
from backend.api.model.team import Team
from backend.api.model.player import Player


class TeamPlayer(Base, CRUDMixin):
    '''
    Dota2 pro-player

    Attributes
    ----------
    player_id: int
        id of the player associated with team entry
    team_id : int
        id of the team the player belongs to
    created_at : datetime
        date the player's profile was created
    '''
    __tablename__ = "team_player"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    player_id: Mapped[int] = mapped_column("player_id", ForeignKey('player.id'), nullable=False)
    is_active: Mapped[Boolean] = mapped_column("is_active", Boolean(), nullable=False)
    team_id: Mapped[int] = mapped_column("team_id", ForeignKey('team.id'), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        "created_at", DateTime("Europe/Moscow"), 
        default=func.now()
    )

    player: Mapped[Player] = relationship('Player', back_populates='team_players')
    team: Mapped[Team] = relationship('Team', back_populates='team_players')
