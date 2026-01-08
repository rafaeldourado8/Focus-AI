# Debug Mode - Implementação Técnica

## Arquitetura

### Fluxo de Dados

```
Frontend (Chat.jsx)
    ↓ debug_mode: true
Backend (session_routes.py)
    ↓ QuestionRequest { content, debug_mode }
Use Case (ask_question.py)
    ↓ execute(..., debug_mode)
Chain Validator (chain_validator_service.py)
    ↓ generate_answer(..., debug_mode)
Senior LLM (senior_llm_service.py)
    ↓ generate_debug(question)
Gemini 2.5 Pro (Debug Model)
    ↓ Resposta estruturada
Frontend (Renderização)
```

## Componentes Modificados

### 1. Frontend (`Chat.jsx`)

**Estado:**
```javascript
const [debugMode, setDebugMode] = useState(false);
```

**Request:**
```javascript
body: JSON.stringify({ 
  content: currentInput,
  debug_mode: debugMode 
})
```

**UI Indicators:**
- Badge "DEBUG" no header
- Botão com animação pulse
- Banner informativo
- Input com borda vermelha
- Placeholder customizado

### 2. Backend Routes (`session_routes.py`)

**Request Model:**
```python
class QuestionRequest(BaseModel):
    content: str
    debug_mode: bool = False
```

**Endpoint:**
```python
result = use_case.execute(
    session_id, 
    user_id, 
    request.content, 
    request.debug_mode
)
```

### 3. Use Case (`ask_question.py`)

**Signature:**
```python
def execute(
    self, 
    session_id: str, 
    user_id: str, 
    content: str, 
    debug_mode: bool = False
) -> dict:
```

**LLM Call:**
```python
llm_response = self.llm_service.generate_answer(
    content, 
    debug_mode=debug_mode
)
```

### 4. Chain Validator (`chain_validator_service.py`)

**Lógica Principal:**
```python
def generate_answer(
    self, 
    question: str, 
    conversation_history: list = None, 
    debug_mode: bool = False
) -> dict:
    
    # Debug Mode: Usa Senior diretamente
    if debug_mode:
        senior_result = self.senior.generate_debug(
            question, 
            conversation_history
        )
        return {
            "content": senior_result["content"],
            "model": "gemini-2.5-pro-debug",
            "used_senior": True
        }
    
    # Modo normal: Junior → Senior (se necessário)
    # ...
```

### 5. Senior LLM (`senior_llm_service.py`)

**Debug Model:**
```python
self.debug_model = genai.GenerativeModel(
    model_name='gemini-2.5-pro',
    generation_config={"temperature": 0.2},
    system_instruction="""
    🎯 MODO DEBUG ATIVADO - Análise Técnica Profunda
    
    Para CADA pergunta, forneça:
    1. 🔍 ANÁLISE DETALHADA
    2. 🎯 CAUSAS RAIZ
    3. 💡 SOLUÇÕES PRÁTICAS
    4. ✅ MELHORES PRÁTICAS
    5. 🏗️ ARQUITETURA & ESCALABILIDADE
    """
)
```

**Método Debug:**
```python
def generate_debug(
    self, 
    question: str, 
    conversation_history: list = None
) -> dict:
    debug_prompt = f"""
    🐛 DEBUG MODE - Análise Técnica Profunda
    
    Pergunta: {question}
    
    Forneça uma análise COMPLETA seguindo a estrutura:
    1. 🔍 ANÁLISE DETALHADA
    2. 🎯 CAUSAS RAIZ  
    3. 💡 SOLUÇÕES PRÁTICAS (com código)
    4. ✅ MELHORES PRÁTICAS
    5. 🏗️ ARQUITETURA & ESCALABILIDADE
    """
    
    response = self.debug_model.generate_content(debug_prompt)
    return {"content": response.text, "debug_mode": True}
```

## Prompt Engineering

### System Instruction (Debug Model)

O prompt do Debug Model é otimizado para:

1. **Profundidade Técnica**: Temperature 0.2 (mais determinístico)
2. **Estrutura Consistente**: 5 seções obrigatórias
3. **Exemplos Práticos**: Código funcional e testado
4. **Múltiplas Linguagens**: Python, JS, Go, Rust, Java, C++
5. **Contexto de Produção**: Escalabilidade e segurança

### Estrutura da Resposta

```markdown
# 🔍 ANÁLISE DETALHADA
- Problema identificado
- Contexto técnico
- O que acontece internamente

# 🎯 CAUSAS RAIZ
- Lista de possíveis causas
- Causa mais provável
- Explicação do "por quê"

# 💡 SOLUÇÕES PRÁTICAS
## Solução 1: [Nome]
```language
// Código completo
```
Trade-offs: ...

## Solução 2: [Nome]
```language
// Código alternativo
```
Trade-offs: ...

# ✅ MELHORES PRÁTICAS
- Padrões da indústria
- Otimizações
- Segurança

# 🏗️ ARQUITETURA & ESCALABILIDADE
- Como escalar
- Patterns recomendados
- Considerações de produção
```

## Performance

### Comparação de Custos

| Modo | Modelo | Custo/Request | Latência |
|------|--------|---------------|----------|
| Normal (Junior) | Gemini 2.0 Flash Lite | ~$0.001 | ~500ms |
| Normal (Senior) | Gemini 2.5 Pro | ~$0.003 | ~1500ms |
| Debug Mode | Gemini 2.5 Pro | ~$0.003 | ~2000ms |

### Otimizações

1. **Cache**: Respostas são cacheadas no Redis
2. **Skip Junior**: Debug Mode pula validação desnecessária
3. **Temperature**: 0.2 para respostas mais consistentes
4. **Streaming**: Futuro - streaming de respostas longas

## Segurança

### Validações

1. **Autenticação**: JWT token obrigatório
2. **Rate Limiting**: Redis locks por sessão
3. **Input Sanitization**: Validação de conteúdo
4. **Output Filtering**: Sem dados sensíveis

### Logs

```python
logger.info(f"Processing question: {question[:50]}... [DEBUG={debug_mode}]")
logger.info("Debug Mode activated - using Senior directly")
logger.info("Debug mode generation completed")
```

## Testes

### Unitários

- `test_debug_mode_uses_senior_directly`
- `test_normal_mode_uses_junior_first`
- `test_debug_mode_prompt_structure`
- `test_debug_mode_fallback_on_error`

### Integração

- `test_debug_mode_end_to_end`

### Executar Testes

```bash
cd backend
pytest tests/test_debug_mode.py -v
```

## Monitoramento

### Métricas

1. **Taxa de Uso**: % de requests com debug_mode=true
2. **Custo**: Gasto total com Senior LLM
3. **Latência**: Tempo médio de resposta
4. **Satisfação**: Feedback dos usuários

### Logs Estruturados

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "message": "Debug mode activated",
  "session_id": "abc123",
  "user_id": "user456",
  "model": "gemini-2.5-pro-debug",
  "latency_ms": 2150
}
```

## Roadmap

### V1 (Atual) ✅
- [x] Toggle Debug Mode no frontend
- [x] Backend processa flag debug_mode
- [x] Senior LLM com prompt especializado
- [x] UI indicators (badge, tooltip, banner)
- [x] Testes unitários

### V2 (Próximo)
- [ ] Streaming de respostas longas
- [ ] Cache inteligente por tipo de pergunta
- [ ] Métricas de uso no dashboard
- [ ] Export de análises em Markdown
- [ ] Templates de debug pré-configurados

### V3 (Futuro)
- [ ] Debug Mode com histórico de sessão
- [ ] Integração com VS Code
- [ ] Análise de código em tempo real
- [ ] Sugestões proativas de otimização
- [ ] Comparação de soluções lado a lado

## Troubleshooting

### Problema: Debug Mode não ativa

**Causa**: Estado não sincronizado
**Solução**: Verificar console do navegador

### Problema: Resposta igual ao modo normal

**Causa**: Flag não chegou ao backend
**Solução**: Verificar network tab, payload deve ter `debug_mode: true`

### Problema: Erro 500 no backend

**Causa**: Gemini API error
**Solução**: Verificar logs, fallback para modelo normal

### Problema: Resposta muito longa

**Causa**: Debug Mode é verbose por design
**Solução**: Implementar streaming (V2)

## Contribuindo

### Adicionar Nova Seção ao Debug

1. Editar `senior_llm_service.py`
2. Atualizar `system_instruction` do `debug_model`
3. Adicionar emoji e estrutura
4. Testar com perguntas variadas
5. Atualizar documentação

### Melhorar Prompt

1. Testar com casos reais
2. Iterar no `system_instruction`
3. Ajustar `temperature` se necessário
4. Validar com testes A/B
5. Documentar mudanças

---

**Desenvolvido com ❤️ pela equipe Focus AI**
