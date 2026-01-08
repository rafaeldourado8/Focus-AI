import { useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

let isRefreshing = false;
let refreshPromise = null;

export const useAxiosInterceptor = (onLogout) => {
  const { refreshAccessToken, accessToken } = useAuth();
  
  useEffect(() => {
    const originalFetch = window.fetch.originalFetch || window.fetch;
    if (!window.fetch.originalFetch) {
      window.fetch.originalFetch = originalFetch;
    }
    
    window.fetch = async (...args) => {
      let [url, config = {}] = args;
      
      const currentToken = accessToken;
      if (currentToken) {
        config.headers = {
          ...config.headers,
          'Authorization': `Bearer ${currentToken}`
        };
      }
      
      config.credentials = 'include';
      
      let response = await originalFetch(url, config);
      
      if (response.status === 401 && !url.includes('/auth/refresh') && !url.includes('/auth/logout')) {
        if (!isRefreshing) {
          isRefreshing = true;
          refreshPromise = refreshAccessToken().finally(() => {
            isRefreshing = false;
            refreshPromise = null;
          });
        }
        
        const newToken = await refreshPromise;
        if (newToken) {
          config.headers = {
            ...config.headers,
            'Authorization': `Bearer ${newToken}`
          };
          response = await originalFetch(url, config);
        } else {
          localStorage.removeItem('sessionId');
          onLogout?.();
        }
      }
      
      return response;
    };

    return () => {
      if (window.fetch !== originalFetch) {
        window.fetch = originalFetch;
      }
    };
  }, [onLogout, accessToken, refreshAccessToken]);
};

export default useAxiosInterceptor;
