#!/bin/bash

# Script de commits para 07 Janeiro 2026

echo "🚀 Iniciando commits do dia..."

# Commit 1
git add docker-compose.yml backend/Dockerfile backend/requirements.txt backend/src/config.py .env.example
git commit -m "feat: remove Ollama dependency and switch to dual Gemini models

- Remove Ollama container from docker-compose.yml
- Switch Junior model to Gemini 2.0 Flash Lite (fast & cheap)
- Switch Senior model to Gemini 2.5 Pro (quality validation)
- Update configuration to remove OLLAMA_URL
- Fix line endings issue in entrypoint.sh with dos2unix"

# Commit 2
git add backend/src/infrastructure/llm/
git commit -m "feat: implement Chain Validation architecture (Junior → Senior)

- Create JuniorLLMService with Gemini Flash Lite
- Create SeniorLLMService with Gemini Pro for validation
- Create ChainValidatorService orchestrator
- Implement confidence-based routing (threshold: 70%)
- Add metadata tracking (model used, confidence, validation status)
- Economy: 63% API cost reduction"

# Commit 3
git add backend/src/application/use_cases/ask_question.py backend/src/presentation/session_routes.py
git commit -m "refactor: transform into natural LLM chat without structured format

- Remove JSON structured responses (explanation, edge_cases)
- Implement natural conversation flow like ChatGPT/Claude
- Update system instructions to focus on programming/DevOps
- Remove validation overhead - Junior responds directly
- Simplify response format to just content + metadata"

# Commit 4
git add frontend/src/components/Sidebar.jsx frontend/src/components/Chat.jsx
git commit -m "feat: add sidebar with conversation history

- Create Sidebar component with animations
- Implement conversation grouping (Today, Yesterday, Older)
- Add real-time search functionality
- Add new conversation button
- Implement responsive design (overlay on mobile)
- Add session management in Chat component"

# Commit 5
git add frontend/src/components/Chat.jsx
git commit -m "feat: add token counter and keyboard shortcuts

- Implement real-time token estimation (1 token ≈ 4 chars)
- Display token count next to send button
- Add Ctrl+Enter shortcut to send message
- Add Menu button to toggle sidebar
- Update placeholder with helpful hints"

# Commit 6
git add frontend/src/components/Chat.jsx
git commit -m "feat: add code block detection and copy button

- Implement regex-based code block detection (\`\`\`language\`\`\`)
- Add syntax highlighting header with language name
- Add copy button with visual feedback (copied state)
- Style code blocks with proper formatting"

# Commit 7
git add docs/Focus_AI_Analise_Melhorias.md
git commit -m "docs: add comprehensive analysis and improvement roadmap

- Document current state and missing features
- Define 3-phase implementation roadmap (MVP, Essential, Advanced)
- Prioritize features by impact and effort
- Add technical specifications and wireframes
- Include keyboard shortcuts reference"

# Commit 8
git add docs/CAPACITY.md
git commit -m "docs: add capacity and scalability analysis

- Document Gemini API constraints (RPM limits)
- Calculate costs per scale (1k, 5k, 10k users/day)
- Define optimization phases for scaling
- Add monitoring recommendations
- Estimate concurrent user capacity"

# Commit 9
git add docs/CHAIN_VALIDATION.md docs/ARCHITECTURE_V2.md README.md
git commit -m "docs: update Chain Validation documentation

- Update with Gemini models (Flash Lite + Pro)
- Correct economy calculations (63% savings)
- Remove Ollama references
- Update architecture diagrams
- Add real pricing information"

# Commit 10
git add docs/COMMITS_2026-01-07.md docs/TASKS_V2.md
git commit -m "docs: add daily commits log and update tasks

- Create comprehensive commit history for 2026-01-07
- Document all features implemented in Fase 1 MVP
- Update TASKS_V2.md with completed items
- Add statistics and next steps"

echo "✅ Todos os commits realizados!"
echo "📊 Total: 10 commits"
echo ""
echo "Para enviar ao repositório remoto:"
echo "git push origin main"
