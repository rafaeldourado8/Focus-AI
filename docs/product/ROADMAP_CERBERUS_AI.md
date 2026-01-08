# 🗺️ ROADMAP COMPLETO - CERBERUS AI

## Visão Geral

Transformar o Focus AI em **Cerberus AI**: um Developer LLM & Code Assistant profissional com modelo próprio e API pública para integração externa.

---

## 📍 FASE 1: REBRANDING & IDENTIDADE (ATUAL → 2 SEMANAS)

### 1.1 Documentação
- [ ] `PRODUCT_VISION.md` - Visão oficial do produto
- [ ] `API_DOCUMENTATION.md` - Docs da API pública (futuro)
- [ ] `SYSTEM_PROMPTS.md` - Prompts oficiais documentados
- [ ] Atualizar `README.md` - Nova identidade
- [ ] Remover referências a "aprendizado socrático"

### 1.2 Backend - Identidade
- [ ] Remover logs com "Google", "Gemini", "OpenAI"
- [ ] Criar `CERBERUS_IDENTITY.py` - Constantes de identidade
- [ ] Atualizar system prompts (remover menções a terceiros)
- [ ] Adicionar header `X-Powered-By: Cerberus-AI` nas respostas

### 1.3 Frontend - UX Developer-First
- [ ] Atualizar textos: "mentor técnico" ao invés de "aprendizado"
- [ ] Sugestões iniciais focadas em código/debug
- [ ] Placeholder: "Descreva seu problema técnico..."
- [ ] Footer: "Cerberus AI - Developer Assistant by Focus AI"

### 1.4 Branding
- [ ] Logo Cerberus (3 cabeças = Junior/Senior/Próprio)
- [ ] Paleta de cores oficial
- [ ] Guia de tom de voz (profissional, técnico, sem hype)

---

## 📍 FASE 2: ARQUITETURA ESCALÁVEL (2-4 SEMANAS)

### 2.1 Message Queue (RabbitMQ)
- [ ] Setup RabbitMQ no `docker-compose.yml`
- [ ] `infrastructure/queue/rabbitmq_service.py`
- [ ] Filas:
  - `llm.requests` - Requisições de IA
  - `llm.responses` - Respostas processadas
  - `training.data` - Dados para treino (futuro)
- [ ] Workers assíncronos para processar LLM
- [ ] Retry logic e dead letter queue

### 2.2 Cache Distribuído (Redis Avançado)
- [ ] Lock distribuído (evitar chamadas duplicadas)
- [ ] Cache de contexto (últimas N mensagens)
- [ ] Cache de respostas (hash da pergunta)
- [ ] TTL inteligente (respostas técnicas = 7 dias)
- [ ] Invalidação por versão de modelo

### 2.3 Orchestrator - Roteamento Inteligente
- [ ] `infrastructure/orchestrator/model_router.py`
- [ ] Lógica de roteamento:
  ```python
  if debug_mode or complexity > 8:
      use_senior_model()
  elif cached:
      return_from_cache()
  else:
      use_junior_model()
  ```
- [ ] Métricas de custo por requisição
- [ ] Fallback automático (Senior → Junior se erro)

### 2.4 Observabilidade
- [ ] Prometheus + Grafana
- [ ] Métricas:
  - Latência por modelo
  - Taxa de cache hit
  - Custo por requisição
  - Erros por endpoint
- [ ] Logs estruturados (JSON)
- [ ] Tracing distribuído (Jaeger)

---

## 📍 FASE 3: API PÚBLICA (4-6 SEMANAS)

### 3.1 API Gateway
- [ ] `presentation/api_gateway/`
- [ ] Rate limiting por API key
- [ ] Autenticação: JWT + API Keys
- [ ] Planos:
  - Free: 100 req/dia, só Junior
  - Pro: 10k req/dia, Junior + Senior
  - Enterprise: Ilimitado, todos os modelos

### 3.2 API Keys Management
- [ ] Tabela `api_keys` (PostgreSQL)
- [ ] CRUD de API keys
- [ ] Rotação automática
- [ ] Logs de uso por key
- [ ] Dashboard de consumo

### 3.3 Endpoints Públicos
```
POST /v1/chat/completions
POST /v1/code/analyze
POST /v1/code/debug
POST /v1/code/refactor
GET  /v1/models
GET  /v1/usage
```

### 3.4 SDKs
- [ ] Python SDK (`cerberus-ai-python`)
- [ ] JavaScript SDK (`@cerberus-ai/sdk`)
- [ ] Exemplos de integração:
  - WhatsApp Bot
  - Slack Bot
  - VS Code Extension
  - CLI Tool

### 3.5 Documentação API
- [ ] OpenAPI 3.0 spec
- [ ] Swagger UI
- [ ] Postman Collection
- [ ] Guias de integração
- [ ] Rate limits e custos

---

## 📍 FASE 4: MODELO PRÓPRIO - RAG (6-10 SEMANAS)

### 4.1 RAG (Retrieval-Augmented Generation)
- [ ] Vector Database (Pinecone ou Weaviate)
- [ ] Embeddings (OpenAI Ada-002 ou Sentence-BERT)
- [ ] Indexação de documentação:
  - Python docs
  - JavaScript/TypeScript docs
  - React, FastAPI, Docker docs
  - Stack Overflow (curado)
  - GitHub repos populares

### 4.2 Pipeline de Dados
- [ ] `infrastructure/rag/document_processor.py`
- [ ] Chunking inteligente (código + contexto)
- [ ] Metadata: linguagem, framework, versão
- [ ] Atualização incremental (weekly)

### 4.3 Retrieval Service
- [ ] `infrastructure/rag/retrieval_service.py`
- [ ] Busca semântica (top-k documentos)
- [ ] Re-ranking (relevância)
- [ ] Injeção de contexto no prompt

### 4.4 Hybrid Model
- [ ] RAG + Gemini Pro (melhor dos dois mundos)
- [ ] Prompt: `[CONTEXT FROM RAG]\n\n[USER QUESTION]`
- [ ] Redução de alucinações
- [ ] Respostas mais precisas

---

## 📍 FASE 5: MODELO PRÓPRIO - FINE-TUNING (10-16 SEMANAS)

### 5.1 Coleta de Dados
- [ ] Logs de conversas (anonimizados)
- [ ] Feedback de usuários (👍👎)
- [ ] Curadoria manual (engenheiros revisam)
- [ ] Formato: `{"prompt": "...", "completion": "...", "rating": 5}`
- [ ] Meta: 50k exemplos de alta qualidade

### 5.2 Modelo Base
- [ ] Opções:
  - **CodeLlama 13B** (Meta) - Open source
  - **Mistral 7B** - Rápido e eficiente
  - **Phi-3** (Microsoft) - Pequeno e poderoso
- [ ] Infraestrutura:
  - GPU: A100 ou H100 (AWS/GCP)
  - Framework: HuggingFace Transformers
  - Técnica: LoRA ou QLoRA (eficiente)

### 5.3 Fine-Tuning Pipeline
- [ ] `training/fine_tune.py`
- [ ] Hyperparameters:
  - Learning rate: 2e-5
  - Batch size: 4-8
  - Epochs: 3-5
  - LoRA rank: 16-32
- [ ] Validação: hold-out set (10%)
- [ ] Métricas: perplexity, BLEU, human eval

### 5.4 Avaliação
- [ ] Benchmark interno:
  - Debugging tasks
  - Code generation
  - Explicação de código
- [ ] Comparação com Gemini Pro
- [ ] A/B testing (10% tráfego)

### 5.5 Deploy do Modelo Próprio
- [ ] Servir com vLLM ou TGI (Text Generation Inference)
- [ ] Autoscaling (Kubernetes)
- [ ] Monitoramento de latência
- [ ] Rollback automático se degradação

---

## 📍 FASE 6: MODELO PRÓPRIO - PRODUÇÃO (16-20 SEMANAS)

### 6.1 Multi-Model Strategy
```
┌─────────────────────────────────────┐
│         API Gateway                 │
│  (Roteamento Inteligente)           │
└─────────────────────────────────────┘
           │
    ┌──────┴──────┬──────────┬─────────┐
    │             │          │         │
┌───▼───┐   ┌────▼────┐  ┌──▼──┐  ┌──▼──────┐
│Cerberus│   │ Gemini  │  │GPT-4│  │ Claude  │
│ Model  │   │  Pro    │  │     │  │         │
│(Próprio│   │(Backup) │  │(Pro)│  │(Pro)    │
└────────┘   └─────────┘  └─────┘  └─────────┘
```

### 6.2 Roteamento Final
- [ ] **Cerberus Model** (70% tráfego)
  - Perguntas gerais de código
  - Debug simples
  - Explicações
- [ ] **Gemini Pro** (20% tráfego)
  - Fallback se Cerberus falhar
  - Validação de respostas críticas
- [ ] **GPT-4 / Claude** (10% tráfego)
  - Clientes Enterprise
  - Casos complexos

### 6.3 Continuous Learning
- [ ] Retreino mensal com novos dados
- [ ] Feedback loop: usuário → curadoria → retreino
- [ ] Versionamento de modelos (`cerberus-v1.0`, `v1.1`, etc)
- [ ] Blue-green deployment

### 6.4 Custos Finais
- [ ] Modelo próprio: ~$0.0001/req (70%)
- [ ] Gemini Pro: ~$0.001/req (20%)
- [ ] GPT-4: ~$0.01/req (10%)
- [ ] **Economia total: ~85% vs usar só GPT-4**

---

## 📍 FASE 7: MONETIZAÇÃO & ESCALA (20+ SEMANAS)

### 7.1 Planos de Preço
```
FREE
- 100 req/dia
- Só Cerberus Model
- Rate limit: 10 req/min

PRO ($29/mês)
- 10k req/dia
- Cerberus + Gemini Pro
- Rate limit: 60 req/min
- Suporte por email

ENTERPRISE (Custom)
- Ilimitado
- Todos os modelos
- SLA 99.9%
- Suporte dedicado
- On-premise option
```

### 7.2 Marketplace de Integrações
- [ ] WhatsApp Bot (template)
- [ ] Slack App
- [ ] Discord Bot
- [ ] VS Code Extension
- [ ] JetBrains Plugin
- [ ] Zapier Integration

### 7.3 White Label
- [ ] Empresas podem hospedar Cerberus
- [ ] Customização de prompts
- [ ] Branding próprio
- [ ] Licença Enterprise

### 7.4 Partnerships
- [ ] Bootcamps de programação
- [ ] Universidades (licença educacional)
- [ ] Empresas de consultoria

---

## 📊 MÉTRICAS DE SUCESSO

### Técnicas
- Latência p95 < 2s
- Uptime > 99.5%
- Cache hit rate > 60%
- Custo por requisição < $0.0005

### Produto
- 10k usuários ativos (6 meses)
- 100k requisições/dia (1 ano)
- NPS > 50
- Churn < 5%/mês

### Negócio
- MRR $50k (1 ano)
- 100 clientes Enterprise (18 meses)
- Break-even (2 anos)

---

## 🛠️ STACK TECNOLÓGICA FINAL

### Backend
- FastAPI (API Gateway)
- RabbitMQ (Message Queue)
- Redis (Cache + Locks)
- PostgreSQL (Dados + API Keys)
- Celery (Workers)

### IA/ML
- Cerberus Model (Fine-tuned CodeLlama/Mistral)
- vLLM (Serving)
- Pinecone (Vector DB)
- HuggingFace (Training)

### Infra
- Kubernetes (Orchestration)
- Terraform (IaC)
- Prometheus + Grafana (Monitoring)
- Jaeger (Tracing)
- AWS/GCP (Cloud)

### Frontend
- React + TypeScript
- Tailwind CSS
- WebSockets (real-time)

---

## 📅 TIMELINE RESUMIDO

| Fase | Duração | Entregável |
|------|---------|------------|
| 1. Rebranding | 2 semanas | Nova identidade |
| 2. Arquitetura | 2-4 semanas | RabbitMQ + Cache |
| 3. API Pública | 4-6 semanas | API Keys + SDKs |
| 4. RAG | 6-10 semanas | Retrieval funcional |
| 5. Fine-Tuning | 10-16 semanas | Modelo próprio (beta) |
| 6. Produção | 16-20 semanas | Multi-model em prod |
| 7. Monetização | 20+ semanas | Planos + Marketplace |

**Total: ~6 meses até modelo próprio em produção**

---

## 🚀 PRÓXIMOS PASSOS IMEDIATOS

1. ✅ Criar este roadmap
2. [ ] Executar Fase 1 (Rebranding)
3. [ ] Setup RabbitMQ (Fase 2.1)
4. [ ] Implementar API Gateway básico (Fase 3.1)
5. [ ] Começar coleta de dados para fine-tuning (Fase 5.1)
