import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import Navbar from './util/Navbar';
import { TeamSelection } from './TeamSelector';
import { FiArrowDownCircle, FiDatabase, FiCode, FiClock, FiPlay, FiBookOpen } from 'react-icons/fi';
import { FaGithub, FaTelegram } from "react-icons/fa6";


interface FeatureItem {
  title: string;
  description: string | null;
  icon: JSX.Element | null;
}

interface Credential {
  service_link: string;
  service_icon: JSX.Element | null;
}

interface CredentialTeamItem {
  name: string,
  description: string,
  avatar: string,
  credentials: Credential[] | null
}


const ArrowLink: React.FC<{ sectionId: string }> = ({ sectionId }) => {
  return (
    <div className='arrow-wrapper'>
      <a href={`#${sectionId}`}>
        <FiArrowDownCircle />
      </a>
    </div>
  );
}


const Home: React.FC = () => {
  const { t } = useTranslation();

  const sections = [
    { id: 'landing', label: t('home.landing.h2')},
    { id: 'features', label: t('home.features.h2') },
    { id: 'predict-match', label: t('home.predict-match.h2') },
    { id: 'team-credential', label: t('home.team-credential.h2') }
  ];

  const featureitems: FeatureItem[] = [
    {
      title: t('home.features.items.0.title'),
      description: t('home.features.items.0.description'),
      icon: <FiDatabase />
    },
    {
      title: t('home.features.items.1.title'),
      description: t('home.features.items.1.description'),
      icon: <FiCode />
    },
    {
      title: t('home.features.items.2.title'),
      description: t('home.features.items.2.description'),
      icon: <FiClock />
    }
  ]

  const credentialteamitems: CredentialTeamItem[] = [
    {
      name: 'Segfaul',
      description: 'Founder, Backend and Frontend developer',
      avatar: 'https://i.postimg.cc/5ydCNSwW/avatar.jpg',
      credentials: [
        {
          service_link: 'https://github.com/segfaul',
          service_icon: <FaGithub />
        },
        {
          service_link: 'https://percoit.t.me/',
          service_icon: <FaTelegram />
        }
      ]
    }
  ]

  return (
    <div className='home'>
      <Navbar sections={sections} />
      <section className='landing' id='landing'>
        <div className='landing-text'>
          <h1>Dotaverse</h1>
          <h3>"{t('home.landing.h3')}"</h3>
          <p>{t('home.landing.p')}</p>
          <div className='landing-nav'>
            <a href='#predict-match'>
              <span className="landing-nav-text">{t('home.landing.nav.0')}</span>
              <span className="landing-nav-icon"><FiPlay /></span>
            </a>
            <Link to={'api/redoc'}>
              <span className="landing-nav-text">{t('home.landing.nav.1')}</span>
              <span className="landing-nav-icon"><FiBookOpen /></span>
            </Link>
          </div>
        </div>
        <div className="landing-img">
          <img src='https://i.postimg.cc/G3P2t6n5/landing-pa-1.png' />
        </div>
        <ArrowLink sectionId='features'/>
      </section>
      <section className='features' id='features'>
        <h2>{t('home.features.h2')}</h2>
        <h3>{t('home.features.h3')}</h3>
        <p>{t('home.features.p')}</p>
        <ul className='features-items'>
          {featureitems.map((item, index) => (
            <li key={index} className='features-item'>
                <span className='feature-item-icon'>{item.icon}</span>
                <h3 className='feature-item-title'>{item.title}</h3>
                <p className="feature-item-description">{item.description}</p>
            </li>
          ))}
        </ul>
        <ArrowLink sectionId='predict-match'/>
      </section>
      <section className='predict-match' id='predict-match'>
        <h2>{t('home.predict-match.h2')}</h2>
        <p>{t('home.predict-match.p')}</p>
        <TeamSelection />
        <ArrowLink sectionId='team-credential'/>
      </section>
      <section className="team-credential" id='team-credential'>
        <h2>{t('home.team-credential.h2')}</h2>
        <h3>{t('home.team-credential.h3')}</h3>
        <ul className='team-credential-items'>
          {credentialteamitems.map((item, index) => (
            <li key={index} className='team-credential-item'>
                <img src={item.avatar} alt='avatar' />
                <div className='team-credential-item-text'>
                  <h3 className='team-credential-item-name'>{item.name}</h3>
                  <p className="team-credential-item-description">{item.description}</p>
                  <div className='team-credential-item-credentials'>
                    {item.credentials?.map((item) => (
                      <a href={item.service_link} target='_blank'>
                        {item.service_icon}
                      </a>
                    ))}
                  </div>
                </div>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}

export default Home;