import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MessageSquare, Search, Plus, Menu, X } from 'lucide-react';

const Sidebar = ({ isOpen, onToggle, sessions, activeSessionId, onSelectSession, onNewSession }) => {
  const [searchQuery, setSearchQuery] = useState('');

  const filteredSessions = sessions.filter(session =>
    session.title?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const groupedSessions = {
    today: filteredSessions.filter(s => isToday(s.created_at)),
    yesterday: filteredSessions.filter(s => isYesterday(s.created_at)),
    older: filteredSessions.filter(s => !isToday(s.created_at) && !isYesterday(s.created_at))
  };

  return (
    <>
      {/* Mobile Overlay */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onToggle}
            className="fixed inset-0 bg-black/50 z-40 md:hidden"
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <motion.aside
        initial={false}
        animate={{ width: isOpen ? 280 : 0 }}
        transition={{ duration: 0.2, ease: 'easeInOut' }}
        className="fixed left-0 top-0 h-full bg-zinc-950 border-r border-zinc-900 z-50 overflow-hidden"
      >
        <div className="flex flex-col h-full w-[280px]">
          {/* Header */}
          <div className="p-4 border-b border-zinc-900 flex items-center justify-between">
            <button
              onClick={onToggle}
              className="p-2 hover:bg-zinc-900 rounded-lg transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
            <button
              onClick={onNewSession}
              className="p-2 hover:bg-zinc-900 rounded-lg transition-colors"
            >
              <Plus className="w-5 h-5" />
            </button>
          </div>

          {/* Search */}
          <div className="p-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-600" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Buscar conversas..."
                className="w-full bg-zinc-900 border border-zinc-800 rounded-lg pl-10 pr-4 py-2 text-sm outline-none focus:border-indigo-500 transition-colors"
              />
            </div>
          </div>

          {/* Sessions List */}
          <div className="flex-1 overflow-y-auto px-2">
            {groupedSessions.today.length > 0 && (
              <SessionGroup title="Hoje" sessions={groupedSessions.today} activeId={activeSessionId} onSelect={onSelectSession} />
            )}
            {groupedSessions.yesterday.length > 0 && (
              <SessionGroup title="Ontem" sessions={groupedSessions.yesterday} activeId={activeSessionId} onSelect={onSelectSession} />
            )}
            {groupedSessions.older.length > 0 && (
              <SessionGroup title="Mais antigos" sessions={groupedSessions.older} activeId={activeSessionId} onSelect={onSelectSession} />
            )}
          </div>
        </div>
      </motion.aside>
    </>
  );
};

const SessionGroup = ({ title, sessions, activeId, onSelect }) => (
  <div className="mb-4">
    <h3 className="text-xs font-semibold text-zinc-600 px-3 mb-2">{title}</h3>
    {sessions.map(session => (
      <button
        key={session.id}
        onClick={() => onSelect(session.id)}
        className={`w-full text-left px-3 py-2 rounded-lg mb-1 transition-colors ${
          session.id === activeId
            ? 'bg-indigo-600 text-white'
            : 'hover:bg-zinc-900 text-zinc-400'
        }`}
      >
        <div className="flex items-center gap-2">
          <MessageSquare className="w-4 h-4 flex-shrink-0" />
          <span className="text-sm truncate">{session.title || 'Nova conversa'}</span>
        </div>
      </button>
    ))}
  </div>
);

const isToday = (date) => {
  const today = new Date();
  const d = new Date(date);
  return d.toDateString() === today.toDateString();
};

const isYesterday = (date) => {
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  const d = new Date(date);
  return d.toDateString() === yesterday.toDateString();
};

export default Sidebar;
