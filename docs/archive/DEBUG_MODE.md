# 🐛 Debug Mode - Cerberus AI

## Visão Geral

O **Debug Mode** é um recurso avançado do Cerberus AI que ativa análise técnica profunda para programação, debugging e arquitetura de software.

## Funcionalidades

### 🎯 Quando Ativar

- **Debugging de Erros**: Análise detalhada de stack traces, exceções e bugs
- **Revisão de Código**: Identificação de code smells, anti-patterns e vulnerabilidades
- **Arquitetura**: Sugestões de design patterns, escalabilidade e melhores práticas
- **Otimização**: Performance, memory leaks, queries N+1, etc.
- **Refatoração**: Melhorias de código com exemplos práticos

### 📊 O Que Você Recebe

Quando o Debug Mode está ativo, cada resposta inclui:

1. **Análise Detalhada**: Explicação profunda do código/erro
2. **Causas Raiz**: Identificação das causas fundamentais do problema
3. **Soluções Práticas**: Exemplos de código funcionais e testados
4. **Melhores Práticas**: Recomendações de padrões da indústria
5. **Considerações Avançadas**: Segurança, escalabilidade e arquitetura

### 🔍 Informações de Debug

Cada resposta mostra:
- **Model**: Qual modelo de IA foi usado (junior/senior)
- **Senior**: Se a validação senior foi acionada
- **Análise Técnica**: Detalhamento completo do problema

## Interface

### Indicadores Visuais

- **Badge "DEBUG"**: Aparece no header quando ativo
- **Botão Vermelho**: Cor vermelha indica modo ativo
- **Pulse Animation**: Animação sutil no botão
- **Border Vermelha**: Input com borda vermelha
- **Placeholder Customizado**: Texto específico para debug
- **Banner Informativo**: Aviso acima do input

### Atalhos

- **Clique no Botão**: Toggle on/off
- **Tooltip**: Hover para ver descrição completa

## Exemplos de Uso

### ❌ Sem Debug Mode
```
Usuário: "Por que meu código dá erro?"
IA: "Pode ser um problema de sintaxe. Verifique as variáveis."
```

### ✅ Com Debug Mode
```
Usuário: "Por que meu código dá erro?"
IA: 
"[ANÁLISE TÉCNICA PROFUNDA]

1. ANÁLISE DO ERRO:
   - TypeError: Cannot read property 'map' of undefined
   - Linha 42: data.users.map(...)
   - Causa: data.users é undefined

2. CAUSAS RAIZ:
   - API retornou estrutura diferente
   - Falta validação de resposta
   - Ausência de error handling

3. SOLUÇÕES:
   ```javascript
   // Solução 1: Optional Chaining
   const users = data?.users ?? [];
   
   // Solução 2: Validação explícita
   if (!data || !Array.isArray(data.users)) {
     console.error('Invalid data structure');
     return;
   }
   ```

4. MELHORES PRÁTICAS:
   - Use TypeScript para type safety
   - Implemente error boundaries
   - Adicione logging estruturado
   - Valide schemas com Zod/Yup

5. ARQUITETURA:
   - Considere usar React Query para cache
   - Implemente retry logic
   - Adicione fallback UI
"

---
🔧 Debug Info: Model=gemini-2.5-pro | Senior=true
```

## Tecnologia

### Backend Enhancement

O prompt enviado ao LLM é automaticamente enriquecido com:

```javascript
const enhancedContent = `[DEBUG MODE ATIVADO - Análise Técnica Profunda]
${userInput}

Por favor, forneça:
1. Análise detalhada do código/erro
2. Possíveis causas raiz
3. Soluções com exemplos práticos
4. Melhores práticas e otimizações
5. Considerações de arquitetura e segurança`;
```

### Chain Validation

- **Junior LLM** (Gemini 2.0 Flash Lite): Resposta inicial
- **Senior LLM** (Gemini 2.5 Pro): Validação quando necessário
- **Economia**: 63% de redução de custos mantendo qualidade

## UX/UI Melhorias

### Feedback Visual
- ✅ Badge de status no header
- ✅ Animação pulse no botão
- ✅ Tooltip informativo
- ✅ Banner explicativo no input
- ✅ Cores temáticas (vermelho para debug)
- ✅ Placeholder contextual

### Acessibilidade
- ✅ ARIA labels
- ✅ Keyboard navigation
- ✅ Focus states
- ✅ Screen reader friendly

## Roadmap

### Próximas Melhorias
- [ ] Histórico de debug sessions
- [ ] Export de análises em Markdown
- [ ] Integração com VS Code
- [ ] Debug templates pré-configurados
- [ ] Métricas de performance
- [ ] Comparação de soluções

## Custos

### Otimização Inteligente
- **Modo Normal**: ~$0.001 por pergunta
- **Debug Mode**: ~$0.003 por pergunta (com senior)
- **Economia**: 63% vs usar sempre senior

### Chain Validation
O sistema decide automaticamente quando usar o modelo senior baseado em:
- Confiança da resposta junior
- Complexidade da pergunta
- Histórico de validações

## Conclusão

O Debug Mode transforma o Cerberus AI em um **Senior Developer virtual**, fornecendo análises profundas que vão além de respostas superficiais.

**Use quando precisar de:**
- 🐛 Debugging profundo
- 🏗️ Decisões de arquitetura
- ⚡ Otimizações de performance
- 🔒 Análise de segurança
- 📚 Aprendizado técnico avançado

---

**Desenvolvido com ❤️ pela equipe Focus AI**
