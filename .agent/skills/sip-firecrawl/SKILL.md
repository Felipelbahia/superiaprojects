---
name: sip-firecrawl
description: Use whenever the current task involves Firecrawl (web scraping, crawling, mapping, search, structured extraction, browser interaction, monitoring, lead gen, SEO audits, etc.) but the active project has no local Firecrawl skills — i.e. any project other than "SIP - Firecrawl" (Firecrawl - local) itself. Routes the task to the central Firecrawl knowledge hub instead of improvising from general knowledge. Also use when the user asks "existe algo de firecrawl pra isso", "tem skill de scraping no hub", "consulta o SIP - Firecrawl", or names Firecrawl explicitly in a project that isn't it. Este stub existe para que IAs que não leem `.claude/skills/` (Google Antigravity/Gemini, Cursor) ainda encontrem este nome via Regra 4 (Fallback Resolution Protocol) — nos projetos que instalaram este SIP, o Claude Code já o acha em `.claude/skills/sip-firecrawl`; nos outros, as regras (módulo `sip-access`) mandam ler este ponteiro.
---

# sip-firecrawl — ponteiro para o hub central de Firecrawl

O conteúdo real desta skill (modo consulta, modo dispatch, modo contribuição)
vive no hub central "SIP - Firecrawl" (Firecrawl - local):

```text
/Users/macbookpro/Documents/IA Projects/_Plataforma/Firecrawl - local/.agent/skills/sip-firecrawl/SKILL.md
```

Leia o `SKILL.md` nesse caminho e siga normalmente — este arquivo só existe
para que a busca por nome (Regra 4) encontre o ponteiro. Se precisar de uma
skill pontual de uso (scrape/crawl/map/search/etc.), o hub tem o roteador
`firecrawl-router` que indica qual skill especialista ler.

Este stub substitui os antigos stubs individuais por sub-skill
(`firecrawl-build`, `firecrawl-scrape`, `firecrawl-crawl`, etc.), que foram
consolidados aqui em 2026-11-06 — um único ponto de entrada, igual ao que o
Claude Code já tinha com `sip-firecrawl`.

Para instalar acesso permanente a este hub em outro projeto (Claude Code via
`.claude/skills/`), veja
`/Users/macbookpro/Documents/IA Projects/_Plataforma/Firecrawl - local/prompts/instalar-skill-sip-firecrawl.md`.

## Agents e workflows do hub

Agents (`.agent/agents/`) e workflows (`.agent/workflows/`) do hub estão listados no resolver acima e podem ser lidos por caminho absoluto em `/Users/macbookpro/Documents/IA Projects/_Plataforma/Firecrawl - local/.agent/` (ou usados localmente se este projeto escolheu instalá-los).

## Atualização

Data da última atualização e instruções: seção "Atualização" do resolver no hub
(`/Users/macbookpro/Documents/IA Projects/_Plataforma/Firecrawl - local/.agent/skills/sip-firecrawl/SKILL.md`). Para atualizar a instalação num
projeto, cole de novo `/Users/macbookpro/Documents/IA Projects/_Plataforma/Firecrawl - local/prompts/instalar-skill-sip-firecrawl.md`.
