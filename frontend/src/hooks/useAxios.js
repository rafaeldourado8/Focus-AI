import { useEffect } from 'react';

const originalFetch = window.fetch;

export const useAxiosInterceptor = (onLogout) => {
  useEffect(() => {
    window.fetch = async (...args) => {
      const response = await originalFetch(...args);
      
      if (response.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('sessionId');
        onLogout?.();
      }
      
      return response;
    };

    return () => {
      window.fetch = originalFetch;
    };
  }, [onLogout]);
};

export default useAxiosInterceptor;
