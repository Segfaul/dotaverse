export interface Hero {
    id: number;
    opendota_name: string;
    player_hero_chances: PlayerHeroChance[] | null;
}

export interface PlayerHeroChance {
    id: number;
    player_id: number;
    hero_id: number;
    win_percentage: number;
    modified_date: Date;
    hero: Hero | null;
    player: Player | null;
    match_players: MatchPlayer[] | null;
    modified_at: Date;
}

export interface Player {
    id: number;
    name: string;
    player_hero_chances: PlayerHeroChance[] | null;
    match_players: MatchPlayer[] | null;
    team_players: TeamPlayer[] | null;
    created_at: Date;
}
  
export interface TeamPlayer {
    id: number;
    player_id: number;
    team_id: number;
    player: Player;
    team: Team;
    chosen_phc: PlayerHeroChance | null;
    created_at: Date;
}

export interface Team {
    id: number;
    name: string;
    opendota_link: string;
    modified_date: Date;
    team_players: TeamPlayer[];
    match_teams: MatchTeam[] | null;
    modified_at: Date;
}

export interface Match {
    id: number;
    created_at: Date;
    match_teams: MatchTeam[];
}

export interface MatchTeam {
    id: number;
    match_id: number;
    team_id: number;
    is_winner: boolean;
    team: Team;
    match: Match;
    match_players: MatchPlayer[] | null;
}

export interface MatchPlayer {
    id: number;
    player_id: number;
    hero_id: number;
    playerherochance_id: number;
    matchteam_id: number;
    match_id: number;
    match: Match;
    player: Player;
    hero: Hero;
    player_hero_chance: PlayerHeroChance;
}

export interface Log {
    created_at: Date;
    level: string;
    service: string;
    message: string;
}
