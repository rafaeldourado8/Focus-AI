# 🐛 BUGS & MELHORIAS - Cerberus AI

**Status:** Em Progresso  
**Última atualização:** 2024-01-15

---

## 🔥 CRÍTICO (P0) - Resolver AGORA

### Backend
- [ ] **IDOR**: Validar ownership em TODOS os endpoints (chat, API keys, sessions)
- [ ] **Rate Limiting**: Implementar por IP e User ID
- [ ] **JWT Security**: Validar algoritmo e implementar refresh token rotation
- [ ] **Error Handling**: Não expor stack traces em produção
- [ ] **N+1 Queries**: Otimizar queries com select_related/prefetch_related
- [ ] **Transaction Atomicity**: Garantir rollback em falhas

### Frontend
- [ ] **Double Click**: Prevenir envio duplo de formulário
- [ ] **Race Condition**: Prevenir múltiplas requisições simultâneas
- [ ] **Token Expiration**: Refresh automático ou logout gracioso
- [ ] **Network Flaky**: Tratamento de erro quando internet cai
- [ ] **XSS Protection**: Sanitizar markdown da IA

### Segurança
- [ ] **API Keys**: Mostrar apenas uma vez após criação
- [ ] **CORS**: Restringir apenas domínios permitidos
- [ ] **Prompt Injection**: Defesa contra jailbreak
- [ ] **PII Redaction**: Mascarar dados sensíveis nos logs

---

## 🚨 ALTO (P1) - Próxima Sprint

### UX & Frontend
- [x] ~~Skeleton Screens no Dashboard~~
- [ ] Toast Notifications empilháveis
- [ ] Modais customizados (substituir alert/confirm)
- [ ] Syntax Highlighting adequado
- [ ] Botão "Stop Generating"
- [ ] Auto-scroll inteligente
- [ ] Atalho Ctrl+Enter para enviar
- [ ] Atalho Esc para fechar modais
- [ ] Página 404 personalizada
- [ ] Tooltips em configurações

### Backend & API
- [ ] Streaming de resposta (SSE)
- [ ] Paginação cursor-based no histórico
- [ ] Health Check endpoint (/health)
- [ ] Structured Logging (JSON)
- [ ] Request ID (Correlation ID)
- [ ] Middleware global de exceções
- [ ] Compressão Gzip/Brotli
- [ ] Soft Delete para recuperação
- [ ] Background Tasks (Celery)

### LLM & IA
- [x] ~~Visualizar Pensamento (Thinking Process)~~
- [ ] Streaming caractere a caractere
- [ ] Contador de tokens em tempo real
- [ ] Estimativa de custo
- [ ] Fallback automático (GPT-4 → Gemini)
- [ ] Botão "Regenerar Resposta"
- [ ] Edição de mensagem (branching)
- [ ] Templates de prompts
- [ ] Feedback (👍👎) para RLHF

---

## ⚠️ MÉDIO (P2) - Backlog

### Frontend
- [ ] Dark/Light Mode real
- [ ] Virtualization na lista de mensagens
- [ ] Drag-and-drop para upload
- [ ] Preview de PDF/Imagens
- [ ] Lazy Loading de rotas
- [ ] Otimizar imagens (WebP)
- [ ] Favicon dinâmico (notificações)
- [ ] Responsividade mobile melhorada
- [ ] Haptic feedback (PWA)

### Backend
- [ ] Versionamento de API (/v1, /v2)
- [ ] Bulk Delete de conversas
- [ ] WebSockets para comunicação real-time
- [ ] Circuit Breaker para APIs externas
- [ ] Testes de carga (Locust)
- [ ] Graceful Shutdown
- [ ] MyPy (tipagem estática)

### LLM
- [ ] RAG com upload de docs
- [ ] Function Calling
- [ ] Ajuste dinâmico de temperatura
- [ ] Parser inteligente de código
- [ ] Vision (análise de screenshots)
- [ ] Audio-to-Text (Whisper)
- [ ] Text-to-Speech
- [ ] Context Pruning
- [ ] Múltiplos provedores (Anthropic, Mistral)

---

## 📝 BAIXO (P3) - Nice to Have

### Polimento
- [ ] Som de notificação
- [ ] Tour guiado (Onboarding)
- [ ] Dica do Dia
- [ ] Exportar conversa (PDF/TXT/JSON)
- [ ] Compartilhar conversa (link público)
- [ ] Busca global (Cmd+K)
- [ ] Avatares customizáveis
- [ ] Renomear conversas
- [ ] Pastas para organizar
- [ ] Suporte a Latex
- [ ] Modo Zen
- [ ] Cronômetro de geração
- [ ] Changelog
- [ ] Sistema de convites
- [ ] Arquivar conversas
- [ ] Feedback de bug in-app
- [ ] Integração com GitHub

### Segurança
- [ ] 2FA (Two-Factor Authentication)
- [ ] Session Timeout
- [ ] Criptografia AES-256 para API keys
- [ ] Audit Log
- [ ] Bloqueio após X tentativas
- [ ] Verificação de email
- [ ] Security Headers (Helmet)
- [ ] CSRF Protection
- [ ] Sessões Ativas (gerenciar)
- [ ] RBAC (Admin vs User)
- [ ] Pentest (OWASP ZAP)

### Infraestrutura
- [ ] CI/CD (GitHub Actions)
- [ ] Linter no pre-commit
- [ ] Monitoramento (Sentry/Datadog)
- [ ] Backups automáticos
- [ ] Auto-scaling
- [ ] CDN (Cloudflare)
- [ ] Staging environment
- [ ] IaC (Terraform)
- [ ] Alertas de custo
- [ ] Multi-stage Docker builds
- [ ] SonarQube
- [ ] Seed scripts

### Analytics & Billing
- [ ] Dashboard Administrativo
- [ ] Custo por usuário
- [ ] Chat Retention
- [ ] Exportação GDPR/LGPD
- [ ] Relatório semanal por email
- [ ] Integração Stripe
- [ ] Sistema de Planos
- [ ] Limites por plano
- [ ] Página de Faturamento
- [ ] Cupons de desconto
- [ ] Webhooks de pagamento
- [ ] Status Page
- [ ] Análise de coorte

---

## 🔍 EDGE CASES & DEEP BUGS

### Frontend Edge Cases
- [ ] Long Text Overflow (nomes com 200 chars)
- [ ] Copy/Paste Rich Text
- [ ] Input Sanitization (emojis, Zalgo)
- [ ] Tab Index (navegação por teclado)
- [ ] Zoom 200% (acessibilidade)
- [ ] Mobile Orientation
- [ ] Browser Back Button
- [ ] Prefers-Reduced-Motion
- [ ] Image Paste (Ctrl+V)
- [ ] Empty States
- [ ] Date Localization
- [ ] Scroll Restoration
- [ ] Text Selection
- [ ] Markdown Injection
- [ ] LocalStorage Quota
- [ ] Focus Management
- [ ] Dead Click (fechar modal)
- [ ] File Type Validation
- [ ] File Size Limit
- [ ] Avatar Fallback

### Concorrência & Estado
- [ ] Race Condition no Chat
- [ ] Stale Closures
- [ ] Optimistic UI Rollback
- [ ] Zombie Children
- [ ] Context Hell (performance)
- [ ] Token Expiration mid-action
- [ ] Request Deduplication
- [ ] WebSocket Reconnection
- [ ] Estado Derivado
- [ ] Prop Drilling

### Segurança Ofensiva
- [ ] IDOR (Insecure Direct Object Reference)
- [ ] Rate Limit Bypass
- [ ] Replay Attack
- [ ] JWT Algorithm Confusion
- [ ] Information Disclosure
- [ ] Error Handling Verboso
- [ ] NoSQL Injection
- [ ] Mass Assignment
- [ ] SSRF
- [ ] CSV Injection
- [ ] Clickjacking
- [ ] Session Fixation
- [ ] Timing Attack
- [ ] Dependency Audit
- [ ] Bucket Pública

### Database & Performance
- [ ] N+1 Queries
- [ ] Database Indexing
- [ ] Transaction Atomicity
- [ ] Connection Pooling
- [ ] Deadlocks
- [ ] Data Migration Tests
- [ ] Soft Delete Indexes
- [ ] UTC Standardization
- [ ] JSONB Performance
- [ ] Backup Restore Test

### LLM Ops
- [ ] Prompt Injection (Jailbreak)
- [ ] Output Validation
- [ ] Token Limit Truncation
- [ ] Context Poisoning
- [ ] Hallucination Check
- [ ] PII Filter
- [ ] Cost Monitoring
- [ ] Model Fallback
- [ ] Latency Timeout
- [ ] Empty Response

### SaaS & Billing
- [ ] Proration
- [ ] Failed Payment
- [ ] Webhook Idempotency
- [ ] Invoice PDF
- [ ] Concurrency Billing
- [ ] Tier Limits
- [ ] Refund Handling

### DevOps & Observability
- [ ] Log Rotation
- [ ] Memory Leaks
- [ ] Cold Start
- [ ] DNS TTL
- [ ] SSL Auto-renew
- [ ] Env Var Validation
- [ ] APM Tracing
- [ ] Alert Fatigue

---

## 🎯 SPRINT ATUAL - Foco Imediato

### Sprint 1: Segurança Crítica (Esta semana)
1. [ ] Validar ownership em todos endpoints
2. [ ] Implementar rate limiting
3. [ ] Esconder API keys após criação
4. [ ] Sanitizar inputs (XSS/SQL Injection)
5. [ ] Não expor stack traces

### Sprint 2: UX Essencial (Próxima semana)
1. [ ] Toast notifications
2. [ ] Modais customizados
3. [ ] Syntax highlighting
4. [ ] Botão "Stop Generating"
5. [ ] Atalhos de teclado

### Sprint 3: Performance & Escala
1. [ ] Streaming de resposta
2. [ ] Paginação
3. [ ] Otimizar queries N+1
4. [ ] Health check
5. [ ] Structured logging

---

**Cerberus AI** - Developer Assistant by Focus AI
