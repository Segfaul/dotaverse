import React, { useEffect } from 'react';
import { useTranslation } from 'react-i18next';

import ForbiddenWebp from '../../assets/403_web.webp'


const PageForbidden: React.FC = () => {
  const { t } = useTranslation();

  useEffect(() => {
    document.title = t('error.403.header') + " - Dotaverse";
  }, [t]);

  return (
    <div className='error-page'>
        <img src={ForbiddenWebp} alt="Forbidden" />
        <h1>{t('error.403.header')}</h1>
        <p>{t('error.403.description')}</p>
    </div>
  );
}

export default PageForbidden;