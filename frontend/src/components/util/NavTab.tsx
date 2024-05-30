import React, { useState } from "react";


export interface NavTab {
  value: string;
  label: string;
  content: JSX.Element;
}

interface NavTabProps {
  defaultTab: string;
  tabs: NavTab[];
}

const NavTab: React.FC<NavTabProps> = ({ defaultTab, tabs }) => {
  const [selectedTab, setSelectedTab] = useState(defaultTab);

  const handleTabChange = (tab: string) => {
    setSelectedTab(tab);
  };

  return (
    <div className="tab-component">
      <div className="tab-buttons">
        {tabs.map(tab => (
          <button
            key={tab.value}
            onClick={() => handleTabChange(tab.value)}
            className={selectedTab === tab.value ? 'active' : ''}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <div className="tab-content">
        {tabs.map(tab => (
          <div key={tab.value} className={selectedTab === tab.value ? 'active' : 'inactive'}>
            {tab.content}
          </div>
        ))}
      </div>
    </div>
  );
};

export default NavTab;