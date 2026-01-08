# 🧪 Debug Mode - Guia de Testes

## Comandos Rápidos

### Iniciar o Sistema

```bash
# Subir todos os serviços
docker-compose up --build

# Ou em background
docker-compose up -d --build

# Ver logs
docker-compose logs -f backend
```

### Testar Backend

```bash
# Entrar no container
docker-compose exec backend bash

# Rodar testes
pytest tests/test_debug_mode.py -v

# Rodar todos os testes
pytest -v

# Com coverage
pytest --cov=src tests/test_debug_mode.py
```

### Verificar Logs

```bash
# Logs do backend
docker-compose logs backend | grep "DEBUG"

# Logs em tempo real
docker-compose logs -f backend | grep -E "DEBUG|Senior|Junior"

# Últimas 100 linhas
docker-compose logs --tail=100 backend
```

## Testes Manuais

### 1. Teste Básico - Ativar/Desativar

**Passos:**
1. Abra http://localhost:3000
2. Faça login
3. Clique no botão 🐛 Debug
4. Verifique badge "DEBUG" aparece
5. Clique novamente
6. Verifique badge desaparece

**Resultado Esperado:**
- ✅ Botão muda de cor (cinza → vermelho)
- ✅ Badge aparece/desaparece
- ✅ Animação pulse quando ativo
- ✅ Tooltip mostra informação

### 2. Teste de Request

**Passos:**
1. Ative Debug Mode
2. Abra DevTools (F12)
3. Vá para Network tab
4. Digite: "Por que meu código dá erro?"
5. Envie a mensagem
6. Inspecione o request

**Resultado Esperado:**
```json
{
  "content": "Por que meu código dá erro?",
  "debug_mode": true
}
```

### 3. Teste de Resposta

**Passos:**
1. Com Debug Mode ativo
2. Pergunte: "Como otimizar esta query SQL?"
3. Aguarde resposta
4. Verifique estrutura

**Resultado Esperado:**
```markdown
# 🔍 ANÁLISE DETALHADA
[conteúdo]

# 🎯 CAUSAS RAIZ
[conteúdo]

# 💡 SOLUÇÕES PRÁTICAS
[código]

# ✅ MELHORES PRÁTICAS
[conteúdo]

# 🏗️ ARQUITETURA & ESCALABILIDADE
[conteúdo]

---
🔧 Debug Info: Model=`gemini-2.5-pro-debug` | Senior=`true`
```

### 4. Teste de Comparação

**Teste A - Sem Debug Mode:**
```
Pergunta: "Por que meu React component não re-renderiza?"
Resposta: ~200 palavras, explicação básica
```

**Teste B - Com Debug Mode:**
```
Pergunta: "Por que meu React component não re-renderiza?"
Resposta: ~800 palavras, análise profunda com:
- Causas raiz
- 3 soluções com código
- Melhores práticas
- Considerações de arquitetura
```

### 5. Teste de Performance

**Passos:**
1. Abra DevTools → Network
2. Ative Debug Mode
3. Envie pergunta complexa
4. Meça tempo de resposta

**Resultado Esperado:**
- Normal: ~500-1000ms
- Debug: ~1500-2500ms
- Aceitável: < 3000ms

### 6. Teste de Erro

**Passos:**
1. Desconecte internet
2. Ative Debug Mode
3. Envie pergunta
4. Verifique fallback

**Resultado Esperado:**
- ✅ Mensagem de erro amigável
- ✅ Não quebra a aplicação
- ✅ Pode tentar novamente

## Testes Automatizados

### Rodar Suite Completa

```bash
# Backend
cd backend
pytest tests/test_debug_mode.py -v

# Resultado esperado:
# test_debug_mode_uses_senior_directly PASSED
# test_normal_mode_uses_junior_first PASSED
# test_debug_mode_prompt_structure PASSED
# test_debug_mode_fallback_on_error PASSED
# test_debug_mode_end_to_end PASSED
```

### Teste Individual

```bash
# Testar apenas um caso
pytest tests/test_debug_mode.py::TestDebugMode::test_debug_mode_uses_senior_directly -v

# Com output detalhado
pytest tests/test_debug_mode.py -v -s
```

### Coverage

```bash
# Gerar relatório de cobertura
pytest --cov=src --cov-report=html tests/test_debug_mode.py

# Abrir relatório
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Testes de Integração

### Teste End-to-End

```bash
# 1. Subir sistema
docker-compose up -d

# 2. Aguardar inicialização
sleep 10

# 3. Testar endpoint
curl -X POST http://localhost:8000/api/sessions/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"

# 4. Enviar pergunta com debug
curl -X POST http://localhost:8000/api/sessions/SESSION_ID/questions \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Como debugar memory leak?",
    "debug_mode": true
  }'
```

### Teste de Carga

```bash
# Instalar Apache Bench
sudo apt-get install apache2-utils  # Linux
brew install ab  # macOS

# Testar 100 requests
ab -n 100 -c 10 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -p request.json \
  http://localhost:8000/api/sessions/SESSION_ID/questions

# request.json:
# {"content": "Test", "debug_mode": true}
```

## Verificações de Qualidade

### 1. Checklist de UX

- [ ] Botão visível e intuitivo
- [ ] Tooltip informativo
- [ ] Animações suaves
- [ ] Feedback visual claro
- [ ] Cores consistentes
- [ ] Responsivo (mobile/desktop)
- [ ] Acessível (keyboard navigation)

### 2. Checklist de Backend

- [ ] Request aceita debug_mode
- [ ] Flag propagado corretamente
- [ ] Senior LLM chamado quando debug=true
- [ ] Junior LLM pulado quando debug=true
- [ ] Resposta estruturada corretamente
- [ ] Metadata incluído (model, used_senior)
- [ ] Logs informativos
- [ ] Tratamento de erros

### 3. Checklist de Qualidade

- [ ] Respostas profundas (>500 palavras)
- [ ] Código completo e funcional
- [ ] Múltiplas soluções apresentadas
- [ ] Trade-offs explicados
- [ ] Melhores práticas incluídas
- [ ] Considerações de arquitetura
- [ ] Formatação markdown correta

## Debugging

### Frontend

```javascript
// Adicionar no Chat.jsx para debug
console.log('Debug Mode:', debugMode);
console.log('Request:', { content, debug_mode: debugMode });

// Ver estado no React DevTools
// Components → Chat → hooks → debugMode
```

### Backend

```python
# Adicionar no chain_validator_service.py
import logging
logger = logging.getLogger(__name__)

logger.info(f"Debug mode: {debug_mode}")
logger.info(f"Using model: {model_name}")
logger.info(f"Response length: {len(response.text)}")
```

### Logs Estruturados

```bash
# Ver apenas logs de debug
docker-compose logs backend | grep "DEBUG"

# Ver chamadas ao LLM
docker-compose logs backend | grep -E "Junior|Senior"

# Ver erros
docker-compose logs backend | grep ERROR

# Ver tudo relacionado a debug
docker-compose logs backend | grep -i debug
```

## Métricas

### Coletar Dados

```python
# Adicionar no backend
import time

start = time.time()
result = llm_service.generate_answer(content, debug_mode=debug_mode)
duration = time.time() - start

logger.info(f"Request completed in {duration:.2f}s [debug={debug_mode}]")
```

### Analisar Logs

```bash
# Tempo médio de resposta
docker-compose logs backend | grep "Request completed" | \
  awk '{print $NF}' | \
  awk '{sum+=$1; count++} END {print "Average:", sum/count "s"}'

# Taxa de uso do debug mode
docker-compose logs backend | grep "debug=" | \
  grep -c "debug=True"
```

## Troubleshooting

### Problema: Botão não aparece

```bash
# Verificar build do frontend
docker-compose logs frontend | grep -i error

# Rebuild
docker-compose up --build frontend
```

### Problema: Debug mode não funciona

```bash
# Verificar request
# DevTools → Network → Payload deve ter debug_mode: true

# Verificar backend
docker-compose logs backend | grep "debug_mode"
```

### Problema: Resposta não estruturada

```bash
# Verificar prompt do Senior LLM
docker-compose exec backend python -c "
from src.infrastructure.llm.senior_llm_service import SeniorLLMService
service = SeniorLLMService()
print(service.debug_model._system_instruction)
"
```

### Problema: Erro 500

```bash
# Ver stack trace completo
docker-compose logs backend --tail=50

# Verificar API key
docker-compose exec backend env | grep GEMINI_API_KEY

# Testar conexão com Gemini
docker-compose exec backend python -c "
import google.generativeai as genai
genai.configure(api_key='YOUR_KEY')
model = genai.GenerativeModel('gemini-2.5-pro')
print(model.generate_content('test'))
"
```

## Checklist Final

Antes de considerar completo:

### Funcionalidade
- [ ] Debug mode ativa/desativa corretamente
- [ ] Request envia flag debug_mode
- [ ] Backend processa flag corretamente
- [ ] Senior LLM é chamado quando debug=true
- [ ] Resposta é estruturada em 5 seções
- [ ] Debug info aparece no final

### UX/UI
- [ ] Botão visível e intuitivo
- [ ] Animações funcionam
- [ ] Tooltip informativo
- [ ] Banner explicativo
- [ ] Cores consistentes
- [ ] Responsivo

### Qualidade
- [ ] Respostas profundas e técnicas
- [ ] Código completo e funcional
- [ ] Múltiplas soluções
- [ ] Melhores práticas
- [ ] Arquitetura e escalabilidade

### Performance
- [ ] Latência < 3s
- [ ] Sem memory leaks
- [ ] Logs informativos
- [ ] Tratamento de erros

### Documentação
- [ ] README atualizado
- [ ] Guias de uso criados
- [ ] Exemplos práticos
- [ ] Documentação técnica
- [ ] Testes documentados

---

## 🎉 Pronto para Produção!

Se todos os testes passaram, o Debug Mode está pronto para uso! 🚀

**Próximo passo:** Coletar feedback dos usuários e iterar.

---

**Desenvolvido com ❤️ pela equipe Focus AI**
