import React from 'react';
import { NavLink } from 'react-router-dom';

import { useStateContext } from '../contexts/StateContextProvider';

const links = [
  { url: '/search', text: '🔎 All' },
  { url: '/news', text: '📰 News' },
  { url: '/images', text: '📸 Images' },
  { url: '/videos', text: '📺 Videos' },
];

export const Links = () => {
  const { setSearchTerm } = useStateContext();

  const handleSearchTerm = (searchTerm) => {
    setSearchTerm(searchTerm);
  };

  return (
    <div className="flex sm:justify-around justify-between items-center mt-4">
      {links.map(({ url, text }, index) => (
        <NavLink
          key={index}
          to={url}
          activeClassName="text-blue-700 border-b-2 dark:text-blue-300 border-blue-700 pb-2"
          onClick={() => handleSearchTerm('')} // Clear search term when navigating to a different link
        >
          {text}
        </NavLink>
      ))}
    </div>
  );
};
