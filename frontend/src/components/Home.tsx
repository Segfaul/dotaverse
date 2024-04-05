import React, { useEffect, useState } from 'react';
import client from './config/client';
import {PlayerHeroChance, Team, TeamPlayer} from './config/types'


const Home: React.FC = () => {
  const [teams, setTeams] = useState<Team[]>([]);
  const [teamStats, setTeamStats] = useState<{ [teamId: number]: TeamPlayer[] }>({});

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
      const response = await client.post(`/api/v1/match/calculate`, teamStats);
      console.log(response.data);
    } else {
      console.log('Please select heroes and team stats.');
      console.log('Team Stats:', teamStats);
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
    <div>
      {Array.from({ length: 2 }, (_, index) => (
        <TeamRepresentation
          key={index}
          teams={teams}
          fetchTeamStats={fetchTeamStats}
          teamStats={teamStats}
          handleHeroChange={handleHeroChange}
        />
      ))}
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
};

interface TeamRepresentationProps {
  teams: Team[];
  fetchTeamStats: (teamId: number, previous_id: number | null) => Promise<void>;
  teamStats: { [teamId: number]: TeamPlayer[] };
  handleHeroChange: (event: React.ChangeEvent<HTMLSelectElement>, playerId: number, selectedTeam: number) => void;
}

const TeamRepresentation: React.FC<TeamRepresentationProps> = ({
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

  return (
    <div>
      <h1>Team Representation</h1>
      <select value={selectedTeam} onChange={handleTeamChange}>
        <option value="">Select a Team</option>
        {teams
          .filter(team => !Object.keys(teamStats).map(Number).includes(team.id) || selectedTeam === team.id)
          .map((team) => (
            <option key={team.id} value={team.id}>
              {team.name}
            </option>
          ))
        }
      </select>
      <h2>Team Stats</h2>
      <ul>
      {teamStats[selectedTeam]?.map((player, index) => (
        <li key={index}>
          {player.player.name}
          <select value={(player.chosen_phc?.hero_id) || 0} onChange={(e) => handleHeroChange(e, player.player.id, selectedTeam)}>
            <option value={0}>Select a PHC</option>
            {player.player.player_hero_chances
                .filter(phc => !Object.values(teamStats[selectedTeam]).map((p) => p.chosen_phc?.hero_id)
                .includes(phc.hero.id) || (player.chosen_phc && player.chosen_phc.hero_id === phc.hero.id))
                .map((phc) => (
                    <option key={phc.id} value={phc.hero.id} phc-instance={JSON.stringify(phc)}>
                        {phc.hero.opendota_name}
                    </option>
                ))
            }
        </select>
        </li>
      ))}
      </ul>
    </div>
  );
};

export default Home;
