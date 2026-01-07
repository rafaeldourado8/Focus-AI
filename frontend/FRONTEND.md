# Frontend Focus AI - Completo

## ✅ Implementado

### Páginas

#### 1. Login (`components/Login.jsx`)
- Design minimalista dark mode
- Toggle entre Login/Registro
- Inputs com ícones (Mail, Lock)
- Integração com backend `/api/auth/login` e `/api/auth/register`
- Armazena token no localStorage
- Tratamento de erros

#### 2. Chat (`components/Chat.jsx`)
- Interface estilo ChatGPT/Gemini
- Header fixo com logo e botão de logout
- Área de mensagens com scroll automático
- Mensagens do usuário (direita, fundo branco)
- Mensagens da IA (esquerda, fundo zinc-900)
- Exibe: content, explanation, edge_cases
- Input fixo no bottom com botão de envio
- Loading animation (3 dots bounce)
- Estado vazio com ícone Sparkles

### Componentes

#### BackgroundGradient.jsx
- Grid sutil de fundo
- Spotlight cinza seguindo mouse
- Vinheta nos cantos
- Blur suave

### Fluxo de Autenticação

```
App.jsx
  ├─ Verifica token no localStorage
  ├─ Se não tem token → Login
  └─ Se tem token → Chat
```

### Integração Backend

#### Login/Registro
```javascript
POST /api/auth/login
POST /api/auth/register
Body: { email, password }
Response: { access_token }
```

#### Chat
```javascript
// 1. Criar sessão
POST /api/sessions/
Headers: { Authorization: Bearer <token> }
Response: { session_id }

// 2. Enviar pergunta
POST /api/sessions/{session_id}/questions
Headers: { Authorization: Bearer <token> }
Body: { content: "pergunta" }
Response: { content, explanation, edge_cases }
```

## Design System

### Cores
- Background: `#000000` (preto absoluto)
- Cards: `bg-zinc-950/50` + `border-zinc-800`
- Inputs: `bg-black` + `border-zinc-800`
- Hover: `border-zinc-600`
- User message: `bg-white text-black`
- AI message: `bg-zinc-900/50 border-zinc-800`

### Tipografia
- Font: Inter
- Títulos: `font-bold tracking-tighter`
- Corpo: `text-sm leading-relaxed`

### Animações
- Framer Motion: `initial={{ opacity: 0, y: 10 }}`
- Loading dots: `animate-bounce` com delays
- Transitions: `transition-colors duration-300`

### Layout

#### Login
- Centralizado vertical e horizontal
- Card: `max-w-md` + `rounded-2xl`
- Inputs: `rounded-lg`
- Button: `rounded-lg` full width

#### Chat
- Header: Fixed top, backdrop-blur
- Messages: `max-w-3xl` centralizado
- Input: Fixed bottom, backdrop-blur
- Scroll: Auto com ref para última mensagem

## Estrutura de Arquivos

```
frontend/
├── src/
│   ├── components/
│   │   ├── BackgroundGradient.jsx  ✅
│   │   ├── Login.jsx               ✅ NEW
│   │   └── Chat.jsx                ✅ NEW
│   ├── App.jsx                      ✅ (router)
│   ├── index.css                    ✅
│   └── main.jsx                     ✅
├── Dockerfile                       ✅ NEW
├── package.json                     ✅
└── tailwind.config.js               ✅
```

## Como Rodar

### Desenvolvimento Local
```bash
cd frontend
npm install
npm run dev
```

### Docker Compose (Full Stack)
```bash
docker-compose up --build
```

Acesse:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000

## Features

### ✅ Implementadas
- [x] Login/Registro com validação
- [x] Autenticação JWT
- [x] Interface chat estilo ChatGPT
- [x] Mensagens estruturadas (content, explanation, edge_cases)
- [x] Loading states
- [x] Scroll automático
- [x] Logout
- [x] Design dark minimalista
- [x] Gradiente spotlight
- [x] Responsive

### 🔜 Próximas
- [ ] Histórico de sessões
- [ ] Editar/deletar mensagens
- [ ] Markdown rendering
- [ ] Code syntax highlight
- [ ] Streaming de respostas
- [ ] Temas customizáveis

## Exemplo de Uso

1. **Registro**: Email + senha → Cria conta
2. **Login**: Email + senha → Recebe token
3. **Chat**: 
   - Sistema cria sessão automaticamente
   - Usuário faz pergunta
   - IA responde com estrutura socrática
   - Scroll automático para última mensagem

## Estilo Visual

### Login
```
┌─────────────────────────┐
│      🧠 Focus AI        │
│   Entre para continuar  │
│                         │
│  ┌─────────────────┐   │
│  │ 📧 Email        │   │
│  └─────────────────┘   │
│  ┌─────────────────┐   │
│  │ 🔒 Senha        │   │
│  └─────────────────┘   │
│                         │
│  ┌─────────────────┐   │
│  │     Entrar      │   │
│  └─────────────────┘   │
│                         │
│  Não tem conta? Criar   │
└─────────────────────────┘
```

### Chat
```
┌─────────────────────────────────┐
│ 🧠 Focus AI          Sair       │ ← Header fixo
├─────────────────────────────────┤
│                                 │
│  🧠  [Resposta da IA]          │
│      ├─ Content                │
│      ├─ Explanation            │
│      └─ Edge Cases             │
│                                 │
│              [Pergunta] 👤      │
│                                 │
│  🧠  [Resposta da IA]          │
│                                 │
├─────────────────────────────────┤
│ [Digite sua pergunta...] [📤]  │ ← Input fixo
└─────────────────────────────────┘
```

## Performance

- Lazy loading de mensagens
- Scroll otimizado com useRef
- Debounce no input (opcional)
- Cache de token no localStorage
- Animações com GPU acceleration

## Segurança

- Token JWT armazenado no localStorage
- Headers Authorization em todas requests
- Logout limpa token
- Validação de inputs
- CORS configurado no backend
