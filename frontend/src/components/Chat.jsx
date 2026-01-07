import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Brain, Send, Loader2, User, LogOut, Sparkles, Menu, Copy, Check } from 'lucide-react';
import BackgroundGradient from './BackgroundGradient';
import Sidebar from './Sidebar';

const Chat = ({ token, onLogout }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [tokenCount, setTokenCount] = useState(0);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    createSession();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    // Estimar tokens (aproximado: 1 token ≈ 4 caracteres)
    setTokenCount(Math.ceil(input.length / 4));
  }, [input]);

  const createSession = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/sessions/', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      setSessionId(data.session_id);
      setSessions(prev => [{ id: data.session_id, title: 'Nova conversa', created_at: new Date() }, ...prev]);
    } catch (err) {
      console.error('Erro ao criar sessão:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || !sessionId) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch(`http://localhost:8000/api/sessions/${sessionId}/questions`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ content: input })
      });

      const data = await response.json();
      
      const aiMessage = {
        role: 'assistant',
        content: data.content
      };
      
      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      setMessages(prev => [...prev, { 
        role: 'error', 
        content: 'Erro ao processar pergunta. Tente novamente.' 
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
      handleSubmit(e);
    }
  };

  return (
    <div className="min-h-screen text-white relative flex">
      <BackgroundGradient />
      
      <Sidebar
        isOpen={sidebarOpen}
        onToggle={() => setSidebarOpen(!sidebarOpen)}
        sessions={sessions}
        activeSessionId={sessionId}
        onSelectSession={(id) => setSessionId(id)}
        onNewSession={createSession}
      />

      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="fixed top-0 right-0 left-0 md:left-0 z-40 border-b border-zinc-900 bg-black/80 backdrop-blur-md">
          <div className="max-w-4xl mx-auto px-6 py-4 flex justify-between items-center">
            <div className="flex items-center gap-3">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="p-2 hover:bg-zinc-900 rounded-lg transition-colors"
              >
                <Menu className="w-5 h-5" />
              </button>
              <div className="flex items-center gap-2 font-bold text-lg tracking-tighter">
                <Brain className="w-5 h-5 text-indigo-500" />
                <span>DevChat AI</span>
              </div>
            </div>
            
            <button
              onClick={onLogout}
              className="text-zinc-600 hover:text-white transition-colors flex items-center gap-2 text-sm"
            >
              <LogOut className="w-4 h-4" />
              Sair
            </button>
          </div>
        </header>

        {/* Messages */}
        <main className="flex-1 overflow-y-auto pt-20 pb-32">
          <div className="max-w-3xl mx-auto px-6">
            {messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
                <Sparkles className="w-12 h-12 text-zinc-800 mb-4" />
                <h2 className="text-2xl font-bold mb-2">DevChat AI</h2>
                <p className="text-zinc-600 text-sm">Assistente especializado em programação, debugging e DevOps</p>
              </div>
            ) : (
              <div className="space-y-6 py-8">
                {messages.map((msg, idx) => (
                  <Message key={idx} message={msg} />
                ))}
                {loading && <LoadingMessage />}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>
        </main>

        {/* Input */}
        <div className="fixed bottom-0 right-0 left-0 md:left-0 border-t border-zinc-900 bg-black/80 backdrop-blur-md">
          <div className="max-w-3xl mx-auto px-6 py-4">
            <form onSubmit={handleSubmit} className="relative">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Pergunte sobre código, debugging, arquitetura... (Ctrl+Enter para enviar)"
                className="w-full bg-black border border-zinc-900 rounded-2xl pl-6 pr-32 py-4 outline-none focus:border-indigo-500 transition-colors placeholder-zinc-700"
                disabled={loading}
              />
              <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-2">
                {tokenCount > 0 && (
                  <span className="text-xs text-zinc-600">{tokenCount} tokens</span>
                )}
                <button
                  type="submit"
                  disabled={loading || !input.trim()}
                  className="bg-indigo-600 text-white p-2 rounded-xl hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

const Message = ({ message }) => {
  const isUser = message.role === 'user';
  const isError = message.role === 'error';
  const [copied, setCopied] = useState(false);

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Detectar blocos de código
  const renderContent = (content) => {
    const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
    const parts = [];
    let lastIndex = 0;
    let match;

    while ((match = codeBlockRegex.exec(content)) !== null) {
      // Texto antes do bloco de código
      if (match.index > lastIndex) {
        parts.push(
          <p key={`text-${lastIndex}`} className="whitespace-pre-wrap">
            {content.substring(lastIndex, match.index)}
          </p>
        );
      }

      // Bloco de código
      const language = match[1] || 'text';
      const code = match[2];
      parts.push(
        <div key={`code-${match.index}`} className="my-4 rounded-lg overflow-hidden bg-zinc-900">
          <div className="flex items-center justify-between px-4 py-2 bg-zinc-800 border-b border-zinc-700">
            <span className="text-xs text-zinc-400">{language}</span>
            <button
              onClick={() => handleCopy(code)}
              className="text-xs text-zinc-400 hover:text-white transition-colors flex items-center gap-1"
            >
              {copied ? <Check className="w-3 h-3" /> : <Copy className="w-3 h-3" />}
              {copied ? 'Copiado!' : 'Copiar'}
            </button>
          </div>
          <pre className="p-4 overflow-x-auto">
            <code className="text-sm">{code}</code>
          </pre>
        </div>
      );

      lastIndex = match.index + match[0].length;
    }

    // Texto restante
    if (lastIndex < content.length) {
      parts.push(
        <p key={`text-${lastIndex}`} className="whitespace-pre-wrap">
          {content.substring(lastIndex)}
        </p>
      );
    }

    return parts.length > 0 ? parts : <p className="whitespace-pre-wrap">{content}</p>;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex gap-4 ${isUser ? 'justify-end' : ''}`}
    >
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-zinc-900 flex items-center justify-center flex-shrink-0">
          <Brain className="w-4 h-4" />
        </div>
      )}
      
      <div className={`flex-1 max-w-2xl ${isUser ? 'text-right' : ''}`}>
        <div className={`inline-block rounded-2xl px-4 py-3 ${
          isUser 
            ? 'bg-indigo-600 text-white' 
            : isError 
            ? 'bg-red-950/50 border border-red-900 text-red-400'
            : 'bg-zinc-950 border border-zinc-900'
        }`}>
          <div className="text-sm leading-relaxed">{renderContent(message.content)}</div>
        </div>
      </div>

      {isUser && (
        <div className="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center flex-shrink-0">
          <User className="w-4 h-4 text-white" />
        </div>
      )}
    </motion.div>
  );
};

const LoadingMessage = () => (
  <div className="flex gap-4">
    <div className="w-8 h-8 rounded-full bg-zinc-950 border border-zinc-900 flex items-center justify-center flex-shrink-0">
      <Brain className="w-4 h-4" />
    </div>
    <div className="bg-zinc-950 border border-zinc-900 rounded-2xl px-4 py-3">
      <div className="flex gap-1">
        <div className="w-2 h-2 bg-zinc-700 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
        <div className="w-2 h-2 bg-zinc-700 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
        <div className="w-2 h-2 bg-zinc-700 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
      </div>
    </div>
  </div>
);

export default Chat;
