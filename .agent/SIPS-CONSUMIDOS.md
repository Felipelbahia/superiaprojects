# SIPs consumidos por este projeto

Manifesto local — contrapartida de `instalacoes/<nome-deste-projeto>.md` do
lado de cada hub. Lista o que este projeto depende de outros hubs de
conhecimento (SIPs), sem precisar abrir `.gitignore` nem seguir cada
symlink manualmente. Mantido pelo prompt de instalação de cada SIP (ver
`0 Padrões/projetos/_sips.md` pro índice central de todos os SIPs).

**Nota: o 0 Padrões é exceção ao padrão duplo** — usa symlink único em
`.claude/` direto pro hub (não `.agent/` + `.claude/`), porque seu próprio
`.agent/skills/sip-<dominio>` já é o stub global real, não pode também ser
symlink pro hub. Ver `_sips.md` seção "Exceção: 0 Padrões não usa o padrão
duplo como consumidor".

## SIP- N8N (`sip-n8n`)
- Hub: /Users/macbookpro/Documents/IA Projects/_Plataforma/SIP- N8N
- Instalado/atualizado em: 2026-11-06
- Skill: sip-n8n
- Agents: n8n-agent
- Workflows: nenhum
- Para atualizar: cole de novo "/Users/macbookpro/Documents/IA Projects/_Plataforma/SIP- N8N/prompts/instalar-skill-sip-n8n.md"

## SIP - Mautic (`sip-mautic`)
- Hub: /Users/macbookpro/Documents/IA Projects/Plinq/Martech/Mautic
- Instalado/atualizado em: 2026-11-05
- Skill: sip-mautic
- Agents: nenhum
- Workflows: nenhum
- Para atualizar: cole de novo "/Users/macbookpro/Documents/IA Projects/Plinq/Martech/Mautic/prompts/instalar-skill-sip-mautic.md"

## SIP - Firecrawl (`sip-firecrawl`)
- Hub: /Users/macbookpro/Documents/IA Projects/_Plataforma/Firecrawl - local
- Instalado/atualizado em: 2026-11-06
- Skill: sip-firecrawl
- Agents: nenhum
- Workflows: nenhum
- Para atualizar: cole de novo "/Users/macbookpro/Documents/IA Projects/_Plataforma/Firecrawl - local/prompts/instalar-skill-sip-firecrawl.md"

## SIP - Trends e Previsão de Demanda (`sip-trends-previsao-demanda`)
- Hub: /Users/macbookpro/Documents/IA Projects/Compartilhado/Previsão de Demanda
- Instalado/atualizado em: 2026-11-05
- Skill: sip-trends-previsao-demanda
- Agents: nenhum
- Workflows: nenhum
- Para atualizar: cole de novo "/Users/macbookpro/Documents/IA Projects/Compartilhado/Previsão de Demanda/prompts/instalar-skill-sip-trends-previsao-demanda.md"

## SIP - Imprensa & PR (`sip-imprensa`)
- Hub: /Users/macbookpro/Documents/IA Projects/Compartilhado/RSS Feed
- Instalado/atualizado em: 2026-11-06
- Skill: sip-imprensa
- Agents: nenhum
- Workflows:
  - buscar-jornalistas-e-veiculos
  - criar-personalizar-releases
  - onboarding-novo-jornalista
  - perfil-jornalista
  - radar-semanal
- Para atualizar: cole de novo "/Users/macbookpro/Documents/IA Projects/Compartilhado/RSS Feed/prompts/instalar-skill-sip-imprensa.md"

## SIP - Astro (`sip-astro`)
- Hub: /Users/macbookpro/Documents/IA Projects/_Plataforma/Base Sites - Astro
- Instalado/atualizado em: 2026-11-07
- Skill: sip-astro (stub global + symlink `.claude/skills/sip-astro`; redirecionador: as skills astro-* são lidas por caminho absoluto no hub, não instaladas)
- Agents: nenhum
- Workflows: nenhum
- Para atualizar: cole de novo "/Users/macbookpro/Documents/IA Projects/_Plataforma/Base Sites - Astro/prompts/instalar-skill-sip-astro.md"

## SIP - Marketing (`sip-marketing`)
- Hub: /Users/macbookpro/Documents/IA Projects/_Plataforma/0 Mkt
- Instalado/atualizado em: 2026-11-09
- Skill: sip-marketing (stub global + symlink `.claude/skills/sip-marketing`; redirecionador: skills, agents e workflows do 0 Mkt são lidos por caminho absoluto no hub, não instalados)
- Agents: nenhum (lidos no hub)
- Workflows: nenhum (lidos no hub)
- Para atualizar: cole de novo "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Mkt/prompts/instalar-skill-sip-marketing.md"
