from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from backend.api.util import _AllOptionalMeta
from backend.api.schema.matchplayer_schema import IndependentMatchPlayerSchema


class MatchTeamSchema(BaseModel):
    """
    Pydantic schema for MatchTeam table data.

    Attributes:
    - match_id: identifier of the match associated with the entry.
    - team_id: id of the team the matchteam belongs to.
    - is_winner : boolean value whether the team is the winner.
    """
    match_id: int
    team_id: int
    is_winner: bool

    model_config = ConfigDict(from_attributes=True)


class PartialMatchTeamSchema(MatchTeamSchema, metaclass=_AllOptionalMeta):
    """
    Pydantic schema for MatchTeam table data (PATCH). 
    """


class IndependentMatchTeamSchema(MatchTeamSchema):
    """
    Pydantic schema for MatchTeam table data (subqueries).

    Attributes:
    - id : unique identifier of the matchteam.
    - match_id: identifier of the match associated with the entry.
    - team_id: id of the team the matchteam belongs to.
    - is_winner : boolean value whether the team is the winner.
    """
    id: int


class MatchTeamResponse(IndependentMatchTeamSchema):
    """
    Pydantic schema for MatchTeam table data.

    Attributes:
    - id : unique identifier of the matchteam.
    - match_id: identifier of the match associated with the entry.
    - team_id: id of the team the matchteam belongs to.
    - is_winner : boolean value whether the team is the winner.
    - match_players : matchteam roster.
    """
    match_players: Optional[List[IndependentMatchPlayerSchema]] = None
