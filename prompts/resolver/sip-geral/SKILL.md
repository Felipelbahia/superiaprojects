---
# Repository: https://github.com/Felipelbahia/superiaprojects
name: sip-geral
description: Use when the current task involves general software engineering, architecture, backend, frontend, mobile, database, testing, security, DevOps, AI/ML or development workflows (spec, planning, execution-loop, TDD, debugging) in any project other than "SIP - Geral" (0 Padrões) itself, or when the user asks "existe algo no 0 Padrões pra isso", "tem skill/agent/workflow pra isso no hub geral", "consulta o SIP - Geral", or names a 0 Padrões skill, agent or workflow explicitly in a consumer project, or when the project rules (CLAUDE.md / AGENTS.md) cite a skill, agent or workflow by name (for example session-handoff, brainstorming, execution-loop) that is missing from the available skills list: search here before saying it does not exist.
author: Futuro Mercado / Felipe Bahia (@felipelbahia)
license: MIT
---

# sip-geral

## Por que isso existe

O projeto `SIP - Geral` (`/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões`) é a referência central de conhecimento em geral. Esse conhecimento só é descoberto automaticamente dentro do próprio hub. Em qualquer outro projeto, nada aponta para ele: sem esta skill, a IA tende a reinventar padrões do zero. Esta skill é o ponteiro que faz a ponte: ela não ensina, leva até quem ensina.

## Passo 0 — acesso ao caminho

Leitura de arquivo fora do diretório de trabalho pode pedir aprovação do usuário na primeira vez; isso é esperado. Sempre use o caminho absoluto entre aspas: `"/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões"`.

## Skill que as regras citam e a ferramenta Skill não acha (`Unknown skill`)

Isso não é erro do projeto: a skill mora no hub (ou em outro SIP) e não está em
`.claude/skills/`. Não repita a chamada e não pare. Na raiz do projeto, rode:
`python3 "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/scripts/resolve_skill.py" <nome ou termo>`
Ele devolve o caminho absoluto, o SIP de origem e se esse SIP está instalado
neste projeto (lê os hubs no disco agora, não o manifesto, que é só uma foto da
instalação). Leia o `SKILL.md` por esse caminho, avise o dono em uma linha ("a
skill X vem do hub, li por caminho") e siga. Sem resultado, o script mostra onde
procurou: só então diga que não existe. SIP não instalado: ofereça o prompt de
instalação que o script mostra. O núcleo (lista em
`/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/prompts/resolver/sip-geral/nucleo.json`, se existir) já vem
linkado no projeto, e essas a ferramenta Skill acha.

## Passo 1 — classifique a tarefa

| Tipo de tarefa | O que fazer |
| --- | --- |
| **Consulta pontual** | **Modo consulta** (abaixo). |
| **Construção grande / multi-arquivo** | **Modo dispatch** (abaixo). |

## Modo consulta (padrão — prefira este)

1. Ache a vertical na tabela do índice abaixo pela coluna "Use quando". Para casos ambíguos, leia o roteador mestre do hub: `"/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/skills/intelligent-routing/SKILL.md"`.
2. Leia só o arquivo da vertical: `"/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/prompts/resolver/sip-geral/verticais/<vertical>.md"`. Ali estão as skills, agents e workflows daquela área, cada um com o seu "Use quando". Sem certeza da vertical: `grep -ril "<palavra>" "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/prompts/resolver/sip-geral/verticais/"`.
3. Leia só o arquivo do item escolhido, por caminho absoluto no hub: `"/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/skills/<nome>/SKILL.md"`. Nunca symlinke nem copie skills especialistas do hub para o projeto (só o núcleo vem linkado pelo instalador).
4. Aplique o conteúdo inline e avise em uma linha que a resposta veio do hub `SIP - Geral`, não de conhecimento genérico.

## Modo dispatch (só para construções grandes)

Não existe invocação nativa de agente cross-projeto no Claude Code. "Disparar" um agent do hub é montar um subagente genérico (`Agent`, `subagent_type: "general-purpose"`) com a persona colada no prompt:

1. Leia a persona do agent especialista (`"/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/agents/<nome>.md"`, achado na vertical) e as skills relevantes.
2. Chame `Agent` com o conteúdo colado + a tarefa concreta.
3. Valide o resultado contra a skill de validação do hub (se existir) antes de aplicar.

Agent ou workflow que o projeto não instalou: use-o assim mesmo, pelo caminho absoluto. Só ofereça instalar se o usuário disser que vai usá-lo com frequência; nunca instale por conta própria.

## Índice de verticais

<!-- indice:start dir=verticais (gerado por build_sip_index.py — não edite à mão) -->

Total: 203 skills, 119 agents, 111 workflows.

| Vertical | Use quando | Skills | Agents | Workflows | Arquivo |
| --- | --- | --- | --- | --- | --- |
| `seguranca` | Segurança: auditoria, SAST, modelagem de ameaças e STRIDE, segredos, vulnerabilidades, engenharia reversa e forense, mTLS, conformidade (LGPD/GDPR, PCI), contratos e agentes de pentest e resposta a incidentes de segurança. | 23 | 11 | 6 | `verticais/seguranca.md` |
| `mobile-e-jogos` | Apps mobile (iOS, Android, React Native, Flutter) e desenvolvimento de jogos (Unity, Godot, Minecraft). | 8 | 6 | 1 | `verticais/mobile-e-jogos.md` |
| `ia-e-ml` | IA e ML: LLMs, RAG, embeddings, busca vetorial e híbrida, avaliação, prompts, pipelines de ML, MCP, agentes de IA e análise quantitativa. | 12 | 8 | 7 | `verticais/ia-e-ml.md` |
| `documentacao` | Documentação: ADRs, templates, runbooks, postmortem, tutoriais, referência de API, diagramas (Mermaid, C4) e explicação de código. | 4 | 10 | 3 | `verticais/documentacao.md` |
| `arquitetura-e-qualidade` | Arquitetura e qualidade: padrões e decisões de arquitetura, microsserviços, CQRS e event sourcing, código limpo, refatoração, modernização, dependências, performance, débito técnico e a família ponytail (simplicidade e auditoria). | 17 | 8 | 6 | `verticais/arquitetura-e-qualidade.md` |
| `dados-e-banco` | Bancos e dados: modelagem, SQL, PostgreSQL, Supabase, migrações, ETL (dbt, Airflow, Spark), qualidade de dados, KPIs e storytelling com dados. | 11 | 5 | 3 | `verticais/dados-e-banco.md` |
| `devops-e-cloud` | DevOps e nuvem: CI/CD, Kubernetes, Helm, service mesh, Terraform, observabilidade, SLO, incidentes, deploy, custo, shell e monorepo. | 30 | 12 | 8 | `verticais/devops-e-cloud.md` |
| `testes-e-depuracao` | Testes e depuração: TDD, testes unitários, E2E e de interface, QA, depuração sistemática, análise de erros e lint. | 14 | 6 | 12 | `verticais/testes-e-depuracao.md` |
| `frontend-e-design` | Frontend e interface: React, Next.js, Tailwind, design system, UX/UI, responsivo, acessibilidade (WCAG), componentes web, i18n e landing pages. | 21 | 10 | 10 | `verticais/frontend-e-design.md` |
| `negocio-e-produto` | Negócio e produto: startups, métricas, mercado, finanças, vendas, suporte, RH, gestão de produto e planejamento de projeto. | 5 | 10 | 6 | `verticais/negocio-e-produto.md` |
| `backend-e-apis` | Backend e APIs: design de API, OpenAPI, Node, Python, Go, Rust, .NET, Java e outras linguagens, pagamentos (Stripe, PayPal), web3 e blockchain. | 16 | 21 | 4 | `verticais/backend-e-apis.md` |
| `git-e-revisao` | Git, commits, pull requests e revisão de código: worktrees, changelog, descrição de PR, revisão local e completa. | 10 | 1 | 14 | `verticais/git-e-revisao.md` |
| `planejamento-e-processo` | Fluxo de trabalho e planejamento: brainstorming, spec, plano, loop de execução, orquestração, subagentes, handoff, pesquisa no código e criação de skills, agents e workflows. | 32 | 11 | 31 | `verticais/planejamento-e-processo.md` |

<!-- indice:end -->

## Modo contribuição (devolver conhecimento ao hub)

**Exceção primeiro:** se o dono do hub pediu a mudança nesta conversa (indicou o hub como destino e revisou a decisão antes de qualquer arquivo ser escrito), edite `.agent/skills/`, `.agent/agents/` ou `.agent/workflows/` do hub direto, sem passar pelo inbox.

Caso contrário (sessão num projeto consumidor, sem o dono revisando aquela edição), nunca edite essas pastas do hub: elas são lidas por caminho absoluto por todos os consumidores e uma edição sem curadoria propagaria na hora. Em vez disso:

1. Leia o formato em `"/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/inbox/README.md"`.
2. Crie `"/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/inbox/NNN-<assunto>.md"` (próximo número livre da pasta) com todas as seções do formato, escrito para quem nunca viu a conversa.
3. Avise o usuário que a contribuição ficou pendente de revisão, com o caminho do arquivo.

## Atualização

- Última atualização do hub: 2026-11-20 (o dono do hub muda esta data sempre que esta skill, um agent, um workflow ou a estrutura do hub mudar).
- Para atualizar a instalação num projeto (refazer links, escolher entre os agents/workflows novos): cole de novo o prompt `"/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/prompts/instalar-skill-sip-geral.md"` numa sessão daquele projeto.
- A data em que **cada projeto** instalou ou atualizou fica no `.agent/SIPS-CONSUMIDOS.md` dele. Se for anterior à data acima, ofereça rodar o prompt.

## Se nada bater

Se a tarefa não é de geral, ou se o projeto atual é o próprio `SIP - Geral`, não force o uso desta skill.
