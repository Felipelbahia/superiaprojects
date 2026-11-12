---
name: sip-marketing
description: Use whenever the current task involves marketing, content, copywriting, branding, social media, SEO, paid ads, email, PR, growth, sales enablement or marketing analytics but the active project has no local marketing skills — i.e. any project other than "SIP - Marketing" (0 Mkt) itself. Routes the task to the central marketing knowledge hub instead of improvising from general knowledge. Also use when the user asks "existe algo de marketing pra isso", "tem skill de marketing no hub", "consulta o SIP - Marketing", or names a 0 Mkt skill, agent or workflow explicitly in a project that isn't the hub.
---

# sip-marketing — ponteiro para o hub central de marketing

O conteúdo real desta skill (redirecionador: marca e destino do projeto consumidor, modo consulta, dispatch, contribuição e a tabela gerada de skills) vive no hub central "SIP - Marketing":

```text
/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Mkt/.agent/skills/sip-marketing/SKILL.md
```

Leia o `SKILL.md` nesse caminho e siga normalmente. Este arquivo só existe para que a busca por nome (Regra 4) encontre o ponteiro. Ele **não lista as skills do hub** (a lista envelheceria): a fonte é a tabela gerada no resolver do hub.

O SIP é um redirecionador: um projeto consumidor instala só o resolver (um symlink). Skills, agents e workflows ficam no hub e são lidos por caminho absoluto; não symlinke nem copie nenhum. Para instalar o acesso permanente em outro projeto, veja `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Mkt/prompts/instalar-skill-sip-marketing.md`.

## Agents e workflows do hub

Agents (`.agent/agents/`) e workflows (`.agent/workflows/`) do hub estão listados no resolver acima e podem ser lidos por caminho absoluto em `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Mkt/.agent/` (ou usados localmente se este projeto escolheu instalá-los).

## Atualização

Data da última atualização e instruções: seção "Atualização" do resolver no hub
(`/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Mkt/.agent/skills/sip-marketing/SKILL.md`). Para atualizar a instalação num
projeto, cole de novo `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Mkt/prompts/instalar-skill-sip-marketing.md`.
