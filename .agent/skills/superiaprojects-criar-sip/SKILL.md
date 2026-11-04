---
name: superiaprojects-criar-sip
description: Use quando o usuário quiser transformar um projeto/repositório em um "SIP" (Super IA Projects) — um repositório central de Skills, Agents, Workflows e Conhecimento de um domínio que outros projetos possam consultar, quase como um agente especializado daquele domínio. Dispara em pedidos como "cria um SIP de marketing", "transforma esse repo num hub de X", "quero um repositório central pra Y como fizemos com o n8n", ou quando o usuário referencia o `SIP - N8N` como modelo a replicar para um novo domínio. Faz o scaffolding da skill resolver (`sip-<dominio>`), do prompt de instalação, do inbox de contribuições e do registro na ficha do projeto — não cria o conhecimento de domínio em si (isso é trabalho de skills/agents específicos, feitos depois).
---

# Criar um SIP (Super IA Projects) — hub de conhecimento de domínio

## O que é um SIP

Um "SIP" é um projeto/repositório cujo papel não é entregar um produto, e sim
**centralizar conhecimento de um domínio** (skills, agents, workflows, docs) para
que outros projetos consultem sob demanda, em vez de cada projeto reinventar ou
duplicar esse conhecimento: skills especialistas em `.agent/skills/`, agent(s)
dedicados, um catálogo de exemplos reais, e — o que esta skill generaliza — uma
camada de acesso cross-project (skill resolver `sip-<dominio>` + prompt de
instalação + `inbox/` de contribuição). Veja `references/` nesta própria skill
para um exemplo completo e preenchido desse padrão.

Esta skill só constrói **essa camada de acesso**. O conhecimento de domínio em si
(as skills especialistas, os agents, os workflows/exemplos) é construído depois,
separadamente — use `project-initializer` para inicializar o projeto do zero, se
ainda não existir, e `writing-skills` para criar as skills de domínio.

## Convenção de nomes (fixa)

- Nome de exibição do hub: `SIP - <Domínio>` (ex: `SIP - N8N`, `SIP - Marketing`).
- Skill resolver instalada em outros projetos: `sip-<dominio>` — sempre
  kebab-case, minúsculo, sem espaços (ex: `sip-n8n`, `sip-marketing`). Não repita
  o erro de nomear com espaços (`SIP - N8N` como nome de skill já foi tentado e
  revertido neste próprio processo por causar fricção em invocação/scripts).
- Caminho do resolver dentro do hub: `<hub>/.agent/skills/sip-<dominio>/SKILL.md`,
  symlink em `<hub>/.claude/skills/sip-<dominio>`.
- Prompt de instalação: `<hub>/prompts/instalar-skill-sip-<dominio>.md`.
- Inbox de contribuição: `<hub>/inbox/README.md`.

## Passo 0 — perguntas antes de gerar qualquer coisa

Não assuma; confirme com o usuário (ou responda com o que já foi dito na
conversa, se for óbvio):

1. **Domínio** (em uma palavra/kebab-case): define `<dominio>` em `sip-<dominio>`.
2. **Repositório**: já existe (caminho absoluto) ou precisa ser criado do zero?
   Se for do zero, isso é trabalho do `project-initializer`, não desta skill —
   rode-o primeiro e volte aqui só para a camada de acesso.
3. **Nome de exibição**: confirme `SIP - <Domínio>` ou se o usuário quer outro
   título (mantenha `sip-<dominio>` como nome da skill independente do título).

## Passo 1 — mostre o plano antes de escrever

Antes de criar qualquer arquivo, liste pro usuário exatamente o que vai ser
gerado (caminhos completos) e espere confirmação — isto cria vários arquivos
num repositório, às vezes um que não é o diretório de trabalho atual:

```
Vou criar em <hub>:
1. .agent/skills/sip-<dominio>/SKILL.md
2. .claude/skills/sip-<dominio> (symlink)
3. prompts/instalar-skill-sip-<dominio>.md
4. inbox/README.md
5. Atualizar a ficha do projeto em 0 Padrões/projetos/<Nome>.md (se existir)
Confirma?
```

## Passo 2 — templates (substituir os placeholders)

Placeholders: `{{DOMINIO}}` (kebab-case, ex: `marketing`), `{{HUB_NOME}}` (ex:
`SIP - Marketing`), `{{HUB_PATH}}` (caminho absoluto do repositório),
`{{SKILL}}` = `sip-{{DOMINIO}}`, `{{ROUTER}}` = nome da skill roteadora de
domínio dentro do hub, se já existir (ex: `n8n-router`; se o hub ainda não tem
um roteador mestre, adapte a seção 1 do modo consulta para apontar direto pro
índice de skills do hub).

### `.agent/skills/{{SKILL}}/SKILL.md`

```markdown
---
name: {{SKILL}}
description: Use whenever the current task involves {{DOMINIO}} but the active project has no local {{DOMINIO}} skills — i.e. any project other than {{HUB_NOME}} itself. Routes the task to the central {{DOMINIO}} knowledge hub at "{{HUB_NOME}}" instead of improvising from general knowledge. Also use when the user asks "existe algo de {{DOMINIO}} pra isso", "tem template pra isso no hub", "consulta o {{HUB_NOME}}", or names {{DOMINIO}} explicitly in a project that isn't it.
---

# {{SKILL}}

## Por que isso existe

O projeto `{{HUB_NOME}}` (`{{HUB_PATH}}`) é a referência central de
conhecimento em {{DOMINIO}}. Esse conhecimento só é descoberto automaticamente
dentro do próprio hub. Em qualquer outro projeto, nada aponta para ele — sem
esta skill, a IA tende a reinventar padrões do zero. Esta skill é o ponteiro
que faz a ponte: ela mesma não ensina {{DOMINIO}}, ela leva até quem ensina.

## Passo 0 — acesso ao caminho

Leitura de arquivo fora do diretório de trabalho pode pedir aprovação do
usuário na primeira vez — isso é esperado. Sempre use o caminho absoluto entre
aspas: `"{{HUB_PATH}}"`.

## Passo 1 — classifique a tarefa

| Tipo de tarefa | O que fazer |
| --- | --- |
| **Consulta pontual** | **Modo consulta** — leia só os arquivos relevantes e aplique inline. |
| **Construção grande / multi-arquivo** | **Modo dispatch** — abra um subagente carregado com a persona do hub. |

## Modo consulta (padrão — prefira este)

1. Leia o índice/roteador mestre do hub (se existir):
   `"{{HUB_PATH}}/.agent/skills/{{ROUTER}}/SKILL.md"`
2. Siga até a skill especialista indicada e leia só o `SKILL.md` dela.
3. Aplique o conteúdo inline. Avise o usuário em uma linha que a resposta veio
   do hub `{{HUB_NOME}}`, não de conhecimento genérico.

## Modo dispatch (só para construções grandes)

Não existe invocação nativa de agente cross-projeto no Claude Code. "Disparar"
o agente do hub é montar um subagente genérico (`Agent`,
`subagent_type: "general-purpose"`) com a persona do hub colada no prompt:

1. Leia a persona do agente especialista do hub (se existir, em
   `.agent/agents/`).
2. Leia a(s) skill(s) relevante(s) do hub.
3. Chame `Agent` com o conteúdo colado + a tarefa concreta.
4. Valide o resultado contra a skill de validação do hub (se existir) antes de
   aplicar.

## Modo contribuição (devolver conhecimento ao hub)

**Exceção primeiro — edição direta quando o dono já revisou:** se o próprio usuário
dono do hub pediu explicitamente a mudança nesta conversa (ele indicou o hub como
destino, revisou a decisão antes de qualquer arquivo ser escrito), a curadoria já
aconteceu em tempo real — edite `.agent/skills/`/`workflows/`/etc. do hub direto,
sem passar pelo inbox. O fluxo de inbox abaixo é para o caso contrário: uma sessão
rodando num projeto consumidor, só com o symlink do resolver instalado, sem o dono
do hub revisando aquela edição específica.

Nesse segundo caso, nunca edite `.agent/skills/` ou equivalentes do hub direto —
são compartilhados por symlink com todo projeto que instalou esta skill; uma
edição sem curadoria propagaria pra todo mundo instantaneamente. Em vez disso:

1. Leia o formato em `"{{HUB_PATH}}/inbox/README.md"`.
2. Crie um arquivo em `inbox/` seguindo esse formato.
3. Avise o usuário que a contribuição ficou pendente de revisão.

## Se nada bater

Se a tarefa não é de {{DOMINIO}}, ou se o projeto atual é o próprio
`{{HUB_NOME}}`, não force o uso desta skill.
```

### `prompts/instalar-skill-{{SKILL}}.md`

```markdown
# Prompt: Instalar/Atualizar a skill "{{SKILL}}" em outro projeto

Cole isto numa sessão do Claude Code dentro do projeto que precisa consultar o
hub central de {{DOMINIO}} ({{HUB_NOME}}):

\`\`\`
Instale/atualize a skill de conhecimento {{DOMINIO}} do hub central {{HUB_NOME}} neste projeto:
1. Crie a pasta .claude/skills/ se ela não existir.
2. Crie (ou recrie, se já existir e estiver desatualizado/quebrado) um symlink:
   .claude/skills/{{SKILL}} -> "{{HUB_PATH}}/.agent/skills/{{SKILL}}"
3. Confirme com `ls -la` que o symlink aponta para esse caminho e que o SKILL.md é legível através dele.
4. Não copie o conteúdo do SKILL.md para este projeto — mantenha como symlink, para
   herdar atualizações futuras do hub automaticamente.
\`\`\`

## Por que symlink e não cópia

A fonte de verdade da skill fica em `{{HUB_PATH}}/.agent/skills/{{SKILL}}/SKILL.md`.
Symlink garante que atualizações futuras nesse arquivo já reflitam em todos os
projetos que instalaram, sem rodar este prompt de novo — exceto se o symlink
quebrar (hub movido/renomeado), caso em que basta colar o prompt outra vez.

## Via de volta: contribuir com o hub

A skill instalada também sabe devolver conhecimento ao hub — nunca edita os
arquivos compartilhados direto, só deixa um arquivo em `{{HUB_PATH}}/inbox/`
para revisão manual. Ver `inbox/README.md` no hub para o formato esperado.
```

### `inbox/README.md`

```markdown
# Inbox — contribuições de outros projetos

Porta de entrada para qualquer projeto que, usando a skill `{{SKILL}}`, tenha
aprendido algo sobre {{DOMINIO}} e queira devolver ao hub: um insight, um
exemplo novo, ou uma melhoria numa skill existente.

**Ninguém edita `.agent/skills/` (ou pastas de exemplos/workflows) direto a
partir de outro projeto.** O conteúdo cai aqui primeiro e é promovido
manualmente para o lugar certo durante uma revisão periódica do hub.

## Como contribuir

1. Crie um arquivo nesta pasta: `AAAA-MM-DD_<projeto>_<assunto-curto>.md`.
2. Formato:
   \`\`\`markdown
   ## Tipo
   insight | exemplo-novo | melhoria-de-skill

   ## Projeto de origem
   <nome do projeto>

   ## Contexto
   O que estava sendo feito, qual problema apareceu.

   ## Proposta
   O insight ou conteúdo sugerido.

   ## Onde provavelmente se aplica
   <skill ou pasta do hub>
   \`\`\`
3. Não edite nada fora desta pasta.

## Revisão (lado do hub)

Periodicamente, revisar os arquivos aqui, promover os que fizerem sentido, e
apagar o arquivo do inbox depois de integrado.
```

## Passo 3 — executar

1. Crie os 4 arquivos acima com os placeholders substituídos.
2. Crie o symlink (`ln -s "<hub>/.agent/skills/{{SKILL}}" "<hub>/.claude/skills/{{SKILL}}"`)
   ou, se o hub já usa `sync_entrypoints.py` (convenção Antigravity Kit), rode-o
   de dentro do hub em vez de criar o symlink manualmente.
3. Se o hub tiver uma ficha em `0 Padrões/projetos/<Nome>.md`, adicione: a linha
   da skill na tabela de skills, uma seção "Acesso Cross-Project" apontando pro
   prompt e pro inbox, e uma linha no histórico de decisões.
4. **Nunca** crie a skill resolver dentro de `0 Padrões` — ela é sempre
   co-localizada no próprio hub (`<hub>/.agent/skills/sip-<dominio>/`). Um
   resolver guardado fora do hub diverge do roteador de domínio com o tempo,
   porque ninguém o atualiza junto. `generate_catalog.py` do `0 Padrões` só
   precisa ser rodado se esta própria skill meta (`superiaprojects-criar-sip`)
   for alterada, não a cada SIP criado.

## Referência

Veja a pasta `references/` desta skill para um exemplo completo e preenchido
de cada arquivo gerado (com caminho mascarado, só para ilustrar a forma):
`skill-resolver-exemplo.md`, `prompt-instalacao-exemplo.md`,
`inbox-readme-exemplo.md`.
