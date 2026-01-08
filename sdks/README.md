# 📦 CERBERUS AI SDKs

Official SDKs and integration examples for Cerberus AI API.

---

## 🐍 Python SDK

### Installation
```bash
pip install cerberus-ai-python
```

### Usage
```python
from cerberus_ai import CerberusAI

cerberus = CerberusAI(api_key="ck_live_...")

# Chat completion
response = cerberus.chat_completion(
    messages=[
        {"role": "user", "content": "Explain async/await in Python"}
    ],
    model="cerberus-pro"
)

print(response["choices"][0]["message"]["content"])

# Code analysis
analysis = cerberus.analyze_code(
    code="def foo(): pass",
    language="python"
)

# Debug code
debug_info = cerberus.debug_code(
    error="TypeError: cannot read property",
    code="const x = null; x.map()",
    language="javascript"
)
```

---

## 📦 JavaScript/TypeScript SDK

### Installation
```bash
npm install @cerberus-ai/sdk
```

### Usage
```typescript
import { CerberusAI } from '@cerberus-ai/sdk';

const cerberus = new CerberusAI('ck_live_...');

// Chat completion
const response = await cerberus.chatCompletion([
  { role: 'user', content: 'Explain async/await in JavaScript' }
], { model: 'cerberus-pro' });

console.log(response.choices[0].message.content);

// Code analysis
const analysis = await cerberus.analyzeCode(
  'function foo() {}',
  'javascript'
);

// Debug code
const debugInfo = await cerberus.debugCode(
  'TypeError: cannot read property',
  'const x = null; x.map()',
  'javascript'
);
```

---

## 🤖 Integration Examples

### WhatsApp Bot (Twilio)
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

### Slack Bot
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

### CLI Tool
```bash
# Install
pip install cerberus-ai-python

# Usage
export CERBERUS_API_KEY="ck_live_..."
cerberus chat "How to use async/await?"
cerberus debug main.py
cerberus analyze app.js
cerberus models
cerberus usage
```

---

## 📚 API Reference

### Chat Completion
```python
cerberus.chat_completion(
    messages: List[Dict[str, str]],
    model: str = "cerberus-pro",
    temperature: float = 0.7,
    max_tokens: int = 2048,
    debug_mode: bool = False
)
```

### Code Analysis
```python
cerberus.analyze_code(
    code: str,
    language: str,
    checks: List[str] = ["security", "performance", "style"]
)
```

### Code Debug
```python
cerberus.debug_code(
    error: str,
    code: str,
    language: str,
    context: Optional[str] = None
)
```

### Code Refactor
```python
cerberus.refactor_code(
    code: str,
    language: str,
    goals: List[str] = ["readability", "maintainability"]
)
```

### List Models
```python
cerberus.list_models()
```

### Get Usage
```python
cerberus.get_usage()
```

---

## 🔑 Authentication

Get your API key from the Cerberus AI dashboard:
1. Login to https://cerberus-ai.com
2. Go to Settings → API Keys
3. Create new key
4. Copy and use in your code

---

## 📖 More Examples

See `examples/` directory for:
- WhatsApp bot (Twilio)
- Slack bot
- Discord bot
- VS Code extension
- CLI tool

---

**Cerberus AI** - Developer Assistant by Focus AI
