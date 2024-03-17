from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from backend.api.util import _AllOptionalMeta
from backend.api.schema.matchplayer_schema import IndependentMatchPlayerSchema


class PlayerHeroChanceSchema(BaseModel):
    """
    Pydantic schema for PlayerHeroChance table data.

    Attributes:
    - player_id: identifier of the player associated with the record.
    - hero_id: identifier of the hero associated with the entry.
    - win_percentage: win percentage of the player with the hero.
    """
    player_id: int
    hero_id: int
    win_percentage: float

    model_config = ConfigDict(from_attributes=True)


class PartialPlayerHeroChanceSchema(PlayerHeroChanceSchema, metaclass=_AllOptionalMeta):
    """
    Pydantic schema for PlayerHeroChance table data (PATCH). 
    """


class IndependentPlayerHeroChanceSchema(PlayerHeroChanceSchema):
    """
    Pydantic schema for PlayerHeroChance table data (subqueries).

    Attributes:
    - id: unique identifier of the record for the probability of a player winning with a hero.
    - player_id: identifier of the player associated with the record.
    - hero_id: identifier of the hero associated with the entry.
    - win_percentage: win percentage of the player with the hero.
    - modified_at: date the record's data was last modified.
    """
    id: int
    modified_at: datetime


class PlayerHeroChanceResponse(IndependentPlayerHeroChanceSchema):
    """
    Pydantic schema for PlayerHeroChance table data.

    Attributes:
    - id: unique identifier of the record for the probability of a player winning with a hero.
    - player_id: identifier of the player associated with the record.
    - hero_id: identifier of the hero associated with the entry.
    - win_percentage: win percentage of the player with the hero.
    - modified_at: date the record's data was last modified.
    - match_players: player's match records.
    """
    match_players: Optional[List[IndependentMatchPlayerSchema]] = None
