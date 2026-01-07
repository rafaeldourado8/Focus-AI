# Segurança - OWASP Top 10

## Implementações de Segurança

### 1. Broken Access Control (A01:2021)
- ✅ JWT com expiração de 3 minutos
- ✅ Verificação de ownership em sessões
- ✅ Validação de user_id em todas as operações

### 2. Cryptographic Failures (A02:2021)
- ✅ Bcrypt para hash de senhas (cost factor padrão)
- ✅ JWT assinado com HS256
- ✅ Senhas nunca armazenadas em plain text

### 3. Injection (A03:2021)
- ✅ SQLAlchemy ORM (previne SQL injection)
- ✅ Validação de input com Pydantic
- ✅ Parametrização de queries

### 4. Insecure Design (A04:2021)
- ✅ Clean Architecture com separação de camadas
- ✅ Domain-Driven Design
- ✅ Locks por sessão (previne race conditions)

### 5. Security Misconfiguration (A05:2021)
- ✅ CORS configurado explicitamente
- ✅ Variáveis de ambiente para secrets
- ✅ TrustedHost middleware

### 6. Vulnerable Components (A06:2021)
- ✅ Dependências atualizadas
- ✅ Versões fixadas no requirements.txt

### 7. Authentication Failures (A07:2021)
- ✅ Validação de força de senha (8+ chars, maiúscula, minúscula, número)
- ✅ JWT com expiração curta (3 min)
- ✅ Mensagens genéricas de erro ("Invalid credentials")

### 8. Software and Data Integrity (A08:2021)
- ✅ Validação de dados com Pydantic
- ✅ Testes unitários com cobertura

### 9. Security Logging (A09:2021)
- ⚠️ TODO: Implementar logging estruturado
- ⚠️ TODO: Monitoramento de tentativas de login

### 10. Server-Side Request Forgery (A10:2021)
- ✅ Validação de URLs externas
- ✅ Timeout em chamadas LLM

## Validações de Senha

```python
- Mínimo 8 caracteres
- Pelo menos 1 letra maiúscula
- Pelo menos 1 letra minúscula
- Pelo menos 1 número
```

## Rate Limiting

- Lock por sessão (Redis SETNX)
- TTL de 180 segundos
- Previne spam de perguntas

## Próximos Passos

1. Implementar rate limiting global por IP
2. Adicionar logging estruturado
3. Implementar 2FA (futuro)
4. Adicionar HTTPS obrigatório em produção