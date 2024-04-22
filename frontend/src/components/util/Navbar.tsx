import React, { useState, useEffect } from 'react';

interface NavbarProps {
    sections: { id: string; label: string }[];
}
  
const Navbar: React.FC<NavbarProps> = ({ sections }) => {
    const [isFixed, setIsFixed] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            const scrollTop = window.scrollY;

            if (scrollTop > 100) {
                setIsFixed(true);
            } else {
                setIsFixed(false);
            }
        };
        window.addEventListener('scroll', handleScroll);
        return () => {
            window.removeEventListener('scroll', handleScroll);
        };
    }, []);

    return (
        <nav className={`navbar-menu ${isFixed ? 'fixed' : ''}`}>
        <ul className='navbar-menu-items'>
            {sections.map((section) => (
            <li key={section.id} className='navbar-menu-item'>
                <a href={`#${section.id}`} className='navbar-menu-item-link'>
                {section.label}
                </a>
            </li>
            ))}
        </ul>
        </nav>
    );
};

export default Navbar
