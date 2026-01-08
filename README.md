# Cerberus AI

**Developer LLM & Code Assistant**

Mentor técnico inteligente que elimina a síndrome do impostor em desenvolvedores, oferecendo um ambiente onde aprender, debugar e tomar decisões técnicas se torna um processo guiado, confiável e profissional.

## Estrutura do Projeto

```
Cerberus AI/
├── backend/
│   ├── src/
│   │   ├── domain/          # Entidades e regras de negócio
│   │   ├── application/     # Casos de uso
│   │   ├── infrastructure/  # Implementações externas
│   │   └── presentation/    # Controllers e rotas
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   └── ...
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── nginx.conf
```

## Tecnologias

### Backend
- FastAPI (Python)
- PostgreSQL
- Redis
- JWT + bcrypt
- Google Gemini (temporário - modelo próprio em desenvolvimento)

### Frontend
- React + JavaScript
- Tailwind CSS
- Axios

### Infraestrutura
- Docker + Docker Compose
- Nginx (Load Balancer)

## Setup Rápido

1. Clone o repositório
2. Copie `.env.example` para `.env` e configure as variáveis
3. Execute: `docker-compose up --build`

## Segurança

- JWT com expiração de 3 minutos
- Senhas hasheadas com bcrypt
- CORS configurado
- Rate limiting por sessão (Redis locks)

## Arquitetura

Baseada em Clean Architecture e DDD:
- **Domain**: Entidades (User, Session, Question, Answer)
- **Application**: Casos de uso (criar sessão, processar pergunta)
- **Infrastructure**: Repositórios, LLM, Cache, Identity
- **Presentation**: API REST

## Funcionalidades

- [x] Autenticação JWT
- [x] Sessões de desenvolvimento
- [x] Chat interface developer-first
- [x] Design dark profissional
- [x] Multi-model LLM (Junior/Senior)
- [x] Persistência PostgreSQL
- [x] Cache Redis inteligente
- [x] **Chain Validation** - Economia de 63%
- [x] **Debug Mode** - Análise técnica profunda
- [x] **Identidade Cerberus AI** - Sem menções a provedores externos

## Roadmap

### Fase 1: Rebranding ✅ (atual)
- [x] Nova identidade (Cerberus AI)
- [x] System prompts profissionais
- [x] Remoção de menções a provedores
- [x] UX developer-first

### Fase 2: Arquitetura Escalável (próximo)
- [ ] RabbitMQ (message queue)
- [ ] Cache distribuído (Redis avançado)
- [ ] Orchestrator inteligente
- [ ] Observabilidade (Prometheus + Grafana)

### Fase 3: API Pública
- [ ] API Gateway
- [ ] API Keys management
- [ ] SDKs (Python, JavaScript)
- [ ] Integrações (WhatsApp, Slack, VS Code)

### Fase 4-7: Modelo Próprio
- [ ] RAG (Retrieval-Augmented Generation)
- [ ] Fine-tuning (CodeLlama/Mistral)
- [ ] Produção multi-model
- [ ] Monetização

Veja [ROADMAP_CERBERUS_AI.md](docs/product/ROADMAP_CERBERUS_AI.md) para detalhes completos.

## Arquitetura Híbrida

Sistema multi-model inteligente:
- **Cerberus Lite** (70% requisições) - Respostas rápidas
- **Cerberus Pro** (20% requisições) - Debug e arquitetura
- **Cerberus Ultra** (futuro) - Modelo próprio fine-tuned

**Economia:** 63% vs usar só modelo premium

## Debug Mode

Análise técnica profunda:
- Identificação de causas raiz
- Múltiplas soluções com trade-offs
- Melhores práticas da indústria
- Considerações de arquitetura e escalabilidade

## Documentação

- [Visão do Produto](docs/product/PRODUCT_VISION.md)
- [Roadmap Completo](docs/product/ROADMAP_CERBERUS_AI.md)
- [API Pública](docs/api/API_PUBLIC_SPEC.md)
- [System Prompts](docs/product/SYSTEM_PROMPTS.md)
- [Arquivos Antigos](docs/archive/) (Focus AI MVP)

---

**Cerberus AI** - Developer Assistant by Focus AI