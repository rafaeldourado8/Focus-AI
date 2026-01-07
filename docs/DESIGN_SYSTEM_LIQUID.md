# Design System: Liquid Dark Premium

## 1. Conceito Visual
"Fluidez Cognitiva". A interface não deve parecer estática. O fundo deve se comportar como um fluido escuro e viscoso (ferrofluido) que reage sutilmente à presença do usuário.

## 2. Paleta de Cores (OLED Friendly)
- **Void Black**: `#000000` (Fundo base)
- **Liquid Mercury**: `#E1E1E1` (Texto principal, com leve brilho)
- **Deep Indigo**: `#312E81` (Acentos de processamento, opacidade 40%)
- **Glass**: Superfícies com `backdrop-filter: blur(20px)` e bordas `rgba(255,255,255,0.05)`.

## 3. O Efeito "Water Gradient"
Não usar apenas CSS gradients. Implementar **Shaders WebGL** ou uma simulação de *Mesh Gradient* animada.

### Comportamento
1. **Idle**: O gradiente se move lentamente como fumaça ou água em câmera lenta.
2. **Thinking**: Quando a IA está processando, o fluido acelera e muda de cor (para índigo/violeta).
3. **Interaction**: O cursor do mouse age como um "imã" ou "repulsor" do fluido.

## 4. Componentes de Interface
- **Input Field**: Não é uma caixa. É uma linha flutuante que brilha quando ativa.
- **Typography**: Fonte monoespaçada (JetBrains Mono) para código, Sans-serif geométrica (Inter) para texto.
- **Sem Bordas Sólidas**: Tudo é definido por luz e sombra (Inner Glows).