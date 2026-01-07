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

**MVP 100% COMPLETO! 🎉**

Veja [IMPLEMENTATION.md](IMPLEMENTATION.md) para detalhes técnicos.