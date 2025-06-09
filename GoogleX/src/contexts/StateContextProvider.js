import React, { createContext, useContext, useState } from 'react';
import axios from 'axios';

const StateContext = createContext();
const baseUrl = 'https://real-time-web-search.p.rapidapi.com/search';
const apiKey = 'be4db81c33mshfbe17f60dedbe8fp18edbajsn1f29f25e40a1';

export const StateContextProvider = ({ children }) => {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  const getResults = async (query) => {
    setLoading(true);

    const url = `${baseUrl}?q=${query}`;

    try {
      const response = await axios.get(url, {
        headers: {
          'X-RapidAPI-Key': apiKey,
          'X-RapidAPI-Host': 'real-time-web-search.p.rapidapi.com',
        },
      });

      // eslint-disable-next-line no-console
      console.log(response.data);

      setResults(response.data);
    } catch (error) {
      // eslint-disable-next-line no-console
      console.error(error);
      setResults(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <StateContext.Provider value={{ getResults, results, searchTerm, setSearchTerm, loading }}>
      {children}
    </StateContext.Provider>
  );
};

export const useStateContext = () => useContext(StateContext);
