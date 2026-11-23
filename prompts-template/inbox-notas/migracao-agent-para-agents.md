# {num} — Varredura local: pasta `.agent/` virou `.agents/` (padrão do Codex)
Status: na inbox · Aberto em: {data} · Pedido por: avisar_projetos_inbox.py · Projeto de origem: {projeto} (kit: {hub})

## O quê
Em {data} o kit (`{hub}`) renomeou a pasta `.agent/` para `.agents/` (o nome que o Codex lê) e migrou este projeto com `migrate_agent_to_agents.py`: a pasta foi renomeada, os links foram reapontados e `.agent/` virou `.agents/` nos arquivos de regras, `.gitignore`, `.githooks/`, `.github/` e nos textos de `.agents/` (planos antigos em `.agents/plans/` ficaram como estavam). Não existe alias `.agent -> .agents`. **Nada foi commitado:** as mudanças estão no working tree. Falta uma varredura local para confirmar que nada ficou para trás.

## Como (o que fazer quando for pedido)
1. `git status` e revise o diff: deve ser rename de `.agent/` para `.agents/` (a árvore mostra apagados + novos até o `git add -A`) e trocas de texto de `.agent/` por `.agents/`.
2. Procure o que ficou: `grep -rIn -E '(^|[^A-Za-z0-9_])\.agent([^A-Za-z0-9_-]|$)' . --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=plans`. Cada achado é um caminho que o script não cobre (código do projeto, docs, CI externa, `.env`, README): troque quando for a pasta do kit.
3. Links: `find . -xtype l -not -path "./.git/*" -not -path "./node_modules/*"` sem saída.
4. Regras: `python3 .agents/scripts/sync_rules.py --check` (se o projeto tiver o script) ou `diff <(tail -n +2 CLAUDE.md) <(tail -n +2 AGENTS.md)` vazio.
5. Skills: abrir uma sessão e conferir que as skills do projeto e do núcleo aparecem; `python3 "{hub}/.agents/scripts/sips_status.py" .` sem erro de link.
6. Rode a suíte de testes e o lint do projeto; se tudo verde, commite (mensagem: `chore: .agent -> .agents`). Config e `.env` seguem a regra de ambiente: avise o dono antes de commitar se o diff tiver config.
7. Mova esta nota para `inbox/arquivo/`.

## Onde
`.agents/` do projeto, `CLAUDE.md`/`AGENTS.md`/`.cursorrules`, `.gitignore`, `.githooks/`, `.github/`, `.claude/skills|agents|commands` (links). Kit: `{hub}/.agents/`.

## Por quê
O Codex e as convenções novas de agentes leem `.agents/`. O script só troca texto em lugares conhecidos; uma varredura local pega o que é específico do projeto. Origem: item 050 da inbox do kit.

## Para quê
O projeto usa só `.agents/`, nenhuma referência ao caminho antigo sobra e os links resolvem.

## Quem
Dono do projeto decide o commit; o Claude da sessão faz a varredura.

## Efeitos e impactos
Até o commit, o projeto funciona com `.agents/` no disco; quem clonar o repositório sem o commit ainda verá `.agent/`. Sem a varredura, referências soltas a `.agent/` (por exemplo em CI externa ou docs) ficam apontando para uma pasta que não existe.

## Exemplos
De `.agent/skills/execution-loop/SKILL.md` para `.agents/skills/execution-loop/SKILL.md`.

## Gatilho para sair da inbox
Próxima sessão de manutenção do projeto, ou o loop "Propagação do Kit para os Projetos".

## Enquanto isso
Os scripts do kit leem `.agents/` e ainda aceitam `.agent/` (suporte dual). Não crie symlink `.agent -> .agents`.
