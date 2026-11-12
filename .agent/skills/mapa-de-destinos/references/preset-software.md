# Preset: projeto de software

Linhas sugeridas para o mapa de um projeto que produz software. Código fica fora do mapa (segue a stack, o `STANDARDS.md` e a skill do framework). Cada pasta nasce quando o projeto precisa dela.

| Tipo de entrega | Caminho | Nome e metadados | Observação |
|---|---|---|---|
| Documentos técnicos (guias, decisões fora do `_projectdefines/`) | docs/ | `<tema>.md` | `ARCHITECTURE.md`, `CODEBASE.md`, `PATTERNS.md` seguem as regras do kit (raiz ou `_projectdefines/`) |
| Decisões de arquitetura (ADR), sem `_projectdefines/` | docs/adr/ | `NNNN-titulo.md` | com `_projectdefines/`, ADRs ficam lá |
| Relatórios (auditoria, launch-readiness, performance, segurança) | docs/relatorios/AAAA-MM-DD - Nome/ | `relatorio.md` + anexos | |
| Apresentações e materiais de demonstração | docs/apresentacoes/ | `AAAA-MM-DD_<tema>.<ext>` | |
| Exportações de dados pedidas por pessoas (CSV, planilhas) | exports/AAAA-MM-DD - Nome/ | `<conteudo>.csv` | **fora do git** (`exports/` no `.gitignore`); nunca em `public/` |
| Dados de exemplo e fixtures | segue a stack (ex.: `tests/fixtures/`) | | código |
| Scripts utilitários do projeto | scripts/ | | código; seguem `STANDARDS.md` |
| Conteúdo de comunicação (newsletter, posts, e-mails) | ver `preset-marketing.md` | | projeto misto: junte as linhas |
