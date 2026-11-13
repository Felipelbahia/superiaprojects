# Memory — 0 Padrões

Problema → Solução, só o que não se deduz do código.

## 2026-11-13 — atualização de projeto cortava regras locais
- **Problema:** na propagação, o `CLAUDE.md` do Remote Brain perdeu 3 frases de segurança (item 7 do Protocolo de Execução Remota) e uma tabela de roteamento; o do Vagas perdeu a regra do prefixo `[jobs]` do banco compartilhado. Causa: `assemble_rules.py --replace` descarta o arquivo antigo; o prompt de atualização mandava conferir com "grep de um trecho" (passa com a linha cortada); nenhum check de máquina.
- **Solução:** `.agent/scripts/check_local_rules.py <backup> <novo>` compara linha inteira (CUT / MISSING / junk), com base de texto genérico `project-initializer/legacy-generic-lines.txt` (linhas repetidas em 2+ backups) e `adaptadas.md` ao lado do backup para o que foi descartado de propósito; `--replace` leva o texto próprio para "A revisar"; `projects_audit.py` ganhou a coluna "Regras locais"; prompt 01 manda rodar o check. Modelo: como projeto novo do initializer (só regras locais completas; lixo antigo sai).
- Loop: `.agent/plans/execution-loops/2026_11_13/Regras Locais Preservadas na Atualização/`.
