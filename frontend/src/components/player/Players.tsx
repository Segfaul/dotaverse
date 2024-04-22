import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

import client from '../config/client';
import { Player } from '../config/types';
import Table, { Column } from '../util/Table';
import SearchBar from '../util/SearchBar';


const Players: React.FC = () => {
  const { t } = useTranslation();

  const [players, setPlayers] = useState<Player[]>([]);
  const [searchTerm, setSearchTerm] = useState<string>('');

  useEffect(() => {
    fetchPlayers();
  }, []);

  const fetchPlayers = async () => {
    try {
      const response = await client.get('/api/v1/player/');
      setPlayers(response.data);
    } catch (error) {
      console.error('Error fetching players:', error);
    }
  };

  const filteredTeams = players.filter(player =>
    player.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const columns: Column<Player>[] = [
    { header: 'ID', accessor: 'id' },
    { header: t('columns.player.name'), accessor: 'name', render: row => (
      <Link className='heroes-list-item-link' to={`/players/${row.id}`}>
        <div className='heroes-list-item-data team-list-item-data'>
          <span className="heroes-list-item-name">{row.name}</span>
        </div>
      </Link>
    )}
  ];

  return (
    <div className='heroes teams'>
      <section className='heroes-list teams-list'>
        <h1>{t('player.h1')}</h1>
        <SearchBar searchTerm={searchTerm} setSearchTerm={setSearchTerm} placeholder={t('search.placeholders.player')}/>
        <Table data={filteredTeams} columns={columns} />
      </section>
    </div>
  );
};

export default Players;
