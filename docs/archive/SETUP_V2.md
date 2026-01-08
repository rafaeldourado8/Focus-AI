# Setup Rápido - V2 Chain Validation

## Pré-requisitos
- Docker + Docker Compose
- 8GB RAM mínimo (para Ollama)
- Chave API do Google Gemini

## Passo a Passo

### 1. Clone e Configure
```bash
git clone <repo>
cd Focus-AI
cp .env.example .env
```

### 2. Edite o .env
```bash
GEMINI_API_KEY=sua-chave-aqui
GOOGLE_CLIENT_ID=seu-client-id
```

### 3. Inicie os Serviços
```bash
docker-compose up -d
```

### 4. Aguarde Ollama Baixar Llama 3
```bash
# Isso pode demorar 5-10 minutos na primeira vez
docker-compose logs -f ollama
```

Aguarde até ver: `✅ Setup completo! Modelo Llama 3 pronto para uso.`

### 5. Inicialize o Backend
```bash
# O backend aguarda Ollama estar pronto automaticamente
docker-compose logs -f backend
```

### 6. Acesse
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Ollama: http://localhost:11434

## Testando Chain Validation

### Pergunta Simples (Junior apenas)
```
Pergunta: "O que é Python?"
Resposta: ~2s, confidence ~85%, sem Senior
```

### Pergunta Complexa (Junior + Senior)
```
Pergunta: "Como implementar um sistema distribuído com microserviços?"
Resposta: ~5s, confidence ~50%, com validação Senior
```

## Verificando Economia

Veja os logs do backend:
```bash
docker-compose logs backend | grep "confidence"
```

Você verá:
```
Junior response - confidence: 85, needs_validation: False  # Economia!
Junior response - confidence: 50, needs_validation: True   # Chamou Senior
```

## Ajustando Threshold

Edite `.env`:
```bash
CONFIDENCE_THRESHOLD=60  # Mais economia, menos qualidade
CONFIDENCE_THRESHOLD=80  # Menos economia, mais qualidade
```

Reinicie:
```bash
docker-compose restart backend
```

## Rodando Testes

```bash
cd backend
docker-compose exec backend pytest tests/ -v --cov=src --cov-report=term-missing
```

Cobertura esperada: **≥85%**

## Troubleshooting

### Ollama não inicia
```bash
# Verifique memória disponível
docker stats

# Reinicie o serviço
docker-compose restart ollama
```

### Backend não conecta ao Ollama
```bash
# Verifique se Ollama está rodando
curl http://localhost:11434

# Verifique logs
docker-compose logs ollama
```

### Modelo Llama 3 não baixou
```bash
# Entre no container e baixe manualmente
docker-compose exec ollama ollama pull llama3
```

## Próximos Passos

1. Teste diferentes tipos de perguntas
2. Monitore % de uso do Senior
3. Ajuste threshold conforme necessário
4. Veja [CHAIN_VALIDATION.md](CHAIN_VALIDATION.md) para detalhes técnicos
