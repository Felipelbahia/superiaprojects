---
# Repository: https://github.com/Felipelbahia/superiaprojects
# Status: Nativa do Projeto (unifica a `geral-arquitetura-de-projeto` do 0 Mkt, 2026-11-12)
name: mapa-de-destinos
description: Use when about to save a deliverable that is not source code (report, document, content piece, campaign, press material, data export, workflow export, study) and the project has no documented place for it, when creating or aligning a project, when a project gains more than one brand or product, or when someone asks where a kind of file should go.
author: Futuro Mercado / Felipe Bahia (@felipelbahia)
license: MIT
---
# Mapa de destinos (onde cada entrega mora)

## Princípio
O lugar de cada tipo de entrega é decidido **uma vez, por projeto**, num documento único: `docs/mapa-de-destinos.md`. Toda IA e toda skill leem o mapa antes de gravar. Ninguém decide pasta por conta própria a cada tarefa: uma escolha que não fica registrada vira uma pasta diferente na próxima sessão.

**Fora do mapa:** código e arquivos que o framework dita (componentes, rotas, testes, configs) seguem a convenção da stack, o `STANDARDS.md` e a skill do framework (ex.: site Astro, Next.js). O mapa pode ter uma linha que só diz "segue a skill X".

**Caminhos fixos pelas regras do kit** entram no mapa como linhas fixas e não se negociam: `.agent/plans/` (planos, loops, handoffs, `prompts/` para prompt de continuação e prompts temporários), `inbox/` (notas do kit: `GERAL-NNN-assunto.md`), `_projectdefines/`, `memory.md`.

## Regra de resolução (nesta ordem)
1. **Leia `docs/mapa-de-destinos.md`** (projeto antigo: `mapa-de-destinos.md` na raiz) e use o **Caminho** da linha do tipo de entrega, preenchendo os placeholders (`{tipo}`, `{marca}`, `{produto}`, `AAAA-MM-DD - Nome`). Nunca monte caminho por conta própria.
2. **Sem mapa: crie o mapa mínimo antes de gravar a primeira entrega, sem bloquear a entrega.**
   - O projeto tem convenção visível (`CLAUDE.md`, `STANDARDS.md`, pastas existentes)? O mapa **documenta o que já existe**, sem mover nada, e a entrega segue essa convenção.
   - Não tem nada? Use o preset do tipo do projeto (bloco `## Project` do `CLAUDE.md`, linha `Produces`): `references/preset-software.md`, `preset-marketing.md` ou `preset-automacao.md`. Mono-marca por padrão.
   - (Isto é o mínimo para não bloquear uma entrega; ao criar ou alinhar o projeto, vale a conversa de criação completa.)
   - Se o dono estiver na sessão, faça uma só pergunta ("há mais de uma marca ou produto?") e confirme o mapa antes de gravá-lo; se ele não puder responder, grave no padrão e marque "suposição" na seção Respostas.
   - Escreva o mapa pelo `references/modelo-mapa.md`, grave a entrega e **diga ao dono, em uma linha por tipo, o que entrou no mapa**, para ele corrigir. "Ninguém pediu o mapa" não é motivo para não criar: sem o mapa a próxima sessão escolhe outro lugar.
3. **Tipo de entrega que não está no mapa:** acrescente a linha no mapa **antes** de gravar e avise o dono. Não invente pasta fora do mapa.
4. **Pasta que o mapa cita e não existe:** crie só essa pasta.
5. **Mono-marca vs. multi-marca/produto:** nunca suponha. Se o mapa não responde, pergunte (conversa de criação) antes de criar subpasta de marca ou produto.
6. **Nunca mova nem apague arquivo existente** para encaixar no mapa. Árvore real diferente do mapa → avise e siga o mapa; migração só com aprovação.
7. **Em conflito entre o mapa e uma skill, vale o mapa.** O mapa não vale sobre o `CLAUDE.md` do projeto, que delega a ele.
8. **Dado sensível** (dados pessoais, exportações de clientes): nunca em pasta pública servida pela aplicação (ex.: `public/`); a linha do mapa diz se a pasta fica fora do git.

## Conversa de criação (projeto novo, alinhamento, ou projeto que passou a ter mais marcas ou produtos)
**O dono guia a construção.** Uma pergunta por vez, na ordem abaixo, esperando a resposta. Antes de cada escolha, mostre a árvore resultante de cada opção, **só a dos cenários relevantes** (os desenhos estão em `references/cenarios-multi-marca.md`). Nenhuma pergunta é pulada por pressa: sem resposta, use o padrão indicado e marque "suposição" na seção Respostas do mapa. **O que o README, as regras ou o contexto já sugerem não substitui a pergunta:** mostre como resposta proposta ("o README diz X, confirma?") e espere a confirmação. Pressa do dono também não pula pergunta; ele pode responder "de acordo".

1. **O que o projeto entrega além de código?** (relatórios, documentos, conteúdo, campanhas, imprensa, dados, exportações de workflow). Parta do `Produces` do bloco `## Project` e do preset correspondente; mostre a tabela do preset e pergunte só as exceções ("de acordo? o que muda?").
2. **Há mais de uma marca ou produto?** Não → estrutura simples, sem subpastas (padrão); vá para a pergunta 6. Sim → perguntas 3 a 5, **todas**.
3. **Como se relacionam?** Mostre as opções com o desenho de cada uma (`cenarios-multi-marca.md`, "Pergunta 2"): (A) marcas independentes; (B) uma marca com vários produtos; (C) marcas independentes, cada uma com produtos; (D) produtos com identidade própria (voz, persona ou kit) sob uma marca-mãe.
4. **Onde moram?** (cenários A e C; em B e D, pergunte se algum produto precisa de repositório próprio). No mesmo projeto (`marcas/{marca}/` ou o eixo `{produto}` nas pastas que divergem) ou um repositório por marca. Mostre a tabela de prós e contras (`cenarios-multi-marca.md`, "Pergunta 3") e **não recomende por padrão**: pergunte antes sobre equipes, clientes e confidencialidade. Repositório por marca → pergunte também onde fica a inteligência compartilhada.
5. **O que é compartilhado?** Mostre a tabela de sugestão por pasta (`cenarios-multi-marca.md`, "Pergunta 4") e peça só as exceções. As respostas preenchem a coluna **Escopo** (`projeto`, `marca`, `produto`) e o caminho completo de cada linha, com os placeholders.
6. **Fluxo de aprovação** (só se o projeto produz conteúdo para publicar ou enviar): opções 0, A, B e C em `references/preset-marketing.md`. Sem resposta = opção 0, sem esteira. Em multi-marca: a esteira é por marca ou global? Pergunte também **quem aprova**.
7. **Escreva o mapa**, explique ao dono o que cada linha significa e registre todas as respostas (e as suposições) na seção "Respostas", para não perguntar de novo.

## Projeto existente sem mapa
Leia as pastas e as regras, monte o mapa com o que existe (inclusive nomes antigos), aponte **inconsistências** numa seção própria e pergunte. Não mova nada. A migração para uma árvore nova é decisão do dono.

## Onde mora o quê
- **No mapa do projeto:** pastas, escopo de cada uma, nomes de arquivo, fluxo de aprovação. Mudou o arranjo? Altera-se só o mapa.
- **Nesta skill:** o princípio, a regra de resolução, a conversa de criação e os presets usados na criação.
- **Técnica reutilizável** (playbooks, modelos de redação) mora na skill do assunto, nunca no projeto.

## Referências
| Arquivo | Quando ler |
|---|---|
| `references/modelo-mapa.md` | Ao escrever ou corrigir um mapa |
| `references/preset-software.md` | Projeto que produz software |
| `references/preset-marketing.md` | Projeto que produz conteúdo, marca, campanhas, imprensa, vendas (inclui o modo 0 Mkt) |
| `references/preset-automacao.md` | Projeto de workflows, raspagem, pipelines, previsões |
| `references/cenarios-multi-marca.md` | Só quando há mais de uma marca ou produto |

Projeto misto: junte as linhas dos presets que se aplicam num mapa só.

## Erros comuns
| Erro | Correção |
|---|---|
| Gravar a entrega numa pasta inventada na hora e não registrar | Linha no mapa antes de gravar; avisar o dono |
| "Ninguém pediu mapa", então não criar | Sem mapa, crie o mínimo (regra 2); a ausência não bloqueia a entrega nem fica sem registro |
| Pôr componente, rota ou teste no mapa | Código segue a stack, o `STANDARDS.md` e a skill do framework |
| Exportação com dado pessoal em `public/` ou versionada | Pasta fora do que é servido e, se for o caso, no `.gitignore`; a linha do mapa diz isso |
| Mover arquivo antigo "para organizar" | Mapear, nunca mover sem aprovação |
| Criar subpasta de marca ou produto sem perguntar | Conversa de criação primeiro |
| Duplicar no projeto o que mora num hub (base de jornalistas, playbooks) | Ler do hub pelo SIP; o projeto guarda só o que é dele |
