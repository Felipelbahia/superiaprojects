Criar um projeto do Zero

Quero criar um projeto novo com base na skill project-initializer em <SUPER_IA_PROJECTS_PATH>/.agent/skills/project-initializer/SKILL.md.

Siga rigorosamente o protocolo de 5 fases para compatibilidade Multi-IA.

REGRA GERAL (vale para todos os passos abaixo): NUNCA afirme no resumo final que algo "existe", "está correto" ou "foi configurado" sem ter verificado de fato com um comando ou leitura direta. Se você não verificou, diga "não verificado" em vez de assumir.

1. Descoberta Interativa (Socratic Gate):
   - Faça APENAS 1 pergunta por vez para definir: Nome e Objetivo, Stack Tecnológica desejada, Público-Alvo/Escopo.
   - Pergunte também explicitamente: "este projeto terá alguma interface (web ou mobile) ou é 100% backend/automação/dados?" — a resposta decide quais seções do template global entram nos arquivos de regra (não inclua regras de Design/UI/Mobile num projeto sem interface nenhuma).

2. Configuração de Regras Interoperáveis Multi-IA (Paridade Total):
   - Na Raiz do Projeto (./): crie ./CLAUDE.md (maiúsculas exatas), ./GEMINI.md, ./AGENTS.md e ./.cursorrules.
   - Na Pasta de Regras (.agent/rules/): crie .agent/rules/GEMINI.md, .agent/rules/CLAUDE.md e .agent/rules/AGENTS.md.
   - Na Pasta .claude/ (se aplicável): crie .claude/CLAUDE.md.
   - Ao copiar o conteúdo-base de Super IA Projects/CLAUDE.md, aplique o mesmo filtro: para cada agente/skill/workflow/script citado, verifique que existe (`ls`/`find` em Super IA Projects/.agent/agents/, /.agent/workflows/ e /.agent/skills/) antes de incluir a referência. Remova as seções que não se aplicam ao tipo de projeto definido no passo 1 (ex: tabela de MOBILE/WEB se o projeto for só backend).
   - **Descoberta de skills pelo Claude Code:** se o projeto já nascer com alguma skill local em `.agent/skills/<nome>/` (copiada de Super IA Projects ou criada do zero), crie também `.claude/skills/<nome>` como symlink (`ln -s "../../.agent/skills/<nome>" ".claude/skills/<nome>"`) — sem isso a skill existe mas o Claude Code nunca a lista (ele só varre `.claude/skills/` e `~/.claude/skills/`, nunca `.agent/skills/`). Vale para qualquer skill local criada depois também, não só nesta etapa inicial. Confira se `~/.claude/skills/skill-resolver/SKILL.md` existe; se não, é uma pendência de setup pessoal a mencionar, não algo deste projeto.
   - **Agents e workflows locais:** se o projeto nascer com `.agent/agents/` ou `.agent/workflows/`, rode da raiz `python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/sync_entrypoints.py"` (cria os symlinks `.claude/agents/`, `.claude/commands/`, `.cursor/commands/` e valida). Agent = persona (`name`+`description`); workflow = comando `/nome` (`description`).
   - Crie o arquivo STANDARDS.md na raiz baseado no template .../STANDARDS_TEMPLATE.md, preenchido com convenções REAIS da stack escolhida (nomenclatura de arquivos, como adicionar um novo módulo/integração) — não deixe placeholders genéricos tipo "{detalhes}".
   - Ao terminar, rode:
     ```
     python3 "<SUPER_IA_PROJECTS_PATH>/.agent/scripts/sync_rules.py"
     ```
     Só prossiga para o passo 3 se a saída disser "100% synchronized".

3. Registro na Central de Projetos:
   - Crie a ficha técnica em <SUPER_IA_PROJECTS_PATH>/projetos/<nome-do-projeto>.md usando o template .../projetos/TEMPLATE.md.
   - Adicione o projeto na tabela do dashboard central em .../projetos/README.md.

4. Scaffolding, Controle de Versão & Clean Code:
   - ANTES de gerar qualquer arquivo, consulte o Context7 para cada tecnologia da stack (versão estável atual, requisitos, comando oficial de criação) — regra "Latest Docs First" do CLAUDE.md. Depois do scaffolding, escreva o bloco `## Stack` no arquivo de regras (só nomes, sem versões congeladas) e rode o sync_rules.py de novo.
   - Execute o scaffolding inicial da stack via a skill app-builder do Super IA Projects, aplicando Clean Code.
   - Inicialize o controle de versão desde o início:
     ```
     git init
     ```
   - Crie um .gitignore cobrindo no mínimo: node_modules/, dist/, .env, .env.local, .env.*.local, certs/, *.crt, *.key, *.pem, *.p12, e qualquer pasta de saída/scratch que o scaffolding gerar (ex: output/).
   - Crie .env e .env.example juntos, com as MESMAS chaves (só nomes — nunca valores reais em .env.example). Registre em STANDARDS.md a regra: "toda nova variável de ambiente deve ser adicionada em .env E .env.example na mesma mudança" — isso evita que os dois arquivos divirjam com o tempo (problema real já encontrado num projeto desta base: 13 variáveis usadas em código nunca documentadas).
   - Antes do primeiro commit, rode uma varredura de segredos:
     ```
     python3 "<SUPER_IA_PROJECTS_PATH>/.agent/skills/vulnerability-scanner/scripts/security_scan.py" .
     ```
     Se apontar algo "critical" ou "high", leia o arquivo apontado e confirme manualmente se é um segredo real ou falso positivo (padrão de nome/documentação) ANTES de decidir se comita. Nunca ignore esse resultado sem checar.
   - Faça o primeiro commit só depois dessa varredura.

5. Plano Inicial & Apresentação:
   - Pergunte UMA vez (padrão: Não) se o dono quer construir uma aplicação agora com a skill `project-defines` (documentos aprovados passo a passo). Se "Não", nada é criado; se "Sim", pule o plano inicial abaixo (o plano passa a ser `_projectdefines/IMPLEMENTATION-PLAN.md`).
   - Gere o plano em .agent/plans/{Nome do Projeto} [PLAN].md.
   - Pergunte ao usuário se deseja publicar o repositório no GitHub agora (privado, por padrão) — não crie/faça push sem essa confirmação explícita, mesmo que o restante do setup seja automático.
   - Exiba o resumo final com: confirmação de que sync_rules.py retornou 100%, lista de qualquer referência do template removida/adaptada por não se aplicar ao tipo de projeto, confirmação de que toda skill local em .agent/skills/<nome>/ tem `.claude/skills/<nome>` como symlink de verdade (verificado com `test -L`, não suposição) e que `~/.claude/skills/skill-resolver/SKILL.md` foi checado, status do git (commit feito, o que foi excluído via .gitignore e por quê), e links para a ficha técnica e os arquivos de regra gerados.
