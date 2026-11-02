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

2. Configuração de Regras Interoperáveis Multi-IA (Paridade Total):
   - Na Raiz do Projeto (./): crie ./CLAUDE.md (maiúsculas exatas), ./GEMINI.md, ./AGENTS.md e ./.cursorrules.
   - Na Pasta de Regras (.agent/rules/): crie .agent/rules/GEMINI.md, .agent/rules/CLAUDE.md e .agent/rules/AGENTS.md.
   - Na Pasta .claude/ (se aplicável): crie .claude/CLAUDE.md.
   - Adaptar o template-base do Super IA Projects/CLAUDE.md para foco estrito em Marketing:
     - Remova seções de Mobile, Banco de Dados, APIs de backend e regras de UI/Web (se o projeto não tiver interface web/código).
     - Mantenha ativo o Protocolo de Fallback com prioridade máxima para o 0 Mkt (<MARKETING_HUB_PATH>) para carregar skills de vídeo (Remotion, ElevenLabs), Sexy Canvas, Growth Lab, Copywriting, mineração de ganchos (`hook-mining`) e análise de reels (`reel-analyzer`).
     - Deixe explícito que o projeto consome o 0 Mkt como Hub de inteligência e salva a produção exclusivamente nas pastas locais do projeto (`conteudos/`, `brand/`, `inteligencia/`, etc.).
     - Inclua obrigatoriamente as diretrizes modernas do kit:
       - **Project Defines Gate:** só se aplica se houver a pasta `_projectdefines/` (projetos de marketing e conteúdo são autônomos por padrão).
       - **Latest Docs First (Context7 MCP):** antes de adotar qualquer script de automação, ferramenta ou biblioteca (ex: `yt-dlp`, `ffmpeg`, `google-genai`), consulte o Context7 (`resolve-library-id` → `query-docs`).
       - **Bloco `## Stack`:** sem números de versão congelados, documentando o tipo do projeto, o Hub 0 Mkt, runtimes/scripts e a data de verificação.
       - **Firecrawl (MCP vs Execução Local):** < 10 buscas/scrapes via Firecrawl MCP remoto; ≥ 10 em lote via `Firecrawl - local` em `<FIRECRAWL_LOCAL_PATH>` (protocolo `start` → `health` → `usar` → `stop`).
       - **Memória de Longo Prazo (`memory.md`):** criar na raiz com lazy load sob demanda e formato direto `Problema → Solução`.
       - **Processamento Humano & Anti-Slop Mandatório:** todo conteúdo final produzido deve passar pelo fluxo anti-slop (`ai-slop-detector` / `geral-anti-slop`) eliminando clichês de IA antes de entregar ao usuário.
   - **Descoberta de skills pelo Claude Code:** se o projeto nascer com ou criar alguma skill local em `.agent/skills/<nome>/`, crie também `.claude/skills/<nome>` como symlink relativo (`ln -s "../../.agent/skills/<nome>" ".claude/skills/<nome>"`). O Claude Code só varre `.claude/skills/` e `~/.claude/skills/`. Valide com `test -L`. Confira se `~/.claude/skills/skill-resolver/SKILL.md` existe (senão registre como pendência de setup pessoal no resumo final).
   - **Agents e workflows locais:** se o projeto nascer com `.agent/agents/` ou `.agent/workflows/`, rode da raiz do projeto:
     ```bash
     python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/sync_entrypoints.py"
     ```
     (cria symlinks `.claude/agents/`, `.claude/commands/`, `.cursor/commands/` e valida metadados `name` e `description`).
   - Crie o arquivo `STANDARDS.md` na raiz baseado no `STANDARDS_TEMPLATE.md`, adaptado para convenções reais de marketing (padrão de nomenclatura de arquivos por data e canal, convenção de tags, metadados e rotina de produção).
   - Ao terminar a edição das regras, rode:
     ```bash
     python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/sync_rules.py"
     ```
     Só prossiga para o próximo passo se a saída disser literalmente "100% synchronized".

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

4. Estrutura Canônica de Pastas & Módulo de Inteligência:
   - Crie a seguinte estrutura de diretórios na raiz do projeto:
     - `brand/` → manual de marca, tom de voz (`brand-voice.md`), personas (`personas.md`), pilares de conteúdo (`content-pillars.md`), style guide (`style-guide.md`) e esteira de ofertas.
     - `inteligencia/` → Módulo Canônico de Inteligência de Negócio estruturado em 4 camadas:
       - `1_radar_tendencias/` (radar ativo, sinais emergentes, hooks minerados via `hook-mining`, desmontagem de virais via `reel-analyzer`, coletas em `trends/`).
       - `2_imprensa_pr/` (matriz de newsjacking, ganchos de imprensa com quotes dos fundadores, mapa de veículos/jornalistas).
       - `3_estudos_embasamento/` (acervo de dados e métricas checadas, banco de cases reais, dossiês temáticos).
       - `4_fontes_e_coleta/` (fontes curadas, `termos_inteligencia.txt` ponderados para RSS Feed, motores conectados, playbook de rotina semanal).
     - `scripts/` → scripts de conveniência locais com permissão de execução (`chmod +x`):
       - `scripts/coletar_trends.sh` (aponta para Previsão de Demanda).
       - `scripts/monitorar_imprensa.sh` (aponta para RSS Feed coletor/avaliador).
       - `scripts/minerar_hooks.sh` (aponta para `mine_hooks.py` do 0 Mkt / `yt-dlp`).
     - `referencias/` → repertório de hooks, estruturas narrativas (storytelling), formatos de alta retenção e benchmarks de concorrentes.
     - `calendarios/` → planejamento mensal/semanal e distribuição editorial.
     - `conteudos/` → produção de posts, carrosséis, roteiros de vídeo e artigos organizada por canal e lote/data (`conteudos/<canal>/YYYY-MM-DD - Nome da Demanda/` contendo `copy-opcao-1.md`, `copy-opcao-2.md`, `briefing.md`, `draft.md`).
     - `campanhas/` → campanhas de lançamento, captação ou eventos sazonais específicos.
     - `assets/` → mídias geradas (imagens, áudios, frames, vídeos).
     - `docs/` → planejamento estratégico, análises de métricas de clientes e notas.
     - `.agent/plans/` → convenção de planos em `execution-loops/`, `handoffs/` e artefatos de sistema.
     - `memory.md` → memória de longo prazo do projeto (formato direto `Problema → Solução`).

5. Controle de Versão (Git), Ambiente Seguro (.env) & Varredura de Segurança:
   - Inicialize o git se ainda não houver:
     ```bash
     git init
     ```
   - Crie um `.gitignore` contendo no mínimo: `.DS_Store`, `node_modules/`, `assets/**/*.mp4`, `assets/**/*.mov`, `*.tmp`, `.env`, `.env.local`, `.env.*.local`, `output/`.
   - Crie `.env` e `.env.example` juntos, com as MESMAS chaves (só nomes sem valores reais em `.env.example`, ex: `FIRECRAWL_API_KEY`, `N8N_WEBHOOK_URL`, chaves de IA/mídia).
   - Registre em `STANDARDS.md` a regra: "toda nova variável de ambiente deve ser adicionada em .env E .env.example na mesma mudança" (evita desvio de envs).
   - Antes do primeiro commit, rode a varredura obrigatória de segredos:
     ```bash
     python3 "<SUPER_IA_PROJECTS_PATH>/.agent/skills/vulnerability-scanner/scripts/security_scan.py" .
     ```
     Se apontar algo "critical" ou "high", leia o arquivo apontado e confirme manualmente se é segredo real ou falso positivo ANTES de comitar. Nunca ignore esse resultado.
   - Faça o primeiro commit só depois dessa varredura limpa.

6. Registro na Central de Projetos:
   - Crie a ficha técnica em `<SUPER_IA_PROJECTS_PATH>/projetos/<nome-do-projeto>.md` usando o template base (`TEMPLATE.md`), marcando:
     - `Tipo: Marketing / Conteúdo & Mídia`
     - `Stack: Markdown / Git / Hub 0 Mkt`
     - `Marcas Atendidas: <Marca>`
     - `Banco Supabase: n/a` (ou indicar banco se aplicável)
     - `Cabeçalho:` `> **Última sincronização com o kit:** AAAA-MM-DD (kit @ HASH)` obtendo o HASH real com `git -C "<SUPER_IA_PROJECTS_PATH>" rev-parse --short HEAD`.
     - `Mapeamento de Integrações & APIs`: listar variáveis documentadas no `.env.example`.
     - `Skills Exclusivas deste Projeto`: registrar skills locais ou consumo global via Fallback.
   - Adicione a linha correspondente no dashboard central em `<SUPER_IA_PROJECTS_PATH>/projetos/README.md`.

7. Plano Inicial, Exportação de Artefatos & Apresentação:
   - Crie o plano inicial em `.agent/plans/{Nome do Projeto} [PLAN].md`.
   - **Exportação de Artefatos do Sistema (MANDATÓRIO):** Sempre que a interface do assistente gerar artefatos nativos (`implementation_plan.md`, `task.md`, `walkthrough.md`), salve uma cópia idêntica no repositório sob `.agent/plans/{Task Name} [{TIPO}].md`.
   - Pergunte ao usuário se deseja publicar o repositório no GitHub agora (privado, por padrão) — não crie/faça push sem essa confirmação explícita.
   - Exiba o resumo final de inicialização contendo:
     - Caminho do projeto configurado.
     - Confirmação de que `sync_rules.py` retornou 100%.
     - Confirmação de que `sync_entrypoints.py` e `generate_catalog.py` rodaram com sucesso (CATALOG.md e catalog.html gerados).
     - Confirmação de que as skills locais têm symlink em `.claude/skills/` validado por `test -L`, e que `~/.claude/skills/skill-resolver/SKILL.md` foi checado.
     - Confirmação de paridade entre `.env` e `.env.example`.
     - Status da varredura de segurança do `security_scan.py` e commit inicial do git.
     - Estrutura canônica de pastas criada.
     - Links clicáveis para a ficha técnica no `Super IA Projects` e os arquivos de regras.
     - Próximos passos recomendados de produção.
