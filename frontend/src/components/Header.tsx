import React from 'react';

interface HeaderProps {
  title: string;
  menuItems: string[];
}

const Header: React.FC<HeaderProps> = ({ title, menuItems }) => {
  return (
    <header>
      <h1>
        <a href={"/"}>
            {title}
        </a>
    </h1>
      <nav className='main-menu'>
        <ul>
          {menuItems.map((item, index) => (
            <li key={index}>
                <a href={"/" + item}>
                    {item}
                </a>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  );
};

export default Header;
