#!/bin/bash

echo "🚀 Iniciando setup do Ollama..."

# Aguarda Ollama estar pronto
echo "⏳ Aguardando Ollama iniciar..."
until curl -s http://localhost:11434 > /dev/null; do
    sleep 2
done

echo "✅ Ollama está rodando!"

# Baixa modelo Llama 3
echo "📦 Baixando modelo Llama 3 (pode demorar alguns minutos)..."
ollama pull llama3

echo "✅ Setup completo! Modelo Llama 3 pronto para uso."
