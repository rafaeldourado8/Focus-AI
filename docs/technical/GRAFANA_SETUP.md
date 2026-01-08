# 📊 GRAFANA SETUP - CERBERUS AI

## Instalação

### Docker Compose
```yaml
grafana:
  image: grafana/grafana:latest
  ports:
    - "3000:3000"
  environment:
    - GF_SECURITY_ADMIN_PASSWORD=admin
  volumes:
    - grafana_data:/var/lib/grafana
```

### Standalone
```bash
docker run -d -p 3000:3000 grafana/grafana:latest
```

---

## Configuração

### 1. Adicionar Data Source (Prometheus)

1. Acesse: http://localhost:3000
2. Login: admin / admin
3. Configuration → Data Sources → Add data source
4. Selecione **Prometheus**
5. URL: `http://localhost:9090` (ou `http://prometheus:9090` no Docker)
6. Save & Test

### 2. Importar Dashboard

1. Dashboards → Import
2. Upload `grafana-dashboard.json`
3. Selecione Prometheus data source
4. Import

---

## Métricas Disponíveis

### Request Metrics
- `cerberus_requests_total` - Total de requisições
- `cerberus_request_duration_seconds` - Duração das requisições

### Cache Metrics
- `cerberus_cache_hits_total` - Cache hits
- `cerberus_cache_misses_total` - Cache misses

### Model Metrics
- `cerberus_model_usage_total` - Uso por modelo

### Cost Metrics
- `cerberus_total_cost_usd` - Custo total em USD

### Error Metrics
- `cerberus_errors_total` - Total de erros

### Session Metrics
- `cerberus_active_sessions` - Sessões ativas

---

## Queries Úteis

### Cache Hit Rate
```promql
rate(cerberus_cache_hits_total[5m]) / 
(rate(cerberus_cache_hits_total[5m]) + rate(cerberus_cache_misses_total[5m])) * 100
```

### Request Duration p95
```promql
histogram_quantile(0.95, rate(cerberus_request_duration_seconds_bucket[5m]))
```

### Error Rate
```promql
rate(cerberus_errors_total[5m])
```

### Cost per Hour
```promql
rate(cerberus_total_cost_usd[1h])
```

---

## Alertas Recomendados

### High Error Rate
```yaml
alert: HighErrorRate
expr: rate(cerberus_errors_total[5m]) > 0.1
for: 5m
annotations:
  summary: "High error rate detected"
```

### Low Cache Hit Rate
```yaml
alert: LowCacheHitRate
expr: rate(cerberus_cache_hits_total[5m]) / (rate(cerberus_cache_hits_total[5m]) + rate(cerberus_cache_misses_total[5m])) < 0.5
for: 10m
annotations:
  summary: "Cache hit rate below 50%"
```

### High Latency
```yaml
alert: HighLatency
expr: histogram_quantile(0.95, rate(cerberus_request_duration_seconds_bucket[5m])) > 2
for: 5m
annotations:
  summary: "p95 latency above 2 seconds"
```

---

**Cerberus AI** - Developer Assistant by Focus AI
