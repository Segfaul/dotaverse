import React from 'react';
import { useTranslation } from 'react-i18next';

import NotFoundWebp from '../../assets/404_web.webp'


const PageNotFound: React.FC = () => {
  const { t } = useTranslation();

  return (
    <div className='error-page'>
        <img src={NotFoundWebp} alt="Page not found" />
        <h1>{t('error.404.header')}</h1>
        <p>{t('error.404.description')}</p>
    </div>
  );
}

export default PageNotFound;