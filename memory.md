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
