import { createContext, useContext, useState } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [accessToken, setAccessToken] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const login = (token) => {
    setAccessToken(token);
    setIsAuthenticated(true);
  };

  const logout = async () => {
    try {
      const originalFetch = window.fetch.originalFetch || window.fetch;
      await originalFetch('http://localhost:8000/api/auth/logout', {
        method: 'POST',
        credentials: 'include'
      });
    } catch (err) {
      console.error('Logout error:', err);
    }
    setAccessToken(null);
    setIsAuthenticated(false);
  };

  const refreshAccessToken = async () => {
    try {
      const originalFetch = window.fetch.originalFetch || window.fetch;
      const res = await originalFetch('http://localhost:8000/api/auth/refresh', {
        method: 'POST',
        credentials: 'include'
      });
      
      if (!res.ok) throw new Error('Refresh failed');
      
      const data = await res.json();
      setAccessToken(data.access_token);
      setIsAuthenticated(true);
      return data.access_token;
    } catch (err) {
      console.error('Refresh error:', err);
      logout();
      return null;
    }
  };

  return (
    <AuthContext.Provider value={{ accessToken, isAuthenticated, login, logout, refreshAccessToken }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};
