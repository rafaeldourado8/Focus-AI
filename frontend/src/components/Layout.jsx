import { useState } from 'react';
import { LayoutDashboard, MessageSquare, Key, BarChart3, Settings, LogOut, Menu, X } from 'lucide-react';
import CerberusIcon from './CerberusIcon';

const Layout = ({ children, currentPage, onNavigate, onLogout }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'chat', label: 'Chat', icon: MessageSquare },
    { id: 'api-keys', label: 'API Keys', icon: Key },
    { id: 'usage', label: 'Usage', icon: BarChart3 },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <div className="h-screen bg-black flex overflow-hidden">
      {/* Sidebar Desktop */}
      <aside className="hidden md:flex w-64 bg-cerberus-dark border-r border-cerberus-border flex-col">
        <div className="p-4 border-b border-cerberus-border">
          <div className="flex items-center gap-2">
            <CerberusIcon className="w-8 h-8 text-white" />
            <span className="font-semibold text-white text-lg">Cerberus AI</span>
          </div>
        </div>

        <nav className="flex-1 p-4 space-y-1">
          {navItems.map((item) => (
            <NavItem
              key={item.id}
              icon={item.icon}
              label={item.label}
              active={currentPage === item.id}
              onClick={() => onNavigate(item.id)}
            />
          ))}
        </nav>

        <div className="p-4 border-t border-cerberus-border">
          <button
            onClick={onLogout}
            className="flex items-center gap-3 w-full px-3 py-2 text-cerberus-text-secondary hover:text-white hover:bg-cerberus-darker rounded-lg transition-colors"
          >
            <LogOut className="w-5 h-5" />
            <span>Sair</span>
          </button>
        </div>
      </aside>

      {/* Mobile Header */}
      <div className="md:hidden fixed top-0 left-0 right-0 h-14 bg-cerberus-dark border-b border-cerberus-border flex items-center justify-between px-4 z-50">
        <div className="flex items-center gap-2">
          <CerberusIcon className="w-6 h-6 text-white" />
          <span className="font-semibold text-white">Cerberus AI</span>
        </div>
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="p-2 text-cerberus-text-secondary hover:text-white"
        >
          {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden fixed inset-0 top-14 bg-black/80 z-40" onClick={() => setMobileMenuOpen(false)}>
          <div className="bg-cerberus-dark border-r border-cerberus-border w-64 h-full p-4" onClick={(e) => e.stopPropagation()}>
            <nav className="space-y-1">
              {navItems.map((item) => (
                <NavItem
                  key={item.id}
                  icon={item.icon}
                  label={item.label}
                  active={currentPage === item.id}
                  onClick={() => {
                    onNavigate(item.id);
                    setMobileMenuOpen(false);
                  }}
                />
              ))}
            </nav>
            <div className="mt-4 pt-4 border-t border-cerberus-border">
              <button
                onClick={onLogout}
                className="flex items-center gap-3 w-full px-3 py-2 text-cerberus-text-secondary hover:text-white hover:bg-cerberus-darker rounded-lg transition-colors"
              >
                <LogOut className="w-5 h-5" />
                <span>Sair</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto md:mt-0 mt-14">
        {children}
      </main>
    </div>
  );
};

const NavItem = ({ icon: Icon, label, active, onClick }) => (
  <button
    onClick={onClick}
    className={`flex items-center gap-3 w-full px-3 py-2 rounded-lg transition-colors ${
      active
        ? 'bg-white text-black'
        : 'text-cerberus-text-secondary hover:text-white hover:bg-cerberus-darker'
    }`}
  >
    <Icon className="w-5 h-5" />
    <span>{label}</span>
  </button>
);

export default Layout;
