Atualização de Projetos

Quero atualizar este projeto para o padrão de Inteligência Global do Super IA Projects SEM APAGAR ou sobrescrever do zero as regras e especificações que este projeto já possui.

Consulte o repositório base <SUPER_IA_PROJECTS_PATH> e execute o processo de MESCLAGEM (Merge & Preserve).

REGRA GERAL (vale para todos os passos abaixo): NUNCA afirme no resumo final que algo "existe", "está correto" ou "foi preservado" sem ter verificado de fato com um comando (find/grep/diff/comm) ou leitura direta do arquivo. Se você não verificou, não afirme — diga "não verificado" em vez de assumir.

1. Leitura & Preservação de Regras Locais:
   - Leia todos os arquivos de regra existentes neste projeto (./CLAUDE.md, ./AGENTS.md, ./.cursorrules, .agent/rules/GEMINI.md, STANDARDS.md, etc.), se existirem.
   - Liste explicitamente, um por um, quais arquivos encontrou e quais regras específicas cada um contém (comandos de build/test, variáveis de ambiente, convenções, exceções). Não resuma de memória — copie/cite o que está escrito.
   - MANTENHA E PRESERVE 100% dessas regras específicas do projeto.

2. Inclusão das Diretrizes de Inteligência Global:
   - Mescle com o conteúdo existente as diretrizes globais do Super IA Projects: paridade de regras, isolamento local de novas skills em .agent/skills/, busca fallback em Super IA Projects e 0 Mkt, e o link da ficha técnica no Super IA Projects/projetos/.
   - ANTES de copiar qualquer referência a agente, skill ou script do template global (ex: nomes como `orchestrator`, `backend-specialist`, `security_scan.py`, ou arquivos como `CODEBASE.md`/`ARCHITECTURE.md`/`PATTERNS.md`/`memory.md`), VERIFIQUE que cada um existe de verdade:
     - Agentes (personas como `orchestrator`): `ls "<SUPER_IA_PROJECTS_PATH>/.agent/agents/<nome>.md"`
     - Workflows (comandos `/nome`, como `/plan`, `/tdd-cycle`): `ls "<SUPER_IA_PROJECTS_PATH>/.agent/workflows/<nome>.md"` — workflow NUNCA está em `agents/`
     - Skills: `ls "<SUPER_IA_PROJECTS_PATH>/.agent/skills/<nome>/"`
     - Scripts: `find "<SUPER_IA_PROJECTS_PATH>/.agent/skills" -name "<nome>.py"`
     - Arquivos citados (CODEBASE.md etc.) dentro DESTE projeto: `find . -maxdepth 2 -iname "<nome>"`
   - Se algo citado no template NÃO existir, NÃO copie a referência cegamente: ou adapte para algo que existe de fato neste projeto (ex: trocar `CODEBASE.md` por `STANDARDS.md` se for o que documenta dependências aqui), ou remova a seção com uma nota explicando por quê.
   - Identifique o tipo do projeto (backend/API, frontend/web, mobile, dados/IA, automação) e REMOVA do arquivo final as seções do template que não se aplicam (ex: regras de Design/UI/Mobile num projeto 100% backend sem interface). Não deixe "por via das dúvidas" — só o que é real para este projeto.

3. Sincronização em Todas as Portas de Entrada (Paridade Total Multi-IA):
   - Atualize de forma idêntica os arquivos de entrada: ./CLAUDE.md (maiúsculas exatas na raiz), ./GEMINI.md, ./AGENTS.md, ./.cursorrules e os arquivos em .agent/rules/ (GEMINI.md, CLAUDE.md, AGENTS.md).
   - Ao terminar, rode a partir da raiz do projeto:
     ```
     python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/sync_rules.py"
     ```
   - Cole a saída completa desse comando no resumo final. Só é aceitável reportar "paridade concluída" se a saída disser literalmente "100% synchronized". Se não disser, corrija e rode de novo até dizer.

3b. Regras novas do kit (confirme que chegaram, por comando):
   - `grep -c "Project Defines Gate" CLAUDE.md`, `grep -c "Latest Docs First" CLAUDE.md` e `grep -c "^## Stack" CLAUDE.md` (cada um deve ser ≥ 1 depois da mesclagem; se o projeto já tinha uma seção própria "Stack e Arquitetura" com versões fixas, PRESERVE-A e acrescente o bloco `## Stack` do kit, sem números de versão).
   - Se o projeto não tiver o bloco `## Stack`: leia o lockfile/manifest, consulte o Context7 pela versão instalada e escreva o bloco (formato no CLAUDE.md, regra "Latest Docs First").
   - Planos e handoffs agora ficam em `.agent/plans/execution-loops/` e `.agent/plans/handoffs/`. Se o projeto já tem `execution-loops/` ou `handoffs/` na raiz, NÃO mova: a regra de legado mantém a raiz até o dono pedir a migração.
   - Se o `.gitignore` do projeto esconde `.agent/plans/` ou pastas de loop, registre como pendência (esconde o histórico do projeto).

4. Varredura Completa e Padronização de Skills Locais:
   - Busque por skills em todas as pastas do projeto (.agent/skills/, .agents/skills/, .claude/skills/, skills/, etc.).
   - Se houver skills locais, garanta que fiquem organizadas em .agent/skills/<nome-da-skill>/SKILL.md com cabeçalho YAML (name + description no mínimo). Esta é a fonte única de CONTEÚDO — mas sozinha ela é invisível para o Claude Code (ver nota "Atualização em 2026-09-03" no topo deste arquivo).
   - Se encontrar MAIS DE UMA pasta de skills com conteúdo próprio (ex: .agent/skills/ e .agents/skills/, ambas com arquivos reais), compare arquivo por arquivo com `diff -rq` antes de sugerir qualquer consolidação. NUNCA apague uma pasta duplicada por conta própria: (a) confirme por diff que nada seria perdido, (b) proponha a remoção no resumo final e PARE, aguardando confirmação explícita do usuário antes de executar. Apagar é uma ação destrutiva.
   - **Distinga duplicata de conteúdo (acima) de espelho de descoberta — NÃO são a mesma coisa:** para cada skill em `.agent/skills/<nome>/`, verifique `.claude/skills/<nome>`:
     ```
     test -L ".claude/skills/<nome>" && echo "OK: já é symlink" || (test -e ".claude/skills/<nome>" && echo "ATENÇÃO: existe como pasta/cópia real, não symlink — comparar com diff -rq antes de tocar" || echo "FALTANDO: criar symlink")
     ```
     - Se **faltando**: crie `ln -s "../../.agent/skills/<nome>" ".claude/skills/<nome>"` — isso NÃO é criar uma skill nova (a regra 3 do CLAUDE.md sobre escopo local não se aplica aqui), é só o ponteiro que faz o Claude Code enxergar uma skill que já existe.
     - Se **existe como pasta real** (não symlink): rode `diff -rq ".claude/skills/<nome>" ".agent/skills/<nome>"`. Em AMBOS os casos (idêntico ou divergente) vale a mesma regra do bullet acima: NUNCA apague/substitua por conta própria — proponha a ação exata (substituir por symlink, se idêntico; ou tratar como duplicata real com conteúdo próprio, se divergente) no resumo final e PARE, aguardando confirmação explícita do usuário antes de executar.
   - **Agents e workflows locais (mesma lógica das skills):** se o projeto tem `.agent/agents/` ou `.agent/workflows/` próprios, rode da raiz do projeto `python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/sync_entrypoints.py" --check`; se apontar link faltando, rode sem `--check` (o script só cria/repara symlinks para `.claude/agents/`, `.claude/commands/` e `.cursor/commands/`; nunca toca em arquivo real nem em link que aponta para fora). Entradas reais (não symlink) ele só reporta: trate como no bullet das skills (diff, propor, PARAR). Cada erro de validação que ele listar (agent sem `name`/`description`, `skills:` inexistente) vai para o resumo final.
   - Verifique que a skill roteadora global existe: `ls ~/.claude/skills/skill-resolver/SKILL.md`. Se não existir, sinalize no resumo final como pendência de setup pessoal (não é algo a recriar por projeto — é um recurso único, fora deste repositório).

5. Registro/Atualização da Ficha Central em Super IA Projects:
   - Crie/atualize a ficha técnica deste projeto em <SUPER_IA_PROJECTS_PATH>/projetos/[NOME_DO_PROJETO].md (baseado em .../projetos/TEMPLATE.md).
   - Toda variável de ambiente que você listar na ficha precisa ter sido confirmada de fato — rode `grep -oE "^[A-Z_]+=" .env.example | sort` e, se existir um `.env` real, compare os dois com `comm -23 <(grep -oE "^[A-Z_]+=" .env | sort -u) <(grep -oE "^[A-Z_]+=" .env.example | sort -u)`. Se sobrar algo do lado esquerdo, o `.env.example` está incompleto — corrija-o antes de documentar a ficha (isso já aconteceu de verdade neste tipo de projeto: 13 variáveis reais usadas em código não estavam documentadas em lugar nenhum).
   - Preencha a stack real, o objetivo, e o catálogo completo de TODAS as skills locais catalogadas no passo 4.
   - Adicione/atualize a linha deste projeto na tabela do <SUPER_IA_PROJECTS_PATH>/projetos/README.md.

6. Verificação Final (checklist obrigatório antes de apresentar o resumo):
   - [ ] sync_rules.py retornou "100% synchronized" (cole a saída)
   - [ ] Os três `grep -c` do passo 3b retornaram ≥ 1 (cole a saída) e o bloco `## Stack` não tem números de versão congelados
   - [ ] Toda referência a agente/skill/script nos arquivos de regra foi confirmada existente por comando (não suposição)
   - [ ] Nenhuma instrução nos arquivos de regra aponta para um arquivo que não existe neste projeto
   - [ ] .env.example (se existir) foi comparado com .env real e está 100% completo (comando do passo 5 retornou vazio ou só variáveis comprovadamente não usadas em código)
   - [ ] Skills duplicadas foram identificadas (inclusive um `.claude/skills/<nome>` real, idêntico ou divergente) e, se existirem, o usuário foi consultado antes de qualquer remoção ou substituição por symlink
   - [ ] Toda skill em .agent/skills/<nome>/ tem um `.claude/skills/<nome>` correspondente e é um symlink de verdade (verificado com `test -L`, não suposição) — garante descoberta nativa pelo Claude Code
   - [ ] `~/.claude/skills/skill-resolver/SKILL.md` foi checado; se ausente, isso foi registrado no resumo como pendência
   - [ ] A ficha técnica no Super IA Projects só contém afirmações verificadas, não copiadas de memória

   Apresente um resumo comparativo destacando: as regras locais que foram preservadas, as diretrizes globais que foram mescladas, as skills catalogadas, E qualquer referência do template que você removeu ou adaptou por não existir de fato — seja transparente sobre isso, não esconda.
