from typing import List, Optional

from backend.api.schema.hero_schema import IndependentHeroSchema
from backend.api.schema.team_schema import IndependentTeamSchema
from backend.api.schema.player_schema import IndependentPlayerSchema
from backend.api.schema.playerherochance_schema import IndependentPlayerHeroChanceSchema
from backend.api.schema.match_schema import IndependentMatchSchema
from backend.api.schema.matchteam_schema import IndependentMatchTeamSchema
from backend.api.schema.matchplayer_schema import IndependentMatchPlayerSchema
from backend.api.schema.teamplayer_schema import IndependentTeamPlayerSchema


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


class IndependentMatchTeamStatsSchema(IndependentMatchTeamSchema):
    """
    Pydantic schema for MatchTeam table data (subqueries).

    Attributes:
    - id : unique identifier of the matchteam.
    - match_id: identifier of the match associated with the entry.
    - team_id: id of the team the matchteam belongs to.
    - is_winner : boolean value whether the team is the winner.
    """
    match: Optional[IndependentMatchSchema] = None
    team: Optional[IndependentTeamSchema] = None


class IndependentMatchStatsSchema(IndependentMatchSchema):
    """
    Pydantic schema for Match table data (big queries).

    Attributes:
    -----------
    - id: unique identifier of the match.
    - created_at: date the match was created.
    - match_teams: teams description associated with match.
    """
    match_teams: Optional[List[IndependentMatchTeamStatsSchema]] = None


class TeamMatchTeamStatsSchema(IndependentMatchTeamSchema):
    """
    Pydantic schema for MatchTeam table data (subqueries).

    Attributes:
    - id : unique identifier of the matchteam.
    - match_id: identifier of the match associated with the entry.
    - team_id: id of the team the matchteam belongs to.
    - is_winner : boolean value whether the team is the winner.
    """
    match: Optional[IndependentMatchStatsSchema] = None


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
    match: Optional[IndependentMatchStatsSchema] = None
    hero: Optional[IndependentHeroSchema] = None
    player: Optional[IndependentPlayerSchema] = None
    playerherochance: Optional[PlayerHeroChanceStatsSchema] = None


class MatchTeamStats(IndependentMatchTeamSchema):
    """
    Pydantic schema for MatchTeam table data (subqueries).

    Attributes:
    - id : unique identifier of the matchteam.
    - match_id: identifier of the match associated with the entry.
    - team_id: id of the team the matchteam belongs to.
    - is_winner: boolean value whether the team is the winner.
    - team: team associated with the entry.
    """
    team: Optional[IndependentTeamSchema] = None
    match_players: Optional[List[MatchPlayerStatsSchema]] = None


class MatchStatsSchema(IndependentMatchSchema):
    """
    Pydantic schema for Match table data (big queries).

    Attributes:
    -----------
    - id: unique identifier of the match.
    - created_at: date the match was created.
    - match_teams: teams description associated with match.
    """
    match_teams: Optional[List[MatchTeamStats]] = None


class IndependentPlayerStatsSchema(IndependentPlayerSchema):
    """
    Pydantic schema for Player table data (big queries).

    Attributes:
    - id: unique identifier of the player.
    - name: name of the player.
    - opendota_link: link to the player's Dotabuff profile.
    - team_id: id of the team the player belongs to.
    - created_at: date the player's profile was created.
    - player_hero_chances: records for the probability of a player winning with a hero.
    """
    player_hero_chances: Optional[List[PlayerHeroChanceStatsSchema]] = None


class PlayerStatsSchema(IndependentPlayerStatsSchema):
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
    - team_players: team players associated with the entry.
    """
    match_players: Optional[List[MatchPlayerStatsSchema]] = None
    team_players: Optional[List[IndependentTeamPlayerSchema]] = None


class TeamPlayerStatsSchema(IndependentTeamPlayerSchema):
    """
    Pydantic schema for Player table data.

    Attributes:
    - id: unique identifier of the player.
    - player_id: id of the player belongs to.
    - is_active: check if roster lock is active.
    - team_id: id of the team the player belongs to.
    - created_at: date the player's profile was created.
    - team: team associated with the player.
    - player: player steam profile associated with the teamplayer.
    """
    team: Optional[IndependentTeamSchema] = None
    player: Optional[IndependentPlayerStatsSchema] = None


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
    team_players: Optional[List[TeamPlayerStatsSchema]] = None
    match_teams: Optional[List[TeamMatchTeamStatsSchema]] = None
