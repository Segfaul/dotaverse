import React, { useEffect, useState } from 'react';
import { Link, useParams, Navigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

import client from '../config/client';
import { Match as MatchSchema, MatchPlayer } from '../config/types';
import PageLoading from '../error/PageLoading';
import Table, { Column } from '../util/Table';


const Match: React.FC = () => {
  const { t } = useTranslation();
  const { id } = useParams<{ id: string }>();

  const [match, setMatch] = useState<MatchSchema | null>(null);
  const [error, setError] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchMatch(Number(id));
  }, [id]);

  const fetchMatch = async (match_id: number) => {
    try {
      const response = await client.get(`/api/v1/match/${match_id}/stats`);
      setMatch(response.data);
      setError(false);
    } catch (error) {
      console.error('Error fetching match:', error);
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <PageLoading />
  }

  if (error) {
    return <Navigate to='unmatched' />;
  }


  const playerColumns: Column<MatchPlayer>[] = [
    { header: t('columns.player.id'), accessor: 'player_id' },
    { header: t('columns.player.name'), accessor: 'player_id', render: row => (
      <Link className='heroes-list-item-link' to={`/players/${row.player_id}`}>
        <div className='heroes-list-item-data match-list-item-data'>
          <span className="heroes-list-item-name">{row.player.name}</span>
        </div>
      </Link>
    )},
    { header: t('columns.hero.name'), accessor: 'hero_id', render: row => (
      <Link className='heroes-list-item-link' to={`/heroes/${row.hero_id}`}>
        <div className='heroes-list-item-data'>
          <img 
              src={`https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/${row.hero?.opendota_name}.png`} 
              alt={row.hero?.opendota_name}
              className="heroes-list-item-pic"
            />
            <span className="heroes-list-item-name">{row.hero?.opendota_name}</span>
        </div>
      </Link>
    )},
    { header: t('columns.player_hero_chance.win_percentage'), accessor: 'playerherochance_id', render: row => {
      let barColor = '';
      if (row.player_hero_chance.win_percentage >= 70) {
        barColor = 'rgb(76 181 81)';
      } else if (row.player_hero_chance.win_percentage >= 40) {
        barColor = 'rgb(228 218 82)';
      } else {
        barColor = 'rgb(203 46 46)';
      }
    
      return (
        <div className='hero-win-percentage-container'>
          <div className='hero-win-percentage'>
            <span>{row.player_hero_chance.win_percentage}%</span>
            <div className='progress-bar'>
              <div className='progress-bar-fill' style={{ width: `${row.player_hero_chance.win_percentage}%`, backgroundColor: barColor }}/>
            </div>
          </div>
        </div>
      );
    }},
    { header: t('columns.player_hero_chance.date'), accessor: 'playerherochance_id', render: row => (
      <div className='hero-match-date'>
        <span>{String(new Date(row.player_hero_chance.modified_at).toLocaleString())}</span>
      </div>
    )}
  ]

  return (
    <div className='hero'>
      <section className="hero-stats">
        <div className='hero-stats-intro'>
        <div className="hero-background-overlay match-background-overlay"/>
          <h1>{t('match.h1')} #{match?.id}</h1>
        </div>
        <div className="hero-stats-players">
          {match?.match_teams.map((match_team, match_teamIndex) => (
            <div className='match-stats-team' key={match_teamIndex}>
              <Link className='match-stat-team-link' to={`/teams/${match_team.team_id}`}>
                <span className={`match-stats-team-name ${match_team.is_winner ? 'winner' : ''}`}>{match_team.team.name}</span>
              </Link>
              <Table className='match-stats-player-table' data={match_team.match_players || []} columns={playerColumns} />
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default Match;
