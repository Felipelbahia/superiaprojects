# Exemplo preenchido: inbox de contribuição

Resultado em `<CAMINHO_DO_HUB>/inbox/README.md`:

```markdown
# Inbox — contribuições de outros projetos

Porta de entrada para qualquer projeto que, usando a skill `sip-exemplo`, tenha
aprendido algo sobre exemplo e queira devolver ao hub: um insight, um exemplo
novo, ou uma melhoria numa skill existente.

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
