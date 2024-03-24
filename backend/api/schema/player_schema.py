from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from backend.api.util import _AllOptionalMeta
from backend.api.schema.teamplayer_schema import IndependentTeamPlayerSchema
from backend.api.schema.matchplayer_schema import IndependentMatchPlayerSchema
from backend.api.schema.playerherochance_schema import IndependentPlayerHeroChanceSchema


class PlayerSchema(BaseModel):
    """
    Pydantic schema for Player table data.

    Attributes:
    - name: name of the player.
    - steamid: steam account id of the player.
    - opendota_link: link to the player's OpenDota profile.
    """
    name: str
    steamid: int
    opendota_link: str

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
    - steamid: steam account id of the player.
    - opendota_link: link to the player's OpenDota profile.
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
    - steamid: steam account id of the player.
    - opendota_link: link to the player's OpenDota profile.
    - created_at: date the player's profile was created.
    - team_players: rosters related to the player.
    - match_players: player's match records.
    - player_hero_chances: records for the probability of a player winning with a hero.
    """
    team_players: Optional[List[IndependentTeamPlayerSchema]] = None
    match_players: Optional[List[IndependentMatchPlayerSchema]] = None
    player_hero_chances: Optional[List[IndependentPlayerHeroChanceSchema]] = None
