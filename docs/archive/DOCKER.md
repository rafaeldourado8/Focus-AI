# Docker Commands - Focus AI Backend

## Iniciar Backend

```bash
# Iniciar todos os serviços
docker-compose up -d

# Ver logs em tempo real
docker-compose logs -f backend

# Ver logs de todos os serviços
docker-compose logs -f
```

## Parar e Limpar

```bash
# Parar serviços
docker-compose down

# Parar e remover volumes (limpa banco de dados)
docker-compose down -v

# Rebuild completo
docker-compose up --build --force-recreate
```

## Debugging

```bash
# Entrar no container do backend
docker-compose exec backend bash

# Ver status dos serviços
docker-compose ps

# Executar migrations manualmente
docker-compose exec backend alembic upgrade head

# Testar conexão PostgreSQL
docker-compose exec postgres psql -U focus -d focusai

# Testar conexão Redis
docker-compose exec redis redis-cli ping
```

## Testes

```bash
# Executar testes dentro do container
docker-compose exec backend pytest -v

# Com cobertura
docker-compose exec backend pytest -v --cov=src
```

## Verificar Saúde

```bash
# Health check do backend
curl http://localhost:8000/health

# Verificar API
curl http://localhost:8000/

# Verificar PostgreSQL
docker-compose exec postgres pg_isready -U focus

# Verificar Redis
docker-compose exec redis redis-cli ping
```

## Ordem de Inicialização

1. **PostgreSQL** (com healthcheck)
2. **Redis** (com healthcheck)
3. **Backend** (aguarda healthchecks + executa migrations)

## Variáveis de Ambiente

Configuradas no `.env`:
- `OPENAI_API_KEY`: Chave da API do Google Gemini
- `JWT_SECRET`: Segredo para tokens JWT
- `DATABASE_URL`: Conexão PostgreSQL (automática)
- `REDIS_URL`: Conexão Redis (automática)

## Troubleshooting

### Backend não inicia
```bash
# Ver logs detalhados
docker-compose logs backend

# Verificar se PostgreSQL está pronto
docker-compose exec postgres pg_isready -U focus
```

### Erro de migrations
```bash
# Resetar banco de dados
docker-compose down -v
docker-compose up -d postgres
docker-compose exec backend alembic upgrade head
```

### Porta já em uso
```bash
# Verificar processos usando porta 8000
netstat -ano | findstr :8000

# Ou mudar porta no docker-compose.yml
ports:
  - "8001:8000"  # Usar 8001 no host
```
