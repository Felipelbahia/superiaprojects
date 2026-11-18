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
- Caminho do resolver dentro do hub: `<hub>/prompts/resolver/sip-<dominio>/SKILL.md`
  (pasta real e versionada, ao lado do prompt de instalação). **Nunca** em
  `<hub>/.agent/skills/` nem em `<hub>/.claude/skills/`: o resolver aponta para o
  próprio hub, então dentro dele seria só ruído (conta como skill do hub e pode
  disparar onde não serve). Ao lado dele: `verticais.json` (a que vertical cada
  item pertence) e `verticais/<vertical>.md` (gerados, ver Passo 3).
  Hubs antigos ainda têm o resolver em `<hub>/.agent/skills/sip-<dominio>`; os
  scripts do kit leem os dois layouts (o novo vence), então um SIP novo já nasce
  no layout novo e os antigos migram quando o dono quiser.
- Prompt de instalação: `<hub>/prompts/instalar-skill-sip-<dominio>.md`.
- Inbox de contribuição: `<hub>/inbox/README.md` (formato) + um arquivo por
  contribuição, `<hub>/inbox/NNN-<assunto>.md`, no padrão de inbox do kit;
  resolvidos vão para `<hub>/inbox/arquivo/`.
- Registro de instalações (consumidores): `<hub>/instalacoes/README.md` +
  um arquivo por projeto consumidor, `<hub>/instalacoes/<nome-do-projeto>.md`.
- **`inbox/` e `instalacoes/` sempre entram no `.gitignore` do próprio hub**
  (não no do 0 Padrões), com exceção dos dois `README.md`, que dizem o formato
  e precisam existir em qualquer clone:
  ```gitignore
  # Conteúdo local do hub: contribuições pendentes e registro de consumidores
  # (caminhos absolutos de outros projetos; não é conhecimento de domínio)
  inbox/*
  !inbox/README.md
  instalacoes/*
  !instalacoes/README.md
  ```

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

```text
Vou criar em <hub>:
1. prompts/resolver/sip-<dominio>/SKILL.md (resolver enxuto, com o índice de verticais gerado)
2. prompts/resolver/sip-<dominio>/verticais.json e verticais/*.md (gerados)
3. prompts/instalar-skill-sip-<dominio>.md
4. inbox/README.md
5. instalacoes/README.md
5b. .gitignore do hub: inbox/* e instalacoes/* (menos os dois README.md)
6. Atualizar a ficha do projeto em 0 Padrões/projetos/<Nome>.md (se existir)

E em 0 Padrões:
7. Stub global em .agent/skills/sip-<dominio>/SKILL.md
8. Symlink .claude/skills/sip-<dominio> -> hub (0 Padrões como consumidor, sempre; agents/workflows: pergunto nenhum / todos / quais)
9. Entrada(s) no .gitignore do 0 Padrões pra cada symlink novo do passo 8
10. Registro em <hub>/instalacoes/0-padroes.md
    (o registro é o que o `propagar_sip.py` lê para achar os consumidores; todo prompt de instalação precisa gravá-lo)
11. 0 Padrões/.agent/SIPS-CONSUMIDOS.md (manifesto local, novo ou atualizado)
Confirma?
```

**Um SIP nunca é só skills, e o consumidor só recebe o que escolher.** Um hub
pode ter 3 tipos de recurso: skills (`.agent/skills/`), agents
(`.agent/agents/`) e workflows (`.agent/workflows/`). O padrão é um só:

| Recurso | No resolver `sip-<dominio>` | No projeto consumidor |
| --- | --- | --- |
| Resolver | — | **sempre** instalado (symlink duplo) |
| Skills especialistas | arquivo da vertical (gerado) | **nunca** symlinkadas: lidas por caminho absoluto |
| Agents | arquivo da vertical (gerado) | **só os escolhidos** pelo usuário na instalação (nenhum, todos ou quais) |
| Workflows | arquivo da vertical (gerado) | **só os escolhidos** pelo usuário na instalação (nenhum, todos ou quais) |

**Dois níveis, para o resolver não crescer com o hub:** o `SKILL.md` do resolver
fica pequeno (passos, modos e uma tabela de verticais, ~100 linhas) e a IA só
abre o arquivo da vertical que a tarefa pede. O consumidor carrega o resolver
inteiro em toda tarefa; uma lista única com uma linha por skill, agent e
workflow pesa mais que a maioria das skills que ela aponta.

O índice e os arquivos de vertical são gerados do frontmatter (`description`)
pelo script do kit
`"/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/scripts/build_sip_index.py"`
(ver Passo 3). Um agent ou workflow não instalado continua usável: a IA o acha
no arquivo da vertical e lê o `.md` no hub por caminho absoluto. Instalar só
serve para quem quer o agent/`/comando` nativo na lista do projeto.

## Passo 2 — templates (substituir os placeholders)

Placeholders: `{{DOMINIO}}` (kebab-case, ex: `marketing`), `{{HUB_NOME}}` (ex:
`SIP - Marketing`), `{{HUB_PATH}}` (caminho absoluto do repositório),
`{{SKILL}}` = `sip-{{DOMINIO}}`, `{{ROUTER}}` = nome da skill roteadora de
domínio dentro do hub, se já existir (ex: `n8n-router`; opcional — as tabelas
geradas do resolver já são o roteador; se o hub não tem roteador mestre, tire
do modo consulta a frase que o cita).

### `prompts/resolver/{{SKILL}}/SKILL.md`

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

1. Ache a vertical na tabela do índice abaixo pela coluna "Use quando". Se o hub
   tiver um roteador mestre para casos ambíguos, leia-o:
   `"{{HUB_PATH}}/.agent/skills/{{ROUTER}}/SKILL.md"`
2. Leia só o arquivo da vertical:
   `"{{HUB_PATH}}/prompts/resolver/{{SKILL}}/verticais/<vertical>.md"`. Ali estão as
   skills, agents e workflows daquela área, cada um com o seu "Use quando". Sem
   certeza da vertical: `grep -ril "<palavra>" "{{HUB_PATH}}/prompts/resolver/{{SKILL}}/verticais/"`.
3. Leia só o arquivo do item escolhido, por caminho absoluto no hub
   (`"{{HUB_PATH}}/.agent/skills/<nome>/SKILL.md"`). Nunca symlinke nem copie
   skills especialistas do hub para o projeto.
4. Aplique o conteúdo inline. Avise o usuário em uma linha que a resposta veio
   do hub `{{HUB_NOME}}`, não de conhecimento genérico.

## Modo dispatch (só para construções grandes)

Não existe invocação nativa de agente cross-projeto no Claude Code. "Disparar"
o agente do hub é montar um subagente genérico (`Agent`,
`subagent_type: "general-purpose"`) com a persona do hub colada no prompt:

1. Leia a persona do agente especialista (seção Agents do arquivo da vertical,
   `"{{HUB_PATH}}/.agent/agents/<nome>.md"`) inteira (name + description + corpo).
2. Leia a(s) skill(s) relevante(s) do hub.
3. Chame `Agent` com o conteúdo colado + a tarefa concreta.
4. Valide o resultado contra a skill de validação do hub (se existir) antes de
   aplicar.

## Índice de verticais

Um arquivo por vertical em `"{{HUB_PATH}}/prompts/resolver/{{SKILL}}/verticais/"`,
com as skills (`.agent/skills/<nome>/SKILL.md`), agents (`.agent/agents/<nome>.md`)
e workflows (`.agent/workflows/<nome>.md`) da área. Um workflow é um
procedimento `/nome`: se o pedido bate com ele, leia o `.md` e siga; não invente
um `/comando` que não está no arquivo da vertical. Se este projeto escolheu
instalar um agent ou workflow, ele também aparece nativo.

<!-- indice:start dir=verticais (gerado por build_sip_index.py — não edite à mão) -->
<!-- indice:end -->

## Agent ou workflow não instalado

Use-o assim mesmo, lendo pelo caminho absoluto acima. Só ofereça instalá-lo
(colando de novo o prompt de instalação e escolhendo o item) se o usuário
disser que vai usá-lo com frequência neste projeto. Não instale por conta própria.

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
2. Crie `"{{HUB_PATH}}/inbox/NNN-<assunto>.md"` (próximo número livre da pasta)
   com todas as seções do formato, escrito para quem nunca viu a conversa.
3. Avise o usuário que a contribuição ficou pendente de revisão, com o caminho do arquivo.

## Atualização

- Última atualização do hub: AAAA-MM-DD (o dono do hub muda esta data sempre
  que esta skill, um agent, um workflow ou a estrutura do hub mudar).
- Para atualizar a instalação num projeto (refazer links, escolher entre os
  agents/workflows novos do hub, mudar a escolha): cole de novo o prompt
  `"{{HUB_PATH}}/prompts/instalar-skill-{{SKILL}}.md"` numa sessão daquele projeto.
- A data em que **cada projeto** instalou ou atualizou fica no
  `.agent/SIPS-CONSUMIDOS.md` dele. Se for anterior à data acima, ofereça
  rodar o prompt.
- **Propagar para todos os consumidores (dono do hub):** depois de mudar este
  hub, rode o comando abaixo (simulação por padrão; `--apply` grava). Ele lê
  `"{{HUB_PATH}}/instalacoes/"`, refaz links quebrados, atualiza a data do
  manifesto de cada projeto e o registro em `instalacoes/` (pulado no projeto com conflito) e deixa agents/workflows novos como nota na
  `inbox/` do projeto (nunca instala sozinho). Se o dono pedir "propaga" /
  "atualiza todos os consumidores" estando neste hub, é este comando:
  `python3 "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/scripts/propagar_sip.py" "{{HUB_PATH}}"`
  (acrescente `--apply` depois de ver a simulação, e `--scan "<pasta dos projetos>"`
  para achar consumidores que não estão registrados).

## Se nada bater

Se a tarefa não é de {{DOMINIO}}, ou se o projeto atual é o próprio
`{{HUB_NOME}}`, não force o uso desta skill.
```

### `prompts/resolver/{{SKILL}}/verticais.json`

```json
{
  "padrao": "outros",
  "verticais": [
    {"nome": "<vertical>", "quando": "<uma frase: quando abrir esta vertical>", "match": ["<prefixo>-*"]},
    {"nome": "outros", "quando": "O que não coube nas outras verticais.", "match": []}
  ]
}
```

Regras: cada item do hub (skill, agent ou workflow) entra na **primeira** vertical
cujo `match` (padrões `fnmatch` sobre o nome) servir; o que não servir em nenhuma
vai para a `padrao`. Sem `padrao`, item sem vertical faz o gerador falhar. Hub com
prefixos regulares (`seo-*`, `copy-*`) usa um padrão por vertical; hub com nomes
soltos usa listas de padrões por tema e ordena as verticais da mais específica
para a mais geral. Toda vertical precisa de `quando`.

### `prompts/instalar-skill-{{SKILL}}.md`

```markdown
# Prompt: Instalar/Atualizar o acesso ao hub "{{HUB_NOME}}" em outro projeto

Cole isto numa sessão do Claude Code dentro do projeto que precisa consultar o
hub central de {{DOMINIO}} ({{HUB_NOME}}). Instala sempre o resolver e, dos
agents e workflows do hub, só os que você escolher (o prompt mostra as tabelas e pergunta):

\`\`\`
Instale/atualize o acesso ao hub central {{HUB_NOME}} ({{DOMINIO}}) neste projeto.
O que entra: o resolver {{SKILL}} sempre; agents e workflows do hub só os que eu
escolher; skills especialistas do hub nunca (o resolver as acha pela tabela e
as lê por caminho absoluto).
Padrão duplo: cada recurso instalado ganha um symlink absoluto em .agent/ (pro
hub) e um symlink relativo em .claude/ (pro symlink local em .agent/) — isso dá
acesso tanto ao Claude Code quanto a Google Antigravity/Gemini/Cursor, que leem
.agent/ direto e não dependem do stub global do 0 Padrões.

REGRA PARA TODO SYMLINK DESTE PROMPT: crie sempre com `ln -sfn <destino> <link>` (nunca
só com `-s`). `-f` recria um link velho/quebrado; `-n` impede que, se <link> já for um
symlink para uma pasta, o novo link seja criado DENTRO dessa pasta (poluiria o hub).
Antes de criar, confira <link> com `test -L` e `readlink`:
- não existe, ou é symlink: pode (re)criar;
- é arquivo ou pasta REAL (não symlink): NÃO rode `ln` (o `-f` apagaria o arquivo).
  Pare só aquele item e me pergunte, caso a caso: (a) renomear o meu arquivo
  (eu digo o novo nome; lembre que o `name:` do frontmatter dele também muda) e
  depois instalar o do hub; (b) substituir: mova o meu arquivo para
  `<link>.bak-AAAA-MM-DD` (nunca apague) e depois instale; (c) pular: não instale.
  Sem resposta = (c). Registre o desfecho na linha "Conflitos" do manifesto
  (passo 10); um item pulado entra em "Vistos no hub" e não em "Agents"/"Workflows",
  e só volta a ser oferecido se eu pedir para mudar a escolha.
REGRA PARA TODA REMOÇÃO DESTE PROMPT: só remova um <link> que seja symlink (`test -L`)
E cujo destino aponte para dentro de "{{HUB_PATH}}". Leia o destino com `readlink`
SEM `-f` (com `-f`, um link quebrado sai com erro no macOS): link de .agent/ tem o
caminho absoluto do hub; link relativo de .claude/ ou .cursor/ aponta para o link de
.agent/ de mesmo nome, então confira esse. Nunca remova arquivo ou pasta real.

1. Skill resolver (obrigatório):
   - Crie a pasta .agent/skills/ se ela não existir.
   - Crie (ou recrie) o symlink absoluto com `ln -sfn`:
     .agent/skills/{{SKILL}} -> "{{HUB_PATH}}/prompts/resolver/{{SKILL}}"
   - Crie a pasta .claude/skills/ se ela não existir.
   - Crie o symlink relativo com `ln -sfn` (pro symlink acima, não direto pro hub):
     .claude/skills/{{SKILL}} -> ../../.agent/skills/{{SKILL}}

2. Migração (instalações antigas): remova, seguindo a regra de remoção, todo
   symlink em .agent/skills/ e .claude/skills/ que aponte para uma skill
   especialista do hub (qualquer uma que não seja {{SKILL}}), e a entrada dele
   no .gitignore. Skills especialistas não são mais instaladas.

3. Escolha de agents e workflows:
   - Leia as seções "Agents" e "Workflows" de cada arquivo de
     "{{HUB_PATH}}/prompts/resolver/{{SKILL}}/verticais/" (nome + "use quando").
   - Leia a entrada deste hub em .agent/SIPS-CONSUMIDOS.md, se existir:
     "Agents"/"Workflows" (escolhidos) e "Vistos no hub" (oferecidos antes).
   - Primeira instalação (sem entrada): mostre as duas tabelas e pergunte
     "Quais instalar? nenhum / todos / lista de nomes". Sem resposta = nenhum.
   - Instalação antiga sem entrada no manifesto, mas com symlinks deste hub já
     em .agent/agents/, .claude/agents/, .agent/workflows/ ou .claude/commands/:
     mostre as tabelas com esses itens já marcados e pergunte "manter esta
     escolha, mudar, ou nenhum?". Sem resposta = manter (nunca remova sem resposta).
   - Reinstalação: mantenha a escolha anterior sem perguntar de novo. Pergunte
     só sobre os itens das tabelas que NÃO estão em "Vistos no hub" (os novos).
     Sem resposta = os novos ficam de fora. Se eu pedir para mudar a escolha,
     mostre as tabelas inteiras com a escolha atual marcada.
   - Tabelas vazias: pule este passo e os passos 4 e 5 sem erro.

4. Instale só o escolhido (seguindo a regra de symlink acima):
   - Cada agent <nome>: .agent/agents/<nome>.md -> "{{HUB_PATH}}/.agent/agents/<nome>.md"
     (absoluto) e .claude/agents/<nome>.md -> ../../.agent/agents/<nome>.md (relativo).
   - Cada workflow <nome>: .agent/workflows/<nome>.md -> "{{HUB_PATH}}/.agent/workflows/<nome>.md"
     (absoluto), e .claude/commands/<nome>.md e .cursor/commands/<nome>.md ->
     ../../.agent/workflows/<nome>.md (relativos).
   - Crie as pastas que faltarem.

5. Remova o que saiu da escolha (seguindo a regra de remoção): symlinks de
   agents/workflows deste hub que não estão mais escolhidos, ou cujo arquivo
   sumiu do hub (link quebrado), e as entradas deles no .gitignore.

6. Confirme com `ls -la` cada symlink criado (os de .agent/ E os de .claude/)
   e que o .md correspondente é legível através de cada um. Depois, na raiz
   deste projeto, rode
   `python3 "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/scripts/sync_entrypoints.py" --check`:
   tem de sair com 0. Se acusar erro de link ou skill do hub, pare e relate
   (não apague links para "limpar" o aviso).
7. Não copie conteúdo de nenhum desses arquivos para este projeto — mantenha
   tudo como symlink, para herdar atualizações futuras do hub automaticamente.
8. Adicione ao .gitignore deste projeto (crie a seção se não existir) uma linha
   por symlink instalado, nunca um curinga do prefixo do domínio:
   .agent/skills/{{SKILL}}
   .claude/skills/{{SKILL}}
   (e, para cada agent/workflow instalado no passo 4, os caminhos
   .agent/agents/<nome>.md, .claude/agents/<nome>.md,
   .agent/workflows/<nome>.md, .claude/commands/<nome>.md,
   .cursor/commands/<nome>.md correspondentes)
   — são symlinks com path absoluto desta máquina, não portáveis entre clones.
9. Registre esta instalação no hub (bookkeeping, não é conteúdo de domínio —
   pode escrever direto, sem passar pelo inbox):
   - Veja o formato em "{{HUB_PATH}}/instalacoes/README.md".
   - Crie ou atualize "{{HUB_PATH}}/instalacoes/<nome-deste-projeto>.md" com:
     nome e caminho absoluto deste projeto, data de hoje, e os recursos
     instalados (skill sempre; agents/workflows escolhidos, ou "nenhum").
10. Atualize o manifesto local deste projeto, `.agent/SIPS-CONSUMIDOS.md`
   (crie se não existir — contrapartida local do registro do passo 9: lá o
   hub sabe quem consome; aqui o projeto sabe o que consome, sem precisar
   abrir .gitignore ou seguir symlink pra descobrir):
   - Formato de cada entrada (uma por SIP instalado neste projeto):
     \`\`\`markdown
     ## {{HUB_NOME}} (\`{{SKILL}}\`)
     - Hub: {{HUB_PATH}}
     - Instalado/atualizado em: AAAA-MM-DD
     - Skill: {{SKILL}}
     - Agents: <escolhidos, ou "nenhum">
     - Workflows: <escolhidos, ou "nenhum">
     - Vistos no hub: agents <todos os nomes da tabela hoje>; workflows <idem>
     - Conflitos: <"nome: pulado" | "nome: meu arquivo renomeado para <novo>" | "nome: substituído (meu em <link>.bak-AAAA-MM-DD)", ou "nenhum">
     - Para atualizar: cole de novo "{{HUB_PATH}}/prompts/instalar-skill-{{SKILL}}.md"
     \`\`\`
   - "Vistos no hub" é o que permite, na próxima vez, perguntar só os novos.
   - Se o arquivo já tiver uma entrada pra este hub (de uma instalação
     anterior), substitua-a em vez de duplicar.
\`\`\`

## Por que o padrão duplo (symlink de symlink) e não um só

A fonte de verdade de cada recurso fica no hub (`{{HUB_PATH}}/.agent/skills/`,
`.agent/agents/`, `.agent/workflows/`). O symlink absoluto em `.agent/` deste
projeto aponta direto pro hub; o symlink relativo em `.claude/` aponta pro
symlink local em `.agent/`, não direto pro hub. Essa cadeia de dois symlinks
(em vez de um só direto em `.claude/`) existe porque **Claude Code e as
outras IAs leem pastas diferentes**: Claude Code só descobre
`.claude/skills/`/`.claude/agents/`/`.claude/commands/`; Google
Antigravity/Gemini/Cursor só leem `.agent/skills/`/`.agent/agents/`/
`.agent/workflows/` direto (via Regra 4, 1ª prioridade: skills locais do
próprio projeto). Um symlink só em `.claude/` (direto pro hub) atende só o
Claude Code — pra essas outras IAs acharem o recurso neste projeto
específico, ele precisa também existir em `.agent/`. Atualizações futuras no
hub já refletem aqui automaticamente nos dois — exceto se um symlink quebrar
(hub movido ou arquivo renomeado), caso em que basta colar o prompt outra
vez, ou se o hub adicionar um agent/workflow novo depois da instalação, caso
em que rodar o prompt de novo pergunta só sobre os novos (a escolha anterior
fica registrada em `.agent/SIPS-CONSUMIDOS.md`, linha "Vistos no hub").

## Para outras IAs (Google Antigravity / Gemini / Cursor)

Com o padrão duplo acima, essas IAs já encontram o resolver e os
agents/workflows escolhidos **direto neste projeto** (via `.agent/skills/`,
`.agent/agents/`, `.agent/workflows/`), sem depender do stub global do
`0 Padrões` nem da Regra 4 (Fallback Resolution Protocol) — a 1ª prioridade
da Regra 4 já é "skills locais do próprio projeto", que é exatamente o que
os passos 1 e 4 criaram aqui. O que não foi escolhido elas acham pelas
verticais do resolver e leem por caminho absoluto no hub. O stub global do `0 Padrões` continua existindo como rede de
segurança pra projetos que *não* instalaram (2ª prioridade da Regra 4), mas
quem instalou via este prompt não depende dele.

## Via de volta: contribuir com o hub

A skill instalada também sabe devolver conhecimento ao hub — nunca edita os
arquivos compartilhados direto, só deixa um arquivo em `{{HUB_PATH}}/inbox/`
para revisão manual. Ver `inbox/README.md` no hub para o formato esperado.

## Registro desta instalação no hub

Este prompt também registra quem instalou, em `{{HUB_PATH}}/instalacoes/`
(ver `instalacoes/README.md` no hub) — isto não é conteúdo de domínio, é
bookkeeping de quem consome o hub, então pode ser escrito direto, sem passar
pelo inbox. Serve pro dono do hub saber, quando mudar algo, quais projetos
revisar ou avisar — sem esse registro, ele teria que adivinhar ou perguntar
projeto por projeto.

## Manifesto local neste projeto

Este prompt também atualiza `.agent/SIPS-CONSUMIDOS.md` **neste projeto**
(contrapartida local do registro acima: lá o hub sabe quem o consome; aqui
o projeto sabe o que consome). Sem esse manifesto, a única forma de saber
que este projeto depende de um SIP é abrir o `.gitignore` ou seguir cada
symlink manualmente — o manifesto deixa isso visível de cara, num lugar só,
pra qualquer pessoa ou IA que abrir o projeto.
```

### `inbox/README.md`

```markdown
# Inbox — contribuições de outros projetos

Porta de entrada para qualquer projeto que, usando a skill `{{SKILL}}`, tenha
aprendido algo sobre {{DOMINIO}} e queira devolver ao hub: um insight, um
exemplo novo, ou uma melhoria numa skill existente.

**Ninguém edita `.agent/skills/` (ou pastas de exemplos/workflows) direto a
partir de outro projeto.** O conteúdo cai aqui primeiro e é promovido
manualmente para o lugar certo durante uma revisão do hub. Os itens desta pasta
ficam fora do git do hub (só este README é versionado).

## Como contribuir

1. Crie `inbox/NNN-<assunto-curto>.md`, com `NNN` = próximo número livre desta
   pasta (contando `arquivo/`). Duas sessões podem usar o mesmo número ao mesmo
   tempo: tudo bem, o assunto diferencia. Nunca renumere arquivos existentes.
2. Escreva para uma IA que nunca viu a sua conversa: caminhos absolutos,
   frases literais como âncora (números de linha mudam), evidência.
3. Formato:
   \`\`\`markdown
   # NNN — <título>
   Status: na inbox · Aberto em: AAAA-MM-DD · Pedido por: <quem> · Projeto de origem: <nome e caminho>

   ## O quê
   ## Como (o que fazer quando for pedido)
   ## Onde (arquivos, skills, pastas do hub)
   ## Por quê (o que depende disto; evidência)
   ## Para quê (critério de sucesso)
   ## Quem (decide / aplica / afetados)
   ## Efeitos e impactos (o que muda, o que acontece se nada for feito)
   ## Exemplos
   ## Gatilho para sair da inbox
   ## Enquanto isso
   \`\`\`
4. Não edite nada fora desta pasta.

## Revisão (lado do hub)

Itens da inbox não são analisados até o dono do hub pedir. Ao resolver um item:
mude o `Status` para `feito em AAAA-MM-DD` com o link do que resolveu e **mova o
arquivo para `inbox/arquivo/`**. Nunca apague. Se o item não for aplicado, o mesmo:
`Status: descartado em AAAA-MM-DD` com o motivo, e mova.
```

### `instalacoes/README.md`

```markdown
# Instalações — quem consome este hub

Registro de todo projeto que instalou acesso a este hub (skill `{{SKILL}}` e
os agents/workflows que o projeto escolheu, se algum) via
`prompts/instalar-skill-{{SKILL}}.md`. Diferente do `inbox/`: isto não é
conteúdo pendente de revisão, é só bookkeeping — por isso o prompt de
instalação escreve aqui direto, sem curadoria.

**Por que existe:** quando algo muda neste hub (a skill resolver, um agent,
um workflow, ou a própria estrutura), esta pasta é como o dono do hub sabe
quais projetos consomem o quê, sem ter que perguntar um por um ou confiar na
memória. Útil também pra saber se vale a pena avisar alguém antes de uma
mudança que quebra compatibilidade.

**Fora do git deste hub** (ver `.gitignore`: `instalacoes/*`, menos este
README) — cada entrada tem caminho absoluto de outro projeto na máquina do
dono; não é portável entre máquinas nem é conhecimento de domínio que valha
versionar.

## Formato de cada arquivo (`<nome-do-projeto>.md`)

\`\`\`markdown
## Projeto
<nome do projeto>

## Caminho absoluto
<path completo do projeto consumidor>

## Instalado em
AAAA-MM-DD

## Última atualização
AAAA-MM-DD (atualize esta data sempre que o prompt for colado de novo nesse projeto)

## Recursos instalados
- Skill: {{SKILL}} (sempre)
- Agents: <escolhidos pelo projeto, ou "nenhum">
- Workflows: <escolhidos pelo projeto, ou "nenhum">
\`\`\`

## Manutenção

Cada vez que o prompt de instalação for colado num projeto (instalação nova
ou atualização), o próprio prompt cria/atualiza o arquivo correspondente
aqui. Se um projeto parar de usar o hub, apague o arquivo dele.
```

## Passo 3 — executar

1. Crie os 5 arquivos dos templates acima com os placeholders substituídos
   (resolver, `verticais.json`, prompt, `inbox/README.md`, `instalacoes/README.md`).
   O resolver vai em `prompts/resolver/{{SKILL}}/` (crie a pasta), nunca em `.agent/skills/`.
1b. **Adicione ao `.gitignore` do próprio hub** (não ao do `0 Padrões` — são
   repositórios diferentes) o bloco de "Convenção de nomes": `inbox/*`,
   `!inbox/README.md`, `instalacoes/*`, `!instalacoes/README.md`, com o
   comentário. Se o hub ainda não tiver `.gitignore`, crie um só com esse bloco.
   Confira com `git check-ignore -v inbox/001-teste.md instalacoes/x.md` (ignorados)
   e `git check-ignore inbox/README.md instalacoes/README.md` (sem saída = versionados).
1c. Na seção "Atualização" do resolver, troque `AAAA-MM-DD` pela data de hoje.
1c2. Preencha `verticais.json` (um `nome`, um `quando` e os padrões `match` por
   vertical; veja o template acima) e gere o índice e os arquivos de vertical:
   `python3 "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/scripts/build_sip_index.py" --hub "<hub>"`
   (reescreve o texto entre `<!-- indice:start … -->` e `<!-- indice:end -->` e
   grava `verticais/<vertical>.md`; `--check` sai 1 se algo estiver desatualizado
   e 2 se um item ficar sem vertical ou uma vertical sem `quando`; ver `--help`).
   Rode de novo sempre que o hub ganhar, perder ou mudar a `description` de uma
   skill, agent ou workflow, e ponha o `--check` no lint ou hook do hub. O
   resolver antigo, com três tabelas (`<!-- skills:start … -->`, `agents`,
   `workflows`, opção `group=prefix`), continua aceito pelo gerador, mas não é
   o modelo para hub novo. Mantenha o `SKILL.md` do resolver em ~100 linhas;
   se passar disso, algo que é lista foi parar fora do índice.
1d. Confira o hub contra este modelo:
   `python3 "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/scripts/check_sip_hub.py" "<hub>" sip-<dominio>`
   tem de sair com 0 (todas as checagens PASS). Rode de novo sempre que mudar o resolver, o
   prompt, o inbox ou o `.gitignore` de um hub. Hub com lint próprio de caminhos
   (ex.: `Base Sites - Astro`): rode também o lint dele; caminho citado em skill
   precisa ser absoluto e existir, então não cite `inbox/arquivo/` (pasta ignorada).
2. **Não** crie symlink do resolver dentro do hub (`.claude/skills/{{SKILL}}`
   ou `.agent/skills/{{SKILL}}`): o resolver só serve a quem está fora. Se o hub
   usa `sync_entrypoints.py` (convenção Antigravity Kit), rode-o de dentro do hub
   e confira que ele não acusa o resolver como skill. Não confundir com o Passo 5
   abaixo, que é o stub em `0 Padrões` pra descoberta cross-project.
3. Se o hub tiver uma ficha em `0 Padrões/projetos/<Nome>.md`, adicione: a linha
   da skill na tabela de skills, uma seção "Acesso Cross-Project" apontando pro
   prompt e pro inbox, e uma linha no histórico de decisões.
3b. **Registre o SIP no índice central** `0 Padrões/projetos/_sips.md` (crie o
   arquivo se ainda não existir, seguindo o formato dos SIPs já listados):
   adicione uma linha na tabela com domínio, nome de exibição, caminho do hub,
   nome da skill resolver, caminho do prompt de instalação (**não duplique o
   conteúdo do prompt** — só referencie o caminho dentro do hub). A coluna de
   instalado no 0 Padrões é sempre "✅ Sim" (ver Passo 6, agora obrigatório).

## Passo 4 — o resolver completo fica só no hub

**Nunca** crie a skill resolver **completa** dentro de `0 Padrões` — ela é
sempre co-localizada no próprio hub (`<hub>/prompts/resolver/sip-<dominio>/`).
Um resolver guardado fora do hub diverge do roteador de domínio com o
tempo, porque ninguém o atualiza junto. `generate_catalog.py` do
`0 Padrões` só precisa ser rodado se esta própria skill meta
(`superiaprojects-criar-sip`) for alterada, não a cada SIP criado.

## Passo 5 — stub global no 0 Padrões

**Sempre crie um stub consolidado em `0 Padrões/.agent/skills/sip-<dominio>/SKILL.md`
(obrigatório — isto não é o Passo 4 acima, nem depende de instalar o
symlink `.claude/skills/sip-<dominio>` no 0 Padrões):**
- Isto é diferente de duplicar o resolver: é um arquivo curto (ver os
  stubs já existentes — `sip-n8n`, `sip-mautic`, `sip-firecrawl`,
  `sip-trends-previsao-demanda` — como modelo) que só aponta pro
  `SKILL.md` real dentro do hub, igual ao padrão antigo usado pelas
  sub-skills do Firecrawl (consolidado em 2026-11-06 de 17 stubs
  individuais pra 1 só por hub).
- **O stub só aponta, não lista**: caminho absoluto do resolver do hub
  (`<hub>/prompts/resolver/sip-<dominio>/SKILL.md`, onde estão o índice e os arquivos
  de vertical com skills, agents e workflows), do roteador
  mestre (se houver) e do prompt de instalação. Não copie nomes de skills,
  agents ou workflows no stub (não crie arquivos em
  `0 Padrões/.agent/agents/` ou `.agent/workflows/` pra isso): a lista
  copiada envelhece; o índice e as verticais do resolver são gerados e conferidos
  por `--check`. Diga no stub, em uma linha, que agents e workflows do hub
  estão nas verticais do resolver e podem ser lidos por caminho absoluto
  (Google Antigravity/Gemini/Cursor chegam neles por esse caminho, já que
  a Regra 4 não os redireciona sozinha para um hub externo).
- **Seção `## Atualização` no stub (obrigatória):** inclua ao final do stub:
  ```markdown
  ## Atualização

  Data da última atualização e instruções: seção "Atualização" do resolver no hub
  (`<hub>/prompts/resolver/sip-<dominio>/SKILL.md`). Para atualizar a instalação num
  projeto, cole de novo `<hub>/prompts/instalar-skill-sip-<dominio>.md`.
  ```
  Não copie a data literal para o stub: ela mudaria em dois lugares e divergiria
  (por isso o stub aponta para o resolver).
- **Por que é obrigatório:** a Regra 4 (Fallback Resolution Protocol) do
  `CLAUDE.md`/`AGENTS.md` faz todo projeto do ecossistema procurar por
  nome em `0 Padrões/.agent/skills/` como 2ª prioridade — isso vale
  globalmente, pra qualquer projeto, sem precisar instalar nada caso a
  caso. Sem este stub, Google Antigravity/Gemini/Cursor em **nenhum**
  projeto conseguem achar o SIP; só o Claude Code consegue (via o
  symlink `.claude/skills/sip-<dominio>`, que é instalação por projeto,
  não global).

## Passo 6 — instalar o SIP no 0 Padrões

**Instale o SIP aqui no 0 Padrões também (obrigatório, não mais opcional)
— além do stub do Passo 5:**
- Crie o symlink `.claude/skills/sip-<dominio>` -> `<hub>/prompts/resolver/sip-<dominio>`
  (absoluto, direto pro hub — **não** o padrão duplo do passo 1 do prompt
  de instalação: o 0 Padrões é exceção a esse padrão, ver `_sips.md`
  seção "Exceção: 0 Padrões não usa o padrão duplo como consumidor" —
  seu `.agent/skills/sip-<dominio>` já é o stub real do Passo 5, não pode
  também ser symlink pro hub).
- Agents e workflows: mesma escolha do passo 3 do prompt de instalação
  (mostre as seções Agents e Workflows das verticais do resolver e pergunte nenhum / todos / quais; sem
  resposta = nenhum; mesmas regras de arquivo real e de remoção). Para cada
  agent escolhido, crie `0 Padrões/.claude/agents/<nome>.md` ->
  `<hub>/.agent/agents/<nome>.md`; para cada workflow escolhido,
  `0 Padrões/.claude/commands/<nome>.md` -> `<hub>/.agent/workflows/<nome>.md`
  (symlink absoluto simples, sem duplicar em `.agent/` do 0 Padrões).
- Adicione cada symlink novo ao `.gitignore` do 0 Padrões (seção já
  existente: `.claude/skills/sip-*`; adicione entradas específicas pros
  agents/workflows, ex. `.claude/agents/<nome>.md`, se algum).
- Rode `python3 .agent/scripts/sync_entrypoints.py --check` na raiz do
  0 Padrões: tem de sair com 0 (o validador aceita o link direto para
  `<hub>/prompts/resolver/sip-<dominio>` de mesmo nome, ou `<hub>/.agent/skills/sip-<dominio>`
  em hub com layout antigo; o hook de commit do
  0 Padrões recusa commits enquanto houver erro).
- Registre esta instalação em `<hub>/instalacoes/0-padroes.md` (mesmo
  formato do passo 9 do prompt de instalação — nome "0 Padrões", caminho
  `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões`, data de
  hoje, recursos instalados).
- Atualize também `0 Padrões/.agent/SIPS-CONSUMIDOS.md` (mesmo formato
  do passo 10 do prompt de instalação, com "Vistos no hub") — o 0 Padrões também é um projeto
  consumidor, então também precisa do manifesto local.
- **Por quê isto virou obrigatório:** manter o 0 Padrões sempre como
  consumidor de toda SIP evita o problema que já aconteceu antes — SIPs
  criadas sem instalação aqui, descobertas só depois por busca manual.
  Mantém o 0 Padrões como referência viva de "como consumir qualquer SIP",
  útil pra testar a própria skill-mãe e pra qualquer trabalho feito
  diretamente aqui que precise de conhecimento do hub.

## Skills que citam caminho absoluto do hub

Como as skills especialistas são lidas por caminho absoluto a partir de
qualquer projeto, todo comando citado nelas usa o caminho do hub **literal**
(nunca variável: cada chamada de shell é nova). Hubs com muitas skills devem
ter um lint (frontmatter, `description` só de gatilho, caminhos existentes,
sem duplicação, sem narrativa de sessão) que compara o texto com o caminho
literal e lê os arquivos do checkout local (ver `writing-skills`, "Skills That
Cite an Absolute Hub Path"); prove uma vez num `git clone` em outro caminho.
Exemplo completo: `Base Sites - Astro` (`scripts/check-skills.mjs`,
`scripts/fix-skill-paths.mjs`, `prompts/instalar-skill-sip-astro.md`).

## Referência

Veja a pasta `references/` desta skill para um exemplo completo e preenchido
de cada arquivo gerado (com caminho mascarado, só para ilustrar a forma):
`skill-resolver-exemplo.md`, `prompt-instalacao-exemplo.md`,
`inbox-readme-exemplo.md`.
