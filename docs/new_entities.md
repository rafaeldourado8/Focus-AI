# Novas Entidades de Domínio (DDD)

Para suportar o modelo SaaS/Enterprise e remover as travas socráticas.

## 1. Entity: `ModelTransaction`
Substitui a lógica simples de Chat. Rastreia custo e rota.
- `id`: UUID
- `user_id`: UUID
- `input_tokens`: Int
- `output_tokens`: Int
- `model_used`: Enum("llama-3-8b-local", "gemini-1.5-pro")
- `cost_in_credits`: Float
- `latency_ms`: Int

## 2. Entity: `ApiKey`
Para permitir acesso externo à nossa API.
- `key_hash`: String (Index)
- `owner_id`: UUID
- `monthly_limit`: Int
- `current_usage`: Int
- `is_active`: Boolean

## 3. Value Object: `SystemPrompt`
Agora dinâmico, não mais fixo no código.
- `role`: "Developer Assistant", "Uncensored Generalist", "Architecture Expert"
- `constraints`: Lista vazia (remover filtros socráticos).