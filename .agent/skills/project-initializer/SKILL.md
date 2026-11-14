---
# Repository: https://github.com/Felipelbahia/superiaprojects
name: project-initializer
description: Use when starting a new project from scratch, when user says "Quero criar um projeto novo com base na skill", or when requested to initialize greenfield project setup.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
author: Futuro Mercado / Felipe Bahia (@felipelbahia)
license: MIT
---
# Project Initializer - Guia Universal de Criação de Projetos do Zero

> **COMPATIBILIDADE MULTI-MODELO:** Este documento é um manual de instrução estrito e passo a passo. Qualquer modelo de IA (Gemini, Claude, GPT-4, DeepSeek, Codex, etc.) DEVE seguir estas etapas sequencialmente sem omitir passos.

---

## 🎯 Gatilhos de Ativação

- Frase exata: `"Quero criar um projeto novo com base na skill"`
- Solicitações equivalentes: *"Inicie um projeto novo do zero"*, *"Crie a estrutura para o projeto X"*, *"Quero criar um novo SaaS/API/App"*.

---

## 📋 Passo a Passo de Execução Multi-Modelo (6 Fases)

### Fase 1: Descoberta Interativa (Socratic Gate)
**A IA DEVE fazer APENAS 1 pergunta por vez ao usuário**, aguardando a resposta antes de enviar a próxima:
Depois de cada resposta, diga em 1 linha o que ela define (módulo de regras, SIP ou agente) e por quê.
1. **Pergunta 1 (Nome & Objetivo):** *"Qual o nome exato do novo projeto e a descrição em uma frase do seu objetivo principal?"*
1b. **Pergunta 1b (O que produz):** *"O que este projeto produz? (1) software: app, site, API, script; (2) conteúdo: e-mails, posts, artigos, roteiros, releases; (3) automação ou dados: workflows n8n, raspagem, pipelines, previsões; (4) uma mistura (diga quais)."* → software = módulo `code`; conteúdo = `content`; automação/dados = `automation` (+ `code` se houver código próprio: scripts, pipelines, Code nodes). As perguntas 1c, 2 e 2b só valem com `code`.
1c. **Pergunta 1c (Interface):** *"Tem interface? web, mobile, site Astro ou nenhuma (backend/CLI)?"* → web, mobile ou Astro = módulo `interface` (a tabela do módulo define o agente primário).
2. **Pergunta 2 (Stack Tecnológica):** *"Qual a stack tecnológica desejada? (ex: Next.js + Tailwind + Supabase, FastAPI + PostgreSQL, Flutter, etc.) Se não souber, responda 'não sei — recomende'."* Se o usuário não souber, recomende uma stack enxuta com base em [`app-builder`](file:///Users/macbookpro/Documents/IA%20Projects/_Plataforma/0%20Padr%C3%B5es/.agent/skills/app-builder/SKILL.md) (`tech-stack.md`) e confirme em linguagem simples, sem jargão. **Antes de recomendar, consulte o Context7** (regra *Docs first (Context7 MCP)*) para a versão estável atual de cada tecnologia: nunca recomende de memória.
2b. **Pergunta 2b (Banco Supabase — só se a stack tiver Supabase):** *"Qual banco Supabase este projeto usa? (consulte `projetos/_bancos-supabase.md`; existente, novo ou ainda não sei)"*. Siga a skill [`supabase`](file:///Users/macbookpro/Documents/IA%20Projects/_Plataforma/0%20Padr%C3%B5es/.agent/skills/supabase/SKILL.md): envs com sufixo do banco (`SUPABASE_<BANCO>_URL`), prefixo de tabelas do app, sem MCP, segredo só no `.env` do projeto. Registre o banco na ficha do projeto e no registro de bancos.
3. **Pergunta 3 (Público-Alvo & Escopo):** *"Quem são os usuários primários da aplicação e qual a funcionalidade principal da primeira versão?"*
4. **Pergunta 4 (SIPs):** leia a tabela de `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/projetos/_sips.md` e mostre TODOS os SIPs (domínio, nome e para que serve: a `description` do resolver em `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/skills/sip-<dominio>/SKILL.md`), em tabela, marcando ⭐ os que você sugere pelas respostas 1b e 1c, com o motivo em uma linha. O `sip-geral` entra sempre (não é pergunta). *"Quais instalar além do sip-geral? (sugeridos / nenhum / lista)"* Sem resposta = só o `sip-geral`.
5. **Agente primário:** sem módulo `interface`, proponha um agente de `.agent/agents/` do kit (ex.: `content-marketer` para conteúdo, `backend-specialist` para API) e confirme.
6. **Aprovação:** mostre o resumo (módulos `core` + `sip-access` + escolhidos, agente primário, stack se houver, SIPs) e só siga para a Fase 2 depois do "ok" do dono.

---

### Fase 2: Configuração Estrita de Arquivos de Regras (.agent, Claude, Antigravity & Cursor)
No diretório raiz do novo projeto (`<project_root>`):
1. **Criar Diretórios de Regras:**
   - Criar a pasta `<project_root>/.claude/` (para skills, agents e commands; **não** para um `CLAUDE.md`).
2. **Montar as Regras por Módulos (nunca recortar à mão):**
   - Os módulos ficam em `modules/` nesta skill (`core`, `sip-access`, `code`, `interface`, `content`, `automation`). Na raiz do projeto, monte com os aprovados na Fase 1 (sempre `core` e `sip-access`):
     ```bash
     python3 "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/scripts/assemble_rules.py" --modules core,sip-access,<escolhidos> --title "<Nome do Projeto>" --out "<project_root>/CLAUDE.md"
     ```
     Se o `CLAUDE.md` já existir: montado pelos módulos, o script mantém `## Project`, `## Stack` e `## Local rules` no fim (só reescreve a linha `- Modules:`, na ordem fixa do kit; se a linha faltar, ela não é criada) e move para `## Local rules`, avisando, as seções cujo título não é de módulo do kit; seções do kit e o texto antes da primeira seção são regenerados, e as de módulo que saiu da montagem são removidas (edição local ali não é mantida; o script avisa quais mudaram e quais saíram); cerca de código aberta e não fechada → o script recusa (código 4) sem gravar; no modelo antigo, o script recusa (código 3): copie os arquivos de regra para `.agent/plans/rules-backup-AAAA-MM-DD/`, rode de novo com `--replace` e passe as regras do arquivo antigo para `## Local rules` (como no prompt 01, passo 3). **Antes de mover cada regra antiga para `## Local rules`, pergunte se ela é sobre o assunto de um SIP** (firecrawl, n8n, marketing…): confira se o SIP já a tem (`<kit>/.agent/skills/sip-<nome>/SKILL.md` e o `SKILL.md` do hub); se não tem, vira item na `inbox/` do hub (formato do `inbox/README.md` do hub), não `## Local rules`. Caso real: a "Regra Global" do Firecrawl virou regra local ou sumiu na remontagem.
   - Acrescente ao fim do `CLAUDE.md` o bloco `## Project` preenchido, se ainda não estiver lá (o `## Stack`, com módulo `code`, é escrito só na Fase 4, depois do Context7).
   - Gere as cópias com `cd "<project_root>" && python3 "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/scripts/sync_rules.py"` (depois `--check` → "Parity OK"): `AGENTS.md` na raiz, cópia idêntica do `CLAUDE.md` (`GEMINI.md`, `.cursorrules` e `.agent/rules/` são legado: não gerar). **Não gerar `.claude/CLAUDE.md`**: o Claude Code carrega ele e o `./CLAUDE.md` juntos (regras em dobro).
   - Instale o `sip-geral` (`/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/prompts/instalar-skill-sip-geral.md`) e cada SIP escolhido (prompt na tabela de `_sips.md`). Agents/workflows de cada SIP: se o prompt perguntar, responda "nenhum"; se ele instalar todos sem perguntar (modelo anterior, inbox SIP-020 do kit), execute só o passo do resolver e pule os passos de agents/workflows. Eles ficam no SIP e só vêm para o projeto se o dono pedir.
3. **Mapa de destinos:** siga a skill `mapa-de-destinos` (conversa de criação a partir do `Produces`, uma pergunta por vez) e crie `<project_root>/docs/mapa-de-destinos.md`. Código fica fora do mapa.
4. **Gerar Padrões Locais (`STANDARDS.md`) e Memória de Longo Prazo (`memory.md`):**
   - Ler o template base `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/STANDARDS_TEMPLATE.md` (se existir) ou estruturar `<project_root>/STANDARDS.md` adaptando o nome do projeto, convenções reais do projeto (com `code`: da stack; com `content`: nomes por data e canal, pastas, voz em `brand/`; com `automation`: workflows e dados) e a regra obrigatória: *"toda nova variável de ambiente deve ser adicionada em `.env` E `.env.example` na mesma mudança"*.
   - Criar o arquivo `<project_root>/memory.md` na raiz do projeto (memória de longo prazo, lazy-loaded sob demanda, no formato direto `Problema → Solução`, sem jargão) para registrar decisões arquiteturais e bugs resolvidos ao longo da vida do projeto.
   - Criar `<project_root>/.env` e `<project_root>/.env.example` juntos, com as **mesmas chaves** (apenas os nomes das variáveis em `.env.example`, nunca valores reais).
5. **Gerar `<project_root>/.gitignore` (Regra Estrita: O que sobe vs. O que fica local):**
   - Usar como base o `.gitignore` do `0 Padrões`, garantindo a separação exata entre o que é versionado no GitHub e o que é ignorado:
     - **DEVE SER VERSIONADO (NUNCA colocar no `.gitignore` do projeto):**
       - **`_projectdefines/`**: se o projeto usar a skill `project-defines`, **tudo** dentro de `_projectdefines/` (`BRIEF.md`, `PRD.md`, `ARCHITECTURE.md`, `APP-FLOW.md`, `PATTERNS.md`, `SCHEMA.md`, `IMPLEMENTATION-PLAN.md`) **TEM que subir para o GitHub**.
       - **Memória, padrões e exemplo de ambiente**: `memory.md`, `STANDARDS.md` e `.env.example`.
       - **`.npmrc` sem token** (projeto Node): só configuração, como `engine-strict=true` (trava de versão do kit de onboarding); token de registro vai em `~/.npmrc` ou como `${NPM_TOKEN}`, nunca literal (decisão do dono 2026-11-12).
       - **Arquivos de regra Multi-IA**: `CLAUDE.md` e `AGENTS.md` (ficam fora do git *só* no `0 Padrões`; num projeto novo, **DEVEM ser versionados**).
     - **DEVE SER IGNORADO (incluir obrigatoriamente no `<project_root>/.gitignore`):**
       - **Variáveis de ambiente e segredos**: `.env`, `.env.*`, `*.env`, `.env.local`, `.env.*.local` — seguidas **obrigatoriamente depois** pelas exceções `!.env.example` e `!*.env.example` (a ordem importa: uma negação antes de `.env.*` ou `*.env` é anulada e esconde o exemplo; `.env.*` cobre variantes e backups como `.env.bak-*`, `.env.old`, `.env.production`), além de `certs/`, `*.pem`, `*.key`, `*.p12`, `*.crt`, `*service-account*.json`, `credentials*.json`. (O `.npmrc` **não** entra aqui: ele é versionado, ver abaixo.)
       - **Planos e artefatos temporários de execução**: `.agent/plans/` e `plans/` (acumulam muitos arquivos de rascunho/loops locais que são "lixo" no repositório remoto — ficam apenas locais; o contrato que sobe é `_projectdefines/`).
       - **Dependências, builds, caches e saídas temporárias**: `node_modules/`, `__pycache__/`, `*.pyc`, `.DS_Store`, `dist/`, `build/`, `.next/`, `out/`, `venv/`, `.venv/`, `output/`, `.temp_ag_kit/`, e equivalentes da stack escolhida.
       - **Configs MCP com API key embutida**: `.mcp.json`, `opencode.json`, `.cursor/mcp.json`, `.vscode/mcp.json`, `.gemini/settings.json`, `.codex/config.toml`, `.zed/settings.json`, `config/mcporter.json`.
       - `.firecrawl/` (se o projeto usar Firecrawl).

---

### Fase 3: Registro na Central de Projetos (`0 Padrões/projetos/`)
1. **Criar Ficha do Projeto:**
   - Ler o template `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/projetos/TEMPLATE.md`.
   - Criar o arquivo `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/projetos/<nome-do-projeto>.md` preenchendo as seções de objetivo, stack e integrações/APIs.
2. **Atualizar Dashboard Central:**
   - Adicionar uma nova linha na tabela do arquivo `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/projetos/README.md` contendo: Nome do projeto, Status, Stack principal e link para a ficha.

---

### Fase 3b: Oferta Opcional — Construir uma Aplicação com `project-defines`
Esta fase **nunca é obrigatória** e o padrão é **"Não"**: o initializer roda quase sempre, esta skill quase nunca. Faça **uma única pergunta**, em uma frase:
> *"Quer que eu conduza agora a construção de uma aplicação, com documentos de definição aprovados passo a passo (skill `project-defines`)? Padrão: Não."*
- **Não (ou sem resposta):** não crie `_projectdefines/` nem nada relacionado. Siga para as Fases 4, 5 e 6 exatamente como descritas abaixo.
- **Sim:** entregue o controle à skill `project-defines` (via `sip-geral` se não estiver local). **Pule as Fases 4 e 5** (o scaffolding vira item de construção do plano e o plano do projeto é o `_projectdefines/IMPLEMENTATION-PLAN.md`, que **sobe no GitHub** por estar em `_projectdefines/`); **execute normalmente a Fase 6** para publicar a estrutura inicial e `_projectdefines/` no GitHub e exiba o resumo final. Pré-preencha o BRIEF com as respostas das Perguntas 1 e 3 e **não pergunte de novo**. A stack **não** é decidida aqui: a Pergunta 2 vira preferência registrada no BRIEF e a decisão é do documento `ARCHITECTURE.md`. Crie `_projectdefines/` **somente depois deste "Sim"**. Como a ficha da Fase 3 já foi criada, atualize-a agora (stack = *a definir, decidida em `_projectdefines/ARCHITECTURE.md`*; status = *em definição*) e atualize-a de novo quando o `ARCHITECTURE.md` for aprovado.

---

### Fase 4: Scaffolding de Código (só com módulo `code`; sem `code`, pule para a Fase 5)
1. Ler a skill [`app-builder`](file:///Users/macbookpro/Documents/IA%20Projects/_Plataforma/0%20Padr%C3%B5es/.agent/skills/app-builder/SKILL.md) no `0 Padrões`.
2. **Antes de gerar qualquer arquivo, consulte o MCP de documentação (Context7)** para cada tecnologia da stack: versão estável atual (candidatas a release só se o usuário pedir), requisitos, mudanças que quebram compatibilidade e o comando oficial de criação (regra *Docs first (Context7 MCP)* do CLAUDE.md). Os templates do `app-builder` são ponto de partida: se estiverem desatualizados, siga a documentação e atualize o template. Sem o MCP, use a documentação oficial e diga qual fonte usou.
3. Gerar a estrutura inicial de arquivos e diretórios da stack selecionada, nas versões confirmadas no passo anterior.
4. **Registre a stack no bloco `## Stack` do arquivo de regras do projeto** (formato no CLAUDE.md, regra *Docs first (Context7 MCP)*): linguagem/runtime, framework e bibliotecas principais, **sem congelar números de versão**, apontando o lockfile como fonte das versões, com a data e a fonte da consulta ao Context7. Depois rode `cd "<project_root>" && python3 "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/scripts/sync_rules.py"` para manter a paridade entre os arquivos de regra.
5. Garantir a aplicação imediata das regras de Clean Code (da skill [`clean-code`](file:///Users/macbookpro/Documents/IA%20Projects/_Plataforma/0%20Padr%C3%B5es/.agent/skills/clean-code/SKILL.md)).
6. **Hook de commit (só se houver checagem rápida):** se o projeto tiver uma checagem determinística de até ~5 s (lint, paridade de regras, validação de esquema, **a parte rápida da suíte de testes**), crie `.githooks/pre-commit` que a rode e recuse o commit em caso de falha, um script `hooks:install` (`git config core.hooksPath .githooks`; em stacks sem `package.json`, o equivalente: alvo do `Makefile` ou comando no README) e uma linha no README sobre como ativar. Rode a checagem antes: se ela já falhar, corrija primeiro; se a falha é de um teste que já falhava, não o tire do hook nem o afrouxe: pergunte ao dono antes de instalar (com ele falhando, o hook recusaria todo commit). Nunca coloque a suíte longa de testes no hook: ela roda no `checklist.py` e no fechamento de mudança significativa. Sem checagem rápida, não crie hook.

---

### Fase 5: Plano Inicial Local
1. Criar o documento de plano inicial em `<project_root>/.agent/plans/{Nome do Projeto} [PLAN].md` (lembrando que `.agent/plans/` fica apenas local via `.gitignore`; se o projeto optou por `project-defines` na Fase 3b, o plano é `_projectdefines/IMPLEMENTATION-PLAN.md`, que é versionado no git).

---

### Fase 6: Criação do Repositório no GitHub, Primeiro Commit & Push (`github-publisher`)
Siga rigorosamente a esteira segura da skill [`github-publisher`](file:///Users/macbookpro/Documents/IA%20Projects/_Plataforma/0%20Padr%C3%B5es/.agent/skills/github-publisher/SKILL.md) para criar o repositório remoto e subir o primeiro commit limpo:
1. **Pré-voo e Fronteira do Repositório (OBRIGATÓRIO):**
   - Verificar autenticação no GitHub CLI: `gh auth status` (se não estiver logado, instruir o usuário a rodar `! gh auth login`).
   - Verificar fronteira git: `git -C "<project_root>" rev-parse --show-toplevel 2>/dev/null`.
     - Se retornar um **diretório-pai** (o projeto foi criado dentro de outro repo git): inicializar um repositório próprio em `<project_root>` (`git init -b main`) e adicionar a pasta do projeto ao `.gitignore` do pai (ou confirmar com o usuário, conforme Step 3 de `github-publisher` — NUNCA rodar `gh repo create --source=.` apontando para o pai).
2. **Auditoria de Segurança Pré-Staging (NUNCA fazer `git add` antes disto):**
   - Rodar o scanner do kit:
     ```bash
     python3 "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/skills/vulnerability-scanner/scripts/security_scan.py" "<project_root>"
     ```
   - Rodar a varredura de conteúdo por chaves literais e arquivos >50MB (Step 4 de `github-publisher`):
     ```bash
     grep -rIlE --exclude-dir={node_modules,.git,.venv,venv,dist,build} -- 'sk_live_[0-9A-Za-z]{10,}|sk-(proj-)?[0-9A-Za-z_-]{20,}|AKIA[0-9A-Z]{16}|gh[pousr]_[0-9A-Za-z]{30,}|xox[abpr]-[0-9A-Za-z-]{10,}|AIza[0-9A-Za-z_-]{35}|-----BEGIN [A-Z ]*PRIVATE KEY-----' "<project_root>"
     find "<project_root>" -path "*/node_modules" -prune -o -path "*/.git" -prune -o -type f -size +50M -print
     ```
   - Se encontrar qualquer segredo real em arquivo de código, **PARE** e mova para `.env` antes de prosseguir.
3. **Inicialização Git, Staging Verificado e Primeiro Commit:**
   - Garantir repositório inicializado na branch `main` e `README.md` mínimo presente. Com módulo `code` (código executável), o README mínimo inclui a seção "Como rodar em outra máquina" e o projeto ganha os arquivos do kit de onboarding (itens 1-7 de `github-publisher/references/onboarding-kit.md`: versão do runtime em arquivo, versão mínima que falha cedo, lockfile, `.env.example`, aviso das pastas de IA, symlinks documentados). A prova do clone limpo (item 8) é exigida antes de compartilhar o repositório, não antes do primeiro push privado (skill `github-publisher`, Step 9):
     ```bash
     git -C "<project_root>" init -b main
     git -C "<project_root>" add -A
     git -C "<project_root>" diff --cached --name-only
     ```
   - **Verificação obrigatória do Stage (`git diff --cached --name-only`):**
     - Confirmar que **NÃO** há `.env`, `.env.local`, `.agent/plans/`, `plans/`, `node_modules/`, `dist/` ou chaves privadas na lista.
     - Confirmar que **ESTÃO** presentes no stage: `CLAUDE.md`, `AGENTS.md`, `STANDARDS.md`, `memory.md`, `.env.example`, `.gitignore` e, se existir, toda a pasta `_projectdefines/`.
   - Realizar o primeiro commit:
     ```bash
     git -C "<project_root>" commit -m "feat: initial commit"
     ```
4. **Criação do Repositório no GitHub & Primeiro Push:**
   - Criar o repositório (privado por padrão, salvo se o usuário pedir público) e fazer o push inicial de forma não-interativa:
     ```bash
     cd "<project_root>" && gh repo create "<repo-slug>" --private --source=. --remote=origin --push --description "<descrição curta da Pergunta 1>"
     ```
   - Validar o remoto após o push (Step 8 de `github-publisher`):
     ```bash
     gh repo view --json url,visibility,defaultBranchRef
     git -C "<project_root>" ls-tree -r --name-only origin/main | grep -E '(^|/)(\.env|\.agent/plans|plans/.*|.*service-account.*\.json|.*\.pem|.*\.key)$'
     ```
     *(O grep acima não deve retornar nada).*
5. **Atualizar a Ficha Central com a URL do GitHub e Exibir Resumo Final:**
   - Atualizar o campo `> **Repositório GitHub:**` em `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/projetos/<nome-do-projeto>.md` com a URL retornada por `gh repo view`.
   - Exibir um resumo claro para o usuário contendo:
     - Caminho local do novo projeto e URL do repositório GitHub criado (visibilidade e confirmação do primeiro push).
     - Regras gêmeas geradas (`CLAUDE.md`, `AGENTS.md`), `STANDARDS.md` e `memory.md`.
     - Confirmação do que subiu no Git (`memory.md`, `_projectdefines/` se houver, `.env.example`, regras) e do que ficou protegido localmente via `.gitignore` (`.env`, `.agent/plans/`, `plans/`, deps/builds).
     - Link para a ficha técnica no `0 Padrões/projetos/`.
     - Próximos passos recomendados.

---

## 🔒 Regras Universais para Qualquer Modelo de IA

1. **Paridade Dual Absoluta:** Os arquivos `CLAUDE.md` e `AGENTS.md` DEVEM permanecer 100% iguais. Se o modelo alterar um, DEVE atualizar o outro.
2. **Isolamento de Skills Locais:** Skills criadas para este projeto DEVEM ser salvas APENAS em `<project_root>/.agent/skills/<skill-name>/SKILL.md`. NUNCA grave na pasta global do `0 Padrões` sem autorização explícita. *(Exceção autorizada pelo usuário: `project-defines` é uma skill global do `0 Padrões`.)*
3. **Acesso a skills de fora:** pelo `sip-geral` e pelos SIPs instalados (`.agent/SIPS-CONSUMIDOS.md`).
4. **Docs first (Context7 MCP):** antes de escolher, instalar ou codificar com qualquer tecnologia, consulte o Context7 (ou a documentação oficial, se o MCP não estiver disponível). A documentação de hoje vence a memória, os templates antigos e o código antigo do repositório.
5. **Scripts do kit não são copiados:** este initializer não copia `.agent/scripts/`. Quando um passo exigir `checklist.py`, `security_scan.py` ou similares e o projeto não tiver cópia local, chame pelo caminho absoluto `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/scripts/`.
