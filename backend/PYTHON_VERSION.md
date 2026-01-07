# IMPORTANTE: Use Python 3.11 ou 3.12

## Problema
Python 3.14 é muito novo e muitas bibliotecas não têm wheels pré-compilados.

## Solução

1. Desinstale Python 3.14
2. Instale Python 3.11 ou 3.12 de https://www.python.org/downloads/
3. Recrie o ambiente virtual:

```bash
# Remova o venv atual
rm -rf venv

# Crie novo venv com Python 3.11/3.12
python -m venv venv

# Ative
venv\Scripts\activate

# Instale dependências
pip install --upgrade pip
pip install psycopg2-binary
pip install -r requirements.txt
```

## Alternativa Rápida (sem recriar venv)

Instale wheels pré-compilados manualmente:

```bash
pip install --only-binary :all: pydantic
pip install --only-binary :all: fastapi
pip install -r requirements.txt
```