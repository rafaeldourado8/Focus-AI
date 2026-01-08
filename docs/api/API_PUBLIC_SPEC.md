# 🔌 API PÚBLICA - CERBERUS AI

## Visão Geral

API RESTful para integração da Cerberus AI em aplicações externas (WhatsApp bots, Slack, VS Code, etc).

---

## 🔑 AUTENTICAÇÃO

### API Keys

```http
POST /v1/auth/keys
Authorization: Bearer <JWT_TOKEN>

Response:
{
  "api_key": "ck_live_abc123...",
  "name": "WhatsApp Bot Prod",
  "plan": "pro",
  "rate_limit": 60,
  "created_at": "2024-01-15T10:00:00Z"
}
```

### Uso da API Key

```http
POST /v1/chat/completions
Authorization: Bearer ck_live_abc123...
Content-Type: application/json
```

---

## 📡 ENDPOINTS

### 1. Chat Completions (Compatível com OpenAI)

```http
POST /v1/chat/completions
```

**Request:**
```json
{
  "model": "cerberus-pro",
  "messages": [
    {"role": "system", "content": "Você é um assistente de código."},
    {"role": "user", "content": "Como fazer async/await em Python?"}
  ],
  "temperature": 0.7,
  "max_tokens": 2048,
  "stream": false,
  "debug_mode": false
}
```

**Response:**
```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1705315200,
  "model": "cerberus-pro",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Em Python, async/await é usado para...\n\n```python\nimport asyncio\n\nasync def main():\n    await asyncio.sleep(1)\n```"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 150,
    "total_tokens": 175
  },
  "metadata": {
    "model_used": "cerberus-v1.2",
    "cache_hit": false,
    "latency_ms": 1250
  }
}
```

---

### 2. Code Analysis

```http
POST /v1/code/analyze
```

**Request:**
```json
{
  "code": "def foo():\n    x = 1\n    return x",
  "language": "python",
  "checks": ["security", "performance", "style"]
}
```

**Response:**
```json
{
  "issues": [
    {
      "type": "style",
      "severity": "low",
      "line": 1,
      "message": "Function name should be more descriptive",
      "suggestion": "Rename 'foo' to describe its purpose"
    }
  ],
  "score": 85,
  "summary": "Code is generally good, minor style improvements suggested"
}
```

---

### 3. Debug Assistant

```http
POST /v1/code/debug
```

**Request:**
```json
{
  "error": "TypeError: cannot read property 'map' of undefined",
  "code": "const items = data.items;\nconst names = items.map(i => i.name);",
  "language": "javascript",
  "context": "React component fetching API data"
}
```

**Response:**
```json
{
  "diagnosis": {
    "root_cause": "data.items is undefined, likely API response issue",
    "explanation": "The error occurs because 'items' doesn't exist on 'data' object..."
  },
  "solutions": [
    {
      "title": "Optional Chaining",
      "code": "const names = data?.items?.map(i => i.name) ?? [];",
      "pros": ["Safe", "Concise"],
      "cons": ["Requires modern JS"]
    },
    {
      "title": "Defensive Check",
      "code": "const items = data.items || [];\nconst names = items.map(i => i.name);",
      "pros": ["Compatible", "Clear"],
      "cons": ["More verbose"]
    }
  ],
  "best_practices": [
    "Always validate API responses",
    "Use TypeScript for type safety"
  ]
}
```

---

### 4. Code Refactor

```http
POST /v1/code/refactor
```

**Request:**
```json
{
  "code": "function calc(a,b,op){if(op=='add')return a+b;if(op=='sub')return a-b;}",
  "language": "javascript",
  "goals": ["readability", "maintainability"]
}
```

**Response:**
```json
{
  "refactored_code": "function calculate(a, b, operation) {\n  const operations = {\n    add: (x, y) => x + y,\n    sub: (x, y) => x - y\n  };\n  return operations[operation](a, b);\n}",
  "improvements": [
    "Used descriptive parameter names",
    "Replaced if-else with strategy pattern",
    "Added proper formatting"
  ],
  "patterns_applied": ["Strategy Pattern", "Object Literal"]
}
```

---

### 5. List Models

```http
GET /v1/models
```

**Response:**
```json
{
  "models": [
    {
      "id": "cerberus-lite",
      "name": "Cerberus Lite",
      "description": "Fast responses, general coding",
      "max_tokens": 2048,
      "cost_per_1k_tokens": 0.0001,
      "available_in": ["free", "pro", "enterprise"]
    },
    {
      "id": "cerberus-pro",
      "name": "Cerberus Pro",
      "description": "Advanced debugging and architecture",
      "max_tokens": 8192,
      "cost_per_1k_tokens": 0.001,
      "available_in": ["pro", "enterprise"]
    },
    {
      "id": "cerberus-ultra",
      "name": "Cerberus Ultra",
      "description": "Our fine-tuned model for complex tasks",
      "max_tokens": 16384,
      "cost_per_1k_tokens": 0.0005,
      "available_in": ["enterprise"]
    }
  ]
}
```

---

### 6. Usage Stats

```http
GET /v1/usage?start_date=2024-01-01&end_date=2024-01-31
```

**Response:**
```json
{
  "period": {
    "start": "2024-01-01",
    "end": "2024-01-31"
  },
  "total_requests": 15420,
  "total_tokens": 2340000,
  "cost": 234.50,
  "breakdown": {
    "cerberus-lite": {
      "requests": 12000,
      "tokens": 1800000,
      "cost": 180.00
    },
    "cerberus-pro": {
      "requests": 3420,
      "tokens": 540000,
      "cost": 54.50
    }
  },
  "daily_usage": [
    {"date": "2024-01-01", "requests": 450, "tokens": 68000},
    {"date": "2024-01-02", "requests": 520, "tokens": 75000}
  ]
}
```

---

## 🚦 RATE LIMITS

| Plan | Requests/min | Requests/day | Burst |
|------|--------------|--------------|-------|
| Free | 10 | 100 | 20 |
| Pro | 60 | 10,000 | 100 |
| Enterprise | 300 | Unlimited | 500 |

**Headers de Rate Limit:**
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1705315260
```

**Resposta quando exceder:**
```json
{
  "error": {
    "type": "rate_limit_exceeded",
    "message": "Rate limit exceeded. Retry after 30 seconds.",
    "retry_after": 30
  }
}
```

---

## 💰 PRICING

### Tokens
- **Input tokens**: $0.0001 / 1K tokens
- **Output tokens**: $0.0002 / 1K tokens

### Modelos
- **cerberus-lite**: $0.0001 / 1K tokens
- **cerberus-pro**: $0.001 / 1K tokens
- **cerberus-ultra**: $0.0005 / 1K tokens (modelo próprio)

### Planos Mensais
```
FREE: $0
- 100 req/dia
- Só cerberus-lite

PRO: $29/mês
- 10k req/dia inclusos
- Todos os modelos
- $0.003 por req adicional

ENTERPRISE: Custom
- Volume ilimitado
- SLA 99.9%
- Suporte dedicado
- On-premise option
```

---

## 🔒 SEGURANÇA

### HTTPS Only
Todas as requisições devem usar HTTPS.

### API Key Rotation
```http
POST /v1/auth/keys/{key_id}/rotate

Response:
{
  "old_key": "ck_live_abc123...",
  "new_key": "ck_live_xyz789...",
  "expires_at": "2024-02-15T10:00:00Z"
}
```

### IP Whitelist (Enterprise)
```http
POST /v1/auth/keys/{key_id}/whitelist
{
  "ips": ["203.0.113.0/24", "198.51.100.42"]
}
```

---

## 📚 SDKs

### Python
```python
from cerberus_ai import CerberusClient

client = CerberusClient(api_key="ck_live_abc123...")

response = client.chat.completions.create(
    model="cerberus-pro",
    messages=[
        {"role": "user", "content": "Explique async/await"}
    ]
)

print(response.choices[0].message.content)
```

### JavaScript/TypeScript
```typescript
import { CerberusAI } from '@cerberus-ai/sdk';

const cerberus = new CerberusAI({
  apiKey: process.env.CERBERUS_API_KEY
});

const response = await cerberus.chat.completions.create({
  model: 'cerberus-pro',
  messages: [
    { role: 'user', content: 'Explique async/await' }
  ]
});

console.log(response.choices[0].message.content);
```

---

## 🤖 EXEMPLOS DE INTEGRAÇÃO

### WhatsApp Bot (Twilio)
```python
from twilio.rest import Client
from cerberus_ai import CerberusClient

cerberus = CerberusClient(api_key="...")
twilio = Client(account_sid, auth_token)

def handle_message(from_number, message):
    response = cerberus.chat.completions.create(
        model="cerberus-lite",
        messages=[{"role": "user", "content": message}]
    )
    
    twilio.messages.create(
        body=response.choices[0].message.content,
        from_='whatsapp:+14155238886',
        to=f'whatsapp:{from_number}'
    )
```

### Slack Bot
```javascript
const { App } = require('@slack/bolt');
const { CerberusAI } = require('@cerberus-ai/sdk');

const cerberus = new CerberusAI({ apiKey: process.env.CERBERUS_API_KEY });
const app = new App({ token: process.env.SLACK_BOT_TOKEN });

app.message(async ({ message, say }) => {
  const response = await cerberus.chat.completions.create({
    model: 'cerberus-pro',
    messages: [{ role: 'user', content: message.text }]
  });
  
  await say(response.choices[0].message.content);
});
```

### VS Code Extension
```typescript
import * as vscode from 'vscode';
import { CerberusAI } from '@cerberus-ai/sdk';

const cerberus = new CerberusAI({ apiKey: config.get('apiKey') });

vscode.commands.registerCommand('cerberus.explain', async () => {
  const editor = vscode.window.activeTextEditor;
  const selection = editor.document.getText(editor.selection);
  
  const response = await cerberus.chat.completions.create({
    model: 'cerberus-pro',
    messages: [
      { role: 'system', content: 'Explain code clearly' },
      { role: 'user', content: `Explain:\n${selection}` }
    ]
  });
  
  vscode.window.showInformationMessage(response.choices[0].message.content);
});
```

---

## 🐛 ERROR HANDLING

### Error Response Format
```json
{
  "error": {
    "type": "invalid_request_error",
    "message": "Missing required parameter: messages",
    "param": "messages",
    "code": "missing_parameter"
  }
}
```

### Error Types
- `invalid_request_error` - Parâmetros inválidos
- `authentication_error` - API key inválida
- `rate_limit_error` - Rate limit excedido
- `server_error` - Erro interno (500)
- `service_unavailable` - Serviço temporariamente indisponível (503)

### Retry Logic
```python
import time
from cerberus_ai import CerberusClient, RateLimitError

client = CerberusClient(api_key="...")

def call_with_retry(max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(...)
        except RateLimitError as e:
            if attempt < max_retries - 1:
                time.sleep(e.retry_after)
            else:
                raise
```

---

## 📊 WEBHOOKS (Futuro)

### Configuração
```http
POST /v1/webhooks
{
  "url": "https://myapp.com/cerberus-webhook",
  "events": ["completion.created", "usage.threshold"]
}
```

### Payload
```json
{
  "event": "completion.created",
  "timestamp": "2024-01-15T10:00:00Z",
  "data": {
    "id": "chatcmpl-abc123",
    "model": "cerberus-pro",
    "tokens_used": 175
  }
}
```

---

## 🚀 PRÓXIMOS PASSOS

1. Implementar API Gateway (FastAPI)
2. Sistema de API Keys (PostgreSQL)
3. Rate Limiting (Redis)
4. SDKs Python e JavaScript
5. Documentação interativa (Swagger)
6. Exemplos de integração
7. Marketplace de templates
