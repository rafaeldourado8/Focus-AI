#!/bin/bash

echo "🚀 Focus AI - Setup Rápido"
echo ""

# Verificar se .env existe
if [ ! -f .env ]; then
    echo "⚠️  Arquivo .env não encontrado!"
    echo "📋 Copiando .env.example para .env..."
    cp .env.example .env
    echo "✅ Arquivo .env criado. Configure sua OPENAI_API_KEY!"
    echo ""
fi

# Subir containers
echo "🐳 Iniciando containers Docker..."
docker-compose up -d postgres redis

# Aguardar PostgreSQL
echo "⏳ Aguardando PostgreSQL inicializar..."
sleep 5

# Instalar dependências
echo "📦 Instalando dependências Python..."
cd backend
pip install -r requirements.txt

# Executar migrations
echo "🗄️  Executando migrations do banco de dados..."
alembic upgrade head

echo ""
echo "✅ Setup completo!"
echo ""
echo "Para iniciar o sistema completo:"
echo "  docker-compose up --build"
echo ""
echo "Endpoints:"
echo "  - Backend: http://localhost:8000"
echo "  - Frontend: http://localhost:3000"
echo "  - PostgreSQL: localhost:5432"
echo "  - Redis: localhost:6379"
echo ""
