# {num} — Remontar as regras do kit: busca no SIP e disciplina de mudança
Status: na inbox · Aberto em: {data} · Pedido por: avisar_projetos_inbox.py · Projeto de origem: {projeto} (kit: {hub})

## O quê
O kit mudou os módulos de regras: (A) skill, agent ou workflow citado nas regras e ausente de `.claude/` deve ser procurado em `.agent/`, nos SIPs instalados e no kit antes de dizer "não existe"; (B) seção nova "Change discipline" (parar e avisar em vez de contornar; mudança mínima dentro do `Scope:` do plano), regras de dependência, config e produção, e suíte inteira antes de "feito". Dois checks de máquina novos: `env_diff_check.py` e `scope_check.py`.

## Como (o que fazer quando for pedido)
Rodar o prompt 01 (`prompts-template/01-atualizar-projeto-existente.md` do kit; cópia pronta em `projetos/prompts/`): ele remonta o `CLAUDE.md` com `assemble_rules.py` (mesmos módulos, só linhas dos módulos no diff), roda `sync_rules.py` e, com módulo `code`, propõe acrescentar os dois checks ao `.githooks/pre-commit`. Prova: `grep -n -F -e "Named in these rules but not in" -e "Change discipline" CLAUDE.md`.

## Onde
`CLAUDE.md` e `AGENTS.md` deste projeto; módulos em `{hub}/.agent/skills/project-initializer/modules/`.

## Por quê
Em três projetos o handoff falhou porque o agente não achou a skill `session-handoff` (só o ponteiro `sip-geral` está instalado) e desistiu em vez de procurar no hub. As regras novas fecham essa falha e as cinco regras de disciplina de mudança.

## Para quê
O `CLAUDE.md` do projeto tem a seção "Change discipline" e a regra de busca; `sync_rules.py --check` → Parity OK.

## Quem
Dono do projeto decide; o Claude da sessão aplica.

## Efeitos e impactos
Nada muda até a decisão. Remontar não apaga regras locais (ficam em `## Local rules`).

## Exemplos
Saída esperada do `grep` acima: uma linha com a regra de busca e uma com `## NN. Change discipline`.

## Gatilho para sair da inbox
Próxima atualização de regras deste projeto, ou o loop "Propagação do Kit para os Projetos".

## Enquanto isso
O agente deve seguir o §Central hub das regras atuais: skill citada e não instalada se resolve pelo `sip-geral`.
