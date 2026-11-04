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

1. Leia o índice/roteador mestre do hub (se existir):
   `"<CAMINHO_DO_HUB>/.agent/skills/exemplo-router/SKILL.md"`
2. Siga até a skill especialista indicada e leia só o `SKILL.md` dela.
3. Aplique o conteúdo inline. Avise o usuário em uma linha que a resposta veio
   do hub `SIP - Exemplo`, não de conhecimento genérico.

## Modo dispatch (só para construções grandes)

1. Leia a persona do agente especialista do hub (se existir, em
   `.agent/agents/`).
2. Leia a(s) skill(s) relevante(s) do hub.
3. Chame `Agent` com o conteúdo colado + a tarefa concreta.
4. Valide o resultado contra a skill de validação do hub (se existir) antes de
   aplicar.

## Modo contribuição (devolver conhecimento ao hub)

**Exceção primeiro:** se o dono do hub pediu a mudança explicitamente nesta
conversa (curadoria já feita em tempo real), edite `.agent/skills/` do hub
direto, sem inbox. Caso contrário (sessão num projeto consumidor, sem o dono
revisando aquela edição), nunca edite `.agent/skills/` do hub direto. Em vez disso:

1. Leia o formato em `"<CAMINHO_DO_HUB>/inbox/README.md"`.
2. Crie um arquivo em `inbox/` seguindo esse formato.
3. Avise o usuário que a contribuição ficou pendente de revisão.

## Se nada bater

Se a tarefa não é de exemplo, ou se o projeto atual é o próprio
`SIP - Exemplo`, não force o uso desta skill.
```
