# {num} — Remontar as regras do kit: perguntar ao dono quando o hook recusa por config
Status: na inbox · Aberto em: {data} · Pedido por: avisar_projetos_inbox.py · Projeto de origem: {projeto} (kit: {hub})

## O quê
A regra "Environment and production" do módulo `core` ganhou uma frase: quando o hook de commit recusa por config ou ambiente (`env_diff_check.py`), o agente pergunta ao dono se quer commitar e dar push mesmo assim; nunca libera com `ALLOW_ENV_DIFF=1` por conta própria. Falso positivo comum: exemplos com `user:pass@localhost` em texto de skill ou catálogo.

## Como (o que fazer quando for pedido)
Rodar o prompt 01 (`prompts-template/01-atualizar-projeto-existente.md` do kit): remonta o `CLAUDE.md` com `assemble_rules.py` (mesmos módulos, só linhas dos módulos no diff) e roda `sync_rules.py`. Prova: `grep -n -F "ask the owner whether to commit and push anyway" CLAUDE.md`.

## Onde
`CLAUDE.md` e `AGENTS.md` deste projeto; módulo em `{hub}/.agent/skills/project-initializer/modules/core.md`.

## Por quê
O hook recusou um commit por falso positivo e o agente precisa saber o que fazer: perguntar, não contornar nem liberar sozinho.

## Para quê
`CLAUDE.md` do projeto contém a frase; `sync_rules.py --check` → Parity OK.

## Quem
Dono do projeto decide; o Claude da sessão aplica.

## Efeitos e impactos
Nada muda até a decisão. Remontar não apaga regras locais (`## Local rules`).

## Exemplos
O `grep` acima devolve uma linha.

## Gatilho para sair da inbox
Próxima atualização de regras deste projeto, ou o loop "Propagação do Kit para os Projetos".

## Enquanto isso
Se o hook recusar, pare e pergunte ao dono antes de qualquer `ALLOW_ENV_DIFF=1`.
