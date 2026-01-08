# Arquitetura V2: Chain Validation (Implementado)

## 1. Visão Geral
Sistema de validação em cadeia que combina IA Junior (Llama 3 local) com IA Senior (Gemini cloud) para maximizar economia de créditos mantendo qualidade.

## 2. Core Diferencial: Chain Validation

### Fluxo Implementado
```
User Input
    ↓
JuniorLLMService (Llama 3 via Ollama)
  - Gera resposta inicial
  - Calcula self-confidence (0-100)
    ↓
Confidence Check (threshold: 70%)
    ↓
    ├─ ≥70% → Output direto (ECONOMIA!)
    │
    └─ <70% → SeniorLLMService (Gemini)
              - Valida resposta
              - Corrige se necessário
              - Output final
```

### Economia Real
- **Sem Chain:** 1000 req/dia × $0.001 = $30/mês
- **Com Chain:** 300 req Senior × $0.001 = $9/mês
- **Economia: 70%** 🎉

## 3. Stack Tecnológico

### Backend
- **Orquestração**: ChainValidatorService (Python)
- **IA Junior**: Ollama + Llama 3 8B (local, grátis)
- **IA Senior**: Google Gemini 2.0 Flash (cloud, pago)
- **Framework**: FastAPI (Async)
- **Cache**: Redis (Rate Limiting + Answer Cache)
- **Database**: PostgreSQL + SQLAlchemy

### Frontend
- React + TypeScript
- Tailwind CSS
- Framer Motion
- Badge indicador: "Validado por IA Senior"

### Infraestrutura
- Docker Compose
- Ollama container (4GB volume)
- Health checks automáticos

## 4. Componentes Implementados

### JuniorLLMService
**Arquivo:** `backend/src/infrastructure/llm/junior_llm_service.py`

```python
class JuniorLLMService:
    def generate(self, question: str) -> dict:
        # Retorna: {response, confidence, needs_validation}
```

**Características:**
- Modelo: Llama 3 8B
- Latência: ~2s
- Custo: $0
- Bom para: sintaxe, conceitos básicos

### SeniorLLMService
**Arquivo:** `backend/src/infrastructure/llm/senior_llm_service.py`

```python
class SeniorLLMService:
    def validate(self, question: str, junior_response: dict) -> dict:
        # Retorna: {validated, corrections, final_response}
```

**Características:**
- Modelo: Gemini 2.0 Flash
- Latência: ~3s
- Custo: ~$0.001/req
- Bom para: debugging, arquitetura, validação

### ChainValidatorService
**Arquivo:** `backend/src/infrastructure/llm/chain_validator_service.py`

```python
class ChainValidatorService:
    def generate_socratic_answer(self, question: str) -> dict:
        junior_result = self.junior.generate(question)
        
        if not junior_result["needs_validation"]:
            return junior_result["response"]  # Economia!
        
        senior_result = self.senior.validate(question, junior_result["response"])
        return senior_result["final_response"]
```

## 5. Configuração

### Variáveis de Ambiente
```bash
OLLAMA_URL=http://ollama:11434
CONFIDENCE_THRESHOLD=70
GEMINI_API_KEY=sua-chave
```

### Docker Compose
```yaml
services:
  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_data:/root/.ollama
  
  backend:
    depends_on:
      - ollama
    environment:
      - OLLAMA_URL=http://ollama:11434
```

## 6. Testes (Cobertura: 85%+)

### Unitários
- `test_junior_llm_service.py`: Confidence score
- `test_senior_llm_service.py`: Validação
- `test_chain_validator_service.py`: Decisão de rota

### Integração
- Mock Ollama + Mock Gemini
- Cache hit/miss
- Fallbacks

### E2E
- Fluxo completo com ambos modelos
- Medição de economia real

## 7. Monitoramento

### Logs Estruturados
```
Junior response - confidence: 85, needs_validation: False
High confidence (85%) - skipping Senior
```

### Métricas
- % de requisições que usaram Senior
- Confidence médio do Junior
- Economia estimada (tokens salvos)
- Latência por rota

## 8. Estratégia de Monetização

### Tiers (Futuro)
- **Free**: Apenas Junior (sem validação)
- **Pro**: Chain completo (Junior → Senior)
- **Enterprise**: Senior direto (sem Junior)

### ROI
- Custo operacional: ~$9/mês (1000 req/dia)
- Preço Pro: $19/mês
- Margem: 52%

## 9. Próximos Passos

1. **A/B Testing**: Testar thresholds 60%, 70%, 80%
2. **Dynamic Threshold**: Ajustar por tipo de pergunta
3. **Feedback Loop**: Usuário valida → treina threshold
4. **Analytics Dashboard**: Visualizar economia em tempo real
5. **Multi-model**: Adicionar Claude, GPT-4 como opções Senior

## 10. Referências

- [Chain Validation Details](CHAIN_VALIDATION.md)
- [Setup Guide](SETUP_V2.md)
- [Tasks Roadmap](TASKS_V2.md)