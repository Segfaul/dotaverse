import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

import client from '../config/client';
import { Log } from '../config/types';
import Table, { Column } from '../util/Table';
import SearchBar from '../util/SearchBar';


const Logs: React.FC = () => {
  const { t } = useTranslation();

  const [logs, setLogs] = useState<Log[]>([]);
  const [searchTerm, setSearchTerm] = useState<string>('');

  useEffect(() => {
    fetchLogs();
  }, []);

  useEffect(() => {
    document.title = t('header.main-menu.5.name') + " - Dotaverse";
  }, [t]);

  const fetchLogs = async () => {
    try {
      const response = await client.get('/api/v1/log/', {headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}});
      setLogs(response.data);
    } catch (error) {
      console.error('Error fetching logs:', error);
    }
  };

  const filteredLogs = logs.filter(log =>
    log.level.toLowerCase().includes(searchTerm.toLowerCase()) ||
    log.service.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const columns: Column<Log>[] = [
    { header: t('columns.log.level'), accessor: 'level' },
    { header: t('columns.log.service'), accessor: 'service' },
    { header: t('columns.log.message'), accessor: 'message', render: row => (
        <div className='heroes-list-item-data hero-match-list-item-data'>
          <span className="heroes-list-item-name">
            {row.message.length > 40 ? row.message.substring(0, 40) + '...' : row.message}
          </span>
        </div>
    )},
    { header: t('columns.log.date'), accessor: 'created_at', render: row => (
      <div className='hero-match-date'>
        <span>{String(new Date(row.created_at).toLocaleString())}</span>
      </div>
    )}
  ];

  return (
    <div className='heroes teams'>
      <section className='heroes-list teams-list'>
        <h1>{t('dashboard.log.h1')}</h1>
        <SearchBar searchTerm={searchTerm} setSearchTerm={setSearchTerm} placeholder={t('search.placeholders.log')}/>
        <Table className='logs-table' data={filteredLogs} columns={columns} />
      </section>
    </div>
  );
};

export default Logs;
