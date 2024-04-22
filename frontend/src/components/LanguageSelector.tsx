import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

type Language = {
  code: string;
  name: string;
  flag: string | null;
};

const languages: Language[] = [
  { code: 'en', name: 'English', flag: '\ud83c\uddfa\ud83c\uddf8' },
  { code: 'fr', name: 'French', flag: '\ud83c\uddeb\ud83c\uddf7' },
  { code: 'ru', name: 'Russian', flag: '\ud83c\uddf7\ud83c\uddfa' },
];

const LanguageSelector: React.FC = () => {
  const { i18n } = useTranslation();
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
