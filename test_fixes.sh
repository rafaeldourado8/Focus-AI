#!/bin/bash

# Script de Teste - Bugs Críticos Corrigidos
# Cerberus AI - Frontend

echo "🧪 Testando correções de bugs críticos..."
echo ""

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contador
PASSED=0
FAILED=0

# Função de teste
test_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $2"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $2"
        ((FAILED++))
    fi
}

test_content() {
    if grep -q "$2" "$1" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $3"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $3"
        ((FAILED++))
    fi
}

echo "📁 Verificando arquivos criados..."
test_file "frontend/src/hooks/useAxios.js" "Hook useAxios criado"
test_file "frontend/src/components/StopButton.jsx" "Componente StopButton criado"
test_file "frontend/CRITICAL_FIXES.md" "Documentação de fixes criada"
test_file "BUGS_FIXED.md" "Documentação completa criada"

echo ""
echo "🔍 Verificando implementações..."

# App.jsx - Token validation
test_content "frontend/src/App.jsx" "validateToken" "Token validation implementado"
test_content "frontend/src/App.jsx" "useAxiosInterceptor" "Interceptor integrado no App"

# Chat.jsx - Persistência
test_content "frontend/src/components/Chat.jsx" "localStorage.getItem('sessionId')" "SessionId persistence implementado"
test_content "frontend/src/components/Chat.jsx" "autoScroll" "Auto-scroll inteligente implementado"
test_content "frontend/src/components/Chat.jsx" "messagesContainerRef" "Ref para container de mensagens"

# Dashboard.jsx - Empty states
test_content "frontend/src/components/Dashboard.jsx" "isEmpty" "Empty states implementados"
test_content "frontend/src/components/Dashboard.jsx" "Comece sua jornada" "Mensagem encorajadora"

# index.html - Loading screen
test_content "frontend/index.html" "loading-screen" "Loading screen implementado"
test_content "frontend/index.html" "@keyframes spin" "Animação de loading"

# vite.config.js - Produção
test_content "frontend/vite.config.js" "drop_console" "Console.log removido em produção"
test_content "frontend/vite.config.js" "sourcemap" "Sourcemaps configurados"

echo ""
echo "📊 Resultados:"
echo -e "${GREEN}Passou: $PASSED${NC}"
echo -e "${RED}Falhou: $FAILED${NC}"

if [ $FAILED -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Todos os testes passaram!${NC}"
    echo ""
    echo "🚀 Próximos passos:"
    echo "1. npm install (se necessário)"
    echo "2. npm run dev (testar localmente)"
    echo "3. Testar fluxos manualmente:"
    echo "   - Login com token inválido"
    echo "   - F5 durante chat"
    echo "   - Auto-scroll durante resposta"
    echo "   - Dashboard vazio"
    exit 0
else
    echo ""
    echo -e "${RED}❌ Alguns testes falharam${NC}"
    echo "Verifique os arquivos acima"
    exit 1
fi
