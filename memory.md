# Memory — 0 Padrões

Problema → Solução, só o que não se deduz do código.

## 2026-11-13 — atualização de projeto cortava regras locais
- **Problema:** na propagação, o `CLAUDE.md` do Remote Brain perdeu 3 frases de segurança (item 7 do Protocolo de Execução Remota) e uma tabela de roteamento; o do Vagas perdeu a regra do prefixo `[jobs]` do banco compartilhado. Causa: `assemble_rules.py --replace` descarta o arquivo antigo; o prompt de atualização mandava conferir com "grep de um trecho" (passa com a linha cortada); nenhum check de máquina.
- **Solução:** `.agent/scripts/check_local_rules.py <backup> <novo>` compara linha inteira (CUT / MISSING / junk), com base de texto genérico `project-initializer/legacy-generic-lines.txt` (linhas repetidas em 2+ backups) e `adaptadas.md` ao lado do backup para o que foi descartado de propósito; `--replace` leva o texto próprio para "A revisar"; `projects_audit.py` ganhou a coluna "Regras locais"; prompt 01 manda rodar o check. Modelo: como projeto novo do initializer (só regras locais completas; lixo antigo sai).
- Loop: `.agent/plans/execution-loops/2026_11_13/Regras Locais Preservadas na Atualização/`.

## 2026-11-14 — regras só em CLAUDE.md + AGENTS.md
- **Problema:** o kit gerava 5 a 7 cópias das regras (`GEMINI.md` na raiz, `.agent/rules/*`, `.cursorrules`) e elas divergiam (a raiz já estava um módulo à frente das cópias). O Antigravity lê `AGENTS.md` na raiz (docs oficiais: antigravity.google/docs/rules); `.agent/rules/` é caminho legado dele.
- **Solução:** padrão = `CLAUDE.md` (Claude Code) + `AGENTS.md` (Antigravity e outras IAs) idênticos na raiz. `sync_rules.py` só grava esses dois (+ `.cursorrules`/`.claude/CLAUDE.md` se já existirem, nunca cria) e nunca usa legado como fonte. `GEMINI.md` e `.agent/rules/` viram legado: `sync_rules.py --clean-legacy` lista, pergunta e só apaga o que é idêntico ao `CLAUDE.md`; o que diverge fica. `projects_audit.py` ganhou a coluna "Legado" (bloqueia "em dia"). Teste `test_rules_standard.py` impede a volta do texto antigo nos arquivos versionados.
- Projetos existentes migram pelo prompt `01-atualizar-projeto-existente.md`, um a um, com confirmação; nada foi apagado em lote.
- Loop: `.agent/plans/execution-loops/2026_11_14/Regras só CLAUDE e AGENTS/`.
