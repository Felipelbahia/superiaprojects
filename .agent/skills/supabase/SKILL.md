---
# Repository: https://github.com/Felipelbahia/superiaprojects
name: supabase
description: Use when a project creates, reads or writes a Supabase database, sets up its .env, writes migrations, or when the owner works with several Supabase databases (each with its own login) and must not mix them up.
author: Super IA Projects / Futuro Mercado
license: MIT
---
# Supabase (multi-banco)

## Overview

O dono usa **vários bancos Supabase**, cada um com login próprio, compartilhados por vários projetos. O risco real é ler ou gravar no banco errado. Esta skill fixa **qual banco é qual**, **como nomear as envs** e **como conferir antes de gravar**. Ela é genérica: nada de refs, tabelas ou chaves de um banco específico.

Decisões do dono (2026-10-12): **sem MCP do Supabase** nos projetos; o `.env` **vive dentro de cada projeto**; o registro central guarda **só referências**, nunca segredo.

## When to Use

- Projeto novo ou existente que vai usar Supabase (banco, Auth, Storage, Edge Functions).
- Criar ou revisar `.env`/`.env.example`, scripts de banco ou migrações.
- Qualquer dúvida de "este projeto aponta para qual banco?".
- **Não** para SQL genérico (use `postgresql`, `sql-optimization-patterns`) nem para modelagem (`database-design`).

## 1. Descobrir o banco do projeto (nunca presumir)

Ordem de busca: (1) registro central `projetos/_bancos-supabase.md` em `0 Padrões`; (2) ficha do projeto (`projetos/<nome>.md`, linha "Banco Supabase"); (3) `.env.example` do projeto. Se as fontes divergirem ou disserem "a confirmar", **pergunte ao dono**; não escolha pelo nome do projeto.

Projeto novo: pergunte "qual banco?" e confirme se vai usar um banco existente (e qual prefixo de tabelas terá) ou um novo (registrar no registro central).

## 2. Nomenclatura das envs

Sufixo do banco em **todo** nome de variável, `<BANCO>` em maiúsculas sem espaços:

```
SUPABASE_<BANCO>_URL
SUPABASE_<BANCO>_ANON_KEY
SUPABASE_<BANCO>_SERVICE_ROLE_KEY     # só servidor; nunca com VITE_/NEXT_PUBLIC_
SUPABASE_<BANCO>_DB_URL               # conexão Postgres direta, se usada
SUPABASE_<BANCO>_PROJECT_REF          # opcional, usado pela trava (seção 5)
SUPABASE_ACCESS_TOKEN_<BANCO>         # opcional, login do CLI deste banco
```

- Prefixo de framework vem **antes**: `VITE_SUPABASE_PESSOAL_URL`, `NEXT_PUBLIC_SUPABASE_PLINQ_URL`.
- Nunca use `SUPABASE_URL` ou `DATABASE_URL` sem sufixo em projeto novo: o nome não diz de qual banco é.
- Projeto existente com nome antigo: não renomeie por conta própria; a ficha indica o banco, e a migração de nomes é decisão do dono.
- Chave `service_role` bypassa RLS: só em backend/script/edge function. Segredo **só** em `.env` (no `.gitignore`) do próprio projeto; `.env.example` só com nomes e valores vazios.

## 3. Banco compartilhado: prefixo de tabelas por app

Quando mais de um app usa o mesmo banco, cada app tem **seu prefixo** (`<app>_tabela`), o prefixo fica no registro central e nenhum app toca tabela de outro sem estar declarado na ficha. Objetos novos (tabela, view, função, policy) nascem com o prefixo.

## 4. Banco, RLS e migrações

- Toda tabela exposta ao cliente nasce com **RLS ativado** e policy explícita.
- Migrações como arquivos em `supabase/migrations/` do projeto, versionadas no git.
- Um projeto de código = um banco "linkado". Antes de qualquer comando que muda o remoto, confira o link e simule:
  `supabase link --project-ref <ref>` (uma vez) → `supabase migration new <nome>` → `supabase db push --dry-run` → só então `supabase db push`.
- Login do CLI é por conta: com logins diferentes por banco, use o token do banco certo (`SUPABASE_ACCESS_TOKEN` carregado do `.env` deste projeto), nunca um login global esquecido de outro banco.
- Comandos, flags e APIs mudam: consulte o Context7 (`/supabase/cli`, `/supabase/supabase`) para a versão instalada antes de citar de memória.

## 5. Trava opcional contra banco errado

Em script ou app que **grava**, valide no início que a URL pertence ao banco esperado e aborte se não:

```
esperado = env.SUPABASE_<BANCO>_PROJECT_REF
if not env.SUPABASE_<BANCO>_URL.contains(esperado): abortar
```

Opcional por decisão do dono; recomendada em scripts de escrita em banco compartilhado. Em leitura, basta cliente nomeado por banco (`supabasePessoal`, `supabasePlinq`), sem cliente "default".

## 6. Sem MCP

Por decisão do dono, projetos **não** usam o MCP do Supabase: o isolamento vem do `.env` correto no projeto, da nomenclatura acima e da trava. Não proponha configurar o MCP; se o dono pedir, trate como mudança de decisão.

## Common Mistakes

| Erro | Correção |
|---|---|
| Criar `SUPABASE_URL` genérico em projeto novo | Use `SUPABASE_<BANCO>_URL` |
| Presumir o banco pelo nome do projeto | Registro → ficha → `.env.example`; senão pergunte |
| Anotar chave ou senha no registro central ou na ficha | Registro guarda só referência; segredo só no `.env` do projeto |
| `VITE_`/`NEXT_PUBLIC_` na `service_role` | Chave de serviço nunca vai ao navegador |
| `db push` sem `--dry-run` em banco compartilhado | Simule e confira o link primeiro |
| Tabela nova sem prefixo do app | Prefixo do app vem do registro central |
| Copiar `project_ref`/tabelas de um banco para esta skill | A skill é genérica; fatos de banco ficam no registro e nas fichas |
| Sugerir MCP "para facilitar" | Decisão do dono: sem MCP |
