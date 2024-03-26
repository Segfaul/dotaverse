import React, {useEffect, useState} from 'react';
import client from './config/client';

const Home: React.FC = () => {
    const [teams, setTeams] = useState<any[]>([]);
    const [selectedTeam1, setSelectedTeam1] = useState<string>('');
    const [selectedTeam2, setSelectedTeam2] = useState<string>('');
    const [team1Data, setTeam1Data] = useState<any>(null);
    const [team2Data, setTeam2Data] = useState<any>(null);

    useEffect(() => {
        const fetchTeams = async () => {
          try {
            const response = await client.get('/api/v1/team/');
            setTeams(response.data);
          } catch (error) {
            console.error('Error fetching teams:', error);
          }
        };
    
        fetchTeams();
      }, []);
    const fetchTeamData = async (teamId: string, setter: React.Dispatch<React.SetStateAction<any>>) => {
        if (teamId) {
            try {
            const response = await client.get(`/api/v1/team/${teamId}/stats`);
            setter(response.data);
            } catch (error) {
            console.error(`Error fetching data for team ${teamId}:`, error);
            setter(null);
            }
            }
    };
    // fetchTeamData(selectedTeam1, setTeam1Data);
    return (
        <main>
            <h1>Teams</h1>
            <div>
                <label htmlFor="team1">Select Team 1:</label>
                <select id="team1" value={selectedTeam1} onChange={(e) => setSelectedTeam1(e.target.value)}>
                <option value="">Select a team</option>
                {teams.map((team) => (
                    <option key={team.id} value={team.name}>
                    {team.name}
                    </option>
                ))}
                </select>
            </div>
            <div>
                <label htmlFor="team2">Select Team 2:</label>
                <select id="team2" value={selectedTeam2} onChange={(e) => setSelectedTeam2(e.target.value)}>
                <option value="">Select a team</option>
                {teams.map((team) => (
                    <option key={team.id} value={team.name}>
                    {team.name}
                    </option>
                ))}
                </select>
            </div>
            <div>
                <p>Selected Team 1: {selectedTeam1}</p>
                <p>Selected Team 2: {selectedTeam2}</p>
            </div>
            <div>
        <h2>Team 1 Data:</h2>
        {team1Data && (
          <ul>
            {Object.entries(team1Data).map(([key, value]) => (
              <li key={key}>
                value
              </li>
            ))}
          </ul>
        )}
      </div>
      <div>
        <h2>Team 2 Data:</h2>
        {team2Data && (
          <ul>
            {Object.entries(team2Data).map(([key, value]) => (
              <li key={key}>
                <h3>value</h3>
              </li>
            ))}
          </ul>
        )}
      </div>
        </main>
    );
};

export default Home;
