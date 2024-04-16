import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

type Language = {
  code: string;
  name: string;
  flag: string | null;
};

const languages: Language[] = [
  { code: 'en', name: 'English', flag: '🇺🇲' },
  { code: 'fr', name: 'French', flag: '🇨🇵' },
  { code: 'ru', name: 'Russian', flag: '🇷🇺' },
];

const LanguageSelector: React.FC = () => {
  const { t, i18n } = useTranslation();
  const [activeLanguage, setActiveLanguage] = useState<string>('');

  useEffect(() => {
    setActiveLanguage(i18n.language);
  }, [i18n.language]);

  const changeLanguage = (code: string) => {
    i18n.changeLanguage(code);
    setActiveLanguage(code);
  };

  return (
    <div className="language-selector">
      <select
        className="language-selector__select"
        value={activeLanguage}
        onChange={(e) => changeLanguage(e.target.value)}
      >
        <option value="0">{t('Language')}</option>
        {languages.map((lang) => (
          <option key={lang.code} value={lang.code}>
            <span className='language-selector-item-flag'>{lang.flag}</span>
            <span className='language-selector-item-code'>  {lang.code.toUpperCase()}</span>
          </option>
        ))}
      </select>
    </div>
  );
};

export default LanguageSelector;
