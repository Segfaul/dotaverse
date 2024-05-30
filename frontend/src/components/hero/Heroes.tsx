import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

import client from '../config/client';
import { Hero } from '../config/types';
import Table, { Column } from '../util/Table';
import SearchBar from '../util/SearchBar';


const Heroes: React.FC = () => {
  const { t } = useTranslation();

  const [heroes, setHeroes] = useState<Hero[]>([]);
  const [searchTerm, setSearchTerm] = useState<string>('');

  useEffect(() => {
    document.title = t('header.main-menu.1.name') + " - Dotaverse";
  }, [t]);

  useEffect(() => {
    fetchHeroes();
  }, []);

  const fetchHeroes = async () => {
    try {
      const response = await client.get('/api/v1/hero/');
      setHeroes(response.data);
    } catch (error) {
      console.error('Error fetching heroes:', error);
    }
  };

  const filteredHeroes = heroes.filter(hero =>
    hero.opendota_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const columns: Column<Hero>[] = [
    { header: 'ID', accessor: 'id' },
    { header: t('columns.hero.name'), accessor: 'opendota_name', render: row => (
      <Link className='heroes-list-item-link' to={`/heroes/${row.id}`}>
        <div className='heroes-list-item-data'>
          <img 
            src={`https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/${row.opendota_name}.png`} 
            alt={row.opendota_name}
            className="heroes-list-item-pic"
          />
          <span className="heroes-list-item-name">{row.opendota_name}</span>
        </div>
      </Link>
    )}
  ];

  return (
    <div className='heroes'>
      <section className='heroes-list'>
        <h1>{t('hero.h1')}</h1>
        <SearchBar searchTerm={searchTerm} setSearchTerm={setSearchTerm} placeholder={t('search.placeholders.hero')}/>
        <Table data={filteredHeroes} columns={columns} />
      </section>
    </div>
  );
};

export default Heroes;
