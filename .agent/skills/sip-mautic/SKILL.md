---
name: sip-mautic
description: Use whenever the current task involves Mautic (contatos, segmentos, campanhas, e-mails, formulários) or Mailgun (envio, webhooks, domínios) but the active project has no local Mautic skills — i.e. any project other than "SIP - Mautic" itself. Routes the task to the central Mautic knowledge hub instead of improvising from general knowledge. Also use when the user asks "existe algo de mautic pra isso", "tem template pra isso no hub", "consulta o SIP - Mautic", or names Mautic/Mailgun explicitly in a project that isn't it. Este stub existe para que IAs que não leem `.claude/skills/` (Google Antigravity/Gemini, Cursor) ainda encontrem este nome via Regra 4 (Fallback Resolution Protocol) — nos projetos que instalaram este SIP, o Claude Code já o acha em `.claude/skills/sip-mautic`; nos outros, as regras (módulo `sip-access`) mandam ler este ponteiro.
---

# sip-mautic — ponteiro para o hub central de Mautic

O conteúdo real desta skill (modo consulta, modo dispatch, modo contribuição)
vive no hub central "SIP - Mautic":

```text
/Users/macbookpro/Documents/IA Projects/Plinq/Martech/Mautic/.agent/skills/sip-mautic/SKILL.md
```

Leia o `SKILL.md` nesse caminho e siga normalmente — este arquivo só existe
para que a busca por nome (Regra 4) encontre o ponteiro. Se a tarefa for
multi-arquivo ou de construção grande, veja no hub a persona do agente
especialista antes de agir.

Para instalar acesso permanente a este hub em outro projeto (Claude Code via
`.claude/skills/`), veja
`/Users/macbookpro/Documents/IA Projects/Plinq/Martech/Mautic/prompts/instalar-skill-sip-mautic.md`.

## Agents e workflows do hub

Agents (`.agent/agents/`) e workflows (`.agent/workflows/`) do hub estão listados no resolver acima e podem ser lidos por caminho absoluto em `/Users/macbookpro/Documents/IA Projects/Plinq/Martech/Mautic/.agent/` (ou usados localmente se este projeto escolheu instalá-los).

## Atualização

Data da última atualização e instruções: seção "Atualização" do resolver no hub
(`/Users/macbookpro/Documents/IA Projects/Plinq/Martech/Mautic/.agent/skills/sip-mautic/SKILL.md`). Para atualizar a instalação num
projeto, cole de novo `/Users/macbookpro/Documents/IA Projects/Plinq/Martech/Mautic/prompts/instalar-skill-sip-mautic.md`.
