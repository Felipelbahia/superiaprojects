---
name: sip-imprensa
description: Use whenever the current task involves imprensa (jornalistas, veículos, pauta, pitch, assessoria de imprensa, PR) but the active project has no local imprensa skills — i.e. any project other than "SIP - Imprensa & PR" (RSS Feed) itself. Routes the task to the central imprensa knowledge hub instead of improvising from general knowledge. Also use when the user asks "existe algo de imprensa pra isso", "tem skill de jornalista no hub", "consulta o SIP - Imprensa & PR", or names imprensa explicitly in a project that isn't it. Este stub existe para que IAs que não leem `.claude/skills/` (Google Antigravity/Gemini, Cursor) ainda encontrem este nome via Regra 4 (Fallback Resolution Protocol) — nos projetos que instalaram este SIP, o Claude Code já o acha em `.claude/skills/sip-imprensa`; nos outros, as regras (módulo `sip-access`) mandam ler este ponteiro.
---

# sip-imprensa — ponteiro para o hub central de Imprensa

O conteúdo real desta skill (modo consulta, modo dispatch, modo contribuição)
vive no hub central "SIP - Imprensa & PR" (RSS Feed):

```text
/Users/macbookpro/Documents/IA Projects/Compartilhado/RSS Feed/.agent/skills/sip-imprensa/SKILL.md
```

Leia o `SKILL.md` nesse caminho e siga normalmente — este arquivo só existe
para que a busca por nome (Regra 4) encontre o ponteiro. Se precisar de uma
skill pontual de uso (pauta/aderência/reescrita/pitch/jornalista/veículo/
etc.), o hub tem o roteador `cliente-hub-imprensa` que indica qual skill
especialista ler.

Para instalar acesso permanente a este hub em outro projeto (Claude Code via
`.claude/skills/` e Google Antigravity/Gemini/Cursor via `.agent/skills/`), veja
`/Users/macbookpro/Documents/IA Projects/Compartilhado/RSS Feed/prompts/instalar-skill-sip-imprensa.md`.

## Agents e workflows do hub

Agents (`.agent/agents/`) e workflows (`.agent/workflows/`) do hub estão listados no resolver acima e podem ser lidos por caminho absoluto em `/Users/macbookpro/Documents/IA Projects/Compartilhado/RSS Feed/.agent/` (ou usados localmente se este projeto escolheu instalá-los).

## Atualização

Data da última atualização e instruções: seção "Atualização" do resolver no hub
(`/Users/macbookpro/Documents/IA Projects/Compartilhado/RSS Feed/.agent/skills/sip-imprensa/SKILL.md`). Para atualizar a instalação num
projeto, cole de novo `/Users/macbookpro/Documents/IA Projects/Compartilhado/RSS Feed/prompts/instalar-skill-sip-imprensa.md`.
