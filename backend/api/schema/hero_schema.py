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
    - dotabuff_name: name of the hero on Dotabuff.
    - gif_link: link to the hero's animation.
    """
    dotabuff_name: str
    gif_link: str

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
    - dotabuff_name: name of the hero on Dotabuff.
    - gif_link: link to the hero's animation.
    """
    id: int


class HeroResponse(IndependentHeroSchema):
    """
    Pydantic schema for Hero table data.

    Attributes:
    -----------
    - id: unique identifier of the hero.
    - dotabuff_name: name of the hero on Dotabuff.
    - gif_link: link to the hero's animation.
    - match_players: hero's match records.
    - player_hero_chances: records for the probability of a hero winning.
    """
    match_players: Optional[List[IndependentMatchPlayerSchema]] = None
    player_hero_chances: Optional[List[IndependentPlayerHeroChanceSchema]] = None
