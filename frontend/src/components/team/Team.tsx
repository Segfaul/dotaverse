import React, { useEffect, useState } from 'react';
import { Link, useParams, Navigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

import client from '../config/client';
import { Team as TeamSchema, MatchTeam, TeamPlayer } from '../config/types';
import PageLoading from '../error/PageLoading';
import Table, { Column } from '../util/Table';
import SearchBar from '../util/SearchBar';
import NavTab, { NavTab as NavTabSchema } from '../util/NavTab';
import { capitalize } from '../util/TextTransform';
import TeamBG from '../../assets/bg_teams.webp';


const Team: React.FC = () => {
  const { t } = useTranslation();
  const { id } = useParams<{ id: string }>();

  const [team, setTeam] = useState<TeamSchema | null>(null);
  const [error, setError] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchPlayerTerm, setSearchPlayerTerm] = useState<string>('');
  const [searchMatchTerm, setSearchMatchTerm] = useState<string>('');
  const uniqueMatches = new Set<number>();

  useEffect(() => {
    fetchTeam(Number(id));
  }, [id]);

  useEffect(() => {
    document.title = `${capitalize(team?.name)} - ${t('header.main-menu.2.name')} - Dotaverse`;
  }, [team, t]);

  const fetchTeam = async (team_id: number) => {
    try {
      const response = await client.get(`/api/v1/team/${team_id}/stats`);
      setTeam(response.data);
      setError(false);
    } catch (error) {
      console.error('Error fetching team:', error);
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

  const filteredPlayers = team?.team_players?.filter(
    team_player =>
      team_player.player?.name.toLowerCase().includes(searchPlayerTerm.toLowerCase())
  );

  const filteredMatches = team?.match_teams
    ?.filter(match_team =>
        match_team.match.match_teams?.some(matchTeam =>
            matchTeam.team.name.toLowerCase().includes(searchMatchTerm.toLowerCase())
        )
    )
    .filter(matchTeam => {
        if (!matchTeam) return false;
        if (uniqueMatches.has(matchTeam.match.id)) return false;
        uniqueMatches.add(matchTeam.match.id);
        return true;
    }) as MatchTeam[];

  const playerColumns: Column<TeamPlayer>[] = [
    { header: t('columns.player.id'), accessor: 'player_id'},
    { header: t('columns.player.name'), accessor: 'player_id', render: row => (
      <Link className='heroes-list-item-link' to={`/players/${row.id}`}>
        <div className='heroes-list-item-data hero-player-list-item-data'>
          <span className="heroes-list-item-name">{row.player?.name}</span>
        </div>
      </Link>
    )},
    { header: t('columns.player.date'), accessor: 'player_id', render: row => (
        <div className='hero-match-date'>
          <span>{String(new Date(row.player.created_at).toLocaleString())}</span>
        </div>
    )}
  ];

  const matchColumns: Column<MatchTeam>[] = [
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

  const playerContent: JSX.Element = (
    <div className="hero-stats-players">
      <h2>{t('player.h1')}</h2>
      <SearchBar searchTerm={searchPlayerTerm} setSearchTerm={setSearchPlayerTerm} placeholder={t('search.placeholders.player')} />
      <Table data={filteredPlayers || []} columns={playerColumns} />
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
        <div
          className="hero-background-overlay team-background-overlay"
          style={{ backgroundImage: `url(${TeamBG})` }}
        />
          <h1>{team?.name}</h1>
        </div>
        <NavTab defaultTab={tabs[0].value} tabs={tabs} />
      </section>
    </div>
  );
};

export default Team;
