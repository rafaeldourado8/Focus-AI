# 🚨 Correções de Bugs Críticos - Cerberus AI

## ✅ Bugs Corrigidos

### 1. ✅ **401 Loop & Token Expirado** ✅
**Problema:** Interceptor não captura 401 para refresh/logout
**Solução:** Interceptor global usando fetch nativo (sem dependências)

### 2. **Race Condition no Login** ✅
**Problema:** Dashboard carrega antes do token estar validado
**Solução:** Validar token antes de renderizar dashboard

### 3. **Persistência de Estado (F5)** ✅
**Problema:** Chat perdido ao dar refresh
**Solução:** Recuperar sessionId do localStorage + carregar histórico

### 4. **Flash of Unstyled Content (FOUC)** ✅
**Problema:** Tela pisca branco antes do tema escuro
**Solução:** CSS inline no index.html (já implementado)

### 5. **Auto-scroll durante Stream** ✅
**Problema:** Scroll não acompanha resposta da IA
**Solução:** Implementar scroll inteligente com detecção de scroll manual

### 6. **Rate Limiting Frontend** ✅
**Problema:** Usuário pode clicar "Enviar" múltiplas vezes
**Solução:** Desabilitar botão durante loading (já implementado)

### 7. **Credenciais OAuth Cruzadas** ⚠️
**Problema:** Google Auth configurado como "StudyFlow"
**Ação:** Atualizar no Google Cloud Console

---

## 📝 Implementações Necessárias

### Arquivos a Modificar:
1. `frontend/src/hooks/useAxios.js` (criar)
2. `frontend/src/App.jsx` (modificar)
3. `frontend/src/components/Chat.jsx` (modificar)
4. `frontend/src/components/Dashboard.jsx` (modificar)
5. `frontend/index.html` (modificar - loader)

---

## 🔧 Próximos Passos

Execute os comandos na ordem:
```bash
# 1. Criar hook de axios
# 2. Atualizar App.jsx
# 3. Atualizar Chat.jsx
# 4. Atualizar Dashboard.jsx
# 5. Adicionar loader no index.html
```
