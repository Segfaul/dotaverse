import React, { useEffect, useState } from 'react';
import { FiShield } from "react-icons/fi";

import client from './config/client';
import {PlayerHeroChance, Team, TeamPlayer, MatchTeam} from './config/types'


export const TeamSelection: React.FC = () => {
    const [teams, setTeams] = useState<Team[]>([]);
    const [teamStats, setTeamStats] = useState<{ [teamId: number]: TeamPlayer[] }>({});
    const [winner, setWinner] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
  
    useEffect(() => {
      fetchTeams();
    }, []);
  
    const fetchTeams = async () => {
      try {
        const response = await client.get('/api/v1/team/');
        setTeams(response.data);
      } catch (error) {
        console.error('Error fetching teams:', error);
      }
    };
  
    const fetchTeamStats = async (teamId: number, previous_id: number | null) => {
      try {
        if (previous_id !== null) {
          delete teamStats[previous_id];
        }
        if (isNaN(teamId)) {
          return;
        }
        const response = await client.get(`/api/v1/team/${teamId}/stats`);
        console.log(response.data.team_players);
  
        const updatedTeamPlayers: TeamPlayer[] = response.data.team_players.slice(0, 5).map((player: TeamPlayer) => {
          const modifiedPlayer = { ...player };
          modifiedPlayer.chosen_phc = null;
          return modifiedPlayer;
        });
        setTeamStats((prevStats) => ({
          ...prevStats,
          [teamId]: updatedTeamPlayers,
        }));
      } catch (error) {
        console.error('Error fetching team stats:', error);
      }
    };
  
    const handleSubmit = async () => {
      if (Object.keys(teamStats).length == 2) {
        console.log('Team Stats:', teamStats);
        try {
          const response = await client.post(`/api/v1/match/calculate`, teamStats);
          console.log(response.data);
          const matchTeams = response.data.match_teams;
          const winnerTeam = matchTeams.find((team: MatchTeam) => team.is_winner)?.team.name || 'Unknown';
          setWinner(winnerTeam);
          setError(null);
        } catch (error) {
          console.error('Error calculating match:', error);
          setError('Error calculating match');
          setWinner(null);
        }
      } else {
        console.log('Please select heroes and team stats.');
        console.log('Team Stats:', teamStats);
        setError('Please select heroes and team stats.');
        setWinner(null);
      }
    };
  
    const handleHeroChange = (event: React.ChangeEvent<HTMLSelectElement>, playerId: number, selectedTeam: number) => {
      const selectedIndex = event.target.options.selectedIndex;
      const phcInstance = event.target.options[selectedIndex].getAttribute('phc-instance');
      let chosen_phc: PlayerHeroChance;
      if (phcInstance !== null) {
        chosen_phc = JSON.parse(phcInstance);
      }
      setTeamStats((prevStats) => ({
        ...prevStats,
        [selectedTeam]: prevStats[selectedTeam].map((player) => {
          if (player.player.id === playerId) {
            return {
              ...player,
              chosen_phc: chosen_phc,
            };
          }
          return player;
        }),
      }));
    };
  
    return (
      <div className='teamselector'>
        <div className='teamselector-items'>
          {Array.from({ length: 2 }, (_, index) => (
            <TeamRepresentation
              key={index}
              teams={teams}
              fetchTeamStats={fetchTeamStats}
              teamStats={teamStats}
              handleHeroChange={handleHeroChange}
            />
          ))}
        </div>
        <div className='teamselector-message'>
          {error && <span className='teamselector-error'>{error}</span>}
          {winner && <span className='teamselector-winner'>Winner: {winner}</span>}
        </div>
        <button className='teamselector-submit' onClick={handleSubmit}>GET Winner</button>
      </div>
    );
};
  
interface TeamRepresentationProps {
    teams: Team[];
    fetchTeamStats: (teamId: number, previous_id: number | null) => Promise<void>;
    teamStats: { [teamId: number]: TeamPlayer[] };
    handleHeroChange: (event: React.ChangeEvent<HTMLSelectElement>, playerId: number, selectedTeam: number) => void;
}
  
export const TeamRepresentation: React.FC<TeamRepresentationProps> = ({
    teams,
    fetchTeamStats,
    teamStats,
    handleHeroChange,
  }) => {
    const [selectedTeam, setSelectedTeam] = useState<number>(0);
  
    const handleTeamChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
      const selectedTeamId = parseInt(event.target.value);
      const previousTeamId = selectedTeam;
      setSelectedTeam(selectedTeamId);
      if (!teamStats[selectedTeamId]) {
        fetchTeamStats(selectedTeamId, previousTeamId);
      }
    };

    const emptyPlayerSlots = Array.from({ length: 5 }).map((_, index) => (
        <li key={index}>
            <div className='teamselector-item-stats-skeleton'>
                <FiShield />
            </div>
            <span className='teamselector-item-stats-player'>Player {index+1}</span>
            <select disabled>
                <option value={0}>Select PHC</option>
            </select>
        </li>
    ));
  
    return (
      <div className='teamselector-item'>
        <div className="teamselector-item-representation">
          <h1>Team Representation</h1>
          <select value={selectedTeam} onChange={handleTeamChange}>
            <option value="">Select Team</option>
            {teams
              .filter(team => !Object.keys(teamStats).map(Number).includes(team.id) || selectedTeam === team.id)
              .map((team) => (
                <option key={team.id} value={team.id}>
                  {team.name}
                </option>
              ))
            }
          </select>
        </div>
        <div className="teamselector-item-stats">
          <h2>Team Stats</h2>
          <ul>
          {selectedTeam ? (
            teamStats[selectedTeam]?.map((player, index) => (
              <li key={index}>
                {player.chosen_phc ? (
                  <img 
                    src={`https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/${player.chosen_phc.hero.opendota_name}.png`} 
                    alt={player.chosen_phc.hero.opendota_name} 
                  />
                ) : (
                  <div className='teamselector-item-stats-skeleton'>
                    <FiShield/>
                  </div>
                )}
                <span className='teamselector-item-stats-player'>{player.player.name}</span>
                <select value={(player.chosen_phc?.hero_id) || 0} onChange={(e) => handleHeroChange(e, player.player.id, selectedTeam)}>
                  <option value={0}>Select PHC</option>
                  {player.player.player_hero_chances
                      .filter(phc => !Object.values(teamStats).flatMap(teamPlayers => teamPlayers.map(p => p.chosen_phc?.hero_id))
                      .includes(phc.hero.id) || (player.chosen_phc && player.chosen_phc.hero_id === phc.hero.id))
                      .map((phc) => (
                          <option key={phc.id} value={phc.hero.id} phc-instance={JSON.stringify(phc)}>
                            {phc.hero.opendota_name}
                          </option>
                      ))
                  }
              </select>
              {player.chosen_phc ? (
                  <span className='teamselector-item-stats-percentage'>{player.chosen_phc.win_percentage} %</span>
                ) : (
                  <span className='teamselector-item-stats-percentage'>~ %</span>
              )}
              </li>
            ))
          ) : (
            emptyPlayerSlots
          )}
          </ul>
        </div>
      </div>
    );
};
