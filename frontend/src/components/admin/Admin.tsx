import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import client from '../config/client';
import { isAuthenticated } from '../context/AuthContext';

interface AuthResponse {
  access_token: string;
  token_type: string;
}

const Admin: React.FC = () => {
  const { t } = useTranslation();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    const isAuth = isAuthenticated();
    if (isAuth) {
      window.location.href = '/'; 
    }
  }, []);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    try {
      const response = await client.post<AuthResponse>(
        '/api/v1/user/token', 
        {
          username: username,
          password: password,
        },
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      );

      const { access_token, token_type } = response.data;

      localStorage.setItem('access_token', access_token);
      localStorage.setItem('token_type', token_type);

      window.location.href = '/'; 

    } catch (err) {
      console.log(err);
      setError(t('auth.login.status_404'));
    }
  };

  return (
    <div className='heroes'>
      <section className="heroes-list admin-auth">
        <h2>{t('auth.login.name')}</h2>
        <form onSubmit={handleSubmit} className='admin-auth-form'>
          <div className='admin-auth-form-el'>
            <input
              type="text"
              value={username}
              placeholder={t('auth.placeholders.username')}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div className='admin-auth-form-el'>
            <input
              type="password"
              value={password}
              placeholder={t('auth.placeholders.password')}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button className='admin-auth-form-submit' type="submit">{t('auth.login.name')}</button>
        </form>
        <div className='admin-auth-form-error teamselector-message'>
         {error && <span className='teamselector-error'>{error}</span> }
        </div>
      </section>
    </div>
  );
};

export default Admin;
