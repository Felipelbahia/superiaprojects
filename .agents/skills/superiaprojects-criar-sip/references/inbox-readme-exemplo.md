# Exemplo preenchido: inbox de contribuição

Resultado em `<CAMINHO_DO_HUB>/inbox/README.md`
(no `.gitignore` do hub: `inbox/*` e `!inbox/README.md`):

```markdown
# Inbox — contribuições de outros projetos

Porta de entrada para qualquer projeto que, usando a skill `sip-exemplo`, tenha
aprendido algo sobre exemplo e queira devolver ao hub: um insight, um
exemplo novo, ou uma melhoria numa skill existente.

**Ninguém edita `.agents/skills/` (ou pastas de exemplos/workflows) direto a
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
