from pydantic import BaseModel, ConfigDict

from backend.api.util import _AllOptionalMeta


class MatchPlayerSchema(BaseModel):
    """
    Pydantic schema for MatchPlayer table data.

    Attributes:
    - player_id: identifier of the player associated with the record.
    - hero_id: identifier of the hero associated with the record.
    - playerherochance_id: identifier of the winning chance associatedwith the player_hero.
    - matchteam_id: identifier of the match_team associated with the entry.
    - match_id: identifier of the match associated with the entry.
    """
    player_id: int
    hero_id: int
    playerherochance_id: int
    matchteam_id: int
    match_id: int

    model_config = ConfigDict(from_attributes=True)


class PartialMatchPlayerSchema(MatchPlayerSchema, metaclass=_AllOptionalMeta):
    """
    Pydantic schema for MatchPlayer table data (PATCH). 
    """


class IndependentMatchPlayerSchema(MatchPlayerSchema):
    """
    Pydantic schema for MatchPlayer table data (subqueries).

    Attributes:
    - id: unique identifier of the player's match record.
    - player_id: identifier of the player associated with the record.
    - hero_id: identifier of the hero associated with the record.
    - playerherochance_id: identifier of the winning chance associatedwith the player_hero.
    - matchteam_id: identifier of the match_team associated with the entry.
    - match_id: identifier of the match associated with the entry.
    """
    id: int


class MatchPlayerResponse(IndependentMatchPlayerSchema):
    """
    Pydantic schema for MatchPlayer table data.

    Attributes:
    - id: unique identifier of the player's match record.
    - player_id: identifier of the player associated with the record.
    - hero_id: identifier of the hero associated with the record.
    - playerherochance_id: identifier of the winning chance associatedwith the player_hero.
    - matchteam_id: identifier of the match_team associated with the entry.
    - match_id: identifier of the match associated with the entry.
    """
