---
name: sip-n8n
description: Use whenever the current task involves n8n (workflows, nodes, expressions, Code nodes, AI Agents in n8n, webhooks, self-hosting, or the n8n REST API) but the active project has no local n8n skills — i.e. any project other than "SIP- N8N" itself. Routes the task to the central n8n knowledge hub instead of improvising from general knowledge. Also use when the user asks "existe algo de n8n pra isso", "tem template pra isso no hub", "consulta o SIP - N8N", or names n8n explicitly in a project that isn't it. Este stub existe para que IAs que não leem `.claude/skills/` (Google Antigravity/Gemini, Cursor) ainda encontrem este nome via Regra 4 (Fallback Resolution Protocol) — o Claude Code já tem acesso direto via `.claude/skills/sip-n8n`.
---

# sip-n8n — ponteiro para o hub central de n8n

O conteúdo real desta skill (modo consulta, modo dispatch, modo contribuição)
vive no hub central "SIP - N8N":

```text
/Users/macbookpro/Documents/IA Projects/_Plataforma/SIP- N8N/.agent/skills/sip-n8n/SKILL.md
```

Leia o `SKILL.md` nesse caminho e siga normalmente — este arquivo só existe
para que a busca por nome (Regra 4) encontre o ponteiro. Se a tarefa for
multi-arquivo ou de construção grande, veja no hub a persona do agente
especialista antes de agir.

Para instalar acesso permanente a este hub em outro projeto (Claude Code via
`.claude/skills/`), veja
`/Users/macbookpro/Documents/IA Projects/_Plataforma/SIP- N8N/prompts/instalar-skill-sip-n8n.md`.

## Agents e workflows do hub

Agents (`.agent/agents/`) e workflows (`.agent/workflows/`) do hub estão listados no resolver acima e podem ser lidos por caminho absoluto em `/Users/macbookpro/Documents/IA Projects/_Plataforma/SIP- N8N/.agent/` (ou usados localmente se este projeto escolheu instalá-los).

## Atualização

Data da última atualização e instruções: seção "Atualização" do resolver no hub
(`/Users/macbookpro/Documents/IA Projects/_Plataforma/SIP- N8N/.agent/skills/sip-n8n/SKILL.md`). Para atualizar a instalação num
projeto, cole de novo `/Users/macbookpro/Documents/IA Projects/_Plataforma/SIP- N8N/prompts/instalar-skill-sip-n8n.md`.
