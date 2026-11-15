---
name: sip-trends-previsao-demanda
description: Use whenever the current task involves demand forecasting, seasonality analysis, or Google Trends data but the active project has no local skills for it — i.e. any project other than "SIP - Trends e Previsão de Demanda (Sazonalidade)" itself. Routes the task to the central knowledge hub instead of improvising from general knowledge. Also use when the user asks "existe algo de sazonalidade/trends pra isso", "tem template pra isso no hub", "consulta o SIP de previsão de demanda", or names Google Trends / sazonalidade explicitly in a project that isn't it. Este stub existe para que IAs que não leem `.claude/skills/` (Google Antigravity/Gemini, Cursor) ainda encontrem este nome via Regra 4 (Fallback Resolution Protocol) — nos projetos que instalaram este SIP, o Claude Code já o acha em `.claude/skills/sip-trends-previsao-demanda`; nos outros, as regras (módulo `sip-access`) mandam ler este ponteiro.
---

# sip-trends-previsao-demanda — ponteiro para o hub central de previsão de demanda

O conteúdo real desta skill (modo consulta, modo dispatch, modo contribuição)
vive no hub central "Previsão de Demanda":

```text
/Users/macbookpro/Documents/IA Projects/Compartilhado/Previsão de Demanda/.agent/skills/sip-trends-previsao-demanda/SKILL.md
```

Leia o `SKILL.md` nesse caminho e siga normalmente — este arquivo só existe
para que a busca por nome (Regra 4) encontre o ponteiro. Se a tarefa for
multi-arquivo ou de construção grande, veja no hub a persona do agente
especialista antes de agir.

Para instalar acesso permanente a este hub em outro projeto (Claude Code via
`.claude/skills/`), veja
`/Users/macbookpro/Documents/IA Projects/Compartilhado/Previsão de Demanda/prompts/instalar-skill-sip-trends-previsao-demanda.md`.

## Agents e workflows do hub

Agents (`.agent/agents/`) e workflows (`.agent/workflows/`) do hub estão listados no resolver acima e podem ser lidos por caminho absoluto em `/Users/macbookpro/Documents/IA Projects/Compartilhado/Previsão de Demanda/.agent/` (ou usados localmente se este projeto escolheu instalá-los).

## Atualização

Data da última atualização e instruções: seção "Atualização" do resolver no hub
(`/Users/macbookpro/Documents/IA Projects/Compartilhado/Previsão de Demanda/.agent/skills/sip-trends-previsao-demanda/SKILL.md`). Para atualizar a instalação num
projeto, cole de novo `/Users/macbookpro/Documents/IA Projects/Compartilhado/Previsão de Demanda/prompts/instalar-skill-sip-trends-previsao-demanda.md`.
