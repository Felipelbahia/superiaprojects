# Instalações — quem consome este hub

Registro de todo projeto que instalou acesso a este hub (skill `sip-geral` e
os agents/workflows que o projeto escolheu, se algum) via
`prompts/instalar-skill-sip-geral.md`. Diferente do `inbox/`: isto não é
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

```markdown
## Projeto
<nome do projeto>

## Caminho absoluto
<path completo do projeto consumidor>

## Instalado em
AAAA-MM-DD

## Última atualização
AAAA-MM-DD (atualize esta data sempre que o prompt for colado de novo nesse projeto)

## Recursos instalados
- Skill: sip-geral (sempre)
- Agents: <escolhidos pelo projeto, ou "nenhum">
- Workflows: <escolhidos pelo projeto, ou "nenhum">
```

## Manutenção

Cada vez que o prompt de instalação for colado num projeto (instalação nova
ou atualização), o próprio prompt cria/atualiza o arquivo correspondente
aqui. Se um projeto parar de usar o hub, apague o arquivo dele.
