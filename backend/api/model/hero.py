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
    dotabuff_name : str
        name of the hero on Dotabuff
    gif_link : str
        link to the hero's animation
    '''
    __tablename__ = "hero"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    dotabuff_name: Mapped[str] = mapped_column("dotabuff_name", String(length=64), nullable=False)
    gif_link: Mapped[str] = mapped_column("gif_link", String(length=128), nullable=False)

    match_players: Mapped[List[MatchPlayer]] = relationship('MatchPlayer', back_populates='hero')
    player_hero_chances: Mapped[List[PlayerHeroChance]] = relationship(
        'PlayerHeroChance', back_populates='hero'
    )

    @validates('gif_link')
    def validate_dotabuff_link(self, key, value):
        if not validate_link(value):
            return ValueError("Provided incorrect gif_link (https://)")
        return value
