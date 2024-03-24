from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from backend.api.util import _AllOptionalMeta
from backend.api.schema.matchplayer_schema import IndependentMatchPlayerSchema
from backend.api.schema.playerherochance_schema import IndependentPlayerHeroChanceSchema


class HeroSchema(BaseModel):
    """
    Pydantic schema for Hero table data.

    Attributes:
    -----------
    - opendota_name: name of the hero on Dotabuff.
    """
    opendota_name: str

    model_config = ConfigDict(from_attributes=True)


class PartialHeroSchema(HeroSchema, metaclass=_AllOptionalMeta):
    """
    Pydantic schema for Hero table data (PATCH). 
    """


class IndependentHeroSchema(HeroSchema):
    """
    Pydantic schema for Hero table data (subqueries).

    Attributes:
    -----------
    - id: unique identifier of the hero.
    - opendota_name: name of the hero on Dotabuff.
    """
    id: int


class HeroResponse(IndependentHeroSchema):
    """
    Pydantic schema for Hero table data.

    Attributes:
    -----------
    - id: unique identifier of the hero.
    - opendota_name: name of the hero on Dotabuff.
    - match_players: hero's match records.
    - player_hero_chances: records for the probability of a hero winning.
    """
    match_players: Optional[List[IndependentMatchPlayerSchema]] = None
    player_hero_chances: Optional[List[IndependentPlayerHeroChanceSchema]] = None
