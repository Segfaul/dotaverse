from datetime import datetime

from pydantic import BaseModel, ConfigDict

from backend.api.util import _AllOptionalMeta


class TeamPlayerSchema(BaseModel):
    """
    Pydantic schema for TeamPlayer table data.

    Attributes:
    - player_id: id of the player belongs to.
    - is_active: check if roster lock is active.
    - team_id: id of the team the player belongs to.
    """
    player_id: int
    is_active: bool
    team_id: int

    model_config = ConfigDict(from_attributes=True)


class PartialTeamPlayerSchema(TeamPlayerSchema, metaclass=_AllOptionalMeta):
    """
    Pydantic schema for TeamPlayer table data (PATCH). 
    """


class IndependentTeamPlayerSchema(TeamPlayerSchema):
    """
    Pydantic schema for TeamPlayer table data (subqueries). 

    Attributes:
    - id: unique identifier of the player.
    - player_id: id of the player belongs to.
    - is_active: check if roster lock is active.
    - team_id: id of the team the player belongs to.
    - created_at: date the player's profile was created.
    """
    id: int
    created_at: datetime


class TeamPlayerResponse(IndependentTeamPlayerSchema):
    """
    Pydantic schema for Player table data.

    Attributes:
    - id: unique identifier of the player.
    - player_id: id of the player belongs to.
    - is_active: check if roster lock is active.
    - team_id: id of the team the player belongs to.
    - created_at: date the player's profile was created.
    """
