Criar um projeto de Marketing, Conteúdo e Mídia do Zero

Quero criar um novo projeto de marketing, conteúdo e mídia com base no Super IA Projects e no hub 0 Mkt (<MARKETING_HUB_PATH>).

Siga rigorosamente este protocolo enxuto para projetos de Marketing / Conteúdo (sem perguntas irrelevantes de banco de dados, APIs de backend ou frameworks mobile).

REGRA GERAL (vale para todos os passos abaixo): NUNCA afirme no resumo final que algo "existe", "está correto" ou "foi configurado" sem ter verificado de fato com um comando ou leitura direta. Se você não verificou, diga "não verificado" em vez de assumir.

1. Descoberta Interativa (Socratic Gate):
   - Faça APENAS 1 pergunta por vez ao usuário, aguardando a resposta antes de enviar a próxima:
     a) Pergunta 1 (Nome & Marca): "Qual o nome exato do novo projeto e a qual marca/empresa ele pertence?"
     b) Pergunta 2 (Canais, Formatos & Frequência): "Quais são os canais prioritários (ex: Instagram, TikTok/Reels, LinkedIn, YouTube, Blog, Newsletter, WhatsApp) e formatos principais (vídeos curtos, carrosséis, artigos, podcasts)?"
     c) Pergunta 3 (Objetivo de Negócio & Esteira): "Qual o objetivo principal do conteúdo (ex: aquisição, autoridade, viralização, captação de leads) e qual a esteira de produtos/serviços que ele apoia ou vende?"
   - Se o projeto for discutir estratégias, scripts ou automações de mídia sem interface gráfica, isso define o escopo sem perguntas de backend ou Supabase.

2. Regras Multi-IA (montadas por módulos, nunca recortadas à mão):
   - Na raiz do projeto, monte o `CLAUDE.md` com os módulos de conteúdo (acrescente `automation` se o projeto raspar dados ou usar n8n, e `code` se tiver scripts próprios):
     ```bash
     python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/assemble_rules.py" --modules core,sip-access,content --title "<Nome do Projeto>" --out "<project_root>/CLAUDE.md"
     ```
     O módulo `content` já cobre voz, fontes, anti-slop (`geral-anti-slop`), aprovação antes de enviar e os SIPs de marketing, imprensa e Mautic; o `core` já cobre `_projectdefines/`, `memory.md`, segurança e handoff; o `automation`, a regra do Firecrawl.
   - Acrescente ao fim do `CLAUDE.md` só o que é deste projeto de marketing: o bloco `## Project` preenchido (formato no próprio arquivo, `Primary agent: content-marketer` salvo outra escolha do dono), as pastas de produção (`conteudos/`, `brand/`, `inteligencia/`, etc.), e, se houver scripts (ex.: `yt-dlp`, `ffmpeg`, `google-genai`), o bloco `## Stack` com consulta ao Context7 antes de adotar cada um.
   - As cópias para as outras IAs (`./GEMINI.md`, `./AGENTS.md`, `./.cursorrules`, `.agent/rules/GEMINI.md`, `.agent/rules/CLAUDE.md`, `.agent/rules/AGENTS.md`) saem do `sync_rules.py`, rodado de dentro do projeto (`cd "<project_root>"`), no fim deste passo. **Não crie `.claude/CLAUDE.md`**: o Claude Code carrega ele e o `./CLAUDE.md` juntos, e as regras ficam em dobro.
   - Instale o `sip-geral` (`<SUPER_IA_PROJECTS_PATH>/prompts/instalar-skill-sip-geral.md`) e o `sip-marketing` (prompt de instalação em `<SUPER_IA_PROJECTS_PATH>/projetos/_sips.md`), que dá acesso ao 0 Mkt: vídeo (Remotion, ElevenLabs), Sexy Canvas, Growth Lab, Copywriting, `hook-mining`, `reel-analyzer`. Mostre os outros SIPs da tabela e sugira com ⭐ os que fizerem sentido (ex.: `sip-imprensa`, `sip-mautic`). Agents/workflows de cada SIP: se o prompt perguntar, responda "nenhum"; se ele instalar todos sem perguntar (modelo anterior, inbox SIP-020 do kit), execute só o passo do resolver e pule os passos de agents/workflows. Eles ficam no SIP e só vêm para o projeto se o dono pedir.
   - **Descoberta de skills pelo Claude Code:** se o projeto nascer com ou criar alguma skill local em `.agent/skills/<nome>/`, crie também `.claude/skills/<nome>` como symlink relativo (`ln -s "../../.agent/skills/<nome>" ".claude/skills/<nome>"`). O Claude Code só varre `.claude/skills/` e `~/.claude/skills/`. Valide com `test -L`. Confira com `test -L` que `.claude/skills/sip-geral` existe (instalado neste passo).
   - **Agents e workflows locais:** se o projeto nascer com `.agent/agents/` ou `.agent/workflows/`, rode da raiz do projeto:
     ```bash
     python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/sync_entrypoints.py"
     ```
     (cria symlinks `.claude/agents/`, `.claude/commands/`, `.cursor/commands/` e valida metadados `name` e `description`).
   - Crie o arquivo `STANDARDS.md` na raiz baseado no `STANDARDS_TEMPLATE.md` (se existir), adaptado para convenções reais de marketing (padrão de nomenclatura de arquivos por data e canal, convenção de tags, metadados e rotina de produção).
   - **Mapa de destinos:** siga a skill `mapa-de-destinos` (via `sip-geral`): conversa de criação a partir do `Produces` do bloco `## Project`, uma pergunta por vez, e crie `docs/mapa-de-destinos.md` (onde cada tipo de entrega que não é código será gravado). Código fica fora do mapa.
   - Ao terminar a edição das regras, rode:
     ```bash
     cd "<project_root>" && python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/sync_rules.py"
     ```
     Depois rode o mesmo script com `--check` e só prossiga para o próximo passo se a saída disser "Parity OK".

3. Catálogo Geral Unificado Multi-Base (MD + HTML Interativo):
   - Rode a partir da raiz do projeto:
     ```bash
     python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/generate_catalog.py"
     ```
     Isso gera e sincroniza no projeto:
     - `.agent/catalog-data.js` (dados exclusivos locais do projeto).
     - `.agent/CATALOG.md` (catálogo unificado nas 13 categorias, em português, unindo Local + Super IA Projects + 0 Mkt).
     - `.agent/catalog-app.css` e `.agent/catalog-app.js` (fallback local offline).
     - `.agent/catalog.html` (dashboard interativo multi-base com busca rápida, filtros e modal central que renderiza o `SKILL.md` e lista arquivos de referências/scripts ao clicar em qualquer skill).

4. Estrutura de pastas (pelo mapa de destinos):
   - Crie só as pastas que o `docs/mapa-de-destinos.md` do passo 2 lista, pela seção "Árvore padrão" de `<SUPER_IA_PROJECTS_PATH>/.agent/skills/mapa-de-destinos/references/preset-marketing.md`; nenhuma pasta fora do mapa (as demais nascem quando precisar). Sem números nos nomes de pasta, exceto a esteira de aprovação.
   - Inteligência de mercado (tendências, estudos, monitoramento) segue as linhas do mapa e os SIPs (`sip-trends-previsao-demanda`, `sip-imprensa`, `sip-marketing`); não crie a árvore antiga `inteligencia/1_radar_tendencias/…4_fontes_e_coleta/`.
   - `scripts/` (só se o dono quiser os atalhos; nesse caso acrescente `code` ao `--modules` já no passo 2, antes de montar; se já montou: remonte, acrescente de novo o bloco `## Project` e as pastas de produção, e rode `cd "<project_root>" && python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/sync_rules.py"`) → scripts de conveniência locais com permissão de execução (`chmod +x`):
     - `scripts/coletar_trends.sh` (aponta para Previsão de Demanda).
     - `scripts/monitorar_imprensa.sh` (aponta para RSS Feed coletor/avaliador).
     - `scripts/minerar_hooks.sh` (aponta para `mine_hooks.py` do 0 Mkt / `yt-dlp`).
   - `.agent/plans/` → convenção de planos em `execution-loops/`, `handoffs/` e artefatos de sistema.
   - `memory.md` → memória de longo prazo do projeto (formato direto `Problema → Solução`).

5. Ambiente Seguro (.env) & Configuração do .gitignore:
   - Crie um `.gitignore` separando rigorosamente o que fica local do que sobe para o GitHub:
     - **DEVE SER IGNORADO (incluir obrigatoriamente no `.gitignore`):** `.DS_Store`, `node_modules/`, `__pycache__/`, `*.pyc`, `assets/**/*.mp4`, `assets/**/*.mov`, `*.tmp`, `.env`, `.env.local`, `.env.*.local`, `.agent/plans/`, `plans/`, `output/`, `.firecrawl/`, `certs/`, `*.pem`, `*.key`, `*.p12`, `*service-account*.json`, `credentials*.json` e configs MCP com chaves embutidas (`.mcp.json`, `opencode.json`, `.cursor/mcp.json`, `.vscode/mcp.json`, `.gemini/settings.json`, `.codex/config.toml`, `.zed/settings.json`, `config/mcporter.json`).
     - **DEVE SER VERSIONADO (NUNCA colocar no `.gitignore`):** `_projectdefines/` (se existir), `memory.md`, `STANDARDS.md`, `.env.example`, as pastas do mapa de destinos (`brand/`, `estrategia/`, `imprensa/`, `vendas/`, `conteudos/`, `inteligencia/`, `referencias/`, `docs/`, `scripts/` se houver) e todos os arquivos de regra Multi-IA (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`, `.cursorrules`, `.agent/rules/`).
   - Crie `.env` e `.env.example` juntos, com as MESMAS chaves (só nomes sem valores reais em `.env.example`, ex: `FIRECRAWL_API_KEY`, `N8N_WEBHOOK_URL`, chaves de IA/mídia).
   - Registre em `STANDARDS.md` a regra: "toda nova variável de ambiente deve ser adicionada em .env E .env.example na mesma mudança" (evita desvio de envs).

6. Registro na Central de Projetos:
   - Crie a ficha técnica em `<SUPER_IA_PROJECTS_PATH>/projetos/<nome-do-projeto>.md` usando o template base (`TEMPLATE.md`), marcando:
     - `Tipo: Marketing / Conteúdo & Mídia`
     - `Stack: Markdown / Git / Hub 0 Mkt`
     - `Marcas Atendidas: <Marca>`
     - `Banco Supabase: n/a` (ou indicar banco se aplicável)
     - `Cabeçalho:` `> **Última sincronização com o kit:** AAAA-MM-DD (kit @ HASH)` obtendo o HASH real com `git -C "<SUPER_IA_PROJECTS_PATH>" rev-parse --short HEAD`.
     - `Mapeamento de Integrações & APIs`: listar variáveis documentadas no `.env.example`.
     - `Skills Exclusivas deste Projeto`: registrar skills locais ou consumo global via SIPs (`.agent/SIPS-CONSUMIDOS.md`).
   - Adicione a linha correspondente no dashboard central em `<SUPER_IA_PROJECTS_PATH>/projetos/README.md`.

7. Plano Inicial Local & Exportação de Artefatos:
   - Crie o plano inicial em `.agent/plans/{Nome do Projeto} [PLAN].md` (lembrando que `.agent/plans/` fica apenas local via `.gitignore`).
   - **Exportação de Artefatos do Sistema (MANDATÓRIO):** Sempre que a interface do assistente gerar artefatos nativos (`implementation_plan.md`, `task.md`, `walkthrough.md`), salve uma cópia idêntica no repositório local sob `.agent/plans/{Task Name} [{TIPO}].md`.

8. Criação do Repositório no GitHub, Primeiro Commit & Push (`github-publisher`):
   - Siga rigorosamente a skill `<SUPER_IA_PROJECTS_PATH>/.agent/skills/github-publisher/SKILL.md`:
     a) **Pré-voo e Fronteira do Repositório:**
        - Verifique `gh auth status` (se não autenticado, instrua o usuário a rodar `! gh auth login`).
        - Rode `git rev-parse --show-toplevel 2>/dev/null` para checar se a pasta está dentro de um repositório-pai. Se retornar um diretório-pai, inicialize um repositório próprio na raiz deste projeto (`git init -b main`) e adicione esta pasta ao `.gitignore` do pai (ou confirme com o usuário conforme `github-publisher` — NUNCA publique o repositório-pai por engano).
     b) **Varredura Obrigatória de Segredos e Arquivos Grandes (antes de qualquer `git add`):**
        - Rode a varredura obrigatória de segredos:
          ```bash
          python3 "<SUPER_IA_PROJECTS_PATH>/.agent/skills/vulnerability-scanner/scripts/security_scan.py" .
          grep -rIlE --exclude-dir={node_modules,.git,.venv,venv,dist,build} -- 'sk_live_[0-9A-Za-z]{10,}|sk-(proj-)?[0-9A-Za-z_-]{20,}|AKIA[0-9A-Z]{16}|gh[pousr]_[0-9A-Za-z]{30,}|xox[abpr]-[0-9A-Za-z-]{10,}|AIza[0-9A-Za-z_-]{35}|-----BEGIN [A-Z ]*PRIVATE KEY-----' .
          find . -path ./node_modules -prune -o -path ./.git -prune -o -type f -size +50M -print
          ```
          Se apontar algo "critical" ou "high", leia o arquivo apontado e confirme manualmente se é segredo real ou falso positivo ANTES de comitar. Nunca ignore esse resultado.
     c) **Staging Verificado & Primeiro Commit:**
        - Inicialize na branch `main` e valide o stage:
          ```bash
          git init -b main
          git add -A
          git diff --cached --name-only
          ```
        - Confira a saída de `git diff --cached --name-only`: garanta que **NÃO** entraram `.env`, `.env.local`, `.agent/plans/`, `plans/`, vídeos pesados (`.mp4`/`.mov`) nem chaves privadas, e que **ESTÃO** presentes `CLAUDE.md`, `GEMINI.md`, `AGENTS.md`, `.cursorrules`, `STANDARDS.md`, `memory.md`, `.env.example`, `.gitignore` (e `_projectdefines/`, se houver).
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
   - Exiba o resumo final de inicialização contendo:
     - Caminho do projeto configurado e URL do repositório GitHub publicado (visibilidade e confirmação do primeiro push).
     - Confirmação de que `sync_rules.py --check` retornou "Parity OK".
     - Confirmação de que `sync_entrypoints.py` e `generate_catalog.py` rodaram com sucesso (CATALOG.md e catalog.html gerados).
     - Confirmação de que as skills locais têm symlink em `.claude/skills/` validado por `test -L`, e que o `sip-geral` está instalado (`test -L .claude/skills/sip-geral`) e que `docs/mapa-de-destinos.md` foi criado.
     - Confirmação de paridade entre `.env` e `.env.example`, criação do `memory.md` e o que foi excluído via `.gitignore` (`.env`, `.agent/plans/`, etc.).
     - Status da varredura de segurança do `security_scan.py` e commit inicial do git.
     - Pastas do mapa de destinos criadas (só as que o mapa lista).
     - Links clicáveis para a ficha técnica no `Super IA Projects` e os arquivos de regras.
     - Próximos passos recomendados de produção.
