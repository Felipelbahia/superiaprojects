Adotar o contrato em projeto existente

Quero adotar o contrato `_projectdefines/` neste projeto, que JÁ EXISTE. Siga o modo brownfield da skill project-defines: <SUPER_IA_PROJECTS_PATH>/.agent/skills/project-defines/brownfield.md (e o prompt em .../prompts/brownfield.md).

REGRAS (valem para tudo): NÃO altere, mova nem apague nenhum arquivo existente. Não instale nada, não rode o projeto, não use rede (exceto Context7/documentação oficial). Segredos: só os NOMES das variáveis. Escreva apenas dentro de `_projectdefines/`. Nunca afirme algo sem ter verificado por comando ou leitura; se não verificou, escreva "não verificado".

1. Preflight: tipo do projeto, manifests/lockfile, bloco `## Stack`, ficha em Super IA Projects/projetos/, arquivos de regras, documentação existente (ARCHITECTURE.md, CODEBASE.md, README, roadmap/backlog, loops antigos), pastas legadas na raiz.
2. Descoberta com evidência (comandos reais). Compare a FICHA e o README com o código e liste toda divergência.
3. Decida quais documentos se aplicam ao tipo do projeto; os que não se aplicam ficam registrados como "não se aplica" com o motivo (nunca invente telas ou regras visuais).
4. Rascunhe TODOS os documentos aplicáveis como as-built (BRIEF com porte proposto, PRD, ARCHITECTURE, APP-FLOW, PATTERNS, SCHEMA). Cada afirmação leva um rótulo: [as-built] (com a evidência na mesma linha), [assumption] ou [owner].
5. Lacunas e divergências (mock, rota sem login, sem testes, documentos que descrevem o que não existe) viram "Open decisions"/backlog com as duas versões e a evidência. Lacuna de segurança vira item bloqueante.
6. Monte o `IMPLEMENTATION-PLAN.md`: Fase 0 (Baseline, o que já existe e funciona, com evidência), Fase 1 (a adoção) e o backlog existente (ex.: BackLog/Roadmap.md) nas fases seguintes, preservando a origem.
7. Verificação de versões: consulte o Context7 pela versão INSTALADA e pela estável atual de cada tecnologia principal; o que estiver atrás vira item de backlog. NÃO suba versão nenhuma.
8. Prepare o bloco `## Stack` e o texto do Gate dentro do rascunho do ARCHITECTURE; só grave no arquivo de regras DEPOIS que eu aprovar o ARCHITECTURE.

Pare ao final e me apresente, em português simples: os arquivos criados, uma tabela documento → aplica / não se aplica (motivo), as principais divergências, e o resumo de aprovação do primeiro documento (o que decide em até 5 linhas, o que limita, a opção recomendada e múltipla escolha). Eu aprovo um documento por vez.
