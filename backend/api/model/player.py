from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, relationship, mapped_column, validates

from backend.api.validator import validate_link
from backend.api.model.base import Base
from backend.api.model.mixin import CRUDMixin

if TYPE_CHECKING:
    from backend.api.model.teamplayer import TeamPlayer
    from backend.api.model.matchplayer import MatchPlayer
    from backend.api.model.playerherochance import PlayerHeroChance
else:
    TeamPlayer = "TeamPlayer"
    MatchPlayer = "MatchPlayer"
    PlayerHeroChance = "PlayerHeroChance"


class Player(Base, CRUDMixin):
    '''
    Dota2 player

    Attributes
    ----------
    name : str
        name of the player
    opendota_link : str
        link to the player's OpenDota profile
    steamid: int
        link to the player's steam profile
    created_at : datetime
        date the player's profile was created
    '''
    __tablename__ = "player"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    name: Mapped[str] = mapped_column("name", String(length=32), nullable=False)
    steamid: Mapped[int] = mapped_column("steamid", Integer(), nullable=False, unique=True)
    opendota_link: Mapped[str] = mapped_column(
        "opendota_link", String(length=128), nullable=False, unique=True
    )
    created_at: Mapped[DateTime] = mapped_column(
        "created_at", DateTime("Europe/Moscow"), 
        default=func.now()
    )

    team_players: Mapped[List[TeamPlayer]] = relationship(
        'TeamPlayer', cascade='all, delete-orphan', back_populates='player'
    )
    match_players: Mapped[List[MatchPlayer]] = relationship(
        'MatchPlayer', cascade='all, delete-orphan', back_populates='player'
    )
    player_hero_chances: Mapped[List[PlayerHeroChance]] = relationship(
        'PlayerHeroChance', cascade='all, delete-orphan', back_populates='player'
    )

    @validates('opendota_link')
    def validate_opendota_link(self, key, value):
        '''Validate link to https://www.opendota.com/ format'''
        if not validate_link(value, 'https://www.opendota.com/'):
            return ValueError("Provided incorrect opendota_link (https://www.opendota.com/)")
        return value
