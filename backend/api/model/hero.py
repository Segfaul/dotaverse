from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase as Base, Mapped, relationship, mapped_column

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

    match_players: Mapped[MatchPlayer] = relationship('MatchPlayer', back_populates='hero')
    player_hero_chances: Mapped[PlayerHeroChance] = relationship('PlayerHeroChance', back_populates='hero')
