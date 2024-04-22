import React from "react";

import { FiSearch } from "react-icons/fi";
import { useTranslation } from "react-i18next";


interface SearchBarProps {
  searchTerm: string;
  setSearchTerm: React.Dispatch<React.SetStateAction<string>>;
  placeholder: string | null;
}
  
  
const SearchBar: React.FC<SearchBarProps> = ({ searchTerm, setSearchTerm, placeholder }) => {
  const { t } = useTranslation();

  return (
    <div className="search-container">
      <input
        type="text"
        placeholder={placeholder ? placeholder + '...' : t('search.placeholders.default') + '...'}
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <FiSearch />
    </div>
  );
};

export default SearchBar;