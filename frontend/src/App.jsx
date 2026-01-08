import { useState, useEffect } from 'react';
import Login from './components/Login';
import Layout from './components/Layout';
import Dashboard from './components/Dashboard';
import Chat from './components/Chat';
import APIKeys from './components/APIKeys';
import Usage from './components/Usage';
import Settings from './components/Settings';
import { useAxiosInterceptor } from './hooks/useAxios';
import { AuthProvider, useAuth } from './contexts/AuthContext';

const AppContent = () => {
  const { isAuthenticated, login, logout } = useAuth();
  const [isLoading, setIsLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState('dashboard');

  useAxiosInterceptor(logout);

  useEffect(() => {
    setIsLoading(false);
  }, []);

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

  if (!isAuthenticated) {
    return <Login onLogin={login} />;
  }

  if (currentPage === 'chat') {
    return <Chat onLogout={logout} onNavigate={handleNavigate} />;
  }

  return (
    <Layout currentPage={currentPage} onNavigate={handleNavigate} onLogout={logout}>
      {currentPage === 'dashboard' && <Dashboard />}
      {currentPage === 'api-keys' && <APIKeys />}
      {currentPage === 'usage' && <Usage />}
      {currentPage === 'settings' && <Settings />}
    </Layout>
  );
};

const App = () => (
  <AuthProvider>
    <AppContent />
  </AuthProvider>
);

export default App;
