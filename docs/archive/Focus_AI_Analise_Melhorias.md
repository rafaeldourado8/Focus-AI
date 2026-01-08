# FOCUS AI
## Análise de Funcionalidades e Melhorias

**Documento de Especificação Técnica**  
*Janeiro 2026*

---

## 1. Resumo Executivo

O Focus AI é uma aplicação de chat LLM voltada para programadores, atualmente em desenvolvimento. Esta análise identifica funcionalidades ausentes e propõe melhorias para tornar a ferramenta mais competitiva e útil para desenvolvedores.

> ⚠️ **Problema identificado:** O container Ollama está falhando ao iniciar, impedindo o funcionamento completo da aplicação. Além disso, funcionalidades essenciais para um chat LLM profissional estão ausentes.

---

## 2. Estado Atual da Aplicação

### ✓ Funcionalidades Existentes

- Interface de chat básica com design dark mode
- Integração com backend FastAPI
- Container Docker para Ollama (com erro)
- Container PostgreSQL para persistência
- Container Redis para cache
- Frontend em localhost:5173 (Vite/React)
- Exibição de blocos de código com formatação básica

### ✗ Funcionalidades Ausentes Críticas

- Sidebar de histórico de conversas
- Indicador de janela de contexto
- Visualização de tokenização
- Sistema de projetos/workspaces
- Configurações de modelo

---

## 3. Melhorias Detalhadas

### 📁 3.1 Sidebar de Histórico de Conversas

A sidebar é essencial para navegação entre conversas e organização do trabalho do desenvolvedor.

#### Requisitos Funcionais

- Sidebar retrátil (toggle com ícone ou atalho `Ctrl+B`)
- Lista de conversas com título, preview e timestamp
- Campo de busca com filtro em tempo real
- Agrupamento por: Hoje, Ontem, Últimos 7 dias, Mais antigos
- Opção de criar pastas/projetos para organização
- Drag and drop para reorganizar conversas
- Menu de contexto: Renomear, Excluir, Mover, Exportar
- Indicador visual de conversa ativa

#### Especificação de UI

| Elemento | Especificação |
|----------|---------------|
| Largura | 280px expandida, 60px colapsada (apenas ícones) |
| Animação | Transição suave de 200ms ease-in-out |
| Persistência | Estado salvo em localStorage |
| Responsivo | Overlay em telas < 768px |

#### Wireframe Sugerido

```
┌─────┬────────────────────────────────────────────┐
│  ≡  │  Focus AI                            ⚙️   │
├─────┼────────────────────────────────────────────┤
│     │                                            │
│ 🔍  │                                            │
│     │                                            │
│ ──  │         [Área de chat principal]          │
│ 📄  │                                            │
│ 📄  │                                            │
│ 📄  │                                            │
│ 📄  │                                            │
│     │                                            │
│ ◀▶  │────────────────────────────────────────────│
└─────┴────────────────────────────────────────────┘
```

---

### 📊 3.2 Indicador de Janela de Contexto

Programadores precisam visualizar o consumo de tokens para otimizar prompts e evitar truncamentos.

#### Requisitos Funcionais

- Barra de progresso visual mostrando tokens usados/disponíveis
- Porcentagem e valores absolutos (ex: `3.2k / 4k - 80%`)
- Cores indicativas:
  - 🟢 Verde: < 50%
  - 🟡 Amarelo: 50-80%
  - 🔴 Vermelho: > 80%
- Alerta quando atingir 90% do limite
- Botão para "resumir/comprimir conversa"
- Tooltip com breakdown: sistema, histórico, última mensagem

#### Localização Sugerida

Posicionar no canto superior direito da área de chat ou como footer fixo abaixo do input.

```
┌──────────────────────────────────────────────────┐
│  [████████████░░░░] 3.2k / 4k tokens (80%)  ⚠️  │
└──────────────────────────────────────────────────┘
```

#### Limites por Modelo

| Modelo | Limite de Contexto |
|--------|-------------------|
| Llama 3.2 (3B) | 8,192 tokens |
| Llama 3.1 (8B) | 128,000 tokens |
| CodeLlama | 16,384 tokens |
| Mistral | 32,768 tokens |

---

### 🔤 3.3 Sistema de Tokenização

Visualizar como o texto é tokenizado ajuda desenvolvedores a entender o comportamento do modelo e otimizar prompts.

#### Requisitos Funcionais

- Contador de tokens em tempo real no campo de input
- Modo de visualização de tokens (opcional, toggle)
- Highlight de tokens individuais com cores alternadas
- Estimativa de tokens antes de enviar
- Histórico de tokens por mensagem

#### Implementação Técnica

- Usar `tiktoken` (OpenAI) ou tokenizer do Hugging Face
- Cache de tokenização para performance
- Debounce de 300ms no input para evitar excesso de cálculos
- Web Worker para não bloquear UI

#### Exemplo Visual

```
Input: "Como fazer um loop em Python?"

Tokens: [Como] [fazer] [um] [loop] [em] [Python] [?]
         1      2       3     4     5      6      7

Total: 7 tokens
```

---

## 4. Melhorias de Frontend

### 🎨 4.1 Interface e Experiência do Usuário

#### Melhorias Essenciais

- Syntax highlighting completo (Prism.js ou Highlight.js)
- Botão "Copiar código" em cada bloco de código
- Seletor de linguagem nos blocos de código
- Toggle dark/light mode
- Indicador de "digitando..." quando modelo processa
- Streaming de resposta (token por token)
- Markdown rendering completo (tabelas, listas, etc)

#### Melhorias Avançadas

- Diff viewer para comparar versões de código
- Terminal integrado para testar comandos
- Upload de arquivos para contexto
- Preview de Markdown no input
- Menções a arquivos (`@arquivo.py`)
- Snippets salvos/favoritos
- Exportar conversa (MD, PDF, JSON)

---

### ⌨️ 4.2 Atalhos de Teclado

| Atalho | Ação |
|--------|------|
| `Ctrl + Enter` | Enviar mensagem |
| `Ctrl + B` | Toggle sidebar |
| `Ctrl + N` | Nova conversa |
| `Ctrl + K` | Busca rápida |
| `Ctrl + /` | Mostrar atalhos |
| `Esc` | Cancelar geração |
| `↑` (no input vazio) | Editar última mensagem |
| `Ctrl + Shift + C` | Copiar último código |

---

### 📱 4.3 Responsividade

- Layout adaptativo para tablets (768px - 1024px)
- Versão mobile com sidebar em overlay
- Touch gestures: swipe para abrir sidebar
- Teclado virtual não sobrepondo input

---

## 5. Funcionalidades Específicas para Programadores

### 💻 5.1 Integração com Código

- Detecção automática de linguagem em blocos de código
- Formatação automática (Prettier integration)
- Lint warnings inline
- Execução de código sandboxed (Python, JS)
- Integração com GitHub Gist para compartilhar

### 🔧 5.2 Ferramentas de Debug

- Modo verbose para ver raw API calls
- Log de requisições/respostas
- Métricas de latência
- Replay de conversas para debug

### 📝 5.3 Templates e Prompts

- Biblioteca de prompts para tarefas comuns:
  - "Explique este código"
  - "Encontre bugs"
  - "Otimize performance"
  - "Escreva testes"
  - "Documente função"
- Templates customizáveis
- Variáveis em prompts (`{linguagem}`, `{framework}`)
- Compartilhamento de prompts

---

## 6. Configurações do Sistema

### ⚙️ 6.1 Configurações de Modelo

- Seletor de modelo (dropdown com modelos disponíveis)
- Ajuste de temperatura (0.0 - 2.0)
- Configuração de `max_tokens`
- Top-p / Top-k sampling
- System prompt customizável
- Presets salvos (criativo, preciso, código)

```
┌─────────────────────────────────────┐
│ Modelo: [Llama 3.1 8B        ▼]    │
│                                     │
│ Temperatura:  [━━━━━●━━━━] 0.7     │
│ Max Tokens:   [━━━━━━━●━━] 2048    │
│ Top-p:        [━━━━━━●━━━] 0.9     │
│                                     │
│ [Salvar Preset] [Resetar]          │
└─────────────────────────────────────┘
```

### 👤 6.2 Preferências do Usuário

- Tema (dark/light/system)
- Tamanho de fonte
- Atalhos customizáveis
- Idioma da interface
- Notificações

---

## 7. Priorização de Implementação

### Fase 1 - MVP (1-2 semanas)

| # | Funcionalidade | Prioridade | Esforço |
|---|----------------|------------|---------|
| 1 | Corrigir container Ollama | 🔴 Crítica | 1 dia |
| 2 | Sidebar de histórico básica | 🔴 Alta | 3 dias |
| 3 | Contador de tokens no input | 🟡 Média | 1 dia |
| 4 | Botão copiar código | 🟡 Média | 0.5 dia |
| 5 | Atalhos de teclado básicos | 🟡 Média | 1 dia |

### Fase 2 - Essencial (2-4 semanas)

| # | Funcionalidade | Prioridade | Esforço |
|---|----------------|------------|---------|
| 6 | Indicador de janela de contexto | 🟡 Média | 2 dias |
| 7 | Streaming de resposta | 🔴 Alta | 2 dias |
| 8 | Configurações de modelo | 🟡 Média | 3 dias |
| 9 | Busca no histórico | 🟢 Baixa | 2 dias |
| 10 | Dark/Light mode toggle | 🟢 Baixa | 1 dia |

### Fase 3 - Avançado (4-8 semanas)

- Visualização de tokenização
- Templates de prompts
- Execução de código sandboxed
- Integração com GitHub
- Diff viewer
- Export de conversas

---

## 8. Considerações Técnicas

### 🐳 8.1 Problema Atual: Container Ollama

> **Erro:** `dependency failed to start: container focus-ai-ollama-1 is unhealthy`

O Ollama não está iniciando corretamente, bloqueando toda a aplicação.

#### Diagnóstico Recomendado

```bash
# Verificar logs do container
docker-compose logs -f ollama

# Ou diretamente
docker logs focus-ai-ollama-1

# Verificar uso de recursos
docker stats focus-ai-ollama-1
```

#### Causas Comuns

1. **RAM insuficiente** - Modelos LLM precisam de muita memória
2. **GPU não configurada** - Drivers NVIDIA/CUDA ausentes
3. **Timeout curto** - Healthcheck expira antes do modelo carregar
4. **Porta ocupada** - 11434 já em uso

#### Soluções

```yaml
# docker-compose.yml - Aumentar timeout do healthcheck
ollama:
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
    interval: 30s
    timeout: 120s  # Aumentar de 30s para 120s
    retries: 5
    start_period: 60s  # Dar tempo para iniciar
```

```bash
# Pré-baixar modelo menor para teste
docker exec -it focus-ai-ollama-1 ollama pull tinyllama
```

---

### 📦 8.2 Stack Tecnológica Recomendada

| Componente | Tecnologia |
|------------|------------|
| Frontend | React + TypeScript + Vite |
| Estilização | Tailwind CSS + shadcn/ui |
| Estado | Zustand ou Jotai |
| Syntax Highlight | Prism.js ou Shiki |
| Markdown | react-markdown + remark-gfm |
| Tokenização | tiktoken (via WASM) |
| Backend | FastAPI (já existente) |
| LLM | Ollama (já existente) |
| Database | PostgreSQL (já existente) |
| Cache | Redis (já existente) |

---

### 🔌 8.3 Estrutura de Componentes Sugerida

```
src/
├── components/
│   ├── Chat/
│   │   ├── ChatWindow.tsx
│   │   ├── MessageList.tsx
│   │   ├── MessageBubble.tsx
│   │   ├── CodeBlock.tsx
│   │   └── InputArea.tsx
│   ├── Sidebar/
│   │   ├── Sidebar.tsx
│   │   ├── ConversationList.tsx
│   │   ├── ConversationItem.tsx
│   │   └── SearchBar.tsx
│   ├── Context/
│   │   ├── TokenCounter.tsx
│   │   └── ContextIndicator.tsx
│   └── Settings/
│       ├── SettingsModal.tsx
│       ├── ModelConfig.tsx
│       └── Preferences.tsx
├── hooks/
│   ├── useChat.ts
│   ├── useTokenizer.ts
│   └── useConversations.ts
├── stores/
│   ├── chatStore.ts
│   └── settingsStore.ts
└── utils/
    ├── tokenizer.ts
    └── api.ts
```

---

## 9. Conclusão

O Focus AI tem uma base sólida com FastAPI, Ollama e infraestrutura Docker. Para se tornar uma ferramenta competitiva para programadores, precisa priorizar:

1. **Resolver o problema do container Ollama** (blocker)
2. **Implementar sidebar de histórico** para UX básica
3. **Adicionar indicadores de contexto/tokens**
4. **Melhorar experiência de código** (copiar, highlight, streaming)

Com essas melhorias implementadas nas fases sugeridas, o Focus AI estará bem posicionado como uma ferramenta de chat LLM especializada para desenvolvedores.

---

*Documento gerado em Janeiro 2026*
