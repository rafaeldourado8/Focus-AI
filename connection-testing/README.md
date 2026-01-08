# Connection Testing - Cerberus AI

Testes de integração para validar acesso à API pública do Cerberus AI.

## Estrutura

```
connection-testing/
├── python/          # Cliente Python
├── nodejs/          # Cliente Node.js
├── whatsapp-bot/    # Bot WhatsApp (exemplo)
└── postman/         # Collection Postman
```

## Casos de Teste

1. **Autenticação** - Validar API Key
2. **Criar Sessão** - Iniciar conversa
3. **Enviar Pergunta** - Processar query
4. **Histórico** - Recuperar mensagens
5. **Rate Limiting** - Validar limites

## Quick Start

### Python
```bash
cd python
pip install -r requirements.txt
python test_api.py
```

### Node.js
```bash
cd nodejs
npm install
node test_api.js
```

### WhatsApp Bot
```bash
cd whatsapp-bot
npm install
node bot.js
```
