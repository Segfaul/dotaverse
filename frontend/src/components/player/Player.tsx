import React, { useEffect, useState } from 'react';
import { Link, useParams, Navigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

import client from '../config/client';
import { Player as PlayerSchema, MatchPlayer, PlayerHeroChance, TeamPlayer } from '../config/types';
import PageLoading from '../error/PageLoading';
import Table, { Column } from '../util/Table';
import SearchBar from '../util/SearchBar';
import NavTab, { NavTab as NavTabSchema } from '../util/NavTab';


const Player: React.FC = () => {
  const { t } = useTranslation();
  const { id } = useParams<{ id: string }>();

  const [player, setPlayer] = useState<PlayerSchema | null>(null);
  const [error, setError] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchTeamTerm, setSearchTeamTerm] = useState<string>('');
  const [searchHeroTerm, setSearchHeroTerm] = useState<string>('');
  const [searchMatchTerm, setSearchMatchTerm] = useState<string>('');
  const uniqueMatches = new Set<number>();

  useEffect(() => {
    fetchPlayer(Number(id));
  }, [id]);

  const fetchPlayer = async (player_id: number) => {
    try {
      const response = await client.get(`/api/v1/player/${player_id}/stats`);
      setPlayer(response.data);
      setError(false);
    } catch (error) {
      console.error('Error fetching player:', error);
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

  const filteredTeams = player?.team_players?.filter(
    team_player =>
      team_player.team.name.toLowerCase().includes(searchTeamTerm.toLowerCase())
  );

  const filteredHeroChances = player?.player_hero_chances?.filter(
    phc =>
      phc.hero?.opendota_name.toLowerCase().includes(searchHeroTerm.toLowerCase())
  );

  const filteredMatches = player?.match_players
    ?.filter(matchPlayer =>
      matchPlayer.match.match_teams?.some(
        matchTeam =>
        matchTeam.team.name.toLowerCase().includes(searchMatchTerm.toLowerCase())
      )
    )
    .filter(matchPlayer => {
      if (!matchPlayer) return false;
      if (uniqueMatches.has(matchPlayer.match.id)) return false;
      uniqueMatches.add(matchPlayer.match.id);
      return true;
    }) as MatchPlayer[];
  

  const teamColumns: Column<TeamPlayer>[] = [
    { header: t('columns.team.id'), accessor: 'id' },
    { header: t('columns.team.name'), accessor: 'team_id', render: row => (
      <Link className='heroes-list-item-link' to={`/teams/${row.team_id}`}>
        <div className='heroes-list-item-data team-list-item-data'>
          <span className="heroes-list-item-name">{row.team.name}</span>
        </div>
      </Link>
    )},
    { header: t('columns.team.date'), accessor: 'created_at', render: row => (
      <div className='hero-match-date'>
        <span>{String(new Date(row.team.modified_at).toLocaleString())}</span>
      </div>
    )}
  ]

  const heroColumns: Column<PlayerHeroChance>[] = [
    { header: t('columns.hero.id'), accessor: 'hero_id'},
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
            <span>{row.win_percentage}%</span>
            <div className='progress-bar'>
              <div className='progress-bar-fill' style={{ width: `${row.win_percentage}%`, backgroundColor: barColor }}/>
            </div>
          </div>
        </div>
      );
    }},
    { header: t('columns.player_hero_chance.date'), accessor: 'modified_at', render: row => (
        <div className='hero-match-date'>
          <span>{String(new Date(row.modified_at).toLocaleString())}</span>
        </div>
    )}
  ];

  const matchColumns: Column<MatchPlayer>[] = [
    { header: t('columns.match.id'), accessor: 'match_id' },
    { header: t('columns.match.name'), accessor: 'match_id', render: row => (
      <Link className='heroes-list-item-link' to={`/matches/${row.match_id}`}>
        <div className='heroes-list-item-data hero-match-list-item-data'>
          <span className="heroes-list-item-name">
            {row.match.match_teams?.map((match_team, match_teamIndex) => (
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

  const teamContent: JSX.Element = (
    <div className="hero-stats-players">
      <h2>{t('team.h1')}</h2>
      <SearchBar searchTerm={searchTeamTerm} setSearchTerm={setSearchTeamTerm} placeholder={t('search.placeholders.team')} />
      <Table data={filteredTeams || []} columns={teamColumns} />
    </div>
  );

  const heroContent: JSX.Element = (
    <div className="hero-stats-players player-stats-heroes">
      <h2>{t('hero.h1')}</h2>
      <SearchBar searchTerm={searchHeroTerm} setSearchTerm={setSearchHeroTerm} placeholder={t('search.placeholders.hero')} />
      <Table className='player-stats-heroes-table' data={filteredHeroChances || []} columns={heroColumns} />
    </div>
  );

  const matchesContent: JSX.Element = (
    <div className="hero-stats-matches player-stats-matches">
      <h2>{t('match.h1')}</h2>
      <SearchBar searchTerm={searchMatchTerm} setSearchTerm={setSearchMatchTerm} placeholder={t('search.placeholders.team')} />
      <Table className='player-stats-matches-table' data={filteredMatches || []} columns={matchColumns} />
    </div>
  );

  const tabs: NavTabSchema[] = [
    { value: 'teams', label: t('team.h1'), content: teamContent},
    { value: 'heroes', label: t('hero.h1'), content: heroContent },
    { value: 'matches', label: t('match.h1'), content: matchesContent },
  ];

  return (
    <div className='hero'>
      <section className="hero-stats">
        <div className='hero-stats-intro'>
        <div className="hero-background-overlay player-background-overlay"/>
          <h1>{player?.name}</h1>
        </div>
        <NavTab defaultTab={tabs[1].value} tabs={tabs} />
      </section>
    </div>
  );
};

export default Player;
