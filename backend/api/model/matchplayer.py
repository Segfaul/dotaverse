from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from backend.api.model.base import Base
from backend.api.model.mixin import CRUDMixin
from backend.api.model.player import Player
from backend.api.model.hero import Hero
from backend.api.model.playerherochance import PlayerHeroChance
from backend.api.model.matchteam import MatchTeam
from backend.api.model.match import Match


class MatchPlayer(Base, CRUDMixin):
    '''
    Dota2 MatchPlayer

    Attributes
    ----------
    player_id : int
        id of the player associated with the record
    hero_id : int
        id of the hero associated with the record
    playerherochance_id : int
        id of the winning chance associatedwith the player_hero
    matchteam_id : int
        id of the match team associated with the entry
    match_id : int
        id of the match associated with the entry
    '''
    __tablename__ = "match_player"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    player_id: Mapped[int] = mapped_column("player_id", ForeignKey('player.id'), nullable=False)
    hero_id: Mapped[int] = mapped_column("hero_id", ForeignKey('hero.id'), nullable=False)
    playerherochance_id: Mapped[int] = mapped_column(
        "playerherochance_id", ForeignKey('player_hero_chance.id'), nullable=False
    )
    matchteam_id: Mapped[int] = mapped_column(
        "matchteam_id", ForeignKey('match_team.id'), nullable=False
    )
    match_id: Mapped[int] = mapped_column("match_id", ForeignKey('match.id'), nullable=False)

    player: Mapped[Player] = relationship('Player', back_populates='match_players')
    hero: Mapped[Hero] = relationship('Hero', back_populates='match_players')
    player_hero_chance: Mapped[PlayerHeroChance] = relationship(
        'PlayerHeroChance', back_populates="match_players"
    )
    match_team: Mapped[MatchTeam] = relationship('MatchTeam', back_populates='match_players')
    match: Mapped[Match] = relationship('Match', back_populates='match_players')
