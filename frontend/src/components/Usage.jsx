import { useState, useEffect } from 'react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { TrendingUp, Activity, Calendar, Zap } from 'lucide-react';

const Usage = ({ token }) => {
  const [stats, setStats] = useState(null);
  const [activity, setActivity] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [statsRes, activityRes] = await Promise.all([
        fetch('http://localhost:8000/api/analytics/stats', {
          headers: { 'Authorization': `Bearer ${token}` }
        }),
        fetch('http://localhost:8000/api/analytics/activity', {
          headers: { 'Authorization': `Bearer ${token}` }
        })
      ]);

      const statsData = await statsRes.json();
      const activityData = await activityRes.json();

      setStats(statsData);
      setActivity(activityData.activities || []);
    } catch (err) {
      console.error('Erro ao carregar dados:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-cerberus-text-secondary">Carregando...</div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold text-white mb-8">Usage & Analytics</h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <StatCard
          icon={<Activity className="w-6 h-6" />}
          label="Total de Perguntas"
          value={stats?.total_questions || 0}
          color="blue"
        />
        <StatCard
          icon={<Calendar className="w-6 h-6" />}
          label="Últimos 7 dias"
          value={stats?.questions_last_7d || 0}
          color="green"
        />
        <StatCard
          icon={<Zap className="w-6 h-6" />}
          label="Sessões Totais"
          value={stats?.total_sessions || 0}
          color="purple"
        />
      </div>

      {/* Chart */}
      <div className="bg-cerberus-dark border border-cerberus-border rounded-xl p-6 mb-8">
        <h2 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
          <TrendingUp className="w-5 h-5" />
          Atividade (Últimos 30 dias)
        </h2>
        {stats?.questions_by_day?.length > 0 ? (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={stats.questions_by_day}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
              <XAxis 
                dataKey="date" 
                stroke="#6b7280"
                tick={{ fill: '#6b7280' }}
              />
              <YAxis 
                stroke="#6b7280"
                tick={{ fill: '#6b7280' }}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#111827',
                  border: '1px solid #374151',
                  borderRadius: '8px',
                  color: '#fff'
                }}
              />
              <Line 
                type="monotone" 
                dataKey="count" 
                stroke="#3b82f6" 
                strokeWidth={2}
                dot={{ fill: '#3b82f6', r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <div className="h-[300px] flex items-center justify-center text-cerberus-text-secondary">
            Sem dados para exibir
          </div>
        )}
      </div>

      {/* Recent Activity */}
      <div className="bg-cerberus-dark border border-cerberus-border rounded-xl p-6">
        <h2 className="text-xl font-semibold text-white mb-4">Atividade Recente</h2>
        {activity.length > 0 ? (
          <div className="space-y-3">
            {activity.map((item) => (
              <div
                key={item.id}
                className="p-3 bg-cerberus-darker border border-cerberus-border rounded-lg"
              >
                <p className="text-sm text-white mb-1">{item.content}</p>
                <p className="text-xs text-cerberus-text-muted">
                  {new Date(item.created_at).toLocaleString('pt-BR')}
                </p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-cerberus-text-secondary text-sm">Nenhuma atividade recente</p>
        )}
      </div>
    </div>
  );
};

const StatCard = ({ icon, label, value, color }) => {
  const colors = {
    blue: 'text-blue-400 bg-blue-500/10 border-blue-500/20',
    green: 'text-green-400 bg-green-500/10 border-green-500/20',
    purple: 'text-purple-400 bg-purple-500/10 border-purple-500/20'
  };

  return (
    <div className="bg-cerberus-dark border border-cerberus-border rounded-xl p-6">
      <div className={`w-12 h-12 rounded-lg ${colors[color]} flex items-center justify-center mb-4`}>
        {icon}
      </div>
      <div className="text-3xl font-bold text-white mb-1">{value}</div>
      <div className="text-sm text-cerberus-text-secondary">{label}</div>
    </div>
  );
};

export default Usage;
