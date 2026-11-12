# Exemplo preenchido: skill resolver de um SIP

Este arquivo mostra como os templates do `SKILL.md` principal ficam depois de
substituir os placeholders — para um SIP fictício de domínio "exemplo", hub
chamado `SIP - Exemplo`, guardado em `<CAMINHO_DO_HUB>` (substitua pelo caminho
real do seu repositório; não é o caminho de nenhum projeto real).

Resultado em `<CAMINHO_DO_HUB>/.agent/skills/sip-exemplo/SKILL.md`:

```markdown
---
name: sip-exemplo
description: Use whenever the current task involves exemplo but the active project has no local exemplo skills — i.e. any project other than SIP - Exemplo itself. Routes the task to the central exemplo knowledge hub at "SIP - Exemplo" instead of improvising from general knowledge. Also use when the user asks "existe algo de exemplo pra isso", "tem template pra isso no hub", "consulta o SIP - Exemplo", or names exemplo explicitly in a project that isn't it.
---

# sip-exemplo

## Por que isso existe

O projeto `SIP - Exemplo` (`<CAMINHO_DO_HUB>`) é a referência central de
conhecimento em exemplo. Esse conhecimento só é descoberto automaticamente
dentro do próprio hub. Em qualquer outro projeto, nada aponta para ele — sem
esta skill, a IA tende a reinventar padrões do zero. Esta skill é o ponteiro
que faz a ponte: ela mesma não ensina exemplo, ela leva até quem ensina.

## Passo 0 — acesso ao caminho

Leitura de arquivo fora do diretório de trabalho pode pedir aprovação do
usuário na primeira vez — isso é esperado. Sempre use o caminho absoluto entre
aspas: `"<CAMINHO_DO_HUB>"`.

## Passo 1 — classifique a tarefa

| Tipo de tarefa | O que fazer |
| --- | --- |
| **Consulta pontual** | **Modo consulta** — leia só os arquivos relevantes e aplique inline. |
| **Construção grande / multi-arquivo** | **Modo dispatch** — abra um subagente carregado com a persona do hub. |

## Modo consulta (padrão — prefira este)

1. Ache a linha que bate com o pedido nas tabelas abaixo (Skills, Agents,
   Workflows): elas são o roteador do hub. Se o hub tiver um roteador mestre
   para casos ambíguos, leia-o:
   `"<CAMINHO_DO_HUB>/.agent/skills/exemplo-router/SKILL.md"`
2. Leia só o arquivo do item escolhido, por caminho absoluto no hub
   (`"<CAMINHO_DO_HUB>/.agent/skills/<nome>/SKILL.md"`). Nunca symlinke nem copie
   skills especialistas do hub para o projeto.
3. Aplique o conteúdo inline. Avise o usuário em uma linha que a resposta veio
   do hub `SIP - Exemplo`, não de conhecimento genérico.

## Modo dispatch (só para construções grandes)

1. Leia a persona do agente especialista do hub (se existir, em
   `.agent/agents/`).
2. Leia a(s) skill(s) relevante(s) do hub.
3. Chame `Agent` com o conteúdo colado + a tarefa concreta.
4. Valide o resultado contra a skill de validação do hub (se existir) antes de
   aplicar.

## Skills do hub

Arquivo: `"<CAMINHO_DO_HUB>/.agent/skills/<nome>/SKILL.md"`.

<!-- skills:start (gerado por build_sip_index.py — não edite à mão) -->

Total: 3.

| Skill | Use quando |
| --- | --- |
| `exemplo-api` | Use quando a tarefa chama a API do exemplo. |
| `exemplo-router` | Use quando não está claro qual skill de exemplo serve. |
| `exemplo-validar` | Use antes de entregar algo de exemplo, para validar. |

<!-- skills:end -->

## Agents do hub

Arquivo: `"<CAMINHO_DO_HUB>/.agent/agents/<nome>.md"`. Um agent da tabela é a
persona preferida pro Modo dispatch acima: leia o `.md` inteiro (name +
description + corpo) antes de montar o subagente. Se este projeto escolheu
instalá-lo, ele também está em `.claude/agents/<nome>.md` (mesmo conteúdo).

<!-- agents:start (gerado por build_sip_index.py — não edite à mão) -->

Total: 2.

| Agent | Use quando |
| --- | --- |
| `exemplo-arquiteto` | Use para desenhar uma solução grande de exemplo. |
| `exemplo-revisor` | Use para revisar algo de exemplo antes de entregar. |

<!-- agents:end -->

## Workflows do hub

Arquivo: `"<CAMINHO_DO_HUB>/.agent/workflows/<nome>.md"`. Um workflow é um
procedimento `/nome`: se o pedido bate com uma linha da tabela, leia o `.md`
e siga o procedimento; não invente um `/comando` que não está na tabela. Se
este projeto escolheu instalá-lo, ele também aparece como `/nome` nativo.

<!-- workflows:start (gerado por build_sip_index.py — não edite à mão) -->

Total: 1.

| Workflow | Use quando |
| --- | --- |
| `/exemplo-publicar` | Publicar uma entrega de exemplo. |

<!-- workflows:end -->

## Agent ou workflow não instalado

Use-o assim mesmo, lendo pelo caminho absoluto acima. Só ofereça instalá-lo
(colando de novo o prompt de instalação e escolhendo o item) se o usuário
disser que vai usá-lo com frequência neste projeto. Não instale por conta própria.

## Modo contribuição (devolver conhecimento ao hub)

**Exceção primeiro:** se o dono do hub pediu a mudança explicitamente nesta
conversa (curadoria já feita em tempo real), edite `.agent/skills/` do hub
direto, sem inbox. Caso contrário (sessão num projeto consumidor, sem o dono
revisando aquela edição), nunca edite `.agent/skills/` do hub direto. Em vez disso:

1. Leia o formato em `"<CAMINHO_DO_HUB>/inbox/README.md"`.
2. Crie `"<CAMINHO_DO_HUB>/inbox/NNN-<assunto>.md"` (próximo número livre da pasta)
   com todas as seções do formato, escrito para quem nunca viu a conversa.
3. Avise o usuário que a contribuição ficou pendente de revisão, com o caminho do arquivo.

## Atualização

- Última atualização do hub: 2026-11-11 (o dono do hub muda esta data sempre
  que esta skill, um agent, um workflow ou a estrutura do hub mudar).
- Para atualizar a instalação num projeto (refazer links, escolher entre os
  agents/workflows novos do hub, mudar a escolha): cole de novo o prompt
  `"<CAMINHO_DO_HUB>/prompts/instalar-skill-sip-exemplo.md"` numa sessão daquele projeto.
- A data em que **cada projeto** instalou ou atualizou fica no
  `.agent/SIPS-CONSUMIDOS.md` dele. Se for anterior à data acima, ofereça
  rodar o prompt.

## Se nada bater

Se a tarefa não é de exemplo, ou se o projeto atual é o próprio
`SIP - Exemplo`, não force o uso desta skill.
```
