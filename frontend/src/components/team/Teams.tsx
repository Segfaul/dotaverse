import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

import client from '../config/client';
import { Team } from '../config/types';
import Table, { Column } from '../util/Table';
import SearchBar from '../util/SearchBar';


const Teams: React.FC = () => {
  const { t } = useTranslation();

  const [teams, setTeams] = useState<Team[]>([]);
  const [searchTerm, setSearchTerm] = useState<string>('');

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

  const filteredTeams = teams.filter(team =>
    team.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const columns: Column<Team>[] = [
    { header: 'ID', accessor: 'id' },
    { header: t('columns.team.name'), accessor: 'name', render: row => (
      <Link className='heroes-list-item-link' to={`/teams/${row.id}`}>
        <div className='heroes-list-item-data team-list-item-data'>
          <span className="heroes-list-item-name">{row.name}</span>
        </div>
      </Link>
    )}
  ];

  return (
    <div className='heroes teams'>
      <section className='heroes-list teams-list'>
        <h1>{t('team.h1')}</h1>
        <SearchBar searchTerm={searchTerm} setSearchTerm={setSearchTerm} placeholder={t('search.placeholders.team')}/>
        <Table data={filteredTeams} columns={columns} />
      </section>
    </div>
  );
};

export default Teams;
