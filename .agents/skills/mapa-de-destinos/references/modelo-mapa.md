# Modelo de `docs/mapa-de-destinos.md`

Copiar para o projeto, preencher com os caminhos reais e datar. Juntar as linhas dos presets que se aplicam (software, marketing, automação). Em mono-marca (o padrão) nenhum caminho leva `{marca}` e a coluna Escopo pode sair.

**Coluna Caminho:** caminho completo, relativo à raiz, já com o prefixo de marca ou produto quando houver. `{tipo}`, `{marca}`, `{produto}` e `AAAA-MM-DD - Nome` são placeholders preenchidos na hora de gravar.

**Onde mora o mapa:** `docs/mapa-de-destinos.md`, sempre. Uma marca por repositório → um mapa por repositório, e a seção "Respostas" aponta os repositórios irmãos.

```markdown
# Mapa de destinos: <Projeto>
Produz: <software | conteúdo | automação/dados | misto>. Estrutura: <mono-marca | multi-marca cenário A/B/C/D>.
Atualizado em AAAA-MM-DD. Se este mapa divergir de uma regra de skill, **vale este mapa**. Tipo de entrega que não está aqui entra aqui antes de ser gravado.

| Tipo de entrega | Caminho | Escopo | Nome e metadados | Observação |
|---|---|---|---|---|
| <linhas do(s) preset(s)> | | | | |
| Código (componentes, rotas, testes, configs) | segue a stack e o `STANDARDS.md` | projeto | | fora do mapa; ex.: "segue a skill astro-development" |
| Planos, loops e handoffs | .agents/plans/ | projeto | `execution-loops/AAAA_MM_DD/<Título>/NN Nome.md`, `handoffs/` | fixo pelas regras do kit; fora do git |
| Prompt para continuar em outra sessão ou outro momento, e prompts temporários | .agents/plans/prompts/ | projeto | `NNN-<Título Curto>.md` (contador próprio) | fixo pelas regras do kit; fora do git; o handoff fica em `handoffs/` |
| Itens adiados | inbox/ | projeto | `NNN-assunto.md`; nota do kit ou de outro projeto: `GERAL-NNN-assunto.md` | fixo pelas regras do kit |
| Contrato do projeto (se houver) | _projectdefines/ | projeto | | fixo; só muda com aprovação do dono |
| Memória de longo prazo | memory.md | projeto | `Problema → Solução` | fixo |
| Este mapa e documentos do projeto | docs/ | projeto | | |

## Como usar este mapa (toda IA e skill que grava arquivo)
1. Leia esta tabela antes de gravar. Use o **Caminho** da linha do tipo de entrega, preenchendo os placeholders. Não monte caminho por conta própria.
2. Tipo de entrega que não está aqui: acrescente a linha antes de gravar e avise o dono.
3. Pasta citada aqui que não existe: crie só essa pasta.
4. Nunca mova nem apague arquivo existente para encaixar na estrutura; mudança de lugar só com aprovação.
5. Dúvida que este mapa não resolve: skill `mapa-de-destinos`.

## Respostas da conversa de criação
| Pergunta | Resposta | Data |
|---|---|---|
| O que o projeto entrega além de código? | <tipos> | |
| Há mais de uma marca ou produto? | <não \| sim: cenário A/B/C/D \| suposição: mono-marca, dono não respondeu> | |
| Onde moram as marcas? (se multi-marca) | <mesmo projeto em marcas/{marca}/ \| um repositório por marca: caminhos> | |
| O que é compartilhado? (escopo por pasta) | <pastas> | |
| Onde está o compartilhado? (se repositório por marca) | <repositório e caminho> | |
| Fluxo de aprovação (se publica ou envia conteúdo) | <0 sem esteira \| A \| B \| C>; em multi-marca, por marca ou global | |
| Quem aprova | <nome ou papel> | |

Se a opção de aprovação for A, B ou C, escrever aqui o caminho resultante de peças, `envios.md`, `clipping/` e `publicados.md`.

## Inconsistências conhecidas (só em projeto existente)
O que as regras do projeto dizem versus a árvore real. Não migrar sem aprovação do dono.
- <ex.: o CLAUDE.md cita ./relatorios/ mas a pasta real é docs/reports/>
```

## Como manter
Revisar o mapa sempre que uma pasta nascer ou mudar e nas revisões periódicas do projeto. Mudança de lugar de arquivo existente exige aprovação do dono.
