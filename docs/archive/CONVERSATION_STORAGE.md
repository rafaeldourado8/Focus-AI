# 💾 Sistema de Armazenamento de Conversas

## ✅ Já Implementado

O sistema **JÁ ARMAZENA** todas as conversas no PostgreSQL automaticamente!

### Estrutura do Banco de Dados

```sql
-- Usuários
users
├── id (PK)
├── email
├── password_hash
├── career_stage
├── is_active
└── created_at

-- Sessões de Conversa
learning_sessions
├── id (PK)
├── user_id (FK → users.id)
├── status (active/processing/completed)
├── created_at
└── updated_at

-- Perguntas do Usuário
questions
├── id (PK)
├── session_id (FK → learning_sessions.id)
├── content (texto da pergunta)
└── created_at

-- Respostas da IA
answers
├── id (PK)
├── question_id (FK → questions.id)
├── content (texto da resposta)
├── explanation
├── edge_cases
└── created_at
```

### Índices de Performance

```sql
-- Otimizações para queries rápidas
CREATE INDEX idx_questions_session_created ON questions(session_id, created_at);
CREATE INDEX idx_answers_question ON answers(question_id);
CREATE INDEX idx_sessions_user_created ON learning_sessions(user_id, created_at);
```

## 🔄 Fluxo de Armazenamento

### 1. Usuário Envia Pergunta

```javascript
// Frontend
POST /api/sessions/{session_id}/questions
{
  "content": "Como fazer um loop em Python?",
  "debug_mode": false
}
```

### 2. Backend Processa e Salva

```python
# 1. Salva a pergunta
question = Question(session_id=session_id, content=content)
created_question = question_repo.create(question)

# 2. Gera resposta da IA
llm_response = llm_service.generate_answer(content, debug_mode)

# 3. Salva a resposta
answer = Answer(
    question_id=created_question.id,
    content=llm_response["content"],
    explanation="",
    edge_cases=""
)
created_answer = answer_repo.create(answer)
```

### 3. Tudo Fica Salvo no PostgreSQL

```
✅ Pergunta armazenada
✅ Resposta armazenada
✅ Timestamp registrado
✅ Vinculado ao usuário
✅ Vinculado à sessão
```

## 📡 APIs Disponíveis

### 1. Listar Sessões do Usuário

```bash
GET /api/sessions/
Authorization: Bearer {token}

Response:
{
  "sessions": [
    {
      "id": "abc123",
      "title": "Como fazer um loop em Python?...",
      "status": "active",
      "created_at": "2024-01-15T10:30:00Z",
      "message_count": 5
    },
    {
      "id": "def456",
      "title": "Debug TypeError...",
      "status": "active",
      "created_at": "2024-01-15T09:15:00Z",
      "message_count": 3
    }
  ]
}
```

### 2. Buscar Histórico de uma Sessão

```bash
GET /api/sessions/{session_id}/history
Authorization: Bearer {token}

Response:
{
  "session_id": "abc123",
  "history": [
    {
      "question": {
        "id": "q1",
        "content": "Como fazer um loop em Python?",
        "created_at": "2024-01-15T10:30:00Z"
      },
      "answer": {
        "id": "a1",
        "content": "Usa `for`:\n\n```python\nfor i in range(10):\n    print(i)\n```",
        "created_at": "2024-01-15T10:30:02Z"
      }
    },
    {
      "question": {
        "id": "q2",
        "content": "E com lista?",
        "created_at": "2024-01-15T10:31:00Z"
      },
      "answer": {
        "id": "a2",
        "content": "```python\nitems = ['a', 'b', 'c']\nfor item in items:\n    print(item)\n```",
        "created_at": "2024-01-15T10:31:01Z"
      }
    }
  ]
}
```

### 3. Criar Nova Sessão

```bash
POST /api/sessions/
Authorization: Bearer {token}

Response:
{
  "session_id": "xyz789",
  "status": "active"
}
```

## 🎨 Frontend - Carregamento de Histórico

### Ao Selecionar Sessão

```javascript
const handleSelectSession = async (id) => {
  setSessionId(id);
  setSidebarOpen(false);
  
  // Carrega histórico do banco
  await loadSessionHistory(id);
};

const loadSessionHistory = async (id) => {
  const response = await fetch(
    `http://localhost:8000/api/sessions/${id}/history`,
    { headers: { 'Authorization': `Bearer ${token}` } }
  );
  
  const data = await response.json();
  
  // Converte para formato de mensagens
  const msgs = [];
  data.history.forEach(item => {
    msgs.push({ role: 'user', content: item.question.content });
    if (item.answer) {
      msgs.push({ role: 'assistant', content: item.answer.content });
    }
  });
  
  setMessages(msgs);
};
```

### Ao Carregar App

```javascript
useEffect(() => {
  createSession();      // Cria nova sessão
  loadSessions();       // Carrega lista de sessões antigas
}, []);

const loadSessions = async () => {
  const response = await fetch('http://localhost:8000/api/sessions/', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  const data = await response.json();
  setSessions(data.sessions || []);
};
```

## 🔍 Queries SQL Executadas

### Buscar Sessões do Usuário

```sql
SELECT 
  ls.id,
  ls.status,
  ls.created_at,
  ls.updated_at,
  COUNT(q.id) as message_count,
  (SELECT content FROM questions WHERE session_id = ls.id ORDER BY created_at LIMIT 1) as first_question
FROM learning_sessions ls
LEFT JOIN questions q ON q.session_id = ls.id
WHERE ls.user_id = 'user123'
GROUP BY ls.id
ORDER BY ls.created_at DESC;
```

### Buscar Histórico de uma Sessão

```sql
SELECT 
  q.id as question_id,
  q.content as question_content,
  q.created_at as question_created_at,
  a.id as answer_id,
  a.content as answer_content,
  a.created_at as answer_created_at
FROM questions q
LEFT JOIN answers a ON a.question_id = q.id
WHERE q.session_id = 'abc123'
ORDER BY q.created_at ASC;
```

## 📊 Dados Armazenados

### Por Usuário

```
user@example.com
├── Sessão 1 (15/01/2024 10:30)
│   ├── Pergunta: "Como fazer loop?"
│   ├── Resposta: "Usa for..."
│   ├── Pergunta: "E com lista?"
│   └── Resposta: "items = [...]"
│
├── Sessão 2 (15/01/2024 09:15)
│   ├── Pergunta: "Debug TypeError"
│   └── Resposta: "TypeError significa..."
│
└── Sessão 3 (14/01/2024 16:45)
    ├── Pergunta: "React hooks"
    └── Resposta: "useState..."
```

### Estatísticas

```sql
-- Total de conversas por usuário
SELECT 
  u.email,
  COUNT(DISTINCT ls.id) as total_sessions,
  COUNT(q.id) as total_questions
FROM users u
LEFT JOIN learning_sessions ls ON ls.user_id = u.id
LEFT JOIN questions q ON q.session_id = ls.id
GROUP BY u.id;

-- Conversas mais recentes
SELECT 
  ls.id,
  ls.created_at,
  COUNT(q.id) as messages
FROM learning_sessions ls
LEFT JOIN questions q ON q.session_id = ls.id
WHERE ls.user_id = 'user123'
GROUP BY ls.id
ORDER BY ls.created_at DESC
LIMIT 10;
```

## 🚀 Funcionalidades Implementadas

### ✅ Armazenamento Automático
- [x] Toda pergunta é salva
- [x] Toda resposta é salva
- [x] Timestamp registrado
- [x] Vinculado ao usuário
- [x] Vinculado à sessão

### ✅ Recuperação de Histórico
- [x] Listar todas as sessões do usuário
- [x] Carregar histórico completo de uma sessão
- [x] Ordenação cronológica
- [x] Contagem de mensagens

### ✅ Performance
- [x] Índices otimizados
- [x] Queries eficientes
- [x] Cache no Redis (respostas duplicadas)
- [x] Paginação (futuro)

### ✅ Segurança
- [x] Autenticação JWT
- [x] Validação de ownership
- [x] Isolamento por usuário
- [x] Sanitização de inputs

## 🔧 Comandos Úteis

### Verificar Dados no Banco

```bash
# Entrar no container do PostgreSQL
docker-compose exec postgres psql -U focus -d focusai

# Ver todas as sessões
SELECT * FROM learning_sessions;

# Ver perguntas de uma sessão
SELECT * FROM questions WHERE session_id = 'abc123';

# Ver respostas
SELECT * FROM answers WHERE question_id = 'q123';

# Histórico completo de um usuário
SELECT 
  ls.id as session_id,
  q.content as question,
  a.content as answer,
  q.created_at
FROM learning_sessions ls
JOIN questions q ON q.session_id = ls.id
LEFT JOIN answers a ON a.question_id = q.id
WHERE ls.user_id = 'user123'
ORDER BY q.created_at DESC;
```

### Rodar Migrations

```bash
# Aplicar migrations
docker-compose exec backend alembic upgrade head

# Ver histórico de migrations
docker-compose exec backend alembic history

# Criar nova migration
docker-compose exec backend alembic revision -m "description"
```

### Backup do Banco

```bash
# Backup completo
docker-compose exec postgres pg_dump -U focus focusai > backup.sql

# Restaurar backup
docker-compose exec -T postgres psql -U focus focusai < backup.sql
```

## 📈 Próximas Melhorias

### Curto Prazo
- [ ] Paginação de histórico (carregar 50 mensagens por vez)
- [ ] Busca em conversas antigas
- [ ] Exportar conversas em Markdown
- [ ] Deletar sessões antigas

### Médio Prazo
- [ ] Tags/categorias para sessões
- [ ] Favoritar conversas importantes
- [ ] Compartilhar conversas (link público)
- [ ] Estatísticas de uso

### Longo Prazo
- [ ] Backup automático
- [ ] Sincronização multi-device
- [ ] Análise de sentimento
- [ ] Recomendações baseadas em histórico

## 🎯 Conclusão

✅ **Sistema de armazenamento COMPLETO e FUNCIONAL!**

Todas as conversas são:
- ✅ Salvas automaticamente no PostgreSQL
- ✅ Vinculadas ao usuário correto
- ✅ Recuperáveis a qualquer momento
- ✅ Organizadas por sessão
- ✅ Ordenadas cronologicamente
- ✅ Protegidas por autenticação

**Nada se perde! Tudo fica salvo! 💾**

---

**Desenvolvido com ❤️ pela equipe Focus AI**
