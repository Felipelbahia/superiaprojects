
# {num} — Remontar as regras do kit: `Unknown skill` não é erro e núcleo de skills linkado
Status: na inbox · Aberto em: {data} · Pedido por: avisar_projetos_inbox.py · Projeto de origem: {projeto} (kit: {hub})

## O quê
O kit mudou a regra "Named in these rules but not in `.claude/skills/`…" do módulo `core`: (A) um `Unknown skill` da ferramenta Skill não é erro do projeto: a IA não para nem repete a chamada, avisa o dono em uma linha e lê o arquivo pelo caminho que o novo script `resolve_skill.py` imprime (projeto, hubs dos SIPs instalados e kit, com o conteúdo lido do disco); (B) só o **núcleo** de skills (9: `execution-loop`, `brainstorming`, `writing-skills`, `session-handoff`, `verification-before-completion`, `spec-writing`, `plan-writing`, `executing-plans`, `systematic-debugging`) passa a ser linkado em `.claude/skills/`. Esse segundo ponto já foi aplicado neste projeto pelo `propagar_sip.py` (links e linhas no `.gitignore`, `.agent/SIPS-CONSUMIDOS.md` com a data nova). Falta só o texto das regras.

## Como (o que fazer quando for pedido)
Rodar o prompt 01 (`prompts-template/01-atualizar-projeto-existente.md` do kit; cópia pronta em `projetos/prompts/`): ele remonta o `CLAUDE.md` com `assemble_rules.py` (mesmos módulos; só a linha dessa regra deve mudar no diff) e roda `sync_rules.py`. Prova: `grep -n -F "resolve_skill.py" CLAUDE.md` deve devolver uma linha.

## Onde
`CLAUDE.md` e `AGENTS.md` deste projeto; módulo em `{hub}/.agent/skills/project-initializer/modules/core.md`; script em `{hub}/.agent/scripts/resolve_skill.py`.

## Por quê
No projeto IL - Portais, `Skill("execution-loop")` devolveu `Unknown skill: execution-loop` e o dono leu como falha, porque a skill vive no hub e não em `.claude/skills/`. O mesmo vale para qualquer skill de hub ou SIP chamada pelo nome. Com o núcleo linkado as de processo funcionam direto; para as demais, a regra nova manda resolver pelo caminho.

## Para quê
O `CLAUDE.md` do projeto tem a regra com `resolve_skill.py`; `sync_rules.py --check` → Parity OK. Ao pedir o `execution-loop`, a IA o carrega sem `Unknown skill`.

## Quem
Dono do projeto decide; o Claude da sessão aplica.

## Efeitos e impactos
Nada muda até a decisão. Remontar não apaga regras locais (ficam em `## Local rules`). O projeto já tem 9 skills a mais na lista da ferramenta Skill (custo de contexto), todas ignoradas pelo git.

## Exemplos
`python3 "{hub}/.agent/scripts/resolve_skill.py" session-handoff` imprime o caminho absoluto da skill no hub e diz se o SIP está instalado aqui.

## Gatilho para sair da inbox
Próxima atualização de regras deste projeto, ou o loop "Propagação do Kit para os Projetos".

## Enquanto isso
O agente que receber `Unknown skill` roda `python3 "{hub}/.agent/scripts/resolve_skill.py" <nome>`, avisa o dono em uma linha e segue pelo caminho impresso.
