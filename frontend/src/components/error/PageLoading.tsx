import React from 'react';
import { useTranslation } from 'react-i18next';

import LoadingWebp from '../../assets/loading_web.webp'


const PageLoading: React.FC = () => {
  const { t } = useTranslation();

  return (
    <div className='error-page'>
        <img src={LoadingWebp} alt="Page is loading" />
        <h1>{t('error.loading.header')}...</h1>
        <p>{t('error.loading.description')}</p>
    </div>
  );
}

export default PageLoading;