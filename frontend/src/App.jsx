import { useState, useEffect } from 'react';
import Login from './components/Login';
import Layout from './components/Layout';
import Dashboard from './components/Dashboard';
import Chat from './components/Chat';
import APIKeys from './components/APIKeys';
import Usage from './components/Usage';
import Settings from './components/Settings';
import { useAxiosInterceptor } from './hooks/useAxios';

const App = () => {
  const [token, setToken] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState('dashboard');

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('sessionId');
    setToken(null);
  };

  useAxiosInterceptor(handleLogout);

  useEffect(() => {
    const validateToken = async () => {
      const savedToken = localStorage.getItem('token');
      if (savedToken) {
        try {
          const response = await fetch('http://localhost:8000/api/sessions/', {
            headers: { 'Authorization': `Bearer ${savedToken}` }
          });
          if (response.ok) {
            setToken(savedToken);
          } else {
            localStorage.removeItem('token');
          }
        } catch {
          localStorage.removeItem('token');
        }
      }
      setIsLoading(false);
    };
    validateToken();
  }, []);

  const handleLogin = (newToken) => {
    setToken(newToken);
  };

  const handleNavigate = (page) => {
    setCurrentPage(page);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="animate-spin w-8 h-8 border-2 border-cerberus-border border-t-white rounded-full" />
      </div>
    );
  }

  if (!token) {
    return <Login onLogin={handleLogin} />;
  }

  // Render page without Layout for Chat (has its own layout)
  if (currentPage === 'chat') {
    return <Chat token={token} onLogout={handleLogout} onNavigate={handleNavigate} />;
  }

  return (
    <Layout currentPage={currentPage} onNavigate={handleNavigate} onLogout={handleLogout}>
      {currentPage === 'dashboard' && <Dashboard token={token} />}
      {currentPage === 'api-keys' && <APIKeys token={token} />}
      {currentPage === 'usage' && <Usage token={token} />}
      {currentPage === 'settings' && <Settings token={token} />}
    </Layout>
  );
};

export default App;
