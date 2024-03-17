from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from backend.api.util import _AllOptionalMeta
from backend.api.schema.player_schema import IndependentPlayerSchema
from backend.api.schema.matchteam_schema import IndependentMatchTeamSchema


class TeamSchema(BaseModel):
    """
    Pydantic schema for Team table data.

    Attributes:
    - name : name of the team.
    - dotabuff_link : link to the team's profile on dotabuff.
    """
    name: str
    dotabuff_link: str

    model_config = ConfigDict(from_attributes=True)


class PartialTeamSchema(TeamSchema, metaclass=_AllOptionalMeta):
    """
    Pydantic schema for Team table data (PATCH). 
    """


class IndependentTeamSchema(TeamSchema):
    """
    Pydantic schema for Team table data (subqueries).

    Attributes:
    - id : unique identifier of the team.
    - name : name of the team.
    - dotabuff_link : link to the team's profile on dotabuff.
    - modified_at : date the team's data was last modified.
    """
    id: int
    modified_at: datetime


class TeamResponse(IndependentTeamSchema):
    """
    Pydantic schema for Team table data.

    Attributes:
    - id : unique identifier of the team.
    - name : name of the team.
    - dotabuff_link : link to the team's profile on dotabuff.
    - modified_at : date the team's data was last modified.
    - players : team roster.
    - match_teams: list of teams in the match.
    """
    players: Optional[List[IndependentPlayerSchema]] = None
    match_teams: Optional[List[IndependentMatchTeamSchema]] = None
