import { useState } from 'react';
import { User, Bell, Shield, Palette, Save } from 'lucide-react';

const Settings = ({ token }) => {
  const [settings, setSettings] = useState({
    debugMode: false,
    notifications: true,
    theme: 'dark',
    language: 'pt-BR'
  });

  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    // TODO: Save to backend
    localStorage.setItem('userSettings', JSON.stringify(settings));
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-white mb-8">Settings</h1>

      <div className="space-y-6">
        {/* Profile Section */}
        <Section icon={<User className="w-5 h-5" />} title="Perfil">
          <div className="space-y-4">
            <div>
              <label className="block text-sm text-cerberus-text-secondary mb-2">
                Email
              </label>
              <input
                type="email"
                disabled
                value="user@example.com"
                className="w-full px-3 py-2 bg-cerberus-darker border border-cerberus-border rounded-lg text-cerberus-text-muted"
              />
            </div>
            <div>
              <label className="block text-sm text-cerberus-text-secondary mb-2">
                Nome
              </label>
              <input
                type="text"
                placeholder="Seu nome"
                className="w-full px-3 py-2 bg-cerberus-darker border border-cerberus-border rounded-lg text-white outline-none focus:border-cerberus-border-light"
              />
            </div>
          </div>
        </Section>

        {/* Preferences */}
        <Section icon={<Palette className="w-5 h-5" />} title="Preferências">
          <div className="space-y-4">
            <ToggleSetting
              label="Debug Mode por padrão"
              description="Ativa análise técnica profunda em todas as respostas"
              checked={settings.debugMode}
              onChange={(checked) => setSettings({ ...settings, debugMode: checked })}
            />
            <div>
              <label className="block text-sm text-cerberus-text-secondary mb-2">
                Idioma
              </label>
              <select
                value={settings.language}
                onChange={(e) => setSettings({ ...settings, language: e.target.value })}
                className="w-full px-3 py-2 bg-cerberus-darker border border-cerberus-border rounded-lg text-white outline-none focus:border-cerberus-border-light"
              >
                <option value="pt-BR">Português (Brasil)</option>
                <option value="en-US">English (US)</option>
                <option value="es-ES">Español</option>
              </select>
            </div>
          </div>
        </Section>

        {/* Notifications */}
        <Section icon={<Bell className="w-5 h-5" />} title="Notificações">
          <ToggleSetting
            label="Notificações de email"
            description="Receba atualizações sobre novos recursos"
            checked={settings.notifications}
            onChange={(checked) => setSettings({ ...settings, notifications: checked })}
          />
        </Section>

        {/* Security */}
        <Section icon={<Shield className="w-5 h-5" />} title="Segurança">
          <button className="px-4 py-2 bg-cerberus-darker border border-cerberus-border rounded-lg text-cerberus-text-secondary hover:text-white hover:border-cerberus-border-light transition-colors">
            Alterar Senha
          </button>
        </Section>

        {/* Save Button */}
        <div className="flex justify-end pt-4">
          <button
            onClick={handleSave}
            className={`flex items-center gap-2 px-6 py-2 rounded-lg transition-all ${
              saved
                ? 'bg-green-500 text-white'
                : 'bg-white text-black hover:bg-gray-200'
            }`}
          >
            <Save className="w-4 h-4" />
            {saved ? 'Salvo!' : 'Salvar Alterações'}
          </button>
        </div>
      </div>
    </div>
  );
};

const Section = ({ icon, title, children }) => (
  <div className="bg-cerberus-dark border border-cerberus-border rounded-xl p-6">
    <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
      {icon}
      {title}
    </h2>
    {children}
  </div>
);

const ToggleSetting = ({ label, description, checked, onChange }) => (
  <div className="flex items-start justify-between">
    <div className="flex-1">
      <div className="text-white font-medium mb-1">{label}</div>
      <div className="text-sm text-cerberus-text-secondary">{description}</div>
    </div>
    <button
      onClick={() => onChange(!checked)}
      className={`relative w-12 h-6 rounded-full transition-colors ${
        checked ? 'bg-blue-500' : 'bg-cerberus-darker border border-cerberus-border'
      }`}
    >
      <div
        className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform ${
          checked ? 'translate-x-7' : 'translate-x-1'
        }`}
      />
    </button>
  </div>
);

export default Settings;
