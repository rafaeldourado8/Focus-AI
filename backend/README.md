# Focus AI Backend

Backend completo com Clean Architecture, DDD e segurança OWASP.

## Estrutura

```
backend/
├── src/
│   ├── domain/              # Entidades (User, LearningSession, Question, Answer)
│   ├── application/         # Casos de uso
│   ├── infrastructure/      # Implementações (DB, Cache, LLM, Auth)
│   └── presentation/        # API REST (FastAPI)
├── tests/                   # Testes unitários
└── requirements.txt
```

## Setup Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp ../.env.example .env

# Rodar testes
pytest

# Iniciar servidor
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Testes

```bash
# Rodar todos os testes
pytest

# Com cobertura
pytest --cov=src --cov-report=html

# Teste específico
pytest tests/test_auth_service.py -v
```

## Segurança

- JWT com expiração de 3 minutos
- Bcrypt para senhas
- Validação de força de senha
- CORS configurado
- Rate limiting por sessão (Redis locks)
- SQL injection prevention (SQLAlchemy ORM)

Ver [SECURITY.md](SECURITY.md) para detalhes.

## API Endpoints

### Auth
- `POST /api/auth/register` - Criar conta
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Usuário atual

### Sessions
- `POST /api/sessions/` - Criar sessão
- `POST /api/sessions/{id}/questions` - Enviar pergunta
- `GET /api/sessions/{id}` - Detalhes da sessão

## Casos de Uso

1. **RegisterUserUseCase** - Registro com validação de senha
2. **LoginUserUseCase** - Login com verificação bcrypt
3. **CreateSessionUseCase** - Criar sessão de aprendizado
4. **AskQuestionUseCase** - Enviar pergunta com lock e LLM

## Tecnologias

- FastAPI
- SQLAlchemy + PostgreSQL
- Redis (cache e locks)
- OpenAI API
- JWT + Bcrypt
- Pytest