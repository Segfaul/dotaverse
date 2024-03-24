from typing import List, Optional

from backend.api.schema.hero_schema import IndependentHeroSchema
from backend.api.schema.team_schema import IndependentTeamSchema
from backend.api.schema.player_schema import IndependentPlayerSchema, PlayerResponse
from backend.api.schema.playerherochance_schema import IndependentPlayerHeroChanceSchema
from backend.api.schema.match_schema import IndependentMatchSchema
from backend.api.schema.matchteam_schema import IndependentMatchTeamSchema
from backend.api.schema.matchplayer_schema import IndependentMatchPlayerSchema


class PlayerHeroChanceStatsSchema(IndependentPlayerHeroChanceSchema):
    """
    Pydantic schema for PlayerHeroChance table data (big queries).

    Attributes:
    - id: unique identifier of the record for the probability of a player winning with a hero.
    - player_id: identifier of the player associated with the record.
    - hero_id: identifier of the hero associated with the entry.
    - win_percentage: win percentage of the player with the hero.
    - modified_at: date the record's data was last modified.
    - hero: hero description associated with chance.
    - player: player description associated with chance.
    """
    hero: Optional[IndependentHeroSchema] = None
    player: Optional[IndependentPlayerSchema] = None


class MatchStatsSchema(IndependentMatchSchema):
    """
    Pydantic schema for Match table data (big queries).

    Attributes:
    -----------
    - id: unique identifier of the match.
    - created_at: date the match was created.
    - match_teams: teams description associated with match.
    """
    match_teams: Optional[List[IndependentMatchTeamSchema]] = None


class MatchPlayerStatsSchema(IndependentMatchPlayerSchema):
    """
    Pydantic schema for MatchPlayer table data (big queries).

    Attributes:
    - id: unique identifier of the player's match record.
    - player_id: identifier of the player associated with the record.
    - hero_id: identifier of the hero associated with the record.
    - playerherochance_id: identifier of the winning chance associatedwith the player_hero.
    - match_id: identifier of the match associated with the entry.
    - matchteam_id: identifier of the match_team associated with the entry.
    - match: match description associated with match_player.
    - hero: hero description associated with match_player.
    - player: player description associated with match_player.
    - playerherochance: hero win probability description.
    """
    match: Optional[MatchStatsSchema] = None
    hero: Optional[IndependentHeroSchema] = None
    player: Optional[IndependentPlayerSchema] = None
    playerherochance: Optional[PlayerHeroChanceStatsSchema] = None


class TeamPlayerStatsSchema(PlayerResponse):
    """
    Pydantic schema for Player table data (big queries).

    Attributes:
    - id: unique identifier of the player.
    - name: name of the player.
    - opendota_link: link to the player's Dotabuff profile.
    - team_id: id of the team the player belongs to.
    - created_at: date the player's profile was created.
    - match_players: player's match records.
    - player_hero_chances: records for the probability of a player winning with a hero.
    """
    player_hero_chances: Optional[List[PlayerHeroChanceStatsSchema]] = None


class PlayerStatsSchema(TeamPlayerStatsSchema):
    """
    Pydantic schema for Player table data (big queries).

    Attributes:
    - id: unique identifier of the player.
    - name: name of the player.
    - opendota_link: link to the player's Dotabuff profile.
    - team_id: id of the team the player belongs to.
    - created_at: date the player's profile was created.
    - match_players: player's match records.
    - player_hero_chances: records for the probability of a player winning with a hero.
    - team: team description associated with the entry.
    """
    team: Optional[IndependentTeamSchema] = None
    match_players: Optional[List[MatchPlayerStatsSchema]] = None


class TeamStatsSchema(IndependentTeamSchema):
    """
    Pydantic schema for Team table data (big queries).

    Attributes:
    - id : unique identifier of the team.
    - name : name of the team.
    - opendota_link : link to the team's profile on opendota.
    - modified_at : date the team's data was last modified.
    - players: players description associated with the team.
    - match_teams: match_team perfomances associated with the entry.
    """
    players: Optional[List[TeamPlayerStatsSchema]] = None
    match_teams: Optional[List[IndependentMatchTeamSchema]] = None
