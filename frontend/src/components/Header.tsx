import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FiHome, FiShield, FiUsers, FiUser, FiColumns, FiBook, FiSidebar, FiGithub, FiBookOpen } from "react-icons/fi";

import dotaverseLogo from '../assets/dotaverse_logo.webp';

interface MenuItem {
  name: string;
  link: string | null;
  icon: JSX.Element | null;
}

const capitalize = (str: string) => {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

const Header: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState<boolean>(() => {
    const storedValue = sessionStorage.getItem('sidebarOpen');
    return storedValue ? JSON.parse(storedValue) : true;
  });
  const [chosenMenuItem, setChosenMenuItem] = useState<string>('');
  const location = useLocation();

  const title = 'Dotaverse';
  const menuItems: MenuItem[] = [
    { name: 'About', link: '/', icon: <FiHome />},
    { name: 'Heroes', link: null, icon: <FiShield /> },
    { name: 'Teams', link: null, icon: <FiUsers /> },
    { name: 'Players', link: null, icon: <FiUser /> },
    { name: 'Matches', link: null, icon: <FiBook /> }
  ];

  const credentials: MenuItem[] = [
    { name: 'Github', link: 'https://github.com/Segfaul/dotaverse', icon: <FiGithub />},
    { name: 'APIDocs', link: '/api/redoc', icon: <FiBookOpen /> }
  ];

  useEffect(() => {
    const path = location.pathname;
    const parts = path.split('/');
    const menuItemName = parts[1] ? capitalize(parts[1]) : 'About';
    setChosenMenuItem(menuItemName);
  }, [location.pathname]);

  const handleMenuItemClick = (itemName: string) => {
    setChosenMenuItem(itemName);
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
            <li key={index} className={chosenMenuItem === item.name ? 'chosen-menu-item' : ''}>
              <Link to={item.link ? item.link: `/${item.name.toLowerCase()}`} onClick={() => handleMenuItemClick(item.name)}>
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
    </header>
  );
};

export default Header;
