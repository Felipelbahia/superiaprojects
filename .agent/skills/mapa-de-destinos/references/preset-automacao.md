# Preset: projeto de automação e dados

Linhas sugeridas para workflows (n8n), raspagem, pipelines e previsões. Código próprio (scripts, Code nodes versionados) segue a stack e o `STANDARDS.md`. Técnica do domínio mora no SIP (`sip-n8n`, `sip-firecrawl`, `sip-trends-previsao-demanda`), não no projeto.

| Tipo de entrega | Caminho | Nome e metadados | Observação |
|---|---|---|---|
| Exportações de workflows | workflows/ | `<nome-do-workflow>.json` | **sem credenciais** no JSON |
| Documentação de cada workflow | docs/workflows/ | `<nome-do-workflow>.md` | gatilho, entradas, saídas, dono |
| Entrada bruta de cada execução | dados/brutos/AAAA-MM-DD - Nome/ | | guardada para poder refazer; fora do git se tiver dado pessoal |
| Resultado processado | dados/processados/AAAA-MM-DD - Nome/ | | |
| Raspagens (páginas, extrações) | dados/raspagens/AAAA-MM-DD - <site>/ | | |
| Previsões e relatórios de dados | docs/relatorios/AAAA-MM-DD - Nome/ | | |
| Testes dos workflows (entrada de exemplo + resultado esperado) | testes/<nome-do-workflow>/ | `entrada.*`, `esperado.*` | rodados de novo a cada mudança no workflow; sem dado pessoal real |
| Termos e consultas de monitoramento | dados/monitoramento/ | `termos.txt`, `consultas.md` | |
