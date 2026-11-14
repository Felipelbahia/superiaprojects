Alinhar projeto existente com o kit (primeira vez ou atualização)

Quero alinhar este projeto, que JÁ EXISTE, ao estado atual do kit em "<SUPER_IA_PROJECTS_PATH>". Serve tanto para a primeira adoção quanto para atualizar um projeto que já foi alinhado antes. Mude só o que falta ou ficou defasado.

REGRAS (valem para todos os passos):
- NUNCA apague nem sobrescreva as regras locais do projeto (comandos de build/teste, variáveis de ambiente, convenções, exceções): elas são PRESERVADAS num bloco próprio.
- Ação destrutiva (apagar, mover, substituir arquivo ou pasta) só com a minha confirmação, caso a caso.
- Do `.env` leia só os NOMES das variáveis (ex.: `cut -d= -f1`), nunca os valores.
- NUNCA afirme que algo "existe", "está correto" ou "foi preservado" sem verificar por comando (find/grep/diff/comm/test -L) ou leitura direta. O que não foi verificado vira "não verificado".
- Sem commit, sem push, sem eu pedir.

1. Leitura e inventário (nada é alterado neste passo):
   - PRIMEIRO: `for d in .agent .agent/rules .agent/plans .agent/skills; do test -L "$d" && echo "$d -> $(readlink "$d")"; done`. Se `.agent` (ou uma dessas subpastas) for um link para o `.agent` do kit (`<SUPER_IA_PROJECTS_PATH>/.agent`), PARE e me pergunte: este prompt gravaria regras, planos, skills e o catálogo dentro do kit. Só continue depois que eu decidir (ex.: trocar o link por uma pasta `.agent/` própria).
   - Leia os arquivos de regra existentes (`./CLAUDE.md`, `./.claude/CLAUDE.md`, `./AGENTS.md`, `./.cursorrules`, `STANDARDS.md`, e o legado `./GEMINI.md` e `.agent/rules/*`, só para não perder regra local), se existirem.
   - Liste, arquivo por arquivo, as regras ESPECÍFICAS deste projeto, citando o texto (não resuma de memória): comandos, variáveis de ambiente, convenções, exceções, pastas. Separe do que é texto genérico do kit antigo (seções como "Fallback Resolution Protocol", "Latest Docs First", "Socratic Gate", "Firecrawl: MCP vs Execução Local"), que será substituído pelos módulos.
   - Abra a ficha do projeto em "<SUPER_IA_PROJECTS_PATH>/projetos/" (ache pela linha "Repositório / Caminho") e leia a linha "Última sincronização com o kit: DATA (kit @ HASH)". Se existir, rode `git -C "<SUPER_IA_PROJECTS_PATH>" log --oneline HASH..HEAD -- CLAUDE.md .agent` e diga, em português simples, o que mudou no kit que afeta este projeto. Se o HASH não existir mais no kit, diga "não verificado" e compare por conteúdo (`diff` das regras). Se a ficha não tiver essa linha, trate como primeira adoção.
   - Rode `python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/projects_audit.py" --no-write` e leia a linha deste projeto.

2. Perfil do projeto (bloco `## Project`):
   - Se o `CLAUDE.md` já tem o bloco `## Project` (Produces / Modules / Primary agent / SIPs), use-o e confirme comigo em uma linha.
   - Se não tem, faça as perguntas guiadas do prompt de criação (`<SUPER_IA_PROJECTS_PATH>/projetos/prompts/02-criar-projeto-do-zero.md`, passo 1, itens b, c, f, g), APENAS 1 por vez, dizendo em 1 linha o que cada resposta define. Mostre os SIPs em tabela com ⭐ nos sugeridos; o `sip-geral` entra sempre.
   - Mostre o resumo (módulos `core` + `sip-access` + escolhidos, agente primário, SIPs) e só siga depois do meu "ok".

3. Montagem das regras (nunca recortar à mão):
   - Backup antes de tudo: copie TODOS os arquivos de regra lidos no passo 1 para `.agent/plans/rules-backup-AAAA-MM-DD/`, na mesma estrutura (o `sync_rules.py` vai sobrescrever `AGENTS.md` e, se existirem, `.cursorrules` e `.claude/CLAUDE.md`; o legado `GEMINI.md` e `.agent/rules/*` ele não toca).
   - Legado: no fim do passo, rode `python3 .agent/scripts/sync_rules.py --clean-legacy` (ou o caminho do kit). Ele lista `GEMINI.md` e `.agent/rules/*`, pergunta, e só apaga o que é idêntico ao `CLAUDE.md`; o que diverge fica e você me mostra para decidirmos.
   - Monte:
     ```
     python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/assemble_rules.py" --modules core,sip-access,<escolhidos> --title "<Nome do Projeto>" --out "<project_root>/CLAUDE.md"
     ```
     - `CLAUDE.md` já montado pelos módulos (tem "Before acting (mandatory sequence)"): o script mantém `## Project`, `## Stack` e `## Local rules` no fim (só reescreve a linha `- Modules:` com os módulos usados, na ordem fixa do kit; se a linha faltar, ela não é criada) e move para `## Local rules`, avisando, toda seção cujo título não é de módulo do kit. As seções do kit e o texto antes da primeira seção são regenerados, e as seções de um módulo que saiu da montagem são removidas: edição local feita ali não é mantida, e o script avisa quais mudaram ("regenerated") e quais saíram ("removed"). Se o arquivo tiver uma cerca de código (```` ``` ```` ou `~~~`) aberta e nunca fechada, o script recusa (código 4), cita a linha e não grava nada: feche a cerca e rode de novo. Confira no `diff` com o backup, leve para `## Local rules` o que for regra do projeto e complete os blocos que faltarem, como abaixo.
     - `CLAUDE.md` no modelo antigo: o script recusa (código 3) para não apagar as regras antigas. Só depois do backup acima, rode o mesmo comando com `--replace`. As regras do arquivo antigo não passam sozinhas: elas entram no `## Local rules` abaixo.
   - Acrescente ao fim do `CLAUDE.md` os blocos que ainda não estiverem lá, nesta ordem: o bloco `## Project` preenchido; com módulo `code`, o bloco `## Stack` (leia o lockfile/manifest e consulte o Context7 pela versão INSTALADA; sem números de versão congelados; se o projeto já tinha uma seção própria de stack com versões, preserve-a dentro do bloco de regras locais); e o bloco `## Local rules` com TODAS as regras específicas listadas no passo 1, com o texto original.
   - Mostre o `diff` entre o `CLAUDE.md` do backup e o novo e confirme, item por item da lista do passo 1, que cada regra local está no bloco `## Local rules` (grep de um trecho literal de cada uma).

4. Cópias para as outras IAs e duplicação:
   - Se existir `.claude/CLAUDE.md`: compare com o `CLAUDE.md` do backup (`cmp`). Igual → proponha apagar (o Claude Code carrega ele e o `./CLAUDE.md` juntos, regras em dobro) e só apague com o meu "ok". Diferente → mostre o `diff` e pergunte.
   - Gere as cópias: `cd "<project_root>" && python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/sync_rules.py"`; depois rode o mesmo com `--check` e só prossiga com "Parity OK".

5. SIPs:
   - Instale o `sip-geral` seguindo `<SUPER_IA_PROJECTS_PATH>/prompts/instalar-skill-sip-geral.md` e cada SIP escolhido (prompt na tabela de `<SUPER_IA_PROJECTS_PATH>/projetos/_sips.md`). Agents/workflows de cada SIP: se o prompt perguntar, responda "nenhum"; se instalar todos sem perguntar (modelo anterior), execute só o passo do resolver. Eles ficam no SIP salvo pedido meu.
   - Menções antigas a "Fallback" ou a caminhos do 0 Mkt/0 Padrões nas regras locais: proponha trocar pelo SIP correspondente, sem aplicar sem o meu "ok".

6. Skills, agents e workflows locais:
   - Busque skills em `.agent/skills/`, `.agents/skills/`, `.claude/skills/`, `skills/`. Cada skill local fica em `.agent/skills/<nome>/SKILL.md` com frontmatter (name + description no mínimo).
   - Mais de uma pasta com conteúdo próprio: compare com `diff -rq` e NUNCA apague por conta própria; proponha a ação.
   - Skill local que é cópia de uma skill do kit ou de um SIP que mudou: aponte as diferenças com `diff -rq` e me pergunte antes de atualizar.
   - Para cada `.agent/skills/<nome>`: `test -L ".claude/skills/<nome>" && echo "OK: symlink" || (test -e ".claude/skills/<nome>" && echo "ATENÇÃO: pasta real, comparar com diff -rq" || echo "FALTANDO: criar symlink")`. Faltando → `ln -s "../../.agent/skills/<nome>" ".claude/skills/<nome>"`. Pasta real → `diff -rq` e pare esperando a minha decisão.
   - Rode `cd "<project_root>" && python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/sync_entrypoints.py"` (symlinks de agents/workflows) e depois `--check`; erros de validação (agent sem `name`/`description`, `skills:` inexistente) vão para o resumo; entrada real (não symlink) em `.claude/agents/` ou `.claude/commands/` → `diff`, proponha e pare. Depois `python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/generate_catalog.py"` e garanta `.agent/catalog.html` no `.gitignore`.

7. Mapa de destinos:
   - Se não existir `docs/mapa-de-destinos.md`, siga a skill `mapa-de-destinos` (via `sip-geral`), caso "projeto existente sem mapa": documente o que já existe, aponte inconsistências e pergunte. NÃO mova nada.
   - Se existir, confira que as pastas citadas existem e liste divergências (sem mover).

8. Ambiente e `.gitignore`:
   - `.env.example` completo: `comm -23 <(grep -oE "^[A-Za-z_][A-Za-z0-9_]*=" .env | sort -u) <(grep -oE "^[A-Za-z_][A-Za-z0-9_]*=" .env.example | sort -u)`; o que sobrar entra no `.env.example` (só o nome) ou é justificado como não usado em código.
   - `.gitignore`: `.env*` (com exceção `!.env.example`), `.agent/plans/` e `plans/` ignorados; `_projectdefines/`, `memory.md`, `STANDARDS.md`, `.env.example`, `docs/` e os arquivos de regra (`CLAUDE.md`, `AGENTS.md`) NUNCA ignorados.
   - Testes (com módulo `code`): rode a suíte inteira e cole a saída. Teste que já falha: registre nome e causa no resumo; NÃO apague, pule nem afrouxe (decisão minha). Sem `.githooks/pre-commit`: proponha o hook com a parte rápida da suíte (passo "Hook de commit" de `<SUPER_IA_PROJECTS_PATH>/.agent/skills/project-initializer/SKILL.md`) e só instale com o meu "ok"; se houver teste que já falha na parte rápida, diga que o hook recusaria todo commit e pergunte antes.
   - `memory.md` na raiz: se faltar, crie (memória de longo prazo, formato `Problema → Solução`, versionado).
   - Planos e handoffs ficam em `.agent/plans/execution-loops/` e `.agent/plans/handoffs/`. Se o projeto já tem `execution-loops/` ou `handoffs/` na raiz, NÃO mova (legado até eu pedir).

9. Ficha central:
   - Crie/atualize "<SUPER_IA_PROJECTS_PATH>/projetos/<nome-do-projeto>.md" (modelo `<SUPER_IA_PROJECTS_PATH>/projetos/TEMPLATE.md`) e a linha em "<SUPER_IA_PROJECTS_PATH>/projetos/README.md": tipo (`Produces`), módulos, SIPs, stack real, objetivo, skills locais, integrações do `.env.example`. Só afirmações verificadas.
   - Por último, grave no cabeçalho: `> **Última sincronização com o kit:** AAAA-MM-DD (kit @ HASH)` com a data de hoje e `git -C "<SUPER_IA_PROJECTS_PATH>" rev-parse --short HEAD`, só depois dos passos 3 a 8 verificados.

10. Verificação final (cole a saída de cada comando):
   - [ ] `sync_rules.py --check` → "Parity OK"
   - [ ] Cada regra local do passo 1 encontrada no bloco `## Local rules` (grep)
   - [ ] Nenhum `.claude/CLAUDE.md` ao lado do `./CLAUDE.md` (ou a minha decisão registrada)
   - [ ] Toda skill local tem `.claude/skills/<nome>` como symlink (`test -L`)
   - [ ] `sync_entrypoints.py --check` OK
   - [ ] Toda skill/agent/script e todo arquivo (`CODEBASE.md`, `ARCHITECTURE.md`…) citado nas regras existe no projeto ou no hub (comando, não suposição)
   - [ ] `comm` do passo 8 vazio (ou só variáveis justificadas)
   - [ ] `docs/mapa-de-destinos.md` existe (ou a minha decisão registrada)
   - [ ] Com módulo `code`: saída da suíte inteira colada; testes que já falhavam listados (nenhum apagado, pulado ou afrouxado); hook instalado ou a minha decisão registrada
   - [ ] `git status` só com os arquivos esperados

Pare e me apresente, em português simples, SÓ o que mudou: módulos e SIPs aplicados, o que o kit trouxe de novo, as regras locais preservadas (com onde ficaram), skills que entraram ou saíram, pendências que dependem de mim e o que ficou "não verificado".
