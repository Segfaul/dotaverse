from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, relationship, mapped_column, validates

from backend.api.validator import validate_link
from backend.api.model.base import Base
from backend.api.model.mixin import CRUDMixin
from backend.api.model.team import Team

if TYPE_CHECKING:
    from backend.api.model.matchplayer import MatchPlayer
    from backend.api.model.playerherochance import PlayerHeroChance
else:
    MatchPlayer = "MatchPlayer"
    PlayerHeroChance = "PlayerHeroChance"


class Player(Base, CRUDMixin):
    '''
    Dota2 pro-player

    Attributes
    ----------
    name : str
        name of the player
    opendota_link : str
        link to the player's OpenDota profile
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
    opendota_link: Mapped[str] = mapped_column("opendota_link", String(length=128), nullable=False)
    is_active: Mapped[Boolean] = mapped_column("is_active", Boolean(), nullable=False)
    team_id: Mapped[int] = mapped_column("team_id", ForeignKey('team.id'), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        "created_at", DateTime("Europe/Moscow"), 
        default=func.now()
    )

    team: Mapped[Team] = relationship('Team', back_populates='players')
    match_players: Mapped[List[MatchPlayer]] = relationship('MatchPlayer', back_populates='player')
    player_hero_chances: Mapped[List[PlayerHeroChance]] = relationship(
        'PlayerHeroChance', back_populates='player'
    )

    @validates('opendota_link')
    def validate_opendota_link(self, key, value):
        '''Validate link to https://www.opendota.com/ format'''
        if not validate_link(value, 'https://www.opendota.com/'):
            return ValueError("Provided incorrect opendota_link (https://www.opendota.com/)")
        return value
