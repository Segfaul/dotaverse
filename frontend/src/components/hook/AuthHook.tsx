import { useEffect, useState } from 'react';

const useTokenExpiration = () => {
  const [isTokenExpired, setIsTokenExpired] = useState<boolean>(false);

  useEffect(() => {
    const accessToken = localStorage.getItem('access_token');
    const tokenType = localStorage.getItem('token_type');

    if (accessToken && tokenType) {
      const tokenData = JSON.parse(atob(accessToken.split('.')[1]));
      const expirationTime = tokenData.exp * 1000;

      if (expirationTime < Date.now()) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('token_type');
        setIsTokenExpired(true);
      }
    } else {
      setIsTokenExpired(true);
    }
  }, []);

  return isTokenExpired;
};

export default useTokenExpiration;
