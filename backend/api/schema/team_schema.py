from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from backend.api.util import _AllOptionalMeta
from backend.api.schema.teamplayer_schema import IndependentTeamPlayerSchema
from backend.api.schema.matchteam_schema import IndependentMatchTeamSchema


class TeamSchema(BaseModel):
    """
    Pydantic schema for Team table data.

    Attributes:
    - name : name of the team.
    - opendota_link : link to the team's profile on opendota.
    """
    name: str
    opendota_link: str

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
    - opendota_link : link to the team's profile on opendota.
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
    - opendota_link : link to the team's profile on opendota.
    - modified_at : date the team's data was last modified.
    - team_players : team roster.
    - match_teams: list of teams in the match.
    """
    team_players: Optional[List[IndependentTeamPlayerSchema]] = None
    match_teams: Optional[List[IndependentMatchTeamSchema]] = None
