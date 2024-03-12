from sqlalchemy import Float, DateTime, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase as Base, Mapped, relationship, mapped_column

from backend.api.model.base import Base
from backend.api.model.mixin import CRUDMixin
from backend.api.model.player import Player
from backend.api.model.hero import Hero


class PlayerHeroChance(Base, CRUDMixin):
    '''
    Dota2 pro-player on_hero_chance

    Attributes
    ----------
    player_id: int
        id of the player associated with the record
    hero_id: int
        id of the hero associated with the entry
    win_percentage: float
        win percentage of the player with the hero
    modified_at : datetime
        date the record's data was last modified
    '''
    __tablename__ = "player_hero_chance"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    player_id: Mapped[int] = mapped_column("player_id", ForeignKey('player.id'), nullable=False)
    hero_id: Mapped[int] = mapped_column("hero_id", ForeignKey('hero.id'), nullable=False)
    win_percentage: Mapped[Float] = mapped_column(
        "win_percentage", Float(precision=3), nullable=False
    )
    modified_at: Mapped[DateTime] = mapped_column(
        "modified_at", DateTime("Europe/Moscow"), nullable=False, 
        default=func.now, onupdate=func.now
    )

    player: Mapped[Player] = relationship('Player', back_populates='player_hero_chances')
    hero: Mapped[Hero] = relationship('Hero', back_populates='player_hero_chances')
