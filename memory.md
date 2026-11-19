# Memory — 0 Padrões

Problema → Solução, só o que não se deduz do código.

## 2026-11-13 — atualização de projeto cortava regras locais
- **Problema:** na propagação, o `CLAUDE.md` do Remote Brain perdeu 3 frases de segurança (item 7 do Protocolo de Execução Remota) e uma tabela de roteamento; o do Vagas perdeu a regra do prefixo `[jobs]` do banco compartilhado. Causa: `assemble_rules.py --replace` descarta o arquivo antigo; o prompt de atualização mandava conferir com "grep de um trecho" (passa com a linha cortada); nenhum check de máquina.
- **Solução:** `.agent/scripts/check_local_rules.py <backup> <novo>` compara linha inteira (CUT / MISSING / junk), com base de texto genérico `project-initializer/legacy-generic-lines.txt` (linhas repetidas em 2+ backups) e `adaptadas.md` ao lado do backup para o que foi descartado de propósito; `--replace` leva o texto próprio para "A revisar"; `projects_audit.py` ganhou a coluna "Regras locais"; prompt 01 manda rodar o check. Modelo: como projeto novo do initializer (só regras locais completas; lixo antigo sai).
- Loop: `.agent/plans/execution-loops/2026_11_13/Regras Locais Preservadas na Atualização/`.

## 2026-11-14 — regras só em CLAUDE.md + AGENTS.md
- **Problema:** o kit gerava 5 a 7 cópias das regras (`GEMINI.md` na raiz, `.agent/rules/*`, `.cursorrules`) e elas divergiam (a raiz já estava um módulo à frente das cópias). O Antigravity lê `AGENTS.md` na raiz (docs oficiais: antigravity.google/docs/rules); `.agent/rules/` é caminho legado dele.
- **Solução:** padrão = `CLAUDE.md` (Claude Code) + `AGENTS.md` (Antigravity e outras IAs) idênticos na raiz. `sync_rules.py` só grava esses dois (+ `.cursorrules`/`.claude/CLAUDE.md` se já existirem, nunca cria) e nunca usa legado como fonte. `GEMINI.md` e `.agent/rules/` viram legado: `sync_rules.py --clean-legacy` lista, pergunta e só apaga o que é idêntico ao `CLAUDE.md`; o que diverge fica. `projects_audit.py` ganhou a coluna "Legado" (bloqueia "em dia"). Teste `test_rules_standard.py` impede a volta do texto antigo nos arquivos versionados.
- Projetos existentes migram pelo prompt `01-atualizar-projeto-existente.md`, um a um, com confirmação; nada foi apagado em lote.
- Loop: `.agent/plans/execution-loops/2026_11_14/Regras só CLAUDE e AGENTS/`.

## 2026-11-14 — skill `writing-agents` e cérebro de agente
- **Problema:** agente do kit era texto livre, sem modelo e sem memória. Sem a skill, um subagente inventou o desenho sozinho (memória numa pasta do projeto, skill separada só para a memória, sem campo de autonomia, campos de lição próprios).
- **Solução:** skill `writing-agents` (só agentes). Agente continua `.agent/agents/<nome>.md`; o cérebro é `.agent/agents/agents_brains/<nome>/` (`contextos.md`, `licoes.md`, `decisoes.md`, `referencias/`, `inbox/`). Campo `autonomy` (`propose` padrão, `contexts`) marca que o agente adotou o modelo; nenhum nível deixa o agente editar o próprio arquivo. Lição só com sinal ou instrução do dono, com contexto e alcance; 3 ocorrências → proposta de promover; ao hub só com ganho exponencial, pela inbox do hub, com aprovação. `sync_entrypoints.py --check` valida o cérebro dos agentes com `autonomy`; os ~130 agentes antigos não são checados. O `sync` e o catálogo só listam `*.md` do topo de `agents/`, então `agents_brains/` não vira agente.
- **Bug achado no teste:** `frontmatter()` de `sync_entrypoints.py` lia `\s*` depois de `chave:`, que come a quebra de linha: um campo vazio (`skills:`) engolia a linha seguinte (`autonomy: propose` virava nome de skill). Corrigido para `[ \t]*`, com teste.
- **Fechamento do QA (ciclo 7):** para eliminar desvios do construtor em `decisoes.md`, a skill adotou atomicidade estrita ("uma frase por item, um rótulo por item"), conjunto fechado de rótulos (`briefing`, `dono (parafraseado)`, `construtor`) e consistência de premissa em todas as seções. O teste verde final zerou os CONTRADICTED (10/10 na rubrica).
- Loop: `.agent/plans/execution-loops/2026_11_14/Skill de Construção de Agentes/`.

## 2026-11-14 — mapeamento de modelos e contenção de contexto de subagentes
- **Problema:** (1) Modelos leves do Antigravity (`flash_lite`) não existem no Claude Code (`haiku`), e arquivos reais em `.claude/agents/` geravam erro no sync. (2) Subagentes com retornos longos (logs, dumps de código) saturavam a janela de contexto do orquestrador.
- **Solução:** (1) `sync_entrypoints.py` converte automaticamente `flash_lite`/`flash` para `haiku` e `pro` para `sonnet` gerando arquivos em `.claude/agents/` com cabeçalho identificador `<!-- antigravity-kit:generated ... -->`; `inherit` continua symlink puro; `--check` valida paridade e integridade. (2) Protocolo de Retorno Limpo formalizado em `core.md`/`AGENTS.md` e `agent-template.md`: payloads pesados ficam no disco, e a resposta ao chat limita-se a status, 3-5 bullets executivos com links e perguntas bloqueantes.
- Loop: `.agent/plans/execution-loops/2026_11_14/Mapeamento de Modelos e Economia de Contexto/`.

## 2026-11-18 — checklist.py verde (UX Audit, lint, Test Runner)
- **Problema:** `checklist.py .` nunca fechava verde no kit: (1) o `ux_audit.py` lia o texto das skills embutido no `catalog.html` (12 MB) como interface (roxo, nav items, fontes, img sem alt) e achava "form sem label" em `.css` por causa da palavra `card`; (2) o `lint_runner.py` rodava `ruff check .` no projeto todo, e os 351 achados antigos reprovavam, apesar da decisão do dono "lint só nos arquivos tocados" existir só como texto; (3) o `test_runner.py` chamava `python` (inexistente no macOS) e exigia pytest, mas o kit usa unittest.
- **Solução:** (1) arquivo gerado com `ux-audit: skip` nos primeiros 1000 caracteres é ignorado (o `generate_catalog.py` emite o marcador) e a checagem de formulário não roda em `.css`; (2) `lint_runner.py` lint só os `.py` alterados ou novos desde HEAD (`--since REF`, `--all`; fora do git, tudo); (3) `test_runner.py` usa `sys.executable` e cai para `unittest discover` quando não há pytest. Testes: `test_ux_audit.py`, `test_lint_runner.py`, `test_test_runner.py`. Itens de inbox 028, 033 e 037.

## 2026-11-18 — Resolver do SIP fora de `.agent/skills/` e em dois níveis
- **Problema:** o resolver (`sip-geral`, `sip-marketing`) morava em `.agent/skills/` do próprio hub, onde só fazia ruído, e era um arquivo único de 450 a 570 linhas carregado inteiro em todo consumidor. Além disso, 6 projetos tinham `.agent/skills/sip-geral` apontando para a raiz do 0 Padrões (sem `SKILL.md`) e o `sips_status.py` dizia "em dia".
- **Solução:** resolver em `<hub>/prompts/resolver/sip-<dominio>/` (SKILL.md enxuto + `verticais.json` + `verticais/*.md` gerados por `build_sip_index.py`, modo `<!-- indice:start -->`). `linkutil.resolver_dir(hub, nome)` acha o resolver nos dois layouts (novo vence); `propagar_sip.py` agora usa caminho absoluto do hub (relativo gerava links quebrados) e `sips_status.link_problem` compara o alvo esperado. Os 6 outros SIPs (astro, firecrawl, imprensa, mautic, n8n, trends) seguem no layout antigo até o dono migrar. Testes: `tests/test_resolver_layout.py` (25).
- **Ao criar SIP novo:** nasce em `prompts/resolver/` (skill `superiaprojects-criar-sip`); item que não bate com nenhum `match` de `verticais.json` faz o gerador falhar.
- Loop: `0 Mkt/.agent/plans/execution-loops/2026_11_18/Resolver Fora das Skills/`.

## 2026-11-18 — UX Audit acerta sozinho (inbox 038)
- **Problema:** `ux_audit.py` aplicava regras de app web a e-mails e usava substring: "acreditando" virava formulário (`credit`), comentário CSS "Magenta" virava roxo; no Inngage eram 12 issues, todas falsas.
- **Solução:** `.agent/` pulado; e-mail (pasta ou markup) só roda `<img alt>` e roxo; formulário só com tag real ou palavra inteira em `type/name/autocomplete`; roxo só em valores de CSS; `.agent/checklist.json` aceita `ux_audit.exclude` e `ux_audit.brand_colors`. 22 testes em `test_ux_audit.py`. Decisão do Felipe: e-mail auditado com regras reduzidas, não pulado.

## 2026-11-18 — Check de memória do Mac (`auditing-memory-usage`, Fase 0)
- **Problema:** o Mac ficou lento (swap em 94%, load 178) por processos de extensões do Antigravity acumulados: `agy --hub` órfãos com 4 MCPs cada, hosts "Plugin" parados com ~4 GB. A skill disparava em "máquina lenta" mas só auditava código (baseline: o agente improvisou, sem mapear pais). Além disso, `ps command` **e `ps comm`** vazaram tokens no chat: `node`/`npm` reescrevem o título e o `comm` passa a trazer os argumentos.
- **Solução:** `.agent/scripts/check_memoria.py` (só leitura; `--limpar` com ok, `SIGTERM`, `SIGKILL` só com segundo ok) + Fase 0 no `SKILL.md` + `references/ambiente-macos.md`. Critérios: `agy` órfão = `ppid=1` e 0 clientes locais na `--hub-port`; host parado = sem nenhum descendente vivo (zumbi e sub-helper não contam) e idade ≥ 20 min; cadeia de pais da sessão sempre protegida; nome do processo cortado antes do primeiro argumento e saída passa por `redact()`. Testes: `tests/test_check_memoria.py` (25, com `FakeSystem`, nenhum processo real). Validado ao vivo: 1 host parado encerrado, swap 5,9 → 4,1 GB.
- **Evidência registrada (SIGTERM no `agy` 38449, 1h54, 11 filhos MCP):** depois do sinal, 0 dos 11 MCPs seguiam vivos e o swap foi de 654 MB para 434 MB. Foi uma observação, não uma garantia do `agy`; o script só sinaliza os alvos listados.
- **Regra para quem for olhar processo à mão:** nunca `ps ... command` nem `comm`; use o script.
- Loop: `.agent/plans/execution-loops/2026_11_18/Protocolo Check de Memoria/`.

## 2026-11-19 — Skill citada e não instalada: o agente desistia (inbox 043)
- **Problema:** em TAAb, Base Sites - Astro e IL - App o pedido de handoff falhou: o `CLAUDE.md` manda usar `session-handoff`, que não está em `.claude/skills/` (só o ponteiro `sip-geral` está, de propósito). O agente procurou direto, não achou e parou, embora o §11 já mandasse resolver pelo `sip-geral`. A regra ficava no fim do arquivo e nada levava o agente até ela.
- **Solução:** regra geral no §2 do `core.md` (ordem: `.agent/` do projeto, SIPs instalados, kit; só dizer "não existe" depois de mostrar onde procurou), gatilho na `description` do `sip-geral` e teste `test_rules_skill_refs.py` (toda skill citada nos módulos existe no hub). Junto entrou a seção "Change discipline" (cinco regras de um vídeo: parar e avisar, suíte inteira, escopo mínimo, padrão e dependência, config e produção) com os checks `scope_check.py` e `env_diff_check.py` no `checklist.py` e no hook.
- **Também achado:** `CLAUDE.example.md` e `ClaudeExample.md` (o que o `install.sh` copia) estavam defasados dos módulos; `test_example_templates.py` agora os compara com a montagem por módulos.
- **Liberação dos checks:** `ALLOW_ENV_DIFF=1` / `ALLOW_SCOPE_DIFF=1` por commit, só depois do dono dizer no chat; o motivo vai no plano.
- Loop: `.agent/plans/execution-loops/2026_11_19/Busca no SIP e Disciplina de Mudança/`. Falta propagar: `avisar_projetos_inbox.py --apply` e remontagem de cada projeto.

## 2026-11-19 — Notas do kit no inbox dos projetos: `GERAL-NNN-` e pasta de prompts
- **Decisão do dono:** nota que o kit (ou outro projeto) deixa no inbox de um projeto se chama `GERAL-NNN-assunto.md` (sequência `GERAL-` própria, conta `arquivo/`); prompt para continuar em outra sessão ou outro momento, e prompts temporários, vão em `.agent/plans/prompts/NNN-Título.md`. Está no `core.md`, no mapa de destinos e na skill `mapa-de-destinos`.
- **Só vale para as próximas:** as 57 notas `NNN-regras-do-kit-...` já gravadas em 2026-11-19 não são renomeadas nem regravadas. `avisar_projetos_inbox.py` e `propagar_sip.py` reescrevem uma nota antiga do mesmo assunto no lugar, sem criar duplicada.
- **Suposições não contestadas:** `plans` (o dono escreveu `plan`), kebab no inbox, título legível nos prompts.

## 2026-11-19 — `scope_check.py` não reconhecia caminhos com ponto (inbox 044)
- **Problema:** `glob.lstrip("./")` tira todo ponto e barra do começo, então `.agent/...`, `.githooks/...` e `.env.example` viravam `agent/...` e eram barrados como "fora do escopo". Meus testes não tinham nenhum glob começando com ponto; quem achou foi o Base Sites - Astro.
- **Solução:** `norm_glob` tira só o prefixo `./`; testes com `.agent/`, `.github/`, `.env.example` e `./.agent/x.md`. Conferido em outro projeto sorteado (`waimonitor`).
- **Regra:** teste de caminho/glob sempre inclui um caso que começa com ponto.
