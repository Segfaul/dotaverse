import React, { useEffect, useState } from 'react';
import { Link, useParams, Navigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

import client from '../config/client';
import { Hero as HeroSchema, MatchPlayer, PlayerHeroChance } from '../config/types';
import PageLoading from '../error/PageLoading';
import Table, { Column } from '../util/Table';
import SearchBar from '../util/SearchBar';
import NavTab, { NavTab as NavTabSchema } from '../util/NavTab';
import { capitalize, truncateText } from '../util/TextTransform';


const Hero: React.FC = () => {
  const { t } = useTranslation();
  const { id } = useParams<{ id: string }>();

  const [hero, setHero] = useState<HeroSchema | null>(null);
  const [error, setError] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchPlayerTerm, setSearchPlayerTerm] = useState<string>('');
  const [searchMatchTerm, setSearchMatchTerm] = useState<string>('');
  const uniqueMatches = new Set<number>();

  useEffect(() => {
    fetchHero(Number(id));
  }, [id]);

  useEffect(() => {
    document.title = `${capitalize(hero?.opendota_name)} - ${t('header.main-menu.1.name')} - Dotaverse`;
  }, [hero, t]);

  const fetchHero = async (hero_id: number) => {
    try {
      const response = await client.get(`/api/v1/hero/${hero_id}/stats`);
      setHero(response.data);
      setError(false);
    } catch (error) {
      console.error('Error fetching heroes:', error);
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

  const filteredPlayerChances = hero?.player_hero_chances?.filter(
    phc =>
      phc.player?.name.toLowerCase().includes(searchPlayerTerm.toLowerCase())
  );

  const filteredMatches = hero?.player_hero_chances
    ?.flatMap(phc =>
      phc.match_players?.filter(matchPlayer =>
        matchPlayer.match.match_teams?.some(
          matchTeam =>
            matchTeam.team.name.toLowerCase().includes(searchMatchTerm.toLowerCase())
        )
      )
    )
    .filter(matchPlayer => {
      if (!matchPlayer) return false;
      if (uniqueMatches.has(matchPlayer.match.id)) return false;
      uniqueMatches.add(matchPlayer.match.id);
      return true;
    }) as MatchPlayer[];

  const playerColumns: Column<PlayerHeroChance>[] = [
    { header: t('columns.player.id'), accessor: 'player_id'},
    { header: t('columns.player.name'), accessor: 'player_id', render: row => (
      <Link className='heroes-list-item-link' to={`/players/${row.player_id}`}>
        <div className='heroes-list-item-data hero-player-list-item-data'>
          <span className="heroes-list-item-name">{row.player?.name}</span>
        </div>
      </Link>
    )},
    { header: t('columns.player_hero_chance.win_percentage'), accessor: 'win_percentage', render: row => {
      let barColor = '';
      if (row.win_percentage >= 70) {
        barColor = 'rgb(76 181 81)';
      } else if (row.win_percentage >= 40) {
        barColor = 'rgb(228 218 82)';
      } else {
        barColor = 'rgb(203 46 46)';
      }
    
      return (
        <div className='hero-win-percentage-container'>
          <div className='hero-win-percentage'>
            <span>{truncateText(row.win_percentage.toString(), 5, '')}%</span>
            <div className='progress-bar'>
              <div className='progress-bar-fill' style={{ width: `${row.win_percentage}%`, backgroundColor: barColor }}/>
            </div>
          </div>
        </div>
      );
    }}
  ];

  const matchColumns: Column<MatchPlayer>[] = [
    { header: t('columns.match.id'), accessor: 'match_id' },
    { header: t('columns.match.name'), accessor: 'match_id', render: row => (
      <Link className='heroes-list-item-link' to={`/matches/${row.match_id}`}>
        <div className='heroes-list-item-data hero-match-list-item-data'>
          <span className="heroes-list-item-name">
            {row.match.match_teams.map((match_team, match_teamIndex) => (
              <React.Fragment key={match_teamIndex}>
                <span className={`hero-match-list-item-data-matchteam ${match_team.is_winner ? 'winner' : ''}`}>{match_team.team.name}</span>
                {match_teamIndex !== row.match.match_teams.length - 1 && <span key={`vs_${match_teamIndex}`}> vs </span>}
              </React.Fragment>
            ))}
          </span>
        </div>
      </Link>
    )},
    { header: t('columns.match.date'), accessor: 'match_id', render: row => (
      <div className='hero-match-date'>
        <span>{String(new Date(row.match.created_at).toLocaleString())}</span>
      </div>
    )}
  ];

  const playerContent: JSX.Element = (
    <div className="hero-stats-players">
      <h2>{t('player.h1')}</h2>
      <SearchBar searchTerm={searchPlayerTerm} setSearchTerm={setSearchPlayerTerm} placeholder={t('search.placeholders.player')} />
      <Table data={filteredPlayerChances || []} columns={playerColumns} />
    </div>
  );

  const matchesContent: JSX.Element = (
    <div className="hero-stats-matches">
      <h2>{t('match.h1')}</h2>
      <SearchBar searchTerm={searchMatchTerm} setSearchTerm={setSearchMatchTerm} placeholder={t('search.placeholders.team')} />
      <Table data={filteredMatches || []} columns={matchColumns} />
    </div>
  );

  const tabs: NavTabSchema[] = [
    { value: 'players', label: t('player.h1'), content: playerContent },
    { value: 'matches', label: t('match.h1'), content: matchesContent },
  ];

  return (
    <div className='hero'>
      <section className="hero-stats">
        <div className='hero-stats-intro'>
          <div className="hero-background-overlay" style={{ backgroundImage: `url('https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/${hero?.opendota_name}.png')` }} />
          <img
            src={`https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/${hero?.opendota_name}.png`} 
            alt={hero?.opendota_name}
            className="heroes-stats-pic"
          />
          <h1>{hero?.opendota_name}</h1>
        </div>
        <NavTab defaultTab={tabs[0].value} tabs={tabs} />
      </section>
    </div>
  );
};

export default Hero;
