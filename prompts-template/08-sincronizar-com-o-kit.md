Sincronizar este projeto com o kit (incremental e auto-detectável)

Quero alinhar este projeto ao estado ATUAL do Super IA Projects em <SUPER_IA_PROJECTS_PATH> (e do hub 0 Mkt em <MARKETING_HUB_PATH>, se aplicável), mudando só o que ficou defasado desde a última sincronização, e atualizar a ficha dele em Super IA Projects/projetos/.

REGRAS: nunca apague nem sobrescreva do zero as regras locais do projeto (comandos, envs, convenções): MESCLE. Nunca apague pasta de skills por conta própria; ação destrutiva exige minha confirmação. Do `.env` leia só os NOMES. Nunca afirme algo sem ter verificado por comando ou leitura; o que não verificou fica "não verificado". Sem commit sem eu pedir.

1. Ponto de partida & Auto-detecção de Tipo:
   - Abra a ficha do projeto em <SUPER_IA_PROJECTS_PATH>/projetos/ (ache pela linha "Repositório / Caminho"). Leia a linha "Última sincronização com o kit: DATA (kit @ HASH)". Se não existir, trate como "nunca sincronizado" e rode a sincronização completa.
   - **Classifique o Tipo do Projeto** (pela linha `Tipo:` da ficha ou inspecionando a raiz):
     a) **Marketing / Conteúdo & Mídia:** projetos com foco em marca, copy, conteúdo, inteligência de nicho ou que possuem pastas `brand/` e `conteudos/`.
     b) **Software / Código:** projetos de backend, APIs, frontend, web, mobile ou dados.

2. O que mudou no ecossistema:
   - Rode `git -C "<SUPER_IA_PROJECTS_PATH>" log --oneline HASH..HEAD -- CLAUDE.md GEMINI.md AGENTS.md .cursorrules .agent` e `git ... diff --stat HASH..HEAD -- CLAUDE.md .agent/rules`. Se o HASH não existir mais, diga "não verificado" e compare por conteúdo.
   - Se for projeto de **Marketing**, verifique também se houve novidades no hub central: `git -C "<MARKETING_HUB_PATH>" log --oneline -n 10` e consulte o prompt [02b-criar-projeto-mkt.md](<SUPER_IA_PROJECTS_PATH>/projetos/prompts/02b-criar-projeto-mkt.md).
   - Complemente com o estado deste projeto: `python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/projects_audit.py" --no-write` e leia a linha dele.
   - Liste, em português simples, as mudanças do kit que AFETAM este projeto (regras, agentes, skills, scripts) e as que não afetam.

3. Regras & Diretrizes (com Roteamento Inteligente por Tipo):
   - Mescle apenas o que falta das regras nos arquivos do projeto (./CLAUDE.md, ./GEMINI.md, ./AGENTS.md, ./.cursorrules e .agent/rules/*), preservando 100% das regras locais.
   - **Se o projeto for de Software / Código:**
     - Use como base o template de Super IA Projects/CLAUDE.md.
     - Remova seções irrelevantes (ex: regras de mobile se o projeto for apenas backend).
   - **Se o projeto for de Marketing / Conteúdo & Mídia:**
     - Use como referência o padrão consolidado em 0 Mkt e no prompt `02b-criar-projeto-mkt.md`.
     - Garanta o **Filtro Anti-Slop mandatório**: todo texto/copy deve passar por `.agent/workflows/ai-slop-detector.md` ou `geral-anti-slop` antes de ser entregue.
     - Garanta o **Protocolo de Fallback de Marketing**: prioridade máxima para 0 Mkt (<MARKETING_HUB_PATH>) para carregar skills de vídeo (Remotion, ElevenLabs), Sexy Canvas, Growth Lab, Copywriting, mineração de ganchos (`hook-mining`) e análise de reels (`reel-analyzer`).
     - **NUNCA injete seções técnicas irrelevantes**: não inclua regras de banco de dados Supabase, APIs de backend ou frameworks mobile.
   - **Diretrizes Globais Universais (obrigatórias em ambos os tipos):**
     - Confirme com `grep -c` que estão presentes nas regras:
       - `Project Defines Gate (only if _projectdefines/ exists)`
       - `Latest Docs First (Context7 MCP)`
       - `Firecrawl: MCP vs Execução Local` (< 10 buscas/scrapes via MCP remoto; ≥ 10 em lote via `Firecrawl - local` em `<FIRECRAWL_LOCAL_PATH>`)
       - `memory.md` na raiz (memória de longo prazo do projeto, formato direto `Problema → Solução`)
       - Bloco `## Stack` sem versões congeladas (com tipo do projeto, ferramentas, runtimes e data de verificação)
       - Convenção de planos em `.agent/plans/execution-loops/`, `handoffs/` e exportação de artefatos de sistema (`[PLAN]`, `[TASK]`, `[WALKTHROUGH]`).
   - Ao terminar a edição das regras, rode da raiz:
     ```bash
     python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/sync_rules.py"
     ```
     Só prossiga se a saída disser literalmente "100% synchronized".

3b. Estrutura Canônica de Marketing (só para projetos de Marketing / Conteúdo):
   - **Módulo de Inteligência:** Se o projeto ainda não tiver a árvore de inteligência em 4 camadas, crie/alinhe em `inteligencia/`:
     - `1_radar_tendencias/` (radar ativo, sinais emergentes, hooks minerados, análise de virais, trends)
     - `2_imprensa_pr/` (matriz de newsjacking, ganchos com quotes dos fundadores, mapa de veículos)
     - `3_estudos_embasamento/` (acervo de dados e métricas, cases reais, dossiês)
     - `4_fontes_e_coleta/` (fontes curadas, termos_inteligencia.txt, motores conectados, playbook)
     - Scripts executáveis em `scripts/` com permissão `chmod +x`: `coletar_trends.sh`, `monitorar_imprensa.sh`, `minerar_hooks.sh`.
   - **Estrutura de Conteúdos:** Garanta que a produção organizada viva sob `conteudos/<canal>/YYYY-MM-DD - Nome da Demanda/` com variações (`copy-opcao-1.md`, `briefing.md`, etc.).

4. Skills e Catálogo Unificado Multi-Base:
   - Liste as skills locais em `.agent/skills/` e compare com o catálogo da ficha (o que entrou e o que saiu desde a última ficha).
   - Rode, da raiz do projeto:
     ```bash
     python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/sync_entrypoints.py"
     ```
     (cria/repara symlinks locais para `.claude/agents/`, `.claude/commands/` e `.cursor/commands/`).
   - Gere e atualize o Catálogo Geral do projeto:
     ```bash
     python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/generate_catalog.py"
     ```
     Isso gera e sincroniza no projeto:
     - `.agent/catalog-data.js` (dados exclusivos das skills/workflows locais do projeto).
     - `.agent/CATALOG.md` (índice completo estruturado em 13 categorias, em Português, unificando as skills locais com as bases globais `Super IA Projects` e `0 Mkt`).
     - `.agent/catalog-app.css` e `.agent/catalog-app.js` (fallback local offline do layout mestre centralizado).
     - `.agent/catalog.html` (dashboard interativo conectado em runtime às 3 bases — Local + Super IA Projects + 0 Mkt —, com busca rápida, filtros, categorias expansíveis e modal central que ao clicar em qualquer skill exibe o conteúdo completo do `SKILL.md`, suas instruções e lista de arquivos de referências/scripts).
   - Para cada skill local em `.agent/skills/<nome>`, confira `.claude/skills/<nome>` com `test -L`: falta symlink, crie (`ln -s "../../.agent/skills/<nome>" ".claude/skills/<nome>"`); existe como pasta real, rode `diff -rq` e PARE esperando minha confirmação. Confirme que `~/.claude/skills/skill-resolver/SKILL.md` existe (senão, registre como pendência pessoal no resumo). Se alguma skill local for cópia de uma skill do kit que mudou, aponte as diferenças com `diff -rq` e me pergunte antes de atualizar.

5. Ficha Técnica Central & Dashboard:
   - Atualize a ficha do projeto em <SUPER_IA_PROJECTS_PATH>/projetos/<nome-do-projeto>.md (stack, objetivo, catálogo completo de skills locais e integrações/APIs documentadas no .env.example, só afirmações verificadas).
   - Atualize a linha correspondente na tabela do dashboard central em <SUPER_IA_PROJECTS_PATH>/projetos/README.md.
   - Por último, grave no cabeçalho da ficha: `> **Última sincronização com o kit:** AAAA-MM-DD (kit @ HASH)`, com a data de hoje e o retorno de:
     ```bash
     git -C "<SUPER_IA_PROJECTS_PATH>" rev-parse --short HEAD
     ```
     Só grave depois de os passos 3 e 4 estarem concluídos e verificados.

6. Verificação Final & Resumo:
   - `git status` do projeto mostrando apenas os arquivos esperados.
   - `sync_rules.py` retornou 100% de paridade.
   - Todos os symlinks de skills verificados com `test -L`.
   - Nenhuma referência nos arquivos de regra aponta para algo inexistente.

Pare ao final e me apresente, em português simples, SÓ o que mudou: o tipo de projeto detectado, o que o kit/hub trouxe de novo e foi aplicado, o que foi preservado, skills que entraram ou saíram, pendências que dependem de mim e qualquer coisa "não verificada". Não repita o que já estava correto.
