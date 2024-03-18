from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from backend.api.util import _AllOptionalMeta
from backend.api.schema.matchplayer_schema import IndependentMatchPlayerSchema
from backend.api.schema.playerherochance_schema import IndependentPlayerHeroChanceSchema


class PlayerSchema(BaseModel):
    """
    Pydantic schema for Player table data.

    Attributes:
    - name: name of the player.
    - dotabuff_link: link to the player's Dotabuff profile.
    - team_id: id of the team the player belongs to.
    """
    name: str
    dotabuff_link: str
    is_active: str
    team_id: int

    model_config = ConfigDict(from_attributes=True)


class PartialPlayerSchema(PlayerSchema, metaclass=_AllOptionalMeta):
    """
    Pydantic schema for Player table data (PATCH). 
    """


class IndependentPlayerSchema(PlayerSchema):
    """
    Pydantic schema for Player table data (subqueries). 

    Attributes:
    - id: unique identifier of the player.
    - name: name of the player.
    - dotabuff_link: link to the player's Dotabuff profile.
    - team_id: id of the team the player belongs to.
    - created_at: date the player's profile was created.
    """
    id: int
    created_at: datetime


class PlayerResponse(IndependentPlayerSchema):
    """
    Pydantic schema for Player table data.

    Attributes:
    - id: unique identifier of the player.
    - name: name of the player.
    - dotabuff_link: link to the player's Dotabuff profile.
    - team_id: id of the team the player belongs to.
    - created_at: date the player's profile was created.
    - match_players: player's match records.
    - player_hero_chances: records for the probability of a player winning with a hero.
    """
    match_players: Optional[List[IndependentMatchPlayerSchema]] = None
    player_hero_chances: Optional[List[IndependentPlayerHeroChanceSchema]] = None
