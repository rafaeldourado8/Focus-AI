# Chain Validation Architecture

## Conceito: Economia Máxima de Créditos

Sistema de validação em cadeia que combina 2 modelos Gemini (Junior barato + Senior caro) para maximizar economia sem perder qualidade.

## Fluxo de Execução

```
User Question
    ↓
┌─────────────────────┐
│  Junior LLM         │  Gemini 2.0 Flash Lite
│  - Gera resposta    │  Custo: ~$0.0001/req
│  - Self-confidence  │  Latência: ~1s
└─────────────────────┘
    ↓
┌─────────────────────┐
│  Confidence Check   │  Threshold: 70%
└─────────────────────┘
    ↓
    ├─ ≥70% → Output (economia!)
    │
    └─ <70% → ┌─────────────────────┐
              │  Senior LLM         │  Gemini 2.5 Pro
              │  - Valida resposta  │  Custo: ~$0.001/req
              │  - Corrige erros    │  Latência: ~2s
              └─────────────────────┘
                  ↓
              Final Output
```

## Componentes

### 1. JuniorLLMService
**Modelo:** Gemini 2.0 Flash Lite  
**Função:** Gera resposta inicial + confidence score (0-100)

```python
{
  "response": {
    "content": "...",
    "explanation": "...",
    "edge_cases": "..."
  },
  "confidence": 85,
  "needs_validation": False
}
```

**Características:**
- Rápido (~1s)
- Custo baixo (~$0.0001/req)
- Bom para perguntas simples/sintaxe

### 2. SeniorLLMService
**Modelo:** Gemini 2.5 Pro  
**Função:** Valida e corrige resposta do Junior

```python
{
  "validated": True,
  "corrections": "Adicionei detalhes sobre...",
  "final_response": {
    "content": "...",
    "explanation": "...",
    "edge_cases": "..."
  }
}
```

**Características:**
- Mais lento (~2s)
- Custo por requisição (~$0.001)
- Excelente para debugging/arquitetura

### 3. ChainValidatorService
**Função:** Orquestra Junior → Senior baseado em confidence

**Lógica:**
```python
if junior.confidence >= THRESHOLD:
    return junior.response  # Economia!
else:
    return senior.validate(junior.response)
```

## Economia Esperada

### Cenário Real (1000 perguntas/dia)

**Sem Chain Validation:**
- 1000 req × $0.001 (Pro) = $1.00/dia
- $30/mês

**Com Chain Validation (70% confidence threshold):**
- 700 req Junior × $0.0001 = $0.07/dia
- 300 req Senior × $0.001 = $0.30/dia
- Total: $0.37/dia = $11/mês

**Economia: 63%** 🎉

## Configuração

### Variáveis de Ambiente
```bash
CONFIDENCE_THRESHOLD=70  # Ajustar conforme necessidade
GEMINI_API_KEY=sua-chave
```

### Tuning do Threshold
- **60%**: Mais economia, menos qualidade
- **70%**: Balanceado (recomendado)
- **80%**: Menos economia, mais qualidade

## Metadata de Resposta

Toda resposta inclui metadata para observabilidade:

```json
{
  "content": "...",
  "explanation": "...",
  "edge_cases": "...",
  "metadata": {
    "used_senior": false,
    "confidence": 85,
    "model": "llama3",
    "corrections": null
  }
}
```

## Testes

### Cobertura Mínima: 85%

**Testes Unitários:**
- JuniorLLMService retorna confidence
- SeniorLLMService valida resposta
- ChainValidator decide corretamente

**Testes de Integração:**
- Mock Ollama + Mock Gemini
- Cache hit evita chamadas
- Fallbacks funcionam

**Testes E2E:**
- Fluxo completo com ambos modelos
- Economia real medida

## Monitoramento

### Métricas Importantes
- % de requisições que usaram Senior
- Confidence médio do Junior
- Economia estimada (tokens salvos)
- Latência por rota (Junior vs Senior)

### Alertas
- Se Senior > 40% das chamadas → Ajustar threshold
- Se Junior confidence < 50 frequente → Melhorar prompts

## Próximos Passos

1. **A/B Testing**: Testar diferentes thresholds
2. **Dynamic Threshold**: Ajustar por tipo de pergunta
3. **Feedback Loop**: Usuário valida resposta → treina threshold
4. **Tiers**: Free (só Junior) vs Pro (Chain completo)

## Referências

- [Google Gemini Models](https://ai.google.dev/gemini-api/docs/models/gemini)
- [Gemini Pricing](https://ai.google.dev/pricing)
