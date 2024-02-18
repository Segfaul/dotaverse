from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PlayerSchema(BaseModel):
    """
    Pydantic schema for Player table data.

    Attributes:
    - id: unique identifier of the player.
    - name: name of the player.
    - dotabuff_link: link to the player's Dotabuff profile.
    - team_id: id of the team the player belongs to.
    - created_at: date the player's profile was created.
    """
    id: int
    name: str
    dotabuff_link: str
    team_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TeamSchema(BaseModel):
    """
    Pydantic schema for Team table data.

    Attributes:
    - id : unique identifier of the team.
    - name : name of the team.
    - dotabuff_link : link to the team's profile on dotabuff.
    - modified_date : date the team's data was last modified.
    - players : team roster.
    """
    id: int
    name: str
    dotabuff_link: str
    modified_date: datetime
    players: list[PlayerSchema]

    model_config = ConfigDict(from_attributes=True)


class RequestSchema(BaseModel):
    """
    Pydantic schema for the data in the Request table.

    Attributes:
    - id: unique identifier of the request.
    - dotabuff_link: link associated with the request.
    - status: status of the request.
    - created_date: date the request was created.
    """
    id: int
    dotabuff_link: str
    status: int
    created_date: datetime

    model_config = ConfigDict(from_attributes=True)


class HeroSchema(BaseModel):
    """
    Pydantic schema for Hero table data.

    Attributes:
    -----------
    - id: unique identifier of the hero.
    - dotabuff_name: name of the hero on Dotabuff.
    - gif_link: link to the hero's animation.
    """
    id: int
    dotabuff_name: str
    gif_link: str

    model_config = ConfigDict(from_attributes=True)


class MatchPlayerSchema(BaseModel):
    """
    Pydantic schema for MatchPlayer table data.

    Attributes:
    - id: unique identifier of the player's match record.
    - player_id: identifier of the player associated with the record.
    - hero_id: identifier of the hero associated with the record.
    - win_chance: identifier of the winning chance associatedwith the player_hero.
    - match_id: identifier of the match associated with the entry.
    """
    id: int
    player_id: int
    hero_id: int
    win_chance: int
    match_id: int

    model_config = ConfigDict(from_attributes=True)


class MatchSchema(BaseModel):
    """
    Pydantic schema for Match table data.

    Attributes:
    -----------
    - id: unique identifier of the match.
    - win_percentage: percentage of wins in the match.
    - created_at: date the match was created.
    - match_players: list of players in the match.
    """
    id: int
    win_percentage: float
    created_at: datetime
    match_players: list[MatchPlayerSchema]

    model_config = ConfigDict(from_attributes=True)


class PlayerHeroChanceSchema(BaseModel):
    """
    Pydantic schema for PlayerHeroChance table data.

    Attributes:
    - id: unique identifier of the record for the probability of a player winning with a hero.
    - player_id: identifier of the player associated with the record.
    - hero_id: identifier of the hero associated with the entry.
    - win_percentage: win percentage of the player with the hero.
    - modified_date: date the record's data was last modified.
    """
    id: int
    player_id: int
    hero_id: int
    win_percentage: float
    modified_date: datetime

    model_config = ConfigDict(from_attributes=True)
