from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from backend.api.util import _AllOptionalMeta
from backend.api.schema.matchteam_schema import IndependentMatchTeamSchema


class MatchSchema(BaseModel):
    """
    Pydantic schema for Match table data.
    """

    model_config = ConfigDict(from_attributes=True)


class PartialMatchSchema(MatchSchema, metaclass=_AllOptionalMeta):
    """
    Pydantic schema for Match table data (PATCH). 
    """


class IndependentMatchSchema(MatchSchema):
    """
    Pydantic schema for Match table data (subqueries).

    Attributes:
    -----------
    - id: unique identifier of the match.
    - created_at: date the match was created.
    """
    id: int
    created_at: datetime


class MatchResponse(IndependentMatchSchema):
    """
    Pydantic schema for Match table data.

    Attributes:
    -----------
    - id: unique identifier of the match.
    - created_at: date the match was created.
    - match_teams: list of teams in the match.
    """
    match_teams: Optional[List[IndependentMatchTeamSchema]] = None
