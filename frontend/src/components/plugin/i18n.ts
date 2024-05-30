import i18n from 'i18next'
import { initReactI18next } from 'react-i18next';

import Backend from 'i18next-http-backend';
import LanguageDetector from 'i18next-browser-languagedetector';

import enTranslation from '../locale/en.json';
import frTranslation from '../locale/fr.json';
import ruTranslation from '../locale/ru.json';

i18n
  .use(Backend)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    fallbackLng: 'en',
    debug: false,
    resources: {
        en: {
            translation: enTranslation
        },
        fr: {
            translation: frTranslation
        },
        ru: {
            translation: ruTranslation
        }
    }
  });

export default i18n;