from typing import TYPE_CHECKING, List

from sqlalchemy import BigInteger, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from backend.api.model.base import Base
from backend.api.model.mixin import CRUDMixin
from backend.api.model.match import Match
from backend.api.model.team import Team

if TYPE_CHECKING:
    from backend.api.model.matchplayer import MatchPlayer
else:
    MatchPlayer = "MatchPlayer"


class MatchTeam(Base, CRUDMixin):
    '''
    Dota2 pro-player on_hero_chance

    Attributes
    ----------
    match_id : int
        id of the match associated with the entry
    team_id : int
        id of the team the player belongs to
    is_winner: bool
        Boolean value whether the team is the winner
    '''
    __tablename__ = "match_team"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    team_id: Mapped[int] = mapped_column("team_id", ForeignKey('team.id'), nullable=False)
    match_id: Mapped[int] = mapped_column("match_id", ForeignKey('match.id'), nullable=False)
    is_winner: Mapped[Boolean] = mapped_column("is_winner", Boolean(), nullable=False)

    team: Mapped[Team] = relationship('Team', back_populates='match_teams')
    match: Mapped[Match] = relationship('Match', back_populates='match_teams')
    match_players: Mapped[List[MatchPlayer]] = relationship(
        'MatchPlayer', cascade='all, delete-orphan', back_populates='match_team'
    )
