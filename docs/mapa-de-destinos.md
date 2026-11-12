# Mapa de destinos: 0 Padrões (Super IA Projects)
Produz: misto (software: scripts e testes do kit; conteúdo: skills, agents, prompts, regras). Estrutura: mono-marca.
Atualizado em 2026-11-12. Se este mapa divergir de uma regra de skill, **vale este mapa**. Tipo de entrega que não está aqui entra aqui antes de ser gravado.

| Tipo de entrega | Caminho | Nome e metadados | Observação |
|---|---|---|---|
| Skill | `.agent/skills/<nome>/SKILL.md` (+ `references/`, `scripts/`, `tests/`) | nome em kebab-case | fixo pelas regras; exposta por link em `.claude/skills/<nome>`; skill aposentada em `.agent/skills/_arquivo/` (a pasta nasce com a primeira aposentadoria; os scripts de catálogo não a enxergam) |
| Agent | `.agent/agents/<nome>.md` | `name` + `description` | fixo pelas regras; link em `.claude/agents/` |
| Workflow (`/comando`) | `.agent/workflows/<nome>.md` | `description`, `disable-model-invocation: true` | fixo pelas regras; link em `.claude/commands/` e `.cursor/commands/` |
| Módulo de regras | `.agent/skills/project-initializer/modules/<nome>.md` | | o `CLAUDE.md` é gerado deles (`assemble_rules.py`); nunca editar o `CLAUDE.md` à mão |
| Scripts do kit e testes | `.agent/scripts/` · `.agent/scripts/tests/test_<script>.py` | | código: segue o `STANDARDS.md` |
| Prompt para colar | `prompts-template/NN-<assunto>.md` (versionado, com `<SUPER_IA_PROJECTS_PATH>`) + `projetos/prompts/NN-<assunto>.md` (cópia local, caminho absoluto) | `NN-` = número do prompt | aposentados em `_arquivo/` nas duas pastas; as duas cópias com o mesmo texto |
| Prompt de instalação do SIP | `prompts/instalar-skill-sip-geral.md` | | padrão SIP (`superiaprojects-criar-sip`) |
| Ficha de projeto | `projetos/<Nome do Projeto>.md` · índice de SIPs em `projetos/_sips.md` | linha "Última sincronização com o kit" | fora do git |
| Registro de instalação de SIP | `instalacoes/<projeto>.md` | | fora do git; só o `README.md` versionado |
| SIPs consumidos | `.agent/SIPS-CONSUMIDOS.md` | | mantido pelo prompt de instalação de cada SIP |
| Catálogo e contagens | `.agent/CATALOG.md`, `.agent/catalog.html`, `.agent/catalog-data.js`, `.agent/ARCHITECTURE.md` | | gerados por script (`generate_catalog.py`, `sync_entrypoints.py --write-docs`); nunca à mão |
| Relatório de projetos vs kit | `.agent/plans/Relatório de projetos vs kit.md` | | gerado pelo `projects_audit.py` |
| Documentação pública do repositório | raiz: `README.md`, `README.en.md`, `SETUP.md`, `STANDARDS.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md` | | imagens em `assets/` |
| Documentação de terceiros | `.agent/vendor/` | | fora do git |
| Código (scripts, hooks, configs) | segue o `STANDARDS.md` | | fora do mapa; hook em `.githooks/` |
| Planos, loops, handoffs, artefatos do Antigravity, backups de regras | `.agent/plans/` | `execution-loops/AAAA_MM_DD/<Título>/NN Nome.md`, `handoffs/`, `{Tarefa} [PLAN\|TASK\|WALKTHROUGH].md` | fixo pelas regras do kit; fora do git |
| Itens adiados | `inbox/` (resolvidos em `inbox/arquivo/`) | `NNN-assunto.md` | fixo pelas regras do kit; fora do git, só o `README.md` versionado |
| Memória de longo prazo | `memory.md` | `Problema → Solução` | fixo pelas regras do kit; ainda não existe (ver Inconsistências) |
| Este mapa e documentos do projeto | `docs/` | | |

## Como usar este mapa (toda IA e skill que grava arquivo)
1. Leia esta tabela antes de gravar. Use o **Caminho** da linha do tipo de entrega, preenchendo os placeholders. Não monte caminho por conta própria.
2. Tipo de entrega que não está aqui: acrescente a linha antes de gravar e avise o dono.
3. Pasta citada aqui que não existe: crie só essa pasta.
4. Nunca mova nem apague arquivo existente para encaixar na estrutura; mudança de lugar só com aprovação.
5. Dúvida que este mapa não resolve: skill `mapa-de-destinos`.

## Respostas da conversa de criação
| Pergunta | Resposta | Data |
|---|---|---|
| O que o projeto entrega além de código? | A tabela acima, montada do que o kit já faz (projeto existente: documentar, sem mover). Dono: "concordo" | 2026-11-12 |
| Há mais de uma marca ou produto? | Não: mono-marca (Super IA Projects, publicado pela Futuro Mercado). Dono: "sim" à proposta mono-marca | 2026-11-12 |
| Onde moram as marcas? | Não se aplica (mono-marca) | 2026-11-12 |
| O que é compartilhado? | Não se aplica (mono-marca) | 2026-11-12 |
| Fluxo de aprovação | Opção 0, sem esteira: o kit não produz peças de conteúdo; o que vai a público é o repositório no GitHub. Dono: "ok" | 2026-11-12 |
| Quem aprova | O dono (Felipe Bahia), a cada push para o GitHub | 2026-11-12 |

## Inconsistências conhecidas
O que as regras dizem versus a árvore real. Nada foi movido; mudança só com aprovação do dono.
- `memory.md` não existe, mas a seção Learn das regras manda atualizá-lo quando um problema crítico é resolvido ou uma decisão é tomada.
- `.agent/eduzz_workflow.json`: exportação de workflow versionada na raiz do `.agent/` desde o commit inicial, sem ser parte do kit (o lugar natural seria o SIP- N8N ou o projeto dono do workflow).
- `.firecrawl/install-check.md` (jul/2026): sobra local do Firecrawl, que saiu do núcleo do kit (ignorado pelo git).
- Os prompts existem em duas cópias (`prompts-template/` e `projetos/prompts/`) que precisam ser mantidas iguais à mão; hoje o `02` diverge entre elas (pendência registrada no handoff de 2026-11-12).
