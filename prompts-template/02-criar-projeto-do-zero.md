Criar um projeto do Zero

Quero criar um projeto novo (software, conteúdo e marketing, automação ou uma mistura) com base na skill project-initializer em <SUPER_IA_PROJECTS_PATH>/.agent/skills/project-initializer/SKILL.md.

Siga rigorosamente o protocolo de 6 fases para compatibilidade Multi-IA.

REGRA GERAL (vale para todos os passos abaixo): NUNCA afirme no resumo final que algo "existe", "está correto" ou "foi configurado" sem ter verificado de fato com um comando ou leitura direta. Se você não verificou, diga "não verificado" em vez de assumir.

1. Descoberta guiada (Socratic Gate):
   - Faça APENAS 1 pergunta por vez. Depois de cada resposta, diga em 1 linha o que ela define (módulo de regras, SIP ou agente) e por quê.
     a) Nome e objetivo em uma frase.
     b) "O que este projeto produz? (1) software: app, site, API, script; (2) conteúdo: e-mails, posts, artigos, roteiros, releases; (3) automação ou dados: workflows n8n, raspagem, pipelines, previsões; (4) uma mistura (diga quais)." → software = módulo `code`; conteúdo = módulo `content`; automação/dados = módulo `automation` (+ `code` se houver código próprio: scripts, pipelines, Code nodes); mistura = todos os citados.
     c) Só se produz software: "Tem interface? web, mobile, site Astro ou nenhuma (backend/CLI)?" → web, mobile ou Astro = módulo `interface` (a tabela do módulo define o agente primário).
     d) Só se produz software: stack desejada ("não sei, recomende" → recomende pela skill `app-builder`, depois de consultar o Context7).
     e) Público-alvo e escopo da primeira versão.
     f) SIPs: leia a tabela de `<SUPER_IA_PROJECTS_PATH>/projetos/_sips.md` e mostre TODOS os SIPs (domínio, nome e para que serve: a `description` do resolver em `<SUPER_IA_PROJECTS_PATH>/.agent/skills/sip-<dominio>/SKILL.md`), em tabela, marcando ⭐ os que você sugere pelas respostas b e c, com o motivo em uma linha. O `sip-geral` entra sempre (não é pergunta). Pergunte: "Quais instalar além do sip-geral? (sugeridos / nenhum / lista)". Sem resposta = só o `sip-geral`.
     g) Agente primário: sem módulo `interface`, proponha um agente de `<SUPER_IA_PROJECTS_PATH>/.agent/agents/` (ex.: `content-marketer` para conteúdo, `backend-specialist` para API) e confirme.
   - Aprovação: mostre o resumo (módulos `core` + `sip-access` + escolhidos, agente primário, stack se houver, SIPs) e só siga depois do "ok" do dono.

2. Regras Multi-IA (montadas por módulos, nunca recortadas à mão):
   - Na raiz do projeto, monte o `CLAUDE.md` com os módulos aprovados (sempre `core` e `sip-access`):
     ```
     python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/assemble_rules.py" --modules core,sip-access,<escolhidos> --title "<Nome do Projeto>" --out "<project_root>/CLAUDE.md"
     ```
     Não edite o arquivo para cortar seções: módulo que não se aplica simplesmente não entra no `--modules`. Depois acrescente ao fim do `CLAUDE.md` o bloco `## Project` preenchido (formato no próprio arquivo) (o bloco `## Stack`, com módulo `code`, é escrito só no passo 4, depois do Context7).
   - A cópia para as outras IAs (`./AGENTS.md`) sai do `sync_rules.py`, rodado de dentro do projeto (`cd "<project_root>"`), no fim deste passo. **Não crie `.claude/CLAUDE.md`**: o Claude Code carrega ele e o `./CLAUDE.md` juntos, e as regras ficam em dobro.
   - Prove que as regras montadas trazem a busca no SIP e a disciplina de mudança: `grep -n -F -e "Named in these rules but not in" -e "Change discipline" "<project_root>/CLAUDE.md"` (cole a saída; sem saída = remonte, não edite à mão).
   - Instale o `sip-geral` seguindo `<SUPER_IA_PROJECTS_PATH>/prompts/instalar-skill-sip-geral.md`; depois, o prompt de instalação de cada SIP escolhido (coluna "Prompt de Instalação" de `_sips.md`). Agents/workflows de cada SIP: responda "nenhum" se o prompt perguntar; se ele instalar todos sem perguntar, execute só o passo do resolver e pule os de agents/workflows. Eles ficam no hub e só vêm para o projeto se o dono pedir.
   - **Descoberta de skills pelo Claude Code:** se o projeto já nascer com alguma skill local em `.agent/skills/<nome>/` (copiada de Super IA Projects ou criada do zero), crie também `.claude/skills/<nome>` como symlink (`ln -s "../../.agent/skills/<nome>" ".claude/skills/<nome>"`) — sem isso a skill existe mas o Claude Code nunca a lista (ele só varre `.claude/skills/` e `~/.claude/skills/`, nunca `.agent/skills/`). Vale para qualquer skill local criada depois também, não só nesta etapa inicial. Confira com `test -L` que `.claude/skills/sip-geral` existe (instalado neste passo).
   - **Agents e workflows locais:** se o projeto nascer com `.agent/agents/` ou `.agent/workflows/`, rode da raiz `python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/sync_entrypoints.py"` (cria os symlinks `.claude/agents/`, `.claude/commands/`, `.cursor/commands/` e valida). Agent = persona (`name`+`description`); workflow = comando `/nome` (`description`).
   - Crie o arquivo STANDARDS.md na raiz baseado no template .../STANDARDS_TEMPLATE.md (se existir), preenchido com convenções REAIS do projeto (com `code`: da stack, nomenclatura de arquivos, como adicionar um novo módulo/integração; com `content`: nomes de arquivos por data e canal, pastas, voz em `brand/`; com `automation`: workflows e dados) — não deixe placeholders genéricos tipo "{detalhes}".
   - **Mapa de destinos:** siga a skill `mapa-de-destinos` (via `sip-geral`): conversa de criação a partir do `Produces` do bloco `## Project`, uma pergunta por vez, e crie `docs/mapa-de-destinos.md` (onde cada tipo de entrega que não é código será gravado). Código fica fora do mapa. Com `content` (ou qualquer entrega que não é código), crie só as pastas que o mapa lista, pela seção "Árvore padrão" do preset da skill (`.agent/skills/mapa-de-destinos/references/preset-*.md`, ex.: `preset-marketing.md`); nenhuma pasta fora do mapa, sem números nos nomes (exceto a esteira de aprovação).
   - Crie o arquivo `memory.md` na raiz do projeto (memória de longo prazo do projeto, lazy-loaded sob demanda, formato direto `Problema → Solução`, sem jargão) para registrar bugs resolvidos e decisões arquiteturais. O `memory.md` DEVE ser versionado no git.
   - Ao terminar, rode:
     ```
     cd "<project_root>" && python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/sync_rules.py"
     ```
     Depois rode o mesmo script com `--check` e só prossiga para o passo 3 se a saída disser "Parity OK".

3. Registro na Central de Projetos:
   - Crie a ficha técnica em <SUPER_IA_PROJECTS_PATH>/projetos/<nome-do-projeto>.md usando o template .../projetos/TEMPLATE.md.
   - Adicione o projeto na tabela do dashboard central em .../projetos/README.md.

4. Scaffolding, Ambiente (.env) & Configuração do .gitignore:
   - Só com módulo `code` (este item e o scaffolding a seguir; sem `code`, pule-os): ANTES de gerar qualquer arquivo, consulte o Context7 para cada tecnologia da stack (versão estável atual, requisitos, comando oficial de criação) — regra "Docs first (Context7 MCP)" do CLAUDE.md. Depois do scaffolding, escreva o bloco `## Stack` no arquivo de regras (só nomes, sem versões congeladas) e rode de novo `cd "<project_root>" && python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/sync_rules.py"`.
   - Execute o scaffolding inicial da stack via a skill app-builder do Super IA Projects, aplicando Clean Code.
   - Crie `.env` e `.env.example` juntos, com as MESMAS chaves (só nomes — nunca valores reais em `.env.example`). Registre em `STANDARDS.md` a regra: "toda nova variável de ambiente deve ser adicionada em .env E .env.example na mesma mudança" — isso evita que os dois arquivos divirjam com o tempo (problema real já encontrado num projeto desta base: 13 variáveis usadas em código nunca documentadas).
   - Crie o `.gitignore` separando rigorosamente o que fica local do que sobe para o GitHub:
     - **DEVE SER IGNORADO (incluir obrigatoriamente no `.gitignore`):** `.env`, `.env.local`, `.env.*.local`, `.agent/plans/`, `plans/`, `node_modules/`, `dist/`, `build/`, `.next/`, `out/`, `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `.DS_Store`, `assets/**/*.mp4`, `assets/**/*.mov` (conteúdo com vídeo), `certs/`, `*.crt`, `*.key`, `*.pem`, `*.p12`, `*service-account*.json`, `credentials*.json`, configs MCP com API key embutida (`.mcp.json`, `opencode.json`, `.cursor/mcp.json`, `.vscode/mcp.json`, `.gemini/settings.json`, `.codex/config.toml`, `.zed/settings.json`, `config/mcporter.json`), `.firecrawl/` e qualquer pasta temporária/saída (`output/`, `.temp_ag_kit/`).
     - **DEVE SER VERSIONADO (NUNCA colocar no `.gitignore`):** toda a pasta `_projectdefines/` (quando utilizada, todos os contratos aprovados e `IMPLEMENTATION-PLAN.md` TEM que subir para o GitHub), `memory.md`, `STANDARDS.md`, `.env.example`, as pastas do mapa de destinos e todos os arquivos de regra Multi-IA (`CLAUDE.md`, `AGENTS.md`).

5. Definição da Aplicação (`project-defines`) & Plano Inicial Local:
   - Pergunte UMA vez (padrão: Não) se o dono quer construir uma aplicação agora com a skill `project-defines` (documentos aprovados passo a passo em `_projectdefines/`). Se "Não", nada é criado em `_projectdefines/` e você gera o plano inicial local em `.agent/plans/{Nome do Projeto} [PLAN].md` (que fica local, ignorado pelo `.gitignore`); se "Sim", o plano do projeto passa a ser `_projectdefines/IMPLEMENTATION-PLAN.md` (que sobe para o GitHub).

6. Criação do Repositório no GitHub, Primeiro Commit & Push (`github-publisher`):
   - Siga rigorosamente a skill `<SUPER_IA_PROJECTS_PATH>/.agent/skills/github-publisher/SKILL.md`:
     a) **Pré-voo e Fronteira do Repositório:**
        - Verifique `gh auth status` (se não autenticado, instrua o usuário a rodar `! gh auth login`).
        - Rode `git rev-parse --show-toplevel 2>/dev/null` para checar se a pasta está dentro de um repositório-pai. Se retornar um diretório-pai, inicialize um repositório próprio na raiz deste projeto (`git init -b main`) e adicione esta pasta ao `.gitignore` do pai (ou pergunte ao usuário conforme `github-publisher` — NUNCA publique o repositório-pai por engano com `gh repo create --source=.`).
     b) **Varredura Obrigatória de Segredos e Arquivos Grandes (antes de qualquer `git add`):**
        - Rode o scanner do kit:
          ```bash
          python3 "<SUPER_IA_PROJECTS_PATH>/.agent/skills/vulnerability-scanner/scripts/security_scan.py" .
          ```
        - Rode também a busca por chaves literais no código e arquivos >50MB:
          ```bash
          grep -rIlE --exclude-dir={node_modules,.git,.venv,venv,dist,build} -- 'sk_live_[0-9A-Za-z]{10,}|sk-(proj-)?[0-9A-Za-z_-]{20,}|AKIA[0-9A-Z]{16}|gh[pousr]_[0-9A-Za-z]{30,}|xox[abpr]-[0-9A-zA-Z-]{10,}|AIza[0-9A-Za-z_-]{35}|-----BEGIN [A-Z ]*PRIVATE KEY-----' .
          find . -path ./node_modules -prune -o -path ./.git -prune -o -type f -size +50M -print
          ```
        - Se apontar algo "critical"/"high" ou chave literal em código, leia o arquivo e confirme manualmente ANTES de prosseguir. Nunca comite segredo real.
     c) **Staging Verificado & Primeiro Commit:**
        - Inicialize na branch `main` e faça o stage:
          ```bash
          git init -b main
          git add -A
          git diff --cached --name-only
          ```
        - Confira a saída de `git diff --cached --name-only`: garanta que **NÃO** entraram `.env`, `.env.local`, `.agent/plans/`, `plans/`, `node_modules/`, `dist/` nem chaves privadas, e que **ESTÃO** presentes `CLAUDE.md`, `AGENTS.md`, `STANDARDS.md`, `memory.md`, `.env.example`, `.gitignore` (e `_projectdefines/`, se criado).
        - Faça o primeiro commit:
          ```bash
          git commit -m "feat: initial commit"
          ```
     d) **Criação do Repositório no GitHub & Push:**
        - Crie o repositório no GitHub (privado por padrão) e faça o push inicial:
          ```bash
          gh repo create "<repo-slug>" --private --source=. --remote=origin --push --description "<descrição curta do projeto>"
          ```
        - Verifique o resultado no remoto:
          ```bash
          gh repo view --json url,visibility,defaultBranchRef
          git ls-tree -r --name-only origin/main | grep -E '(^|/)(\.env|\.agent/plans|plans/.*|.*service-account.*\.json|.*\.pem|.*\.key)$'
          ```
          *(O grep acima deve retornar vazio).*
        - Atualize a ficha técnica em `<SUPER_IA_PROJECTS_PATH>/projetos/<nome-do-projeto>.md` preenchendo `> **Repositório GitHub:** <URL>`.
   - Exiba o resumo final com: confirmação de que `sync_rules.py --check` retornou "Parity OK", módulos de regras e SIPs aprovados e instalados (com a saída do `assemble_rules.py`), confirmação de que toda skill local em `.agent/skills/<nome>/` tem `.claude/skills/<nome>` como symlink de verdade (verificado com `test -L`, não suposição) e que o `sip-geral` está instalado (`test -L .claude/skills/sip-geral`) e que `docs/mapa-de-destinos.md` foi criado, confirmação da criação do `memory.md`, status do Git e URL do repositório GitHub publicado (o que subiu — incluindo `_projectdefines/` e `memory.md` — e o que foi excluído via `.gitignore` como `.env` e `.agent/plans/`), e links para a ficha técnica e os arquivos de regra gerados.
