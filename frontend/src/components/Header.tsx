import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { FiFileText, FiHome, FiShield, FiUsers, FiUser, FiColumns, FiBook, FiSidebar, FiGithub, FiBookOpen } from "react-icons/fi";

import LanguageSelector from './LanguageSelector';
import { isAuthenticated } from './context/AuthContext';
import dotaverseLogo from '../assets/dotaverse_logo.webp';

interface MenuItem {
  name: string;
  link: string;
  icon: JSX.Element | null;
}

const Header: React.FC = () => {
  const { t } = useTranslation();
  const isAuth = isAuthenticated();
  const [sidebarOpen, setSidebarOpen] = useState<boolean>(() => {
    const storedValue = sessionStorage.getItem('sidebarOpen');
    return storedValue ? JSON.parse(storedValue) : (window.innerWidth < 1132 ? true : false);
  });
  const [chosenMenuItem, setChosenMenuItem] = useState<string>('');
  const location = useLocation();

  const title = 'Dotaverse';
  const menuItems: MenuItem[] = [
    { name: t('header.main-menu.0.name'), link: '/', icon: <FiHome />},
    { name: t('header.main-menu.1.name'), link: '/heroes', icon: <FiShield /> },
    { name: t('header.main-menu.2.name'), link: '/teams', icon: <FiUsers /> },
    { name: t('header.main-menu.3.name'), link: '/players', icon: <FiUser /> },
    { name: t('header.main-menu.4.name'), link: '/matches', icon: <FiBook /> },
    ...(isAuth ? [{ name: t('header.main-menu.5.name'), link: "/logs", icon: <FiFileText /> }] : [])
  ];

  const credentials: MenuItem[] = [
    { name: 'Github', link: 'https://github.com/Segfaul/dotaverse', icon: <FiGithub />},
    { name: 'APIDocs', link: '/api/redoc', icon: <FiBookOpen /> }
  ];

  useEffect(() => {
    const path = location.pathname;
    const parts = path.split('/');
    const menuItemName = parts[1] ? `/${parts[1]}` : '/';
    setChosenMenuItem(menuItemName);
  }, [location.pathname]);

  const handleMenuItemClick = (itemName: string) => {
    setChosenMenuItem(itemName);
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: 'auto',
    });
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  useEffect(() => {
    sessionStorage.setItem('sidebarOpen', JSON.stringify(sidebarOpen));
  }, [sidebarOpen]);

  return (
    <header className={sidebarOpen ? 'open' : 'closed'}>
      <div className='header-title'>
        {sidebarOpen && (
          <Link to={"/"}>
          <div className='header-title-nav'>
            <img src={dotaverseLogo} alt='Logo' />
            <span>
              {title}
            </span>
          </div>
          </Link>
        )}
        <button className="sidebar-toggle" onClick={toggleSidebar}>
          {sidebarOpen ? <FiSidebar /> : <FiColumns />}
        </button>
      </div>
      <nav className="main-menu">
        <ul>
          {menuItems.map((item, index) => (
            <li key={index} className={chosenMenuItem === item.link ? 'chosen-menu-item' : ''}>
              <Link to={item.link ? item.link: `/${item.name.toLowerCase()}`} onClick={() => handleMenuItemClick(item.link)}>
                <span className='menu-item-icon'>{item.icon}</span>
                {sidebarOpen && 
                  <span className='menu-item-text'>
                    {item.name}
                  </span>
                }
              </Link>
            </li>
          ))}
        </ul>
      </nav>
      <div className='footer'>
        <LanguageSelector />
        <div className='credentials'>
        <ul>
          {credentials.map((item, index) => (
            <li key={index}>
              <Link to={item.link ? item.link: `/${item.name.toLowerCase()}`} target="_blank">
                  <span className='credential-item-icon'>{item.icon}</span>
                  {sidebarOpen && 
                    <span className='credential-item-text'>
                      {item.name}
                    </span>
                  }
              </Link>
            </li>
          ))}
        </ul>
        </div>
      </div>
    </header>
  );
};

export default Header;
