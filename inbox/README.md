# Inbox — contribuições de outros projetos

Porta de entrada para qualquer projeto que, usando a skill `sip-geral`, tenha
aprendido algo sobre geral e queira devolver ao hub: um insight, um
exemplo novo, ou uma melhoria numa skill existente.

**Ninguém edita `.agent/skills/` (ou pastas de exemplos/workflows) direto a
partir de outro projeto.** O conteúdo cai aqui primeiro e é promovido
manualmente para o lugar certo durante uma revisão do hub. Os itens desta pasta
ficam fora do git do hub (só este README é versionado).

## Como contribuir

1. Crie `inbox/NNN-<assunto-curto>.md`, com `NNN` = próximo número livre desta
   pasta (contando `arquivo/`). Duas sessões podem usar o mesmo número ao mesmo
   tempo: tudo bem, o assunto diferencia. Nunca renumere arquivos existentes.
2. Escreva para uma IA que nunca viu a sua conversa: caminhos absolutos,
   frases literais como âncora (números de linha mudam), evidência.
3. Formato:
   ```markdown
   # NNN — <título>
   Status: na inbox · Aberto em: AAAA-MM-DD · Pedido por: <quem> · Projeto de origem: <nome e caminho>

   ## O quê
   ## Como (o que fazer quando for pedido)
   ## Onde (arquivos, skills, pastas do hub)
   ## Por quê (o que depende disto; evidência)
   ## Para quê (critério de sucesso)
   ## Quem (decide / aplica / afetados)
   ## Efeitos e impactos (o que muda, o que acontece se nada for feito)
   ## Exemplos
   ## Gatilho para sair da inbox
   ## Enquanto isso
   ```
4. Não edite nada fora desta pasta.

## Revisão (lado do hub)

Itens da inbox não são analisados até o dono do hub pedir. Ao resolver um item:
mude o `Status` para `feito em AAAA-MM-DD` com o link do que resolveu e **mova o
arquivo para `inbox/arquivo/`**. Nunca apague. Se o item não for aplicado, o mesmo:
`Status: descartado em AAAA-MM-DD` com o motivo, e mova.

## Itens

| # | Item | Onde muda | Prioridade |
|---|---|---|---|
| 001 | ~~Reabertura de loop encerrado~~ (aplicado 2026-11-11, em `arquivo/`) | skill `execution-loop` | Alta |
| 002 | ~~Quem gradua: revisão independente e script de verificação~~ (aplicado 2026-11-11, em `arquivo/`) | skill `execution-loop` | Alta |
| 003 | ~~Briefing para subagente leitor (imagens e documentos)~~ (aplicado 2026-11-11, em `arquivo/`) | skill `execution-loop` (e `orchestrator`) | Alta |
| 004 | ~~Convenção `inbox/` para itens adiados~~ (aplicado 2026-11-11, em `arquivo/`) | `CLAUDE.md` (paridade) e `project-defines` | Média |
| 005 | ~~Documento único gerado + script de verificação~~ (aplicado 2026-11-11 como skill `deliverable-verification`, em `arquivo/`) | nova skill (ou seção de `plan-writing`) | Média |
| 006 | ~~Combinar a forma do entregável antes de construir~~ (aplicado 2026-11-11, em `arquivo/`) | skill `brainstorming` | Média |
| 007 | ~~Teste de base de skill de processo dentro do repositório~~ (aplicado 2026-11-11, em `arquivo/`) | skill `writing-skills` | Média |
| 008 | ~~Corrigir o texto da sincronização do catálogo~~ (aplicado 2026-11-11, em `arquivo/`) | skill `writing-skills` | Baixa |
| 009 | ~~Falso erro do `sync_entrypoints.py` com agente-link para o hub N8N~~ (aplicado 2026-11-11 com o 018, em `arquivo/`) | script `sync_entrypoints.py` | Baixa |
| 010 | ~~Número reportado ao usuário vem de comando~~ (aplicado 2026-11-11, em `arquivo/`) | skill `verification-before-completion` | Média |
| 011 | ~~Portão de fechamento: lint e suíte inteira, com o código congelado~~ (aplicado 2026-11-11, em `arquivo/`) | skill `execution-loop` | Alta |
| 012 | ~~Citação literal do dono, conferida com grep~~ (encerrado 2026-11-11 sem mudança: RED já passa, em `arquivo/`) | skill `execution-loop` (e `spec-writing`) | Média |
| 013 | ~~Artefatos que a rubrica avalia são atualizados antes do QA~~ (encerrado 2026-11-11 sem mudança: RED já passa, em `arquivo/`) | skill `execution-loop` | Média |
| 014 | ~~Passos com código de terceiros ou que mudam a configuração do agente: combinar no Brainstorm~~ (aplicado 2026-11-11, em `arquivo/`) | skill `execution-loop` | Alta |
| 015 | ~~Sessões concorrentes: retrato antes e depois, e atribuição~~ (aplicado 2026-11-11, em `arquivo/`) | skill `execution-loop` | Média |
| 016 | ~~Comando impresso funciona como impresso~~ (encerrado 2026-11-11 sem mudança: RED já passa; em `arquivo/`) | skill `verification-before-completion` | Média |
| 017 | ~~Testes de skills: texto com o caminho literal, arquivos com o local~~ (aplicado 2026-11-11, em `arquivo/`) | skill `writing-skills` | Média |
| 018 | ~~Hook de commit versionado para checagens rápidas~~ (aplicado 2026-11-11, hook ativo; em `arquivo/`) | skill `project-initializer` + próprio 0 Padrões | Média |
| 019 | ~~Nova skill `github-publisher`~~ (criada 2026-11-11, em `arquivo/`) | nova skill global (`github-publisher`) | Média |
| SIP-020 | ~~Migrar os 7 SIPs para o padrão único (tabelas + instalação opcional)~~ (feito 2026-11-15, em `arquivo/`; reverificado 2026-11-18: 23/23 PASS nos 7 hubs) | 7 hubs SIP, `_sips.md` | Média |
| SIP-020 | ~~Manifestos dos consumidores de SIP sem a linha "Para atualizar"~~ (feito 2026-11-15, em `arquivo/`; reverificado 2026-11-18: 59 manifestos, nenhum sem a linha) | `.agent/SIPS-CONSUMIDOS.md` dos 8 consumidores externos | Baixa |
| 021 | ~~Stubs de SIP do 0 Padrões sem a seção "Atualização"~~ (aplicado 2026-11-11, em `arquivo/`) | 7 stubs `sip-*` + `superiaprojects-criar-sip` (Passo 5) | Média |
| 022 | ~~`.gitignore` padrão: backups de `.env` e 0 Padrões sem regras de `.env`~~ (aplicado 2026-11-11, em `arquivo/`) | `project-initializer` + `.gitignore` do 0 Padrões + `github-publisher` | Média |
| 023 | ~~`.claude/CLAUDE.md` duplicado e regras antigas~~ (resolvido na auditoria geral em 2026-11-15, em `arquivo/`) | todos os projetos com regras | Alta |
| 024 | ~~README do FM aponta para os prompts de inteligência arquivados~~ (aplicado 2026-11-17, em `arquivo/`) | README do Futuro Mercado | Média |
| 025 | ~~Kit de onboarding para clonar e rodar em outra máquina~~ (feito 2026-11-15, em `arquivo/`: regra nas skills e no módulo `code`; retrofit registrado na `inbox/` de cada projeto, que o aplica ao processar a própria inbox) | `project-initializer` + `github-publisher` + retrofit dos projetos | Média |
| 028 | ~~UX Audit falha no catálogo~~ (aplicado 2026-11-17, em `arquivo/`; checklist completo depende do 033) | `ux_audit.py`, `generate_catalog.py` | Média |
| 037 | ~~test_runner.py chama `python` no macOS~~ (aplicado 2026-11-18, em `arquivo/`) | `test_runner.py` | Média |
| 038 | ~~UX Audit aplica regras de app a e-mail e acusa falsos positivos~~ (aplicado 2026-11-18, em `arquivo/`) | `ux_audit.py` | Média |
| 032 | ~~Regras locais perdidas ou lixo antigo achados pelo check_local_rules.py~~ (resolvido na auditoria em 2026-11-15, em `arquivo/`) | #22, #42, #44 e ecossistema | Alta |
| 034 | ~~writing-agents: ideias de estrutura da revisão~~ (aplicado 2026-11-18: hook de auto-edição, check de ferramentas, modo do Papel; em `arquivo/`) | `writing-agents`, `sync_entrypoints.py`, `.claude/settings.json` | Média |
| 035 | ~~Mapeamento de modelos Antigravity/Claude e migração dos agentes~~ (aplicado 2026-11-18, Opção A, em `arquivo/`) | `.agent/agents/*.md` | Média |
| 040 | ~~propagar_sip.py aceitar a cópia gerada do resolver~~ (aplicado 2026-11-18, em `arquivo/`; stub `sip-astro` do 0 Padrões reinstalado como cópia gerada em 2026-11-18) | `propagar_sip.py`, `sips_status.py` | Média |
| 036 | ~~session-handoff: armadilha do zsh~~ (encerrado 2026-11-18 sem mudança: RED já passa, em `arquivo/`) | skill `session-handoff` | Baixa |
| 042 | ~~A seção 3 das regras ainda exige GEMINI.md, mas o `sync_rules.py` o trata como legado~~ (aplicado antes de 2026-11-19, commit `f05fbd8`; conferido e arquivado em 2026-11-19, em `arquivo/`) | `core.md`, `sync_rules.py` | Média |
| 043 | ~~Regras: buscar no SIP o que não está instalado e disciplina de mudança~~ (aplicado 2026-11-19, em `arquivo/`; notas gravadas nos 58 projetos; remontagem de cada um no loop de propagação) | módulos de regras, `project-initializer`, kit de instalação, `checklist.py` | Alta |
| 044 | ~~`scope_check.py`: glob que começa com ponto (`.agent/...`) nunca casa~~ (aplicado 2026-11-19, em `arquivo/`) | `scope_check.py` | Alta |
| 045 | ~~`execution-loop` dá `Unknown skill` em projeto consumidor~~ (aplicado 2026-11-20 como núcleo de skills + `resolve_skill.py`, em `arquivo/`) | `sip-geral`, regras (core), scripts de SIP | Alta |
| 047 | Propagar o núcleo aos consumidores e provar em sessão real | `propagar_sip.py`, 63 projetos | Alta |
| 048 | ~~Cópia global do `skill-resolver` diverge do hub~~ (aplicado 2026-11-20, em `arquivo/`) | `~/.claude/skills/skill-resolver` | Baixa |
| 049 | Remontar as regras do kit nos projetos, em sessões por faixa (loop pronto em `.agent/plans/execution-loops/2026_11_20/Remontar Regras nos Projetos/`) | 58 projetos (`CLAUDE.md`/`AGENTS.md`) | Média |


Ordem sugerida: 001, 002, 003 (maior retorno na origem); depois 010, 006, 007; o resto quando fizer sentido. Os itens 001 a 003 mexem no mesmo arquivo: aplique em sequência, com um commit por item. Os itens 011 a 017 vieram do SIP Astro (`/Users/macbookpro/Documents/IA Projects/_Plataforma/Base Sites - Astro`, 2026-11-10); 011 a 015 também mexem no `execution-loop`, então entram na mesma fila sequencial (sugestão: 011 e 014 primeiro).

## Protocolo geral para aplicar um item (obrigatório)

1. **Peça confirmação do Felipe** para aquele item. Não aplique vários de uma vez.
2. **Leia** a skill de destino inteira e `writing-skills/SKILL.md` (lei de ferro: nenhuma skill, nem edição de skill, sem teste de base que falhe primeiro; método em `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/skills/writing-skills/testing-skills-with-subagents.md`).
3. **RED:** rode o cenário do item em um subagente **sem** a mudança e guarde as respostas literais. Se o agente já fizer o certo, **pare** e relate: não há o que corrigir.
4. **Edite** só o que o item descreve, no idioma da skill de destino (as skills do kit estão em inglês; comentários em português apenas onde a skill já usa). Não reescreva o resto, não mude o `description` do frontmatter para resumir o fluxo (o `description` diz só *quando usar*).
5. **GREEN:** repita o cenário com a skill editada; o agente deve cumprir. Se achar brecha, feche com um contra explícito e repita.
6. **Sincronize**, a partir da raiz do `0 Padrões`:
   - `python3 .agent/scripts/generate_catalog.py` (sempre que uma skill muda);
   - `python3 .agent/scripts/sync_entrypoints.py` (se mudou frontmatter, agente ou workflow; `--check` só valida);
   - `python3 .agent/scripts/sync_rules.py` (se mudou qualquer arquivo de regras: `CLAUDE.md`, `AGENTS.md`, e `.cursorrules`/`.claude/CLAUDE.md` se existirem; precisam ficar idênticos).
7. **Cópias locais:** verifique se algum projeto tem cópia local da skill (`find "/Users/macbookpro/Documents/IA Projects" -maxdepth 7 -path "*/.agent/skills/<nome>" -type d`). Em 2026-11-10 só o `0 Padrões` tinha `execution-loop`. Cópia nunca é a fonte; se achar, sincronize ou avise.
8. **Registre:** atualize o `Status` do arquivo do item para `aplicado em AAAA-MM-DD` com o commit e o link do teste, e a tabela acima. Depois **mova o arquivo para `inbox/arquivo/`** (pedido do Felipe em 2026-11-11). Não apague o arquivo.
9. **Não faça commit** sem o Felipe pedir. O repositório `0 Padrões` já tinha alterações não commitadas em 2026-11-10 (catálogo, traduções, remoção de `firecrawl-agent`) que não são deste trabalho: não as inclua sem perguntar.

## Convenções destes arquivos
Seções: o quê · onde · por quê · para quê · quem · quando · contexto e evidência · texto pronto · como aplicar (RED e GREEN) · não fazer · perguntas abertas. Caminhos são absolutos. Âncoras de edição são **títulos e frases literais** (números de linha mudam). Evidências citam arquivos do projeto de origem (`/Users/macbookpro/Documents/IA Projects/Plinq/Martech/Inngage/.agent/plans/execution-loops/2026_11_10/Mapeamento de Eventos e Engajamento`), que pode ser lido, não editado.

## Origem em uma página
Em 2026-11-10 o projeto Inngage produziu um diagnóstico de plano de rastreamento (`/Users/macbookpro/Documents/IA Projects/Plinq/Martech/Inngage/docs/diagnostico-engajamento`) sob o `execution-loop`. O loop fechou nota 10 no ciclo 2 e, quando chegou material novo, a revisão seguinte reprovou 6 de 10 itens; uma terceira revisão achou 28 pontos no catálogo. Os pontos abaixo são o que valeria levar ao kit. A skill local nascida do trabalho é `/Users/macbookpro/Documents/IA Projects/Plinq/Martech/Inngage/.agent/skills/diagnostico-tracking-plan/`.
