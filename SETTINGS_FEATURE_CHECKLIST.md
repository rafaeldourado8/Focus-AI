# Settings Feature - Checklist de Implementação

## 🎯 Objetivo
Implementar sistema completo de configurações de usuário com persistência, sincronização e autenticação híbrida (Google + Email/Senha).

---

## ✅ Fase 1: Correção de Bugs Críticos

### 1.1 Perfil - Nome do Usuário
- [x] Migration 006 criada (colunas: name, debug_mode, language, notifications)
- [x] Modelo SQLAlchemy atualizado
- [ ] **UserRepository._to_domain() incluir novos campos**
- [ ] **Testar salvamento do nome**
- [ ] **Testar carregamento do nome**

### 1.2 Debug Mode
- [x] Backend aceita debug_mode no endpoint
- [x] Frontend envia debug_mode para API
- [x] Chat carrega debug_mode das configurações
- [ ] **Verificar se debug_mode está sendo salvo no banco**
- [ ] **Testar sincronização entre Settings e Chat**
- [ ] **Validar análise técnica profunda quando ativo**

### 1.3 Idioma
- [x] Campo language no banco de dados
- [x] Dropdown no frontend (pt-BR, en-US, es-ES)
- [ ] **Backend salvar idioma corretamente**
- [ ] **Frontend aplicar idioma nas respostas**
- [ ] **Passar idioma para LLM service**
- [ ] **Testar mudança de idioma em tempo real**

### 1.4 Notificações
- [x] Campo notifications no banco
- [x] Toggle no frontend
- [ ] **Backend salvar preferência**
- [ ] **Configurar SMTP (SendGrid/AWS SES)**
- [ ] **Implementar envio de emails**
- [ ] **Testar notificação de boas-vindas**
- [ ] **Testar notificação de novos recursos**

---

## 🔐 Fase 2: Autenticação Híbrida

### 2.1 Estrutura de Dados
- [ ] **Adicionar campo `auth_provider` (google, email, both)**
- [ ] **Adicionar campo `google_id` (nullable)**
- [ ] **Migration para novos campos**
- [ ] **Atualizar modelo User**

### 2.2 Login Convencional (Email/Senha)
- [ ] **Endpoint POST /api/auth/register**
  - Validar email único
  - Hash senha com bcrypt
  - Enviar email de ativação
  - Retornar tokens JWT
- [ ] **Endpoint POST /api/auth/login**
  - Validar credenciais
  - Verificar conta ativa
  - Retornar tokens JWT
- [ ] **Endpoint POST /api/auth/activate**
  - Validar código de ativação
  - Ativar conta
- [ ] **Frontend: Tela de Registro**
- [ ] **Frontend: Tela de Login**
- [ ] **Frontend: Tela de Ativação**

### 2.3 Alterar Senha
- [ ] **Endpoint PUT /api/auth/change-password**
  - Validar senha atual
  - Validar nova senha (min 8 chars)
  - Hash nova senha
  - Atualizar banco
- [ ] **Endpoint POST /api/auth/forgot-password**
  - Gerar token de reset
  - Enviar email com link
- [ ] **Endpoint POST /api/auth/reset-password**
  - Validar token
  - Atualizar senha
- [ ] **Frontend: Modal de Alterar Senha**
- [ ] **Frontend: Tela de Esqueci Senha**
- [ ] **Frontend: Tela de Reset Senha**

### 2.4 Integração Google Auth
- [ ] **Manter endpoint POST /api/auth/google**
- [ ] **Salvar google_id ao autenticar**
- [ ] **Permitir vincular conta Google a conta existente**
- [ ] **Permitir desvincular conta Google**

---

## 🧪 Fase 3: Testes Automatizados

### 3.1 Testes Backend (pytest)
- [ ] **test_user_settings_update.py**
  - Testar atualização de nome
  - Testar atualização de debug_mode
  - Testar atualização de language
  - Testar atualização de notifications
  - Testar validação de dados
- [ ] **test_auth_email_password.py**
  - Testar registro
  - Testar login
  - Testar ativação
  - Testar senha incorreta
  - Testar email duplicado
- [ ] **test_change_password.py**
  - Testar alteração com senha correta
  - Testar senha atual incorreta
  - Testar senha fraca
- [ ] **test_forgot_password.py**
  - Testar geração de token
  - Testar envio de email
  - Testar reset com token válido
  - Testar token expirado

### 3.2 Testes de Integração
- [ ] **test_settings_sync.py**
  - Salvar no Settings
  - Verificar no Chat
  - Verificar no banco
- [ ] **test_hybrid_auth.py**
  - Login com Google
  - Login com Email/Senha
  - Vincular contas
  - Desvincular contas

### 3.3 Testes Frontend (Vitest/Playwright)
- [ ] **Settings.test.jsx**
  - Renderização
  - Salvamento
  - Validação
- [ ] **Auth.test.jsx**
  - Login
  - Registro
  - Recuperação de senha

---

## 📊 Fase 4: Validação e Documentação

### 4.1 Validação Manual
- [ ] **Testar fluxo completo de registro**
- [ ] **Testar fluxo completo de login**
- [ ] **Testar alteração de senha**
- [ ] **Testar recuperação de senha**
- [ ] **Testar todas as configurações**
- [ ] **Testar sincronização entre telas**

### 4.2 Documentação
- [ ] **Atualizar README.md**
- [ ] **Documentar endpoints de auth**
- [ ] **Documentar endpoints de settings**
- [ ] **Criar guia de configuração SMTP**
- [ ] **Criar guia de testes**

### 4.3 Segurança
- [ ] **Rate limiting em endpoints de auth**
- [ ] **Validação de força de senha**
- [ ] **Proteção contra brute force**
- [ ] **Sanitização de inputs**
- [ ] **HTTPS obrigatório em produção**

---

## 🚀 Fase 5: Deploy e Monitoramento

### 5.1 Configuração
- [ ] **Variáveis de ambiente para SMTP**
- [ ] **Configurar SendGrid/AWS SES**
- [ ] **Configurar domínio para emails**
- [ ] **Testar envio de emails em staging**

### 5.2 Monitoramento
- [ ] **Métricas de autenticação**
- [ ] **Métricas de alteração de settings**
- [ ] **Logs de erros de email**
- [ ] **Alertas de falhas críticas**

---

## 📝 Notas Técnicas

### Prioridade de Implementação
1. **CRÍTICO**: Corrigir UserRepository (nome não salva)
2. **CRÍTICO**: Corrigir debug_mode (não persiste)
3. **CRÍTICO**: Implementar idioma no LLM
4. **ALTO**: Autenticação Email/Senha
5. **ALTO**: Alterar Senha
6. **MÉDIO**: Sistema de notificações
7. **BAIXO**: Testes automatizados completos

### Dependências Externas
- SendGrid ou AWS SES (emails)
- Redis (rate limiting)
- PostgreSQL (persistência)

### Estimativa de Tempo
- Fase 1: 2-3 horas
- Fase 2: 4-6 horas
- Fase 3: 3-4 horas
- Fase 4: 2-3 horas
- Fase 5: 1-2 horas
- **Total: 12-18 horas**
