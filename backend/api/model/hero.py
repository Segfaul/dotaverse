from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column, validates

from backend.api.validator import validate_link
from backend.api.model.base import Base
from backend.api.model.mixin import CRUDMixin

if TYPE_CHECKING:
    from backend.api.model.matchplayer import MatchPlayer
    from backend.api.model.playerherochance import PlayerHeroChance
else:
    MatchPlayer = "MatchPlayer"
    PlayerHeroChance = "PlayerHeroChance"


class Hero(Base, CRUDMixin):
    '''
    Dota2 hero

    Attributes
    ----------
    opendota_name : str
        name of the hero on OpenDota
    '''
    __tablename__ = "hero"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    opendota_name: Mapped[str] = mapped_column(
        "opendota_name", String(length=64), nullable=False, unique=True
    )

    match_players: Mapped[List[MatchPlayer]] = relationship(
        'MatchPlayer', cascade='all, delete-orphan', back_populates='hero'
    )
    player_hero_chances: Mapped[List[PlayerHeroChance]] = relationship(
        'PlayerHeroChance', cascade='all, delete-orphan', back_populates='hero'
    )
