import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Brain, Send, Loader2, User, LogOut, Sparkles } from 'lucide-react';
import BackgroundGradient from './BackgroundGradient';

const Chat = ({ token, onLogout }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    createSession();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const createSession = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/sessions/', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      setSessionId(data.session_id);
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
        content: data.content,
        explanation: data.explanation,
        edge_cases: data.edge_cases
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

  return (
    <div className="min-h-screen text-white relative flex flex-col">
      <BackgroundGradient />
      
      {/* Header */}
      <header className="fixed top-0 w-full z-50 border-b border-zinc-900 bg-black/80 backdrop-blur-md">
        <div className="max-w-4xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2 font-bold text-lg tracking-tighter">
            <Brain className="w-5 h-5 text-indigo-500" />
            <span>Focus AI</span>
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
              <h2 className="text-2xl font-bold mb-2">Como posso ajudar?</h2>
              <p className="text-zinc-600 text-sm">Faça uma pergunta sobre tecnologia</p>
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
      <div className="fixed bottom-0 w-full border-t border-zinc-900 bg-black/80 backdrop-blur-md">
        <div className="max-w-3xl mx-auto px-6 py-4">
          <form onSubmit={handleSubmit} className="relative">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Faça sua pergunta..."
              className="w-full bg-black border border-zinc-900 rounded-2xl pl-6 pr-12 py-4 outline-none focus:border-indigo-500 transition-colors placeholder-zinc-700"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="absolute right-2 top-1/2 -translate-y-1/2 bg-indigo-600 text-white p-2 rounded-xl hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

const Message = ({ message }) => {
  const isUser = message.role === 'user';
  const isError = message.role === 'error';

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
          <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
          
          {message.explanation && (
            <div className="mt-4 pt-4 border-t border-zinc-900">
              <p className="text-xs text-zinc-600 mb-2 font-semibold">EXPLICAÇÃO</p>
              <p className="text-sm text-zinc-400 leading-relaxed">{message.explanation}</p>
            </div>
          )}
          
          {message.edge_cases && (
            <div className="mt-4 pt-4 border-t border-zinc-900">
              <p className="text-xs text-zinc-600 mb-2 font-semibold">EDGE CASES</p>
              <p className="text-sm text-zinc-400 leading-relaxed">{message.edge_cases}</p>
            </div>
          )}
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
