import { useState } from 'react';
import { MessageSquare, Search, Plus, X, Trash2, MoreHorizontal } from 'lucide-react';
import CerberusIcon from './CerberusIcon';

const Sidebar = ({ 
  isOpen, 
  onToggle, 
  sessions, 
  activeSessionId, 
  onSelectSession, 
  onNewSession,
  onDeleteSession 
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [hoveredSession, setHoveredSession] = useState(null);

  const filteredSessions = sessions.filter(session =>
    session.title?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const groupedSessions = {
    today: filteredSessions.filter(s => isToday(s.created_at)),
    yesterday: filteredSessions.filter(s => isYesterday(s.created_at)),
    older: filteredSessions.filter(s => !isToday(s.created_at) && !isYesterday(s.created_at))
  };

  if (!isOpen) return null;

  return (
    <>
      {/* Overlay for mobile */}
      <div 
        className="fixed inset-0 bg-black/60 z-40 md:hidden animate-fade-in"
        onClick={onToggle}
      />

      {/* Sidebar */}
      <aside className="fixed left-0 top-0 h-full w-72 bg-black border-r border-cerberus-border z-50 flex flex-col animate-slide-in-left">
        {/* Header */}
        <div className="h-14 flex items-center justify-between px-3 border-b border-cerberus-border">
          <button
            onClick={onToggle}
            className="p-2 hover:bg-cerberus-dark rounded-lg transition-colors"
            aria-label="Fechar sidebar"
          >
            <X className="w-5 h-5 text-cerberus-text-secondary" />
          </button>
          
          <button
            onClick={onNewSession}
            className="p-2 hover:bg-cerberus-dark rounded-lg transition-colors"
            aria-label="Nova conversa"
          >
            <Plus className="w-5 h-5 text-cerberus-text-secondary" />
          </button>
        </div>

        {/* Search */}
        <div className="p-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-cerberus-text-muted" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Buscar conversas..."
              className="w-full bg-cerberus-dark border border-cerberus-border rounded-lg pl-10 pr-4 py-2.5 text-sm outline-none focus:border-cerberus-border-light transition-colors placeholder:text-cerberus-text-muted"
            />
          </div>
        </div>

        {/* Sessions List */}
        <div className="flex-1 overflow-y-auto px-2 pb-4">
          {filteredSessions.length === 0 ? (
            <div className="text-center py-8">
              <MessageSquare className="w-8 h-8 text-cerberus-text-muted mx-auto mb-2" />
              <p className="text-sm text-cerberus-text-muted">
                {searchQuery ? 'Nenhuma conversa encontrada' : 'Nenhuma conversa ainda'}
              </p>
            </div>
          ) : (
            <>
              {groupedSessions.today.length > 0 && (
                <SessionGroup 
                  title="Hoje" 
                  sessions={groupedSessions.today} 
                  activeId={activeSessionId} 
                  onSelect={onSelectSession}
                  onDelete={onDeleteSession}
                  hoveredSession={hoveredSession}
                  setHoveredSession={setHoveredSession}
                />
              )}
              {groupedSessions.yesterday.length > 0 && (
                <SessionGroup 
                  title="Ontem" 
                  sessions={groupedSessions.yesterday} 
                  activeId={activeSessionId} 
                  onSelect={onSelectSession}
                  onDelete={onDeleteSession}
                  hoveredSession={hoveredSession}
                  setHoveredSession={setHoveredSession}
                />
              )}
              {groupedSessions.older.length > 0 && (
                <SessionGroup 
                  title="Anterior" 
                  sessions={groupedSessions.older} 
                  activeId={activeSessionId} 
                  onSelect={onSelectSession}
                  onDelete={onDeleteSession}
                  hoveredSession={hoveredSession}
                  setHoveredSession={setHoveredSession}
                />
              )}
            </>
          )}
        </div>

        {/* Footer */}
        <div className="p-3 border-t border-cerberus-border">
          <div className="flex items-center gap-2 px-2 py-1">
            <CerberusIcon className="w-5 h-5 text-cerberus-text-secondary" />
            <span className="text-xs text-cerberus-text-muted">Cerberus AI</span>
          </div>
        </div>
      </aside>
    </>
  );
};

const SessionGroup = ({ title, sessions, activeId, onSelect, onDelete, hoveredSession, setHoveredSession }) => (
  <div className="mb-4">
    <h3 className="text-2xs font-medium text-cerberus-text-muted uppercase tracking-wider px-3 mb-1.5">
      {title}
    </h3>
    <div className="space-y-0.5">
      {sessions.map(session => (
        <button
          key={session.id}
          onClick={() => onSelect(session.id)}
          onMouseEnter={() => setHoveredSession(session.id)}
          onMouseLeave={() => setHoveredSession(null)}
          className={`w-full text-left px-3 py-2.5 rounded-lg transition-colors group relative ${
            session.id === activeId
              ? 'bg-cerberus-dark text-white'
              : 'text-cerberus-text-secondary hover:bg-cerberus-dark/50 hover:text-white'
          }`}
        >
          <div className="flex items-center gap-2.5 pr-6">
            <MessageSquare className="w-4 h-4 flex-shrink-0 opacity-50" />
            <span className="text-sm truncate">
              {session.title || 'Nova conversa'}
            </span>
          </div>
          
          {/* Delete button on hover */}
          {hoveredSession === session.id && onDelete && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                onDelete(session.id);
              }}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-1 hover:bg-cerberus-border rounded transition-colors"
            >
              <Trash2 className="w-3.5 h-3.5 text-cerberus-text-muted hover:text-red-400" />
            </button>
          )}
        </button>
      ))}
    </div>
  </div>
);

const isToday = (date) => {
  if (!date) return false;
  const today = new Date();
  const d = new Date(date);
  return d.toDateString() === today.toDateString();
};

const isYesterday = (date) => {
  if (!date) return false;
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  const d = new Date(date);
  return d.toDateString() === yesterday.toDateString();
};

export default Sidebar;
