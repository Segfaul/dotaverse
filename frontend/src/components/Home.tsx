import React, { useEffect, useState } from 'react';
import client from './config/client';

interface Player {
  name: string;
}

interface Team {
  id: string;
  name: string;
}

const Home: React.FC = () => {
  const [teams, setTeams] = useState<Team[]>([]);
  const [teamStats, setTeamStats] = useState<{ [teamId: string]: Player[] }>({});

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

  const fetchTeamStats = async (teamId: string) => {
    try {
      const response = await client.get(`/api/v1/team/${teamId}/stats`);
      console.log(response.data.team_players);
      setTeamStats((prevStats) => ({
        ...prevStats,
        [teamId]: response.data.team_players.slice(0, 5),
      }));
    } catch (error) {
      console.error('Error fetching team stats:', error);
    }
  };

  return (
    <div>
      <TeamRepresentation
        teams={teams}
        fetchTeamStats={fetchTeamStats}
        teamStats={teamStats}
      />
      <TeamRepresentation
        teams={teams}
        fetchTeamStats={fetchTeamStats}
        teamStats={teamStats}
      />
    </div>
  );
};

interface TeamRepresentationProps {
  teams: Team[];
  fetchTeamStats: (teamId: string) => Promise<void>;
  teamStats: { [teamId: string]: Player[] };
}

const TeamRepresentation: React.FC<TeamRepresentationProps> = ({
  teams,
  fetchTeamStats,
  teamStats,
}) => {
  const [selectedTeam, setSelectedTeam] = useState<string>('');

  const handleTeamChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedTeamId = event.target.value;
    setSelectedTeam(selectedTeamId);
    if (!teamStats[selectedTeamId]) {
      fetchTeamStats(selectedTeamId);
    }
  };

  return (
    <div>
      <h1>Team Representation</h1>
      <select value={selectedTeam} onChange={handleTeamChange}>
        <option value="">Select a Team</option>
        {teams.map((team) => (
          <option key={team.id} value={team.id}>
            {team.name}
          </option>
        ))}
      </select>
      <h2>Team Stats</h2>
      <ul>
      {teamStats[selectedTeam]?.map((player, index) => (
        <li key={index}>
          {player.player.name}
          <select>
            <option value="">Select a PHC</option>
            {player.player.player_hero_chances.map((phc) => (
              <option key={phc.id} value={phc.name}>
                {phc.hero.opendota_name}
              </option>
            ))}
          </select>
        </li>
      ))}
      </ul>
    </div>
  );
};

export default Home;
