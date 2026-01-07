#!/bin/sh
set -e

echo "🔍 Aguardando PostgreSQL..."
until PGPASSWORD=focus123 psql -h postgres -U focus -d focusai -c '\q' 2>/dev/null; do
  echo "⏳ PostgreSQL não está pronto - aguardando..."
  sleep 2
done
echo "✅ PostgreSQL pronto!"

echo "🔍 Aguardando Redis..."
until redis-cli -h redis ping 2>/dev/null; do
  echo "⏳ Redis não está pronto - aguardando..."
  sleep 2
done
echo "✅ Redis pronto!"

echo "🗄️  Executando migrations..."
alembic upgrade head

echo "🚀 Iniciando servidor FastAPI..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000
