# 📚 DOCUMENTAÇÃO CERBERUS AI

Documentação oficial do projeto Cerberus AI - Developer LLM & Code Assistant.

---

## 📁 Estrutura

```
docs/
├── README.md                    # Este arquivo
├── product/                     # Visão de produto e roadmap
│   └── ROADMAP_CERBERUS_AI.md  # Roadmap completo até modelo próprio
├── api/                         # Especificações da API pública
│   └── API_PUBLIC_SPEC.md      # Endpoints, autenticação, SDKs
├── technical/                   # Documentação técnica (futuro)
│   ├── ARCHITECTURE.md         # Arquitetura do sistema
│   ├── DEPLOYMENT.md           # Deploy e infraestrutura
│   └── DEVELOPMENT.md          # Setup de desenvolvimento
└── archive/                     # Documentos antigos (Focus AI MVP)
```

---

## 🚀 Início Rápido

### Para Desenvolvedores
1. Leia [ROADMAP_CERBERUS_AI.md](product/ROADMAP_CERBERUS_AI.md) - Visão completa do produto
2. Veja [API_PUBLIC_SPEC.md](api/API_PUBLIC_SPEC.md) - Como integrar com a API

### Para Usuários da API
1. [API_PUBLIC_SPEC.md](api/API_PUBLIC_SPEC.md) - Documentação completa
2. Exemplos de integração (WhatsApp, Slack, VS Code)

---

## 📖 Documentos Principais

### Produto
- **[ROADMAP_CERBERUS_AI.md](product/ROADMAP_CERBERUS_AI.md)** - Roadmap completo (7 fases)
  - Rebranding
  - Arquitetura escalável (RabbitMQ, Redis)
  - API pública
  - RAG
  - Fine-tuning (modelo próprio)
  - Produção multi-model
  - Monetização

### API
- **[API_PUBLIC_SPEC.md](api/API_PUBLIC_SPEC.md)** - Especificação da API pública
  - Endpoints REST
  - Autenticação (API Keys)
  - Rate limits
  - Pricing
  - SDKs (Python, JavaScript)
  - Exemplos de integração

---

## 🗂️ Archive

Documentos da versão anterior (Focus AI MVP) foram movidos para `archive/`:
- Implementações antigas
- Debug mode v1
- Chain validation v1
- Natural responses v1

Mantidos para referência histórica.

---

## 🔄 Próximas Adições

### Technical (em breve)
- `ARCHITECTURE.md` - Diagrama completo do sistema
- `DEPLOYMENT.md` - Guia de deploy (Docker, K8s)
- `DEVELOPMENT.md` - Setup local, testes, CI/CD
- `SECURITY.md` - Práticas de segurança
- `MONITORING.md` - Observabilidade (Prometheus, Grafana)

### API (em breve)
- `WEBHOOKS.md` - Sistema de webhooks
- `SDKS.md` - Guias detalhados dos SDKs
- `INTEGRATIONS.md` - Templates de integração
- `CHANGELOG.md` - Histórico de versões da API

---

## 📝 Convenções

### Nomenclatura de Arquivos
- `UPPERCASE.md` - Documentos principais
- `lowercase.md` - Documentos auxiliares
- Prefixos: `API_`, `TECH_`, `PRODUCT_`

### Estrutura de Documentos
```markdown
# Título

## Visão Geral
Resumo executivo

## Seções Principais
Conteúdo detalhado

## Próximos Passos
Ações práticas
```

---

## 🤝 Contribuindo

Ao adicionar documentação:
1. Coloque na pasta correta (`product/`, `api/`, `technical/`)
2. Atualize este README.md
3. Use markdown consistente
4. Adicione exemplos práticos

---

**Cerberus AI** - Developer Assistant by Focus AI
