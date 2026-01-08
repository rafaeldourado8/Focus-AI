import { useState, useEffect } from 'react';
import { BarChart3, Key, Zap, TrendingUp, Clock, Code } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const Dashboard = () => {
  const { accessToken } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
    const interval = setInterval(loadStats, 5000);
    return () => clearInterval(interval);
  }, [accessToken]);

  const loadStats = async () => {
    if (!accessToken) return;
    
    try {
      const [sessionsRes, keysRes] = await Promise.all([
        fetch('http://localhost:8000/api/sessions/', {
          headers: { 'Authorization': `Bearer ${accessToken}` }
        }),
        fetch('http://localhost:8000/api/keys/', {
          headers: { 'Authorization': `Bearer ${accessToken}` }
        })
      ]);
      
      const sessionsData = await sessionsRes.json();
      const keysData = await keysRes.json();
      
      setStats({
        totalSessions: sessionsData.sessions?.length || 0,
        totalQuestions: sessionsData.sessions?.reduce((acc, s) => acc + (s.message_count || 0), 0) || 0,
        apiKeys: keysData.keys?.length || 0,
        avgResponseTime: '1.2s'
      });
    } catch (err) {
      console.error('Erro ao carregar stats:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="flex flex-col items-center gap-4">
          <div className="animate-spin w-8 h-8 border-2 border-cerberus-border border-t-white rounded-full" />
          <div className="text-cerberus-text-secondary text-sm">Carregando dashboard...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold text-white mb-8">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          icon={<BarChart3 className="w-6 h-6" />}
          label="Sessões"
          value={stats.totalSessions}
          color="blue"
          isEmpty={stats.totalSessions === 0}
        />
        <StatCard
          icon={<Code className="w-6 h-6" />}
          label="Perguntas"
          value={stats.totalQuestions}
          color="green"
          isEmpty={stats.totalQuestions === 0}
        />
        <StatCard
          icon={<Key className="w-6 h-6" />}
          label="API Keys"
          value={stats.apiKeys}
          color="purple"
          isEmpty={stats.apiKeys === 0}
        />
        <StatCard
          icon={<Clock className="w-6 h-6" />}
          label="Tempo Médio"
          value={stats.avgResponseTime}
          color="orange"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-cerberus-dark border border-cerberus-border rounded-xl p-6">
          <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5" />
            Atividade Recente
          </h2>
          <p className="text-cerberus-text-secondary text-sm">
            Nenhuma atividade recente
          </p>
        </div>

        <div className="bg-cerberus-dark border border-cerberus-border rounded-xl p-6">
          <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5" />
            Quick Actions
          </h2>
          <div className="space-y-2">
            <QuickAction label="Nova Sessão" href="/chat" />
            <QuickAction label="Gerenciar API Keys" href="/api-keys" />
            <QuickAction label="Ver Documentação" href="/docs" />
          </div>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ icon, label, value, color, isEmpty }) => {
  const colors = {
    blue: 'text-blue-400 bg-blue-500/10 border-blue-500/20',
    green: 'text-green-400 bg-green-500/10 border-green-500/20',
    purple: 'text-purple-400 bg-purple-500/10 border-purple-500/20',
    orange: 'text-orange-400 bg-orange-500/10 border-orange-500/20'
  };

  return (
    <div className="bg-cerberus-dark border border-cerberus-border rounded-xl p-6 relative overflow-hidden">
      {isEmpty && (
        <div className="absolute inset-0 bg-gradient-to-br from-cerberus-dark via-transparent to-transparent opacity-50" />
      )}
      <div className={`w-12 h-12 rounded-lg ${colors[color]} flex items-center justify-center mb-4 relative z-10`}>
        {icon}
      </div>
      <div className="text-2xl font-bold text-white mb-1 relative z-10">{value}</div>
      <div className="text-sm text-cerberus-text-secondary relative z-10">{label}</div>
      {isEmpty && (
        <div className="text-xs text-cerberus-text-muted mt-2 relative z-10">Comece sua jornada!</div>
      )}
    </div>
  );
};

const QuickAction = ({ label, href }) => (
  <a
    href={href}
    className="block px-4 py-2 bg-cerberus-darker border border-cerberus-border rounded-lg text-sm text-cerberus-text-secondary hover:text-white hover:border-cerberus-border-light transition-colors"
  >
    {label}
  </a>
);

export default Dashboard;
