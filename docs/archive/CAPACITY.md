# Capacidade e Escalabilidade - Focus AI

## Análise de Gargalos

### 1. Gemini API (Principal Limitador)
**Limites Google Gemini:**
- Flash Lite: 1500 RPM (requests per minute)
- Pro: 360 RPM
- Quota diária: ~1M tokens/dia (tier gratuito)

**Com Chain Validation (70% Junior):**
- 70% das requests → Flash Lite (1500 RPM)
- 30% das requests → Pro (360 RPM)
- **Gargalo:** Pro limita a 360 req/min = 21,600 req/hora

### 2. Redis (Cache + Locks)
**Capacidade:**
- ~50k ops/segundo (single instance)
- Memória: configurável (default 256MB)
- **Não é gargalo** para <10k usuários simultâneos

### 3. PostgreSQL
**Capacidade:**
- ~1k writes/segundo (config padrão)
- ~10k reads/segundo
- **Não é gargalo** para <5k usuários simultâneos

### 4. FastAPI Backend
**Capacidade:**
- ~1k requests/segundo (single worker)
- Escalável horizontalmente (múltiplos containers)
- **Não é gargalo** com load balancer

## Capacidade Atual (Setup Padrão)

### Usuários Simultâneos
**Cenário Conservador:**
- 1 usuário = 10 perguntas/hora
- 30% usam Senior (360 RPM limit)
- **Máximo: ~1,200 usuários simultâneos**

**Cenário Otimista (com cache 50% hit):**
- Cache reduz chamadas API em 50%
- **Máximo: ~2,400 usuários simultâneos**

### Usuários Totais/Dia
**Assumindo uso médio:**
- Usuário ativo: 30 min/dia, 20 perguntas
- Pico: 20% dos usuários online simultaneamente
- **Capacidade: ~6,000-12,000 usuários/dia**

## Custos por Escala

### 1,000 Usuários/Dia
- 20k perguntas/dia
- 14k Junior ($1.40) + 6k Senior ($6.00)
- **Total: ~$7.40/dia = $222/mês**

### 5,000 Usuários/Dia
- 100k perguntas/dia
- 70k Junior ($7) + 30k Senior ($30)
- **Total: ~$37/dia = $1,110/mês**

### 10,000 Usuários/Dia
- 200k perguntas/dia
- 140k Junior ($14) + 60k Senior ($60)
- **Total: ~$74/dia = $2,220/mês**

## Otimizações para Escalar

### Fase 1: Otimização Imediata (0-5k usuários)
- ✅ Cache Redis (já implementado)
- ✅ Session locks (já implementado)
- [ ] Aumentar cache TTL (1h → 24h)
- [ ] Implementar cache warming (perguntas comuns)

**Ganho:** +50% capacidade (hit rate 50%)

### Fase 2: Infraestrutura (5k-20k usuários)
- [ ] Múltiplos workers FastAPI (4-8 workers)
- [ ] Redis Cluster (3 nodes)
- [ ] PostgreSQL read replicas (2 replicas)
- [ ] Load balancer (Nginx/AWS ALB)

**Ganho:** +300% capacidade

### Fase 3: API Optimization (20k-50k usuários)
- [ ] Batch requests para Gemini (quando disponível)
- [ ] Upgrade Gemini tier (mais RPM)
- [ ] Fallback para múltiplas API keys (round-robin)
- [ ] Queue system (Celery + RabbitMQ)

**Ganho:** +500% capacidade

### Fase 4: Arquitetura Distribuída (50k+ usuários)
- [ ] Microserviços (separar LLM service)
- [ ] Kubernetes (auto-scaling)
- [ ] CDN para assets estáticos
- [ ] Multi-region deployment

**Ganho:** Ilimitado (horizontal scaling)

## Monitoramento Crítico

### Métricas para Alertas
```python
# Alerta se:
- Gemini API rate limit > 80%
- Redis memory > 80%
- PostgreSQL connections > 80%
- Response time > 5s (p95)
- Error rate > 1%
```

### Dashboard Recomendado
- Usuários simultâneos (real-time)
- Requests/min (Junior vs Senior)
- Cache hit rate
- API quota usage (Gemini)
- Custo estimado/hora

## Recomendações por Fase

### MVP (0-1k usuários)
**Setup atual é suficiente!**
- Single container backend
- Redis single instance
- PostgreSQL single instance
- Custo: ~$7/dia

### Growth (1k-5k usuários)
**Otimizações necessárias:**
- Cache warming
- 2-4 backend workers
- Monitoramento básico
- Custo: ~$37/dia

### Scale (5k-20k usuários)
**Infraestrutura robusta:**
- Load balancer
- Redis cluster
- DB replicas
- Queue system
- Custo: ~$150-300/dia

### Enterprise (20k+ usuários)
**Arquitetura distribuída:**
- Kubernetes
- Multi-region
- Dedicated Gemini tier
- 24/7 monitoring
- Custo: Negociar com Google

## Limitações Conhecidas

### Hard Limits (não contornáveis facilmente)
1. **Gemini API RPM** - Requer upgrade de tier
2. **JWT expiration (3 min)** - Pode causar UX ruim em alta carga
3. **Session locks** - Previne concorrência, mas limita throughput

### Soft Limits (contornáveis com otimização)
1. **Cache TTL** - Aumentar para reduzir API calls
2. **Single backend** - Escalar horizontalmente
3. **Confidence threshold** - Ajustar dinamicamente

## Conclusão

**Capacidade Atual:** 1,200-2,400 usuários simultâneos
**Capacidade Diária:** 6,000-12,000 usuários/dia
**Custo Operacional:** $7-74/dia dependendo da escala

**Próximo Gargalo:** Gemini API RPM (Pro tier)
**Solução:** Upgrade para tier pago ou múltiplas API keys

---

**Recomendação:** Sistema atual suporta MVP e early growth sem modificações.
Para >5k usuários/dia, implementar Fase 2 (infraestrutura).
