import { useState, useRef, useEffect } from 'react';
import { Send, Menu, LogOut, Copy, Check, User, RotateCcw, Sparkles, Bug, ArrowLeft, ThumbsUp, ThumbsDown } from 'lucide-react';
import CerberusIcon from './CerberusIcon';
import Sidebar from './Sidebar';

const Chat = ({ token, onLogout, onNavigate }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [debugMode, setDebugMode] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    loadSessions();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    // Focus input on load
    inputRef.current?.focus();
  }, [sessionId]);

  const createSession = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/sessions/', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      setSessionId(data.session_id);
      setMessages([]);
      loadSessions();
    } catch (err) {
      console.error('Erro ao criar sessão:', err);
    }
  };

  const loadSessions = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/sessions/', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      setSessions(data.sessions || []);
    } catch (err) {
      console.error('Erro ao carregar sessões:', err);
    }
  };

  const loadSessionHistory = async (id) => {
    try {
      const response = await fetch(`http://localhost:8000/api/sessions/${id}/history`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      
      // Converte histórico para formato de mensagens
      const msgs = [];
      data.history.forEach(item => {
        msgs.push({ role: 'user', content: item.question.content });
        if (item.answer) {
          msgs.push({ role: 'assistant', content: item.answer.content });
        }
      });
      
      setMessages(msgs);
    } catch (err) {
      console.error('Erro ao carregar histórico:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    // Cria sessão apenas na primeira mensagem
    if (!sessionId) {
      await createSession();
      return; // Aguarda próximo submit após criar sessão
    }

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    const currentInput = input;
    setInput('');
    setLoading(true);

    try {
      const response = await fetch(`http://localhost:8000/api/sessions/${sessionId}/questions`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
          content: currentInput,
          debug_mode: debugMode 
        })
      });

      const data = await response.json();
      
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.content,
        answerId: data.answer_id  // Store answer ID for feedback
      }]);

      // Update session title with first message
      if (messages.length === 0) {
        loadSessions();
      }
    } catch (err) {
      setMessages(prev => [...prev, { 
        role: 'error', 
        content: 'Erro ao processar. Tente novamente.' 
      }]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleSelectSession = async (id) => {
    setSessionId(id);
    setSidebarOpen(false);
    await loadSessionHistory(id);
  };

  return (
    <div className="h-screen bg-black flex overflow-hidden">
      <Sidebar
        isOpen={sidebarOpen}
        onToggle={() => setSidebarOpen(!sidebarOpen)}
        sessions={sessions}
        activeSessionId={sessionId}
        onSelectSession={handleSelectSession}
        onNewSession={createSession}
      />

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <header className="h-14 flex items-center justify-between px-4 border-b border-cerberus-border bg-black shrink-0">
          <div className="flex items-center gap-3">
            <button
              onClick={() => onNavigate?.('dashboard')}
              className="p-2 hover:bg-cerberus-dark rounded-lg transition-colors"
              aria-label="Voltar"
              title="Voltar ao Dashboard"
            >
              <ArrowLeft className="w-5 h-5 text-cerberus-text-secondary" />
            </button>
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 hover:bg-cerberus-dark rounded-lg transition-colors"
              aria-label="Menu"
            >
              <Menu className="w-5 h-5 text-cerberus-text-secondary" />
            </button>
            
            <div className="flex items-center gap-2">
              <CerberusIcon className="w-6 h-6 text-white" />
              <span className="font-semibold text-white tracking-tight">Cerberus AI</span>
              {debugMode && (
                <span className="text-xs px-2 py-0.5 bg-red-500/20 text-red-400 border border-red-500/30 rounded-full font-mono">
                  DEBUG
                </span>
              )}
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setDebugMode(!debugMode)}
              className={`flex items-center gap-2 px-3 py-2 rounded-lg transition-all text-sm relative group ${
                debugMode 
                  ? 'bg-red-500/20 text-red-400 border border-red-500/30 hover:bg-red-500/30 debug-pulse' 
                  : 'text-cerberus-text-secondary hover:text-white hover:bg-cerberus-dark'
              }`}
              title="Ativa análise técnica profunda para debugging e arquitetura"
            >
              <Bug className="w-4 h-4" />
              <span className="hidden sm:inline">Debug</span>
              
              {/* Tooltip */}
              <div className="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 px-3 py-2 bg-cerberus-darker border border-cerberus-border rounded-lg text-xs whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-50">
                <div className="font-medium text-white mb-1">
                  {debugMode ? '✅ Debug Mode Ativo' : '🔧 Ativar Debug Mode'}
                </div>
                <div className="text-cerberus-text-muted text-2xs">
                  Análise profunda + Arquitetura + Otimizações
                </div>
                <div className="absolute top-full left-1/2 -translate-x-1/2 -mt-1 border-4 border-transparent border-t-cerberus-border" />
              </div>
            </button>
            
            <button
              onClick={onLogout}
              className="flex items-center gap-2 text-cerberus-text-secondary hover:text-white px-3 py-2 rounded-lg hover:bg-cerberus-dark transition-colors text-sm"
            >
              <LogOut className="w-4 h-4" />
              <span className="hidden sm:inline">Sair</span>
            </button>
          </div>
        </header>

        {/* Messages Area */}
        <main className="flex-1 overflow-y-auto">
          {messages.length === 0 ? (
            <EmptyState />
          ) : (
            <div className="max-w-3xl mx-auto px-4 py-6">
              <div className="space-y-6">
                {messages.map((msg, idx) => (
                  <Message key={idx} message={msg} token={token} />
                ))}
                {loading && <LoadingMessage />}
                <div ref={messagesEndRef} />
              </div>
            </div>
          )}
        </main>

        {/* Input Area */}
        <div className="shrink-0 border-t border-cerberus-border bg-black">
          <div className="max-w-3xl mx-auto px-4 py-4">
            {debugMode && (
              <div className="mb-3 flex items-center gap-2 px-3 py-2 bg-red-500/10 border border-red-500/20 rounded-lg text-sm text-red-400">
                <Bug className="w-4 h-4" />
                <span className="font-medium">Debug Mode:</span>
                <span className="text-cerberus-text-secondary">Respostas com análise técnica profunda, causas raiz e otimizações</span>
              </div>
            )}
            <form onSubmit={handleSubmit} className="relative">
              <textarea
                ref={inputRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder={debugMode ? "Descreva o erro, código ou arquitetura para análise profunda..." : "Descreva seu problema técnico ou pergunta sobre código..."}
                rows={1}
                className={`w-full bg-cerberus-dark border rounded-xl px-4 py-3 pr-12 outline-none focus:border-cerberus-border-light transition-colors placeholder:text-cerberus-text-muted resize-none text-white ${
                  debugMode ? 'border-red-500/30 focus:border-red-500/50' : 'border-cerberus-border'
                }`}
                style={{ minHeight: '48px', maxHeight: '200px' }}
                disabled={loading}
              />
              <button
                type="submit"
                disabled={loading || !input.trim()}
                className={`absolute right-2 bottom-2 p-2 rounded-lg transition-all ${
                  debugMode 
                    ? 'bg-red-500 text-white hover:bg-red-600' 
                    : 'bg-white text-black hover:bg-gray-200'
                } disabled:opacity-30 disabled:cursor-not-allowed`}
                aria-label="Enviar"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>
            <p className="text-2xs text-cerberus-text-muted text-center mt-2">
              Cerberus AI pode cometer erros. Sempre valide código crítico.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

const EmptyState = () => (
  <div className="h-full flex items-center justify-center">
    <div className="text-center max-w-md px-4 animate-fade-in">
      <CerberusIcon className="w-16 h-16 text-cerberus-text-muted mx-auto mb-6" />
      <h2 className="text-2xl font-semibold text-white mb-2">Cerberus AI</h2>
      <p className="text-cerberus-text-secondary mb-8">
        Mentor técnico inteligente para desenvolvedores. Debug, arquitetura e code assistant.
      </p>
      
      <div className="grid gap-3">
        <SuggestionCard 
          icon={<Sparkles className="w-4 h-4" />}
          text="Como implementar autenticação JWT em FastAPI?"
        />
        <SuggestionCard 
          icon={<Bug className="w-4 h-4" />}
          text="Debug: NullPointerException na linha 42"
        />
        <SuggestionCard 
          icon={<Sparkles className="w-4 h-4" />}
          text="Qual padrão usar: Repository ou Active Record?"
        />
      </div>
    </div>
  </div>
);

const SuggestionCard = ({ icon, text }) => (
  <button className="flex items-center gap-3 w-full p-3 bg-cerberus-dark border border-cerberus-border rounded-xl text-left text-sm text-cerberus-text-secondary hover:text-white hover:border-cerberus-border-light transition-colors">
    <span className="text-cerberus-text-muted">{icon}</span>
    <span>{text}</span>
  </button>
);

const Message = ({ message, token }) => {
  const isUser = message.role === 'user';
  const isError = message.role === 'error';
  const [copied, setCopied] = useState(false);
  const [feedback, setFeedback] = useState(null);

  const handleFeedback = async (rating) => {
    if (!message.answerId) return;
    
    try {
      await fetch('http://localhost:8000/api/feedback/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          answer_id: message.answerId,
          rating: rating
        })
      });
      setFeedback(rating);
    } catch (err) {
      console.error('Erro ao enviar feedback:', err);
    }
  };

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const renderContent = (content) => {
    const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
    const parts = [];
    let lastIndex = 0;
    let match;

    while ((match = codeBlockRegex.exec(content)) !== null) {
      if (match.index > lastIndex) {
        parts.push(
          <span key={`text-${lastIndex}`} className="whitespace-pre-wrap">
            {content.substring(lastIndex, match.index)}
          </span>
        );
      }

      const language = match[1] || 'code';
      const code = match[2].trim();
      parts.push(
        <div key={`code-${match.index}`} className="my-3 rounded-lg overflow-hidden bg-cerberus-darker border border-cerberus-border">
          <div className="flex items-center justify-between px-4 py-2 bg-cerberus-dark border-b border-cerberus-border">
            <span className="text-xs text-cerberus-text-muted font-mono">{language}</span>
            <button
              onClick={() => handleCopy(code)}
              className="flex items-center gap-1.5 text-xs text-cerberus-text-muted hover:text-white transition-colors"
            >
              {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
              {copied ? 'Copiado' : 'Copiar'}
            </button>
          </div>
          <pre className="p-4 overflow-x-auto">
            <code className="code-block text-cerberus-text-secondary">{code}</code>
          </pre>
        </div>
      );

      lastIndex = match.index + match[0].length;
    }

    if (lastIndex < content.length) {
      parts.push(
        <span key={`text-${lastIndex}`} className="whitespace-pre-wrap">
          {content.substring(lastIndex)}
        </span>
      );
    }

    return parts.length > 0 ? parts : <span className="whitespace-pre-wrap">{content}</span>;
  };

  return (
    <div className={`flex gap-4 message-enter ${isUser ? 'justify-end' : ''}`}>
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-cerberus-dark border border-cerberus-border flex items-center justify-center shrink-0">
          <CerberusIcon className="w-5 h-5 text-white" />
        </div>
      )}
      
      <div className={`flex-1 max-w-[85%] ${isUser ? 'flex justify-end' : ''}`}>
        <div className={`inline-block rounded-2xl px-4 py-3 ${
          isUser 
            ? 'bg-white text-black' 
            : isError 
            ? 'bg-red-950/30 border border-red-900/50 text-red-400'
            : 'bg-cerberus-dark border border-cerberus-border text-white'
        }`}>
          <div className="text-[15px] leading-relaxed">
            {renderContent(message.content)}
          </div>
          {!isUser && !isError && message.answerId && (
            <div className="flex items-center gap-2 mt-3 pt-3 border-t border-cerberus-border">
              <span className="text-xs text-cerberus-text-muted">Útil?</span>
              <button
                onClick={() => handleFeedback(5)}
                disabled={feedback !== null}
                className={`p-1 rounded transition-colors ${
                  feedback === 5
                    ? 'text-green-400'
                    : 'text-cerberus-text-muted hover:text-green-400'
                } disabled:cursor-not-allowed`}
              >
                <ThumbsUp className="w-4 h-4" />
              </button>
              <button
                onClick={() => handleFeedback(1)}
                disabled={feedback !== null}
                className={`p-1 rounded transition-colors ${
                  feedback === 1
                    ? 'text-red-400'
                    : 'text-cerberus-text-muted hover:text-red-400'
                } disabled:cursor-not-allowed`}
              >
                <ThumbsDown className="w-4 h-4" />
              </button>
              {feedback && (
                <span className="text-xs text-cerberus-text-muted ml-2">Obrigado!</span>
              )}
            </div>
          )}
        </div>
      </div>

      {isUser && (
        <div className="w-8 h-8 rounded-full bg-cerberus-accent flex items-center justify-center shrink-0">
          <User className="w-4 h-4 text-white" />
        </div>
      )}
    </div>
  );
};

const LoadingMessage = () => (
  <div className="flex gap-4 message-enter">
    <div className="w-8 h-8 rounded-full bg-cerberus-dark border border-cerberus-border flex items-center justify-center shrink-0">
      <CerberusIcon className="w-5 h-5 text-white" />
    </div>
    <div className="bg-cerberus-dark border border-cerberus-border rounded-2xl px-4 py-4">
      <div className="flex gap-1.5">
        <div className="w-2 h-2 bg-cerberus-text-muted rounded-full typing-dot" />
        <div className="w-2 h-2 bg-cerberus-text-muted rounded-full typing-dot" />
        <div className="w-2 h-2 bg-cerberus-text-muted rounded-full typing-dot" />
      </div>
    </div>
  </div>
);

export default Chat;
