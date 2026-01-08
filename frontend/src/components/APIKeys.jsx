import { useState, useEffect } from 'react';
import { Key, Plus, Copy, RotateCcw, Trash2, Check, Eye, EyeOff } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const APIKeys = () => {
  const { accessToken } = useAuth();
  const [keys, setKeys] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showNewKeyModal, setShowNewKeyModal] = useState(false);
  const [newKeyName, setNewKeyName] = useState('');
  const [newKeyPlan, setNewKeyPlan] = useState('free');
  const [createdKey, setCreatedKey] = useState(null);

  useEffect(() => {
    loadKeys();
  }, []);

  const loadKeys = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/keys/', {
        headers: { 'Authorization': `Bearer ${accessToken}` }
      });
      const data = await response.json();
      setKeys(data.keys || []);
    } catch (err) {
      console.error('Erro ao carregar keys:', err);
    } finally {
      setLoading(false);
    }
  };

  const createKey = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/keys/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: newKeyName, plan: newKeyPlan })
      });
      const data = await response.json();
      setCreatedKey(data.key);
      setNewKeyName('');
      setShowNewKeyModal(false);
      loadKeys();
    } catch (err) {
      console.error('Erro ao criar key:', err);
    }
  };

  const deleteKey = async (key) => {
    if (!confirm('Deseja realmente desativar esta API key?')) return;
    
    try {
      await fetch(`http://localhost:8000/api/keys/${key}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${accessToken}` }
      });
      loadKeys();
    } catch (err) {
      console.error('Erro ao deletar key:', err);
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold text-white">API Keys</h1>
        <button
          onClick={() => setShowNewKeyModal(true)}
          className="flex items-center gap-2 px-4 py-2 bg-white text-black rounded-lg hover:bg-gray-200 transition-colors"
        >
          <Plus className="w-4 h-4" />
          Nova API Key
        </button>
      </div>

      {createdKey && (
        <div className="mb-6 p-4 bg-green-500/10 border border-green-500/30 rounded-xl">
          <div className="flex items-center gap-2 text-green-400 mb-2">
            <Check className="w-5 h-5" />
            <span className="font-semibold">API Key criada com sucesso!</span>
          </div>
          <p className="text-sm text-cerberus-text-secondary mb-3">
            Copie esta chave agora. Ela não será exibida novamente.
          </p>
          <div className="flex items-center gap-2">
            <code className="flex-1 px-3 py-2 bg-cerberus-darker border border-cerberus-border rounded-lg text-sm font-mono text-white">
              {createdKey}
            </code>
            <button
              onClick={() => {
                navigator.clipboard.writeText(createdKey);
                setTimeout(() => setCreatedKey(null), 2000);
              }}
              className="px-3 py-2 bg-cerberus-dark border border-cerberus-border rounded-lg hover:bg-cerberus-darker transition-colors"
            >
              <Copy className="w-4 h-4 text-cerberus-text-secondary" />
            </button>
          </div>
        </div>
      )}

      {loading ? (
        <div className="text-center text-cerberus-text-secondary py-12">Carregando...</div>
      ) : keys.length === 0 ? (
        <div className="text-center py-12">
          <Key className="w-12 h-12 text-cerberus-text-muted mx-auto mb-4" />
          <p className="text-cerberus-text-secondary mb-4">Nenhuma API key criada</p>
          <button
            onClick={() => setShowNewKeyModal(true)}
            className="px-4 py-2 bg-white text-black rounded-lg hover:bg-gray-200 transition-colors"
          >
            Criar primeira API Key
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {keys.map((key) => (
            <KeyCard key={key.key} apiKey={key} onDelete={deleteKey} />
          ))}
        </div>
      )}

      {showNewKeyModal && (
        <Modal onClose={() => setShowNewKeyModal(false)}>
          <h2 className="text-xl font-semibold text-white mb-4">Nova API Key</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm text-cerberus-text-secondary mb-2">Nome</label>
              <input
                type="text"
                value={newKeyName}
                onChange={(e) => setNewKeyName(e.target.value)}
                placeholder="Ex: Produção, Desenvolvimento"
                className="w-full px-3 py-2 bg-cerberus-darker border border-cerberus-border rounded-lg text-white outline-none focus:border-cerberus-border-light"
              />
            </div>
            <div>
              <label className="block text-sm text-cerberus-text-secondary mb-2">Plano</label>
              <select
                value={newKeyPlan}
                onChange={(e) => setNewKeyPlan(e.target.value)}
                className="w-full px-3 py-2 bg-cerberus-darker border border-cerberus-border rounded-lg text-white outline-none focus:border-cerberus-border-light"
              >
                <option value="free">Free (10 req/min)</option>
                <option value="pro">Pro (60 req/min)</option>
                <option value="enterprise">Enterprise (300 req/min)</option>
              </select>
            </div>
            <div className="flex gap-2 pt-2">
              <button
                onClick={createKey}
                disabled={!newKeyName.trim()}
                className="flex-1 px-4 py-2 bg-white text-black rounded-lg hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Criar
              </button>
              <button
                onClick={() => setShowNewKeyModal(false)}
                className="px-4 py-2 bg-cerberus-dark border border-cerberus-border rounded-lg text-cerberus-text-secondary hover:text-white transition-colors"
              >
                Cancelar
              </button>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
};

const KeyCard = ({ apiKey, onDelete }) => {
  const [showKey, setShowKey] = useState(false);
  const [copied, setCopied] = useState(false);

  const copyKey = () => {
    navigator.clipboard.writeText(apiKey.key);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const maskedKey = apiKey.key.slice(0, 8) + '...' + apiKey.key.slice(-4);

  return (
    <div className="bg-cerberus-dark border border-cerberus-border rounded-xl p-6">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-white mb-1">{apiKey.name}</h3>
          <span className="inline-block px-2 py-1 bg-cerberus-darker border border-cerberus-border rounded text-xs text-cerberus-text-secondary uppercase">
            {apiKey.plan}
          </span>
        </div>
        <button
          onClick={() => onDelete(apiKey.key)}
          className="p-2 text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
        >
          <Trash2 className="w-4 h-4" />
        </button>
      </div>

      <div className="flex items-center gap-2 mb-4">
        <code className="flex-1 px-3 py-2 bg-cerberus-darker border border-cerberus-border rounded-lg text-sm font-mono text-white">
          {showKey ? apiKey.key : maskedKey}
        </code>
        <button
          onClick={() => setShowKey(!showKey)}
          className="p-2 bg-cerberus-darker border border-cerberus-border rounded-lg hover:bg-black transition-colors"
        >
          {showKey ? <EyeOff className="w-4 h-4 text-cerberus-text-secondary" /> : <Eye className="w-4 h-4 text-cerberus-text-secondary" />}
        </button>
        <button
          onClick={copyKey}
          className="p-2 bg-cerberus-darker border border-cerberus-border rounded-lg hover:bg-black transition-colors"
        >
          {copied ? <Check className="w-4 h-4 text-green-400" /> : <Copy className="w-4 h-4 text-cerberus-text-secondary" />}
        </button>
      </div>

      <div className="grid grid-cols-3 gap-4 text-sm">
        <div>
          <div className="text-cerberus-text-muted mb-1">Uso</div>
          <div className="text-white font-medium">{apiKey.usage_count || 0} reqs</div>
        </div>
        <div>
          <div className="text-cerberus-text-muted mb-1">Rate Limit</div>
          <div className="text-white font-medium">{apiKey.rate_limit}/min</div>
        </div>
        <div>
          <div className="text-cerberus-text-muted mb-1">Status</div>
          <div className={`font-medium ${apiKey.is_active ? 'text-green-400' : 'text-red-400'}`}>
            {apiKey.is_active ? 'Ativa' : 'Inativa'}
          </div>
        </div>
      </div>
    </div>
  );
};

const Modal = ({ children, onClose }) => (
  <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
    <div className="bg-cerberus-dark border border-cerberus-border rounded-xl p-6 max-w-md w-full">
      {children}
    </div>
  </div>
);

export default APIKeys;
