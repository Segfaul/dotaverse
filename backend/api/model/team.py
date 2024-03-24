from typing import TYPE_CHECKING, List

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, relationship, mapped_column, validates

from backend.api.validator import validate_link
from backend.api.model.base import Base
from backend.api.model.mixin import CRUDMixin

if TYPE_CHECKING:
    from backend.api.model.player import Player
    from backend.api.model.matchteam import MatchTeam
else:
    Player = "Player"
    MatchTeam = "MatchTeam"


class Team(Base, CRUDMixin):
    '''
    Dota2 pro-team

    Attributes
    ----------
    name : str
        name of the team
    opendota_link : str
        link to the team's profile on opendota
    modified_at : datetime
        date the team's data was last modified
    '''
    __tablename__ = "team"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    name: Mapped[str] = mapped_column("name", String(length=32), nullable=False, unique=True)
    opendota_link: Mapped[str] = mapped_column("opendota_link", String(length=128), nullable=False)
    modified_at: Mapped[DateTime] = mapped_column(
        "modified_at", DateTime("Europe/Moscow"), nullable=False, 
        default=func.now(), onupdate=func.now()
    )

    players: Mapped[List[Player]] = relationship('Player', back_populates='team')
    match_teams: Mapped[List[MatchTeam]] = relationship('MatchTeam', back_populates='team')

    @validates('opendota_link')
    def validate_opendota_link(self, key, value):
        '''Validate link to https://www.opendota.com/ format'''
        if not validate_link(value, 'https://www.opendota.com/'):
            return ValueError("Provided incorrect opendota_link (https://www.opendota.com/)")
        return value
