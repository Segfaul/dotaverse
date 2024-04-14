export interface Hero {
    id: number;
    opendota_name: string;
}

export interface PlayerHeroChance {
    id: number;
    player_id: number;
    hero_id: number;
    win_percentage: number;
    modified_date: Date;
    hero: Hero;
}

export interface Player {
    id: number;
    name: string;
    player_hero_chances: PlayerHeroChance[];
}
  
export interface TeamPlayer {
    id: number;
    player: Player;
    team: Team;
    chosen_phc: PlayerHeroChance | null;
}

export interface Team {
    id: number;
    name: string;
    opendota_link: string;
    modified_date: Date;
    team_players: TeamPlayer[];
}

export interface MatchTeam {
    id: number;
    match_id: number;
    team_id: number;
    is_winner: boolean;
    team: Team;
}
