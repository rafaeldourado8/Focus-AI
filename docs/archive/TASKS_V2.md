# Tarefas - Arquitetura V2: Chain Validation (Junior → Senior)

## Conceito: Economia Máxima de Créditos
**Fluxo:**
```
User Input
  ↓
IA Junior (Llama 3 Local) → Gera resposta inicial [BARATO]
  ↓
IA Senior (Gemini Cloud) → Valida/Corrige apenas se necessário [CARO]
  ↓
Output Final (melhor resposta)
```

**Economia:** Senior só é chamada quando Junior precisa de correção/refinamento.

---

## Fase 1: Infraestrutura Chain Validation

### 1.1 Setup Ollama (IA Junior)
- [ ] Instalar Ollama no ambiente de desenvolvimento
- [ ] Baixar modelo Llama 3 8B
- [ ] Configurar docker-compose com serviço Ollama
- [ ] Adicionar OLLAMA_URL no .env

### 1.2 Dependências Backend
- [ ] Adicionar langchain no requirements.txt
- [ ] Adicionar langchain-community
- [ ] Adicionar langchain-google-genai
- [ ] Adicionar ollama-python

### 1.3 IA Junior Service
- [ ] Criar `infrastructure/llm/junior_llm_service.py` (Ollama/Llama 3)
- [ ] Implementar geração de resposta inicial
- [ ] Adicionar self-confidence score (0-100)
- [ ] Retornar JSON: {response, confidence, needs_validation}

### 1.4 IA Senior Service
- [ ] Renomear `openai_service.py` para `senior_llm_service.py` (Gemini)
- [ ] Implementar validação de resposta Junior
- [ ] Prompt: "Valide esta resposta e corrija se necessário"
- [ ] Retornar JSON: {validated, corrections, final_response}

### 1.5 Chain Orchestrator
- [ ] Criar `infrastructure/llm/chain_validator_service.py`
- [ ] Fluxo: Junior → Avalia confidence → Senior (se necessário)
- [ ] Threshold: confidence < 70 = chama Senior
- [ ] Logs: track quando Senior foi chamado

### 1.6 Integração Use Case
- [ ] Modificar `ask_question.py` para usar ChainValidatorService
- [ ] Adicionar metadata: {used_senior: bool, confidence: int}
- [ ] Atualizar testes unitários

## Fase 2: Otimizações de Economia

### 2.1 Cache Inteligente por Camada
- [ ] Cache Junior: TTL 30min (respostas rápidas)
- [ ] Cache Senior: TTL 24h (respostas validadas)
- [ ] Key: hash(question + model_type)
- [ ] Métricas: hit rate por camada

### 2.2 Confidence Tuning
- [ ] Testar diferentes thresholds (60, 70, 80)
- [ ] A/B test: qual economiza mais sem perder qualidade
- [ ] Ajustar threshold dinamicamente por tipo de pergunta

### 2.3 Observabilidade de Custos
- [ ] Logging: % de chamadas que usaram Senior
- [ ] Métrica: economia estimada (tokens salvos)
- [ ] Dashboard: Junior vs Senior usage
- [ ] Alerta: se Senior > 30% das chamadas

## Fase 3: Frontend

### 3.1 Indicador de Validação
- [ ] Badge: "Validado por IA Senior" (quando Senior foi usado)
- [ ] Badge: "Resposta Rápida" (quando só Junior)
- [ ] Ícone de confiança (confidence score)

### 3.2 Transparência
- [ ] Tooltip: "Esta resposta foi validada por IA avançada"
- [ ] Mostrar confidence score (opcional, dev mode)

## Fase 4: Testes & Deploy

### 4.1 Testes
- [ ] Teste unitário: JuniorLLMService.generate() retorna confidence
- [ ] Teste unitário: SeniorLLMService.validate() corrige resposta
- [ ] Teste unitário: ChainValidator com confidence alta (não chama Senior)
- [ ] Teste unitário: ChainValidator com confidence baixa (chama Senior)
- [ ] Teste integração: Mock Ollama + Mock Gemini
- [ ] Teste E2E: Fluxo completo com ambos modelos
- [ ] Teste: Cache hit evita chamadas desnecessárias
- [ ] Teste: Fallback quando Junior falha
- [ ] Teste: Fallback quando Senior falha
- [ ] Coverage mínimo: 85%

### 4.2 Documentação
- [ ] Atualizar ARCHITECTURE_V2.md com Chain Validation
- [ ] Criar CHAIN_VALIDATION.md (detalhes técnicos)
- [ ] Documentar threshold e tuning

### 4.3 Deploy
- [ ] Configurar Ollama em produção
- [ ] Ajustar docker-compose.prod.yml
- [ ] Monitorar custos Gemini API (deve cair 60-80%)

## Fase 5: Monetização (Futuro)

### 5.1 Tiers
- [ ] Free: apenas Junior (sem validação)
- [ ] Pro: Chain completo (Junior → Senior)
- [ ] Enterprise: Senior direto (sem Junior)

### 5.2 Analytics
- [ ] Dashboard: economia por usuário
- [ ] Relatório: % de economia vs qualidade
- [ ] ROI: custo Junior vs Senior

---

## Prioridade Imediata (MVP V2)
1. ✅ Setup Ollama
2. ✅ Junior Service
3. ✅ Senior Service (validação)
4. ✅ Chain Orchestrator
5. ✅ Integração Use Case
6. ✅ Testes básicos
7. ✅ Deploy

**Meta**: Reduzir custos de API em 70% mantendo qualidade
**Prazo**: 1 semana
