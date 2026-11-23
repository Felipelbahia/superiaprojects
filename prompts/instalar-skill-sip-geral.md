# Prompt: Instalar/Atualizar o acesso ao hub "SIP - Geral" em outro projeto

Cole isto numa sessão do Claude Code dentro do projeto que precisa consultar o
hub central de geral (SIP - Geral). Instala sempre o resolver e, dos
agents e workflows do hub, só os que você escolher (o prompt mostra as tabelas e pergunta):

```
Instale/atualize o acesso ao hub central SIP - Geral (geral) neste projeto.
O que entra: o resolver sip-geral sempre; agents e workflows do hub só os que eu
escolher; skills especialistas do hub nunca (o resolver as acha pela tabela e
as lê por caminho absoluto).
Padrão duplo: cada recurso instalado ganha um symlink absoluto em .agents/ (pro
hub) e um symlink relativo em .claude/ (pro symlink local em .agents/) — isso dá
acesso tanto ao Claude Code quanto a Google Antigravity/Gemini/Cursor, que leem
.agents/ direto e não dependem do stub global do 0 Padrões.

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
E cujo destino aponte para dentro de "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões". Leia o destino com `readlink`
SEM `-f` (com `-f`, um link quebrado sai com erro no macOS): link de .agents/ tem o
caminho absoluto do hub; link relativo de .claude/ ou .cursor/ aponta para o link de
.agents/ de mesmo nome, então confira esse. Nunca remova arquivo ou pasta real.

1. Skill resolver (obrigatório):
   - Crie a pasta .agents/skills/ se ela não existir.
   - Crie (ou recrie) o symlink absoluto com `ln -sfn`:
     .agents/skills/sip-geral -> "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/prompts/resolver/sip-geral"
   - Crie a pasta .claude/skills/ se ela não existir.
   - Crie o symlink relativo com `ln -sfn` (pro symlink acima, não direto pro hub):
     .claude/skills/sip-geral -> ../../.agents/skills/sip-geral

2. Migração (instalações antigas): remova, seguindo a regra de remoção, todo
   symlink em .agents/skills/ e .claude/skills/ que aponte para uma skill
   especialista do hub (qualquer uma que não seja sip-geral nem do núcleo do passo 2b), e a
   entrada dele no .gitignore. As skills especialistas fora do núcleo não são mais instaladas.

2b. Núcleo (as skills de processo que as regras citam; só elas são linkadas):
   - Leia "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/prompts/resolver/sip-geral/nucleo.json" (`{"skills": [...]}`).
     Arquivo ausente: pule este passo.
   - Nome que não existe no hub (o `sips_status.py` acusa "núcleo <n>: não existe no hub"): pule e me avise.
   - Para cada nome <n> (seguindo a regra de symlink acima): se
     .agents/skills/<n> já é uma pasta REAL, é skill do próprio projeto: mantenha-a
     e só garanta .claude/skills/<n> -> ../../.agents/skills/<n> (relativo).
     Senão crie .agents/skills/<n> -> "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agents/skills/<n>" (absoluto) e
     .claude/skills/<n> -> ../../.agents/skills/<n> (relativo).
   - As outras skills especialistas continuam não instaladas: leia-as por caminho
     absoluto (`resolve_skill.py`).

3. Escolha de agents e workflows:
   - Leia as seções "Agents" e "Workflows" de cada arquivo de
     "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/prompts/resolver/sip-geral/verticais/" (nome + "use quando").
     Instalações antigas apontavam para ".agents/skills/sip-geral" do hub: esse
     caminho não existe mais, o link acima o substitui (recrie-o com `ln -sfn`).
   - Leia a entrada deste hub em .agents/SIPS-CONSUMIDOS.md, se existir:
     "Agents"/"Workflows" (escolhidos) e "Vistos no hub" (oferecidos antes).
   - Primeira instalação (sem entrada): mostre as duas tabelas e pergunte
     "Quais instalar? nenhum / todos / lista de nomes". Sem resposta = nenhum.
   - Instalação antiga sem entrada no manifesto, mas com symlinks deste hub já
     em .agents/agents/, .claude/agents/, .agents/workflows/ ou .claude/commands/:
     mostre as tabelas com esses itens já marcados e pergunte "manter esta
     escolha, mudar, ou nenhum?". Sem resposta = manter (nunca remova sem resposta).
   - Reinstalação: mantenha a escolha anterior sem perguntar de novo. Pergunte
     só sobre os itens das tabelas que NÃO estão em "Vistos no hub" (os novos).
     Sem resposta = os novos ficam de fora. Se eu pedir para mudar a escolha,
     mostre as tabelas inteiras com a escolha atual marcada.
   - Tabelas vazias: pule este passo e os passos 4 e 5 sem erro.

4. Instale só o escolhido (seguindo a regra de symlink acima):
   - Cada agent <nome>: .agents/agents/<nome>.md -> "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agents/agents/<nome>.md"
     (absoluto) e .claude/agents/<nome>.md -> ../../.agents/agents/<nome>.md (relativo).
   - Cada workflow <nome>: .agents/workflows/<nome>.md -> "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agents/workflows/<nome>.md"
     (absoluto), e .claude/commands/<nome>.md e .cursor/commands/<nome>.md ->
     ../../.agents/workflows/<nome>.md (relativos).
   - Crie as pastas que faltarem.

5. Remova o que saiu da escolha (seguindo a regra de remoção): symlinks de
   agents/workflows deste hub que não estão mais escolhidos, ou cujo arquivo
   sumiu do hub (link quebrado), e as entradas deles no .gitignore.

6. Confirme com `ls -la` cada symlink criado (os de .agents/ E os de .claude/, incluindo
   os do núcleo) e que o .md/SKILL.md correspondente é legível através de cada um. Depois, na raiz
   deste projeto, rode
   `python3 "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agents/scripts/sync_entrypoints.py" --check`:
   tem de sair com 0. Se acusar erro de link ou skill do hub, pare e relate
   (não apague links para "limpar" o aviso).
7. Não copie conteúdo de nenhum desses arquivos para este projeto — mantenha
   tudo como symlink, para herdar atualizações futuras do hub automaticamente.
8. Adicione ao .gitignore deste projeto (crie a seção se não existir) uma linha
   por symlink instalado, nunca um curinga do prefixo do domínio:
   .agents/skills/sip-geral
   .claude/skills/sip-geral
   (e, para cada skill do núcleo linkada no passo 2b, .agents/skills/<n> e
   .claude/skills/<n>; e, para cada agent/workflow instalado no passo 4, os caminhos
   .agents/agents/<nome>.md, .claude/agents/<nome>.md,
   .agents/workflows/<nome>.md, .claude/commands/<nome>.md,
   .cursor/commands/<nome>.md correspondentes)
   — são symlinks com path absoluto desta máquina, não portáveis entre clones.
9. Registre esta instalação no hub (bookkeeping, não é conteúdo de domínio —
   pode escrever direto, sem passar pelo inbox):
   - Veja o formato em "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/instalacoes/README.md".
   - Crie ou atualize "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/instalacoes/<nome-deste-projeto>.md" com:
     nome e caminho absoluto deste projeto, data de hoje, e os recursos
     instalados (skill sempre; agents/workflows escolhidos, ou "nenhum").
10. Atualize o manifesto local deste projeto, `.agents/SIPS-CONSUMIDOS.md`
   (crie se não existir — contrapartida local do registro do passo 9: lá o
   hub sabe quem consome; aqui o projeto sabe o que consome, sem precisar
   abrir .gitignore ou seguir symlink pra descobrir):
   - Formato de cada entrada (uma por SIP instalado neste projeto):
     ```markdown
     ## SIP - Geral (`sip-geral`)
     - Hub: /Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões
     - Instalado/atualizado em: AAAA-MM-DD
     - Skill: sip-geral
     - Agents: <escolhidos, ou "nenhum">
     - Workflows: <escolhidos, ou "nenhum">
     - Vistos no hub: agents <todos os nomes da tabela hoje>; workflows <idem>
     - Conflitos: <"nome: pulado" | "nome: meu arquivo renomeado para <novo>" | "nome: substituído (meu em <link>.bak-AAAA-MM-DD)", ou "nenhum">
     - Para atualizar: cole de novo "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/prompts/instalar-skill-sip-geral.md"
     ```
   - "Vistos no hub" é o que permite, na próxima vez, perguntar só os novos.
   - Se o arquivo já tiver uma entrada pra este hub (de uma instalação
   anterior), substitua-a em vez de duplicar.
11. Confirme que as regras deste projeto sabem achar o que não está
   instalado: rode `grep -n -F "Named in these rules but not in" CLAUDE.md`
   e cole a saída. Sem saída: as regras estão atrás do kit. Avise o dono
   (remontar com `assemble_rules.py`, prompt 01 de `prompts-template/`) e
   não edite o `CLAUDE.md` à mão.
```

## Por que o padrão duplo (symlink de symlink) e não um só

A fonte de verdade de cada recurso fica no hub (`/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agents/skills/`,
`.agents/agents/`, `.agents/workflows/`). O symlink absoluto em `.agents/` deste
projeto aponta direto pro hub; o symlink relativo em `.claude/` aponta pro
symlink local em `.agents/`, não direto pro hub. Essa cadeia de dois symlinks
(em vez de um só direto em `.claude/`) existe porque **Claude Code e as
outras IAs leem pastas diferentes**: Claude Code só descobre
`.claude/skills/`/`.claude/agents/`/`.claude/commands/`; Google
Antigravity/Gemini/Cursor só leem `.agents/skills/`/`.agents/agents/`/
`.agents/workflows/` direto (1ª etapa da regra "Skills, agents, workflows: where they live" do
`CLAUDE.md`/`AGENTS.md`: o `.agents/` do próprio projeto). Um symlink só em `.claude/` (direto pro hub) atende só o
Claude Code — pra essas outras IAs acharem o recurso neste projeto
específico, ele precisa também existir em `.agents/`. Atualizações futuras no
hub já refletem aqui automaticamente nos dois — exceto se um symlink quebrar
(hub movido ou arquivo renomeado), caso em que basta colar o prompt outra
vez, ou se o hub adicionar um agent/workflow novo depois da instalação, caso
em que rodar o prompt de novo pergunta só sobre os novos (a escolha anterior
fica registrada em `.agents/SIPS-CONSUMIDOS.md`, linha "Vistos no hub").

## Para outras IAs (Google Antigravity / Gemini / Cursor)

Com o padrão duplo acima, essas IAs já encontram o resolver e os
agents/workflows escolhidos **direto neste projeto** (via `.agents/skills/`,
`.agents/agents/`, `.agents/workflows/`), sem depender do stub global do
`0 Padrões` nem da regra "Skills, agents, workflows: where they live" do
`CLAUDE.md`/`AGENTS.md` — a 1ª etapa dela já é "o `.agents/` do próprio projeto", que é exatamente o que
os passos 1 e 4 criaram aqui. O que não foi escolhido elas acham pelas
tabelas do resolver e leem por caminho absoluto no hub. O stub global do `0 Padrões` continua existindo como rede de
segurança pra projetos que *não* instalaram (a busca dessa regra no kit, 3ª etapa), mas
quem instalou via este prompt não depende dele.

## Via de volta: contribuir com o hub

A skill instalada também sabe devolver conhecimento ao hub — nunca edita os
arquivos compartilhados direto, só deixa um arquivo em `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/inbox/`
para revisão manual. Ver `inbox/README.md` no hub para o formato esperado.

## Registro desta instalação no hub

Este prompt também registra quem instalou, em `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/instalacoes/`
(ver `instalacoes/README.md` no hub) — isto não é conteúdo de domínio, é
bookkeeping de quem consome o hub, então pode ser escrito direto, sem passar
pelo inbox. Serve pro dono do hub saber, quando mudar algo, quais projetos
revisar ou avisar — sem esse registro, ele teria que adivinhar ou perguntar
projeto por projeto.

## Manifesto local neste projeto

Este prompt também atualiza `.agents/SIPS-CONSUMIDOS.md` **neste projeto**
(contrapartida local do registro acima: lá o hub sabe quem o consome; aqui
o projeto sabe o que consome). Sem esse manifesto, a única forma de saber
que este projeto depende de um SIP é abrir o `.gitignore` ou seguir cada
symlink manualmente — o manifesto deixa isso visível de cara, num lugar só,
pra qualquer pessoa ou IA que abrir o projeto.
