import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

import client from '../config/client';
import { Match } from '../config/types';
import Table, { Column } from '../util/Table';
import SearchBar from '../util/SearchBar';


const Matches: React.FC = () => {
  const { t } = useTranslation();

  const [matches, setMatches] = useState<Match[]>([]);
  const [searchTerm, setSearchTerm] = useState<string>('');

  useEffect(() => {
    fetchMatches();
  }, []);

  useEffect(() => {
    document.title = t('header.main-menu.4.name') + " - Dotaverse";
  }, [t]);

  const fetchMatches = async () => {
    try {
      const response = await client.get('/api/v1/match/');
      setMatches(response.data);
    } catch (error) {
      console.error('Error fetching matches:', error);
    }
  };

  const filteredMatches = matches.filter(match =>
    match.match_teams?.some(
      matchTeam =>
      matchTeam.team.name.toLowerCase().includes(searchTerm.toLowerCase())
    )
  );

  const columns: Column<Match>[] = [
    { header: t('columns.match.id'), accessor: 'id' },
    { header: t('columns.match.name'), accessor: 'id', render: row => (
      <Link className='heroes-list-item-link' to={`/matches/${row.id}`}>
        <div className='heroes-list-item-data hero-match-list-item-data'>
          <span className="heroes-list-item-name">
            {row.match_teams?.map((match_team, match_teamIndex) => (
              <React.Fragment key={match_teamIndex}>
                <span className={`hero-match-list-item-data-matchteam ${match_team.is_winner ? 'winner' : ''}`}>{match_team.team.name}</span>
                {match_teamIndex !== row.match_teams.length - 1 && <span key={`vs_${match_teamIndex}`}> vs </span>}
              </React.Fragment>
            ))}
          </span>
        </div>
      </Link>
    )},
    { header: t('columns.match.date'), accessor: 'created_at', render: row => (
      <div className='hero-match-date'>
        <span>{String(new Date(row.created_at).toLocaleString())}</span>
      </div>
    )}
  ];

  return (
    <div className='heroes teams'>
      <section className='heroes-list teams-list'>
        <h1>{t('match.h1')}</h1>
        <SearchBar searchTerm={searchTerm} setSearchTerm={setSearchTerm} placeholder={t('search.placeholders.team')}/>
        <Table data={filteredMatches} columns={columns} />
      </section>
    </div>
  );
};

export default Matches;
