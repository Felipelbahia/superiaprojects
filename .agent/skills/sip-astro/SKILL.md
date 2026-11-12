---
name: sip-astro
description: Use whenever the current task involves Astro (building or migrating a site, choosing a theme, integrations, SEO/GEO, deploy, forms, analytics, i18n, e-commerce, testing, upgrades, a pre-launch audit) but the active project has no local Astro skills — i.e. any project other than "SIP - Astro" itself. Routes the task to the central Astro knowledge hub instead of improvising from general knowledge. Also use when the user asks "existe algo de astro pra isso", "tem skill de astro no hub", or names Astro skills explicitly in a project that isn't the hub.
---

# sip-astro — ponteiro para o hub central de Astro

O conteúdo real desta skill (redirecionador: modo consulta, dispatch, contribuição, e a tabela gerada de skills) vive no hub central "SIP - Astro":

```text
/Users/macbookpro/Documents/IA Projects/_Plataforma/Base Sites - Astro/.agent/skills/sip-astro/SKILL.md
```

Leia o `SKILL.md` nesse caminho e siga normalmente — este arquivo só existe para que a busca por nome (Regra 4) encontre o ponteiro. Ele **não lista as skills do hub** (a lista envelheceria): a fonte é a tabela gerada no resolver do hub e o roteador `/Users/macbookpro/Documents/IA Projects/_Plataforma/Base Sites - Astro/.agent/skills/astro-development/SKILL.md`.

O SIP é um redirecionador: um projeto consumidor instala só o resolver (um symlink). As skills `astro-*` e os scripts ficam no hub e são lidos/rodados por caminho absoluto; não symlinke nem copie nenhuma. Para instalar o acesso permanente em outro projeto, veja `/Users/macbookpro/Documents/IA Projects/_Plataforma/Base Sites - Astro/prompts/instalar-skill-sip-astro.md`.

## Agents e workflows do hub

Agents (`.agent/agents/`) e workflows (`.agent/workflows/`) do hub estão listados no resolver acima e podem ser lidos por caminho absoluto em `/Users/macbookpro/Documents/IA Projects/_Plataforma/Base Sites - Astro/.agent/` (ou usados localmente se este projeto escolheu instalá-los).

## Atualização

Data da última atualização e instruções: seção "Atualização" do resolver no hub
(`/Users/macbookpro/Documents/IA Projects/_Plataforma/Base Sites - Astro/.agent/skills/sip-astro/SKILL.md`). Para atualizar a instalação num
projeto, cole de novo `/Users/macbookpro/Documents/IA Projects/_Plataforma/Base Sites - Astro/prompts/instalar-skill-sip-astro.md`.
