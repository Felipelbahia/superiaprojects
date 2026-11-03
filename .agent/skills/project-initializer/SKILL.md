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

## 📋 Passo a Passo de Execução Multi-Modelo (5 Fases)

### Fase 1: Descoberta Interativa (Socratic Gate)
**A IA DEVE fazer APENAS 1 pergunta por vez ao usuário**, aguardando a resposta antes de enviar a próxima:
1. **Pergunta 1 (Nome & Objetivo):** *"Qual o nome exato do novo projeto e a descrição em uma frase do seu objetivo principal?"*
2. **Pergunta 2 (Stack Tecnológica):** *"Qual a stack tecnológica desejada? (ex: Next.js + Tailwind + Supabase, FastAPI + PostgreSQL, Flutter, etc.) Se não souber, responda 'não sei — recomende'."* Se o usuário não souber, recomende uma stack enxuta com base em [`app-builder`](file:///Users/macbookpro/Documents/IA%20Projects/_Plataforma/0%20Padr%C3%B5es/.agent/skills/app-builder/SKILL.md) (`tech-stack.md`) e confirme em linguagem simples, sem jargão. **Antes de recomendar, consulte o Context7** (regra *Latest Docs First*) para a versão estável atual de cada tecnologia: nunca recomende de memória.
2b. **Pergunta 2b (Banco Supabase — só se a stack tiver Supabase):** *"Qual banco Supabase este projeto usa? (consulte `projetos/_bancos-supabase.md`; existente, novo ou ainda não sei)"*. Siga a skill [`supabase`](file:///Users/macbookpro/Documents/IA%20Projects/_Plataforma/0%20Padr%C3%B5es/.agent/skills/supabase/SKILL.md): envs com sufixo do banco (`SUPABASE_<BANCO>_URL`), prefixo de tabelas do app, sem MCP, segredo só no `.env` do projeto. Registre o banco na ficha do projeto e no registro de bancos.
3. **Pergunta 3 (Público-Alvo & Escopo):** *"Quem são os usuários primários da aplicação e qual a funcionalidade principal da primeira versão?"*

---

### Fase 2: Configuração Estrita de Arquivos de Regras (.agent, Claude, Antigravity & Cursor)
No diretório raiz do novo projeto (`<project_root>`):
1. **Criar Diretórios de Regras:**
   - Criar a pasta `<project_root>/.agent/rules/`.
   - Criar a pasta `<project_root>/.claude/` (para suporte nativo ao Claude).
2. **Copiar & Gerar Regras Interoperáveis (Paridade Total Multi-AI):**
   - **Na Raiz do Projeto (`<project_root>/`):** Gerar `<project_root>/CLAUDE.md` (em maiúsculas exatas), `<project_root>/GEMINI.md`, `<project_root>/AGENTS.md` e `<project_root>/.cursorrules`.
   - **Na Pasta de Regras (`<project_root>/.agent/rules/`):** Gerar `<project_root>/.agent/rules/GEMINI.md`, `<project_root>/.agent/rules/CLAUDE.md` e `<project_root>/.agent/rules/AGENTS.md`.
   - **Na Pasta Claude (`<project_root>/.claude/`):** Gerar `<project_root>/.claude/CLAUDE.md`.
   *(Garantir paridade de 100% no conteúdo de todos os arquivos de regra via `sync_rules.py`)*.
3. **Gerar Padrões Locais (`STANDARDS.md`):**
   - Ler o template base `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/STANDARDS_TEMPLATE.md`.
   - Criar o arquivo `<project_root>/STANDARDS.md` adaptando o nome do projeto e convenções.

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
- **Não (ou sem resposta):** não crie `_projectdefines/` nem nada relacionado. Siga para a Fase 4 e a Fase 5 exatamente como descritas abaixo.
- **Sim:** entregue o controle à skill `project-defines` (resolva pelo Protocolo Fallback se não estiver local). **Pule as Fases 4 e 5** (o scaffolding vira item de construção do plano e o plano é o `_projectdefines/IMPLEMENTATION-PLAN.md`); ainda exiba o resumo final da Fase 5, sem os itens de scaffold e plano inicial. Pré-preencha o BRIEF com as respostas das Perguntas 1 e 3 e **não pergunte de novo**. A stack **não** é decidida aqui: a Pergunta 2 vira preferência registrada no BRIEF e a decisão é do documento `ARCHITECTURE.md`. Crie `_projectdefines/` **somente depois deste "Sim"**. Como a ficha da Fase 3 já foi criada, atualize-a agora (stack = *a definir, decidida em `_projectdefines/ARCHITECTURE.md`*; status = *em definição*) e atualize-a de novo quando o `ARCHITECTURE.md` for aprovado.

---

### Fase 4: Scaffolding de Código
1. Ler a skill [`app-builder`](file:///Users/macbookpro/Documents/IA%20Projects/_Plataforma/0%20Padr%C3%B5es/.agent/skills/app-builder/SKILL.md) no `0 Padrões`.
2. **Antes de gerar qualquer arquivo, consulte o MCP de documentação (Context7)** para cada tecnologia da stack: versão estável atual (candidatas a release só se o usuário pedir), requisitos, mudanças que quebram compatibilidade e o comando oficial de criação (regra *Latest Docs First* do CLAUDE.md). Os templates do `app-builder` são ponto de partida: se estiverem desatualizados, siga a documentação e atualize o template. Sem o MCP, use a documentação oficial e diga qual fonte usou.
3. Gerar a estrutura inicial de arquivos e diretórios da stack selecionada, nas versões confirmadas no passo anterior.
4. **Registre a stack no bloco `## Stack` do arquivo de regras do projeto** (formato no CLAUDE.md, regra *Latest Docs First*): linguagem/runtime, framework e bibliotecas principais, **sem congelar números de versão**, apontando o lockfile como fonte das versões, com a data e a fonte da consulta ao Context7. Depois rode `sync_rules.py` para manter a paridade entre os arquivos de regra.
5. Garantir a aplicação imediata das regras de Clean Code (da skill [`clean-code`](file:///Users/macbookpro/Documents/IA%20Projects/_Plataforma/0%20Padr%C3%B5es/.agent/skills/clean-code/SKILL.md)).

---

### Fase 5: Plano Inicial & Apresentação Final
1. Criar o documento de plano inicial em `<project_root>/.agent/plans/{Nome do Projeto} [PLAN].md`.
2. Exibir um resumo claro para o usuário contendo:
   - Caminho do novo projeto.
   - Regras gêmeas geradas (`GEMINI.md` e `CLAUDE.md`).
   - Link para a ficha técnica no `0 Padrões/projetos/`.
   - Próximos passos recomendados.

---

## 🔒 Regras Universais para Qualquer Modelo de IA

1. **Paridade Dual Absoluta:** Os arquivos `GEMINI.md` e `CLAUDE.md` DEVEM permanecer 100% iguais. Se o modelo alterar um, DEVE atualizar o outro.
2. **Isolamento de Skills Locais:** Skills criadas para este projeto DEVEM ser salvas APENAS em `<project_root>/.agent/skills/<skill-name>/SKILL.md`. NUNCA grave na pasta global do `0 Padrões` sem autorização explícita. *(Exceção autorizada pelo usuário: `project-defines` é uma skill global do `0 Padrões`.)*
3. **Protocolo Fallback:** Ao procurar por skills não encontradas no projeto local, a IA DEVE buscar em:
   - `1º` `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/skills/`
   - `2º` `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Mkt/` (para marketing, SEO, copy e growth)
4. **Latest Docs First:** antes de escolher, instalar ou codificar com qualquer tecnologia, consulte o Context7 (ou a documentação oficial, se o MCP não estiver disponível). A documentação de hoje vence a memória, os templates antigos e o código antigo do repositório.
5. **Scripts do kit não são copiados:** este initializer não copia `.agent/scripts/`. Quando um passo exigir `checklist.py`, `security_scan.py` ou similares e o projeto não tiver cópia local, chame pelo caminho absoluto `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/scripts/`.
