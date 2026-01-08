# 🛡️ Security Checklist - Cerberus AI

## 🔐 1. Gerenciamento de Sessão & Tokens

- [x] **HttpOnly & Secure Cookies**
  - Armazenar Refresh Tokens em cookies com `HttpOnly`, `Secure` e `SameSite=Strict`
  - Access Token permanece em memória (não localStorage)

- [ ] **Access Tokens de Curta Duração**
  - TTL do Access Token: 15-30 minutos
  - ✅ Atual: 7 dias (CRÍTICO - reduzir)

- [ ] **Refresh Token Rotation**
  - Emitir novo Refresh Token a cada uso
  - Invalidar token anterior
  - Detectar reutilização = invalidar toda cadeia

- [ ] **Blacklist/Revogação (Redis)**
  - Lista de bloqueio para invalidar tokens antes da expiração
  - Implementar logout forçado

- [ ] **MFA (Autenticação de Dois Fatores)**
  - TOTP/SMS para ações sensíveis
  - Login suspeito (novo IP/dispositivo)

- [ ] **Bloqueio de Força Bruta**
  - Bloquear conta/IP após 5-10 tentativas falhas
  - ✅ Parcial: Rate limiting existe

---

## 🌐 2. Proteção de API & Headers

- [x] **Rate Limiting**
  - ✅ Implementado: Redis locks por sessão
  - [ ] Adicionar: Rate limit por IP (100 req/min)

- [ ] **CORS Restritivo**
  - ✅ Configurado
  - [ ] Validar: Nunca usar `*` em produção

- [ ] **HSTS (Strict-Transport-Security)**
  - Header: `Strict-Transport-Security: max-age=31536000; includeSubDomains`
  - Forçar HTTPS

- [ ] **CSP (Content Security Policy)**
  - Definir domínios permitidos para scripts/imagens/estilos
  - Mitigar XSS

- [ ] **X-Content-Type-Options**
  - Header: `X-Content-Type-Options: nosniff`
  - Prevenir upload de script disfarçado

---

## 💻 3. Validação de Dados & Código (OWASP Top 10)

- [x] **Sanitização de Input**
  - ✅ Pydantic para validação de schema
  - ✅ Sanitizer implementado

- [ ] **Output Encoding**
  - Escapar caracteres especiais no front-end
  - Prevenir XSS

- [x] **Prepared Statements/ORM**
  - ✅ SQLAlchemy ORM (sem concatenação SQL)

- [ ] **Tratamento de Erros Genérico**
  - ✅ Parcial: Mensagens genéricas
  - [ ] Validar: Nunca expor stack traces em produção

- [ ] **Verificação de Dependências**
  - Usar `pip-audit` (Python) e `npm audit` (JS)
  - Automatizar em CI/CD

---

## 🔒 4. Dados Sensíveis & Operacional

- [ ] **Logs Sanitizados**
  - Mascarar automaticamente: senhas, tokens, CPFs
  - Configurar logger com filtros

- [ ] **Least Privilege (Banco de Dados)**
  - Usuário da aplicação: apenas READ/WRITE nas tabelas necessárias
  - Sem permissões DROP/ALTER/GRANT

- [x] **Segredos Fora do Código**
  - ✅ `.env` para credenciais
  - ✅ `.env` no `.gitignore`

- [x] **Senhas Hasheadas**
  - ✅ bcrypt implementado

---

## 🚨 Prioridades Críticas

### 🔴 URGENTE (Implementar Agora)
1. **Reduzir TTL do Access Token** (7 dias → 15-30 min)
2. **Implementar Refresh Token com Rotation**
3. **Adicionar Headers de Segurança** (HSTS, CSP, X-Content-Type-Options)

### 🟡 ALTA (Próxima Sprint)
4. **Blacklist de Tokens (Redis)**
5. **Rate Limiting por IP**
6. **Logs Sanitizados**
7. **Least Privilege no PostgreSQL**

### 🟢 MÉDIA (Roadmap)
8. **MFA (TOTP)**
9. **Verificação Automática de Dependências**
10. **Output Encoding no Frontend**

---

## 📋 Comandos Úteis

```bash
# Verificar vulnerabilidades (Backend)
pip-audit

# Verificar vulnerabilidades (Frontend)
npm audit

# Testar headers de segurança
curl -I https://cerberus-ai.com

# Verificar CORS
curl -H "Origin: https://malicious.com" https://api.cerberus-ai.com
```

---

**Última Atualização:** 2025-01-07  
**Status:** 6/24 itens completos (25%)
