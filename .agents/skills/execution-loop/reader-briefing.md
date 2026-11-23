# Reader subagent briefing template

Use with the "Briefing for reader subagents" rule in `SKILL.md`: one briefing per reader, one folder (or document set) per reader. Fill the `<...>` fields; keep the labels and the last paragraph verbatim. Run readers on the session's model, never below `sonnet`.

```text
Contexto: <objetivo, escopo>. Tarefa: leia TODAS as imagens/arquivos de <pasta> (Read em cada um, em ordem de nome). Antes, leia <molde> e <lista de eventos/fontes existentes>.
Entregue <arquivo> com: (1) telas/estados vistos, citando o arquivo e a hora; (2) por tela, ações e o evento existente (nome exato) ou a lacuna; (3) lacunas com propriedades sugeridas; (4) o que NÃO deve ser enviado (privacidade); (5) achados e perguntas candidatos, sem IDs; (6) referências a algo fora da sua pasta.
Rótulos: `visto` (cite o arquivo), `inferido` (diga de quê), `a confirmar` (diga com quem). Um estado visto não é uma regra. Uma ausência nunca é `visto`.
Outras áreas existem e são lidas por outros agentes. Liste toda referência a algo fora da sua pasta em vez de concluir que não existe. Ausência = "não visível nas capturas", nunca "não existe no produto". Não invente telas. Não edite outros arquivos.
```

## After all readers return (main session)

1. Merge every reader's list (6) of external references.
2. For each feature that appears in two or more areas, compare what each reader said; resolve contradictions by checking the source, not by picking a reader.
3. Re-word any absence that another area contradicts; register findings only after this pass.
