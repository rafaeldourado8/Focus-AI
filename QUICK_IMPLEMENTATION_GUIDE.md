# 🚀 Guia Rápido - Implementação das Correções

## ✅ Já Implementado (Pronto para Usar)

1. **401 Interceptor** - Logout automático em token expirado
2. **Token Validation** - Valida token antes de renderizar
3. **Session Persistence** - Chat mantido após F5
4. **Auto-scroll Inteligente** - Scroll que respeita o usuário
5. **Loading Screen** - Sem flash branco
6. **Empty States** - Dashboard encorajador
7. **Production Security** - Console.log e sourcemaps removidos

## 🔧 Implementações Rápidas (5-10 min cada)

### 1. Stop Generation Button

**Arquivo:** `frontend/src/components/Chat.jsx`

```jsx
// No topo, adicionar import:
import StopButton from './StopButton';

// Adicionar state para controlar abort:
const [abortController, setAbortController] = useState(null);

// No handleSubmit, antes do fetch:
const controller = new AbortController();
setAbortController(controller);

// Modificar o fetch:
const response = await fetch(`http://localhost:8000/api/sessions/${sessionId}/questions`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ 
    content: currentInput,
    debug_mode: debugMode 
  }),
  signal: controller.signal  // ← ADICIONAR
});

// No JSX, antes de LoadingMessage:
{loading && (
  <StopButton 
    onStop={() => {
      abortController?.abort();
      setLoading(false);
    }} 
    loading={loading} 
  />
)}
```

### 2. Retry/Regenerate Button

**Arquivo:** `frontend/src/components/Chat.jsx`

```jsx
// Na Message component, adicionar:
const handleRegenerate = () => {
  // Remove última resposta da IA
  setMessages(prev => prev.slice(0, -1));
  // Reenvia última pergunta
  const lastUserMessage = messages[messages.length - 2];
  setInput(lastUserMessage.content);
  // Trigger submit
  setTimeout(() => handleSubmit(new Event('submit')), 100);
};

// No JSX da Message (só para IA):
{!isUser && !isError && (
  <button
    onClick={handleRegenerate}
    className="flex items-center gap-1 text-xs text-cerberus-text-muted hover:text-white mt-2"
  >
    <RotateCcw className="w-3 h-3" />
    Regenerar
  </button>
)}
```

### 3. Edit Last Message

**Arquivo:** `frontend/src/components/Chat.jsx`

```jsx
// Adicionar states:
const [editingIndex, setEditingIndex] = useState(null);
const [editContent, setEditContent] = useState('');

// Função de edição:
const handleEdit = (index) => {
  setEditingIndex(index);
  setEditContent(messages[index].content);
};

const handleSaveEdit = () => {
  const newMessages = [...messages];
  newMessages[editingIndex].content = editContent;
  setMessages(newMessages);
  setEditingIndex(null);
};

// Na Message component, adicionar botão de editar:
{isUser && idx === messages.length - 1 && (
  <button
    onClick={() => handleEdit(idx)}
    className="text-xs text-cerberus-text-muted hover:text-white"
  >
    Editar
  </button>
)}

// Renderizar input de edição se editingIndex === idx
{editingIndex === idx ? (
  <textarea
    value={editContent}
    onChange={(e) => setEditContent(e.target.value)}
    className="w-full bg-cerberus-darker border border-cerberus-border rounded p-2"
  />
) : (
  renderContent(message.content)
)}
```

### 4. Sanitização HTML (Segurança)

**Terminal:**
```bash
cd frontend
npm install dompurify
```

**Arquivo:** `frontend/src/components/Chat.jsx`

```jsx
// No topo:
import DOMPurify from 'dompurify';

// Na função renderContent, antes de retornar:
const sanitize = (html) => {
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['code', 'pre', 'span', 'div', 'br'],
    ALLOWED_ATTR: ['class']
  });
};

// Usar em vez de dangerouslySetInnerHTML (se houver)
```

### 5. Virtualização (Performance)

**Terminal:**
```bash
cd frontend
npm install react-window
```

**Arquivo:** `frontend/src/components/Chat.jsx`

```jsx
// Só implementar se chat tiver >50 mensagens
import { FixedSizeList } from 'react-window';

// Substituir map por:
<FixedSizeList
  height={600}
  itemCount={messages.length}
  itemSize={100}
  width="100%"
>
  {({ index, style }) => (
    <div style={style}>
      <Message message={messages[index]} token={token} />
    </div>
  )}
</FixedSizeList>
```

## 📄 Páginas Legais (Obrigatório para Google OAuth)

### Criar: `frontend/src/pages/Terms.jsx`

```jsx
const Terms = () => (
  <div className="min-h-screen bg-black text-white p-8">
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Termos de Serviço</h1>
      <p className="text-cerberus-text-secondary mb-4">
        Última atualização: {new Date().toLocaleDateString()}
      </p>
      {/* Adicionar conteúdo legal */}
    </div>
  </div>
);

export default Terms;
```

### Criar: `frontend/src/pages/Privacy.jsx`

```jsx
const Privacy = () => (
  <div className="min-h-screen bg-black text-white p-8">
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Política de Privacidade</h1>
      <p className="text-cerberus-text-secondary mb-4">
        Última atualização: {new Date().toLocaleDateString()}
      </p>
      {/* Adicionar conteúdo legal */}
    </div>
  </div>
);

export default Privacy;
```

### Atualizar: `frontend/src/App.jsx`

```jsx
import Terms from './pages/Terms';
import Privacy from './pages/Privacy';

// Adicionar rotas (se usar React Router)
// Ou adicionar no currentPage state
```

## 🔐 Google OAuth - Atualização Manual

1. Acessar: https://console.cloud.google.com
2. Selecionar projeto
3. Menu: "APIs & Services" > "Credentials"
4. Clicar no OAuth 2.0 Client ID
5. Atualizar:
   - **Nome:** Cerberus AI
   - **Authorized JavaScript origins:**
     - http://localhost:5173
     - https://seu-dominio.com
   - **Authorized redirect URIs:**
     - http://localhost:5173
     - https://seu-dominio.com
6. Salvar
7. Atualizar `.env`:
   ```
   VITE_GOOGLE_CLIENT_ID=seu_novo_client_id
   ```

## 🧪 Testes Manuais

### Checklist de Testes:

- [ ] Login com token inválido → Deve fazer logout
- [ ] F5 durante chat → Deve recuperar sessão
- [ ] Scroll manual durante resposta → Não deve forçar scroll
- [ ] Dashboard vazio → Deve mostrar mensagem encorajadora
- [ ] Abrir em aba anônima → Não deve ter flash branco
- [ ] Clicar "Enviar" múltiplas vezes → Botão deve desabilitar
- [ ] Abrir DevTools Console → Não deve ter logs (em produção)

## 📦 Build de Produção

```bash
cd frontend
npm run build

# Verificar:
# 1. Sem console.log no bundle
# 2. Sem sourcemaps (.map files)
# 3. Bundle size otimizado
```

## 🚀 Deploy

```bash
# Vercel (recomendado)
npm install -g vercel
vercel --prod

# Ou Netlify
npm install -g netlify-cli
netlify deploy --prod
```

## ⚡ Performance Tips

1. **Lazy Loading de Componentes:**
```jsx
const Dashboard = lazy(() => import('./components/Dashboard'));
const Chat = lazy(() => import('./components/Chat'));
```

2. **Memoização:**
```jsx
const Message = memo(({ message, token }) => {
  // ...
});
```

3. **Debounce no Input:**
```jsx
import { useDebouncedCallback } from 'use-debounce';

const debouncedSetInput = useDebouncedCallback(
  (value) => setInput(value),
  300
);
```

## 📊 Monitoramento

Adicionar analytics (opcional):

```bash
npm install @vercel/analytics
```

```jsx
// Em App.jsx
import { Analytics } from '@vercel/analytics/react';

<Analytics />
```

---

**Tempo estimado total:** 1-2 horas
**Prioridade:** Alta (bugs críticos já corrigidos)
**Impacto:** Médio-Alto (melhorias de UX)

---

*Cerberus AI - Developer Assistant*
