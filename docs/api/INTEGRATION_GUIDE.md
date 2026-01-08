# 🚀 GUIA DE INTEGRAÇÃO - CERBERUS AI

Guia completo para integrar Cerberus AI em suas aplicações.

---

## 📋 Pré-requisitos

1. **Conta Cerberus AI**: Crie em https://cerberus-ai.com
2. **API Key**: Gere em Settings → API Keys
3. **Plano**: Free, Pro ou Enterprise

---

## 🔑 Autenticação

Todas as requisições requerem API key no header:

```http
Authorization: Bearer ck_live_your_api_key_here
```

### Tipos de API Keys

- `ck_test_...` - Plano Free (10 req/min)
- `ck_live_...` - Planos Pro/Enterprise (60-300 req/min)

---

## 🐍 Integração Python

### Instalação
```bash
pip install cerberus-ai-python
```

### Uso Básico
```python
from cerberus_ai import CerberusAI

cerberus = CerberusAI(api_key="ck_live_...")

# Chat
response = cerberus.chat_completion([
    {"role": "user", "content": "Explain async/await"}
])
print(response["choices"][0]["message"]["content"])

# Debug
debug_info = cerberus.debug_code(
    error="TypeError: cannot read property",
    code="const x = null; x.map()",
    language="javascript"
)
```

---

## 📦 Integração JavaScript

### Instalação
```bash
npm install @cerberus-ai/sdk
```

### Uso Básico
```javascript
import { CerberusAI } from '@cerberus-ai/sdk';

const cerberus = new CerberusAI('ck_live_...');

// Chat
const response = await cerberus.chatCompletion([
  { role: 'user', content: 'Explain async/await' }
]);
console.log(response.choices[0].message.content);

// Debug
const debugInfo = await cerberus.debugCode(
  'TypeError: cannot read property',
  'const x = null; x.map()',
  'javascript'
);
```

---

## 🌐 Integração REST API

### Chat Completion
```bash
curl -X POST https://api.cerberus-ai.com/v1/chat/completions \
  -H "Authorization: Bearer ck_live_..." \
  -H "Content-Type: application/json" \
  -d '{
    "model": "cerberus-pro",
    "messages": [
      {"role": "user", "content": "Explain async/await"}
    ]
  }'
```

### Code Analysis
```bash
curl -X POST https://api.cerberus-ai.com/v1/code/analyze \
  -H "Authorization: Bearer ck_live_..." \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def foo(): pass",
    "language": "python",
    "checks": ["security", "performance"]
  }'
```

---

## 🤖 Casos de Uso

### 1. WhatsApp Bot
```python
from cerberus_ai import CerberusAI
from twilio.rest import Client

cerberus = CerberusAI(api_key="...")
twilio = Client(account_sid, auth_token)

def handle_message(from_number, message):
    response = cerberus.chat_completion([
        {"role": "user", "content": message}
    ])
    
    twilio.messages.create(
        body=response["choices"][0]["message"]["content"],
        from_=f'whatsapp:+14155238886',
        to=f'whatsapp:{from_number}'
    )
```

### 2. Slack Bot
```javascript
const { App } = require('@slack/bolt');
const { CerberusAI } = require('@cerberus-ai/sdk');

const cerberus = new CerberusAI(process.env.CERBERUS_API_KEY);
const app = new App({ token: process.env.SLACK_BOT_TOKEN });

app.event('app_mention', async ({ event, say }) => {
  const response = await cerberus.chatCompletion([
    { role: 'user', content: event.text }
  ]);
  
  await say(response.choices[0].message.content);
});
```

### 3. VS Code Extension
```javascript
const vscode = require('vscode');
const { CerberusAI } = require('@cerberus-ai/sdk');

const cerberus = new CerberusAI(apiKey);

vscode.commands.registerCommand('cerberus.explain', async () => {
  const editor = vscode.window.activeTextEditor;
  const selection = editor.document.getText(editor.selection);
  
  const response = await cerberus.chatCompletion([
    { role: 'user', content: `Explain: ${selection}` }
  ]);
  
  vscode.window.showInformationMessage(response.choices[0].message.content);
});
```

---

## ⚡ Rate Limits

| Plano | Req/min | Req/dia | Burst |
|-------|---------|---------|-------|
| Free | 10 | 100 | 20 |
| Pro | 60 | 10,000 | 100 |
| Enterprise | 300 | Unlimited | 500 |

### Headers de Rate Limit
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1705315260
```

### Tratamento de Rate Limit
```python
import time

def call_with_retry(cerberus, messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            return cerberus.chat_completion(messages)
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise
```

---

## 🔒 Segurança

### Boas Práticas

1. **Nunca exponha API keys**
```python
# ✅ Correto
api_key = os.getenv("CERBERUS_API_KEY")

# ❌ Errado
api_key = "ck_live_abc123..."  # Hardcoded
```

2. **Use HTTPS**
```python
cerberus = CerberusAI(
    api_key="...",
    base_url="https://api.cerberus-ai.com"  # HTTPS
)
```

3. **Rotacione keys regularmente**
```bash
# Via API
curl -X POST https://api.cerberus-ai.com/api/keys/{key}/rotate \
  -H "Authorization: Bearer jwt_token"
```

---

## 📊 Monitoramento

### Verificar Uso
```python
usage = cerberus.get_usage()
print(f"Total requests: {usage['total_requests']}")
print(f"Rate limit: {usage['rate_limit']} req/min")
```

### Listar Modelos
```python
models = cerberus.list_models()
for model in models["models"]:
    print(f"{model['name']}: ${model['cost_per_1k_tokens']}/1K tokens")
```

---

## 🐛 Troubleshooting

### Erro 401 - Unauthorized
```
Causa: API key inválida ou expirada
Solução: Verifique a key ou gere uma nova
```

### Erro 429 - Rate Limit
```
Causa: Muitas requisições
Solução: Implemente retry com backoff exponencial
```

### Erro 500 - Server Error
```
Causa: Erro interno
Solução: Tente novamente ou contate suporte
```

---

## 📚 Recursos

- **Documentação**: https://docs.cerberus-ai.com
- **Swagger UI**: http://localhost:8000/docs
- **Postman Collection**: [Download](postman_collection.json)
- **SDKs**: Python, JavaScript/TypeScript
- **Exemplos**: WhatsApp, Slack, Discord, VS Code

---

## 💬 Suporte

- **Email**: support@cerberus-ai.com
- **Discord**: https://discord.gg/cerberus-ai
- **GitHub**: https://github.com/focus-ai/cerberus-ai

---

**Cerberus AI** - Developer Assistant by Focus AI
