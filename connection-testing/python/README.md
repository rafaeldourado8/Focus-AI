# Python Client - Cerberus AI

## Setup

```bash
pip install -r requirements.txt
```

## Obter API Key

### Opção 1: Via Dashboard (Recomendado)
1. Acesse http://localhost:3000
2. Faça login com Google
3. Vá em "API Keys"
4. Clique em "Nova API Key"
5. Copie a key gerada

### Opção 2: Via Script
```bash
cd ../../backend
python -m src.infrastructure.database.connection  # Inicializa DB
cd ../connection-testing/python
python create_api_key.py
```

## Testes

### 1. Teste de Conectividade (sem API key)
```bash
python test_connection.py
```

### 2. Teste Completo (com API key)
```bash
# Edite test_api.py e substitua:
API_KEY = "sua-api-key-aqui"

python test_api.py
```

## Uso

```python
from test_api import CerberusClient

client = CerberusClient("sua-api-key")

# Chat
answer = client.ask("Como implementar JWT?")
print(answer['choices'][0]['message']['content'])

# Análise de código
result = client.analyze_code(
    code="def hello(): pass",
    language="python"
)

# Debug
debug = client.debug_code(
    error="NullPointerException",
    code="String s = null; s.length();",
    language="java"
)

# Listar modelos
models = client.get_models()
```
