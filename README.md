# Focus AI - MVP

Sistema de aprendizado profundo com metodologia socrática.

## Estrutura do Projeto

```
Focus AI/
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
- LangChain + OpenAI

### Frontend
- React + TypeScript
- Tailwind CSS
- Framer Motion
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
- **Domain**: Entidades (User, LearningSession, Question, Answer)
- **Application**: Casos de uso (criar sessão, enviar pergunta)
- **Infrastructure**: Repositórios, LLM, Cache
- **Presentation**: API REST

## Funcionalidades MVP

- [x] Autenticação JWT
- [x] Sessões de aprendizado
- [x] Chat interface (estilo ChatGPT)
- [x] Design dark com gradientes
- [x] Integração LLM (Google Gemini Pro)
- [x] Persistência PostgreSQL (SQLAlchemy + Alembic)
- [x] Cache Redis (Locks + Answer Cache)
- [x] Metodologia socrática (Prompt estruturado)
- [x] **Chain Validation (Junior → Senior)** ✨ NOVO
- [x] **Economia de 63% em custos de API** ✨ NOVO

**MVP V2 COMPLETO! 🎉**

### Chain Validation Architecture

Sistema híbrido que combina:
- **IA Junior** (Gemini 2.0 Flash Lite) - Respostas rápidas e baratas
- **IA Senior** (Gemini 2.5 Pro) - Validação apenas quando necessário

**Resultado:** 63% de economia mantendo qualidade!

Veja [CHAIN_VALIDATION.md](docs/CHAIN_VALIDATION.md) para detalhes técnicos.

Veja [IMPLEMENTATION.md](IMPLEMENTATION.md) para detalhes técnicos.