# Ambiente macOS: critérios e armadilhas da Fase 0

Script: `.agent/scripts/check_memoria.py` (só leitura; `--limpar` pede ok). Testes: `.agent/scripts/tests/test_check_memoria.py`.

## Critérios que o script aplica (não relaxar à mão)
| Alvo | Critério |
|---|---|
| `agy` órfão (Gemini) | `ppid=1` **e** 0 conexões locais `ESTABLISHED` na `--hub-port`. Só `ppid=1` não basta. Contagem que não deu para medir = nunca órfão. |
| Host "Plugin" parado (Antigravity) | helper "Plugin" cujo pai não é outro "Plugin", idade ≥ 20 min e **nenhum descendente vivo** (zumbis `Z` e sub-helpers "Plugin" não contam; um `zsh` já conta como vivo). |
| MCP, `claude`, `kilo`, `codex` órfão | `ppid=1`. MCP = processo `node`/`npm`/`npx` (ou com marcador no nome) cuja linha de comando contém `mcp`, `sequential-thinking`, `testsprite`, `shadcn`, `context7`, `stitch` ou `openapi`; se ela não puder ser lida (vazia), vale o nome/título; lida e sem marcador, o nome não salva. A linha de comando é lida só para detectar o MCP, achar o nome do pacote e (no `agy`) a porta do hub; do que sai só o nome do pacote (sem ele, o nome tirado do título do processo; se também falhar, o nome do processo se for seguro, senão a palavra `MCP`). |
| Dono desconhecido | só pode aparecer em "Mais pesados" (seção que só sai com métrica amarela/vermelha ou com alvos, até 5 linhas); nunca é alvo. |
| Sessão atual | a cadeia de pais do script (terminal, host, Electron) e todo processo chamado `Antigravity IDE`, `Electron` ou `launchd` são excluídos de qualquer ação e da lista de alvos (podem aparecer em "Mais pesados", que é só informativo). |

Sinal: `SIGTERM`; `SIGKILL` só com um segundo ok e só para quem ainda vive 8 s depois. O script sinaliza só os alvos listados (`agy` órfão, host "Plugin" parado, MCP/`claude`/`kilo`/`codex` órfão), nunca os filhos de um alvo. Um filho só vira alvo depois, quando o pai morre e ele passa a `ppid=1`; por isso o script manda rodar o check de novo. Observado em 2026-11-18 (registro em `memory.md`), não garantido: depois do `SIGTERM` num `agy` (1h54, 11 MCPs filhos), 0 dos 11 seguiam vivos.

## Medir de verdade
- `ps -o rss` subestima o que foi para o swap/compressor. Use `top -l 1 -o mem -stats pid,command,mem,cmprs` (footprint e comprimido por processo).
- Limites do script (amarelo/vermelho): swap 3/5 GB, compressor 4/7 GB, load por CPU 1/2, `node` 50/90. São absolutos: o swap total do macOS cresce sozinho ao longo do dia.
- O script não lê a pressão de memória: compressor ≥ 4 GB fica amarelo mesmo com pressão verde (que pode ser normal). Quem decide é o swap e a presença de órfãos.

## Segredos: nunca imprimir
- `ps ... command` traz tokens como argumento (`--access-token`, `--api-key`, `X-Goog-Api-Key`).
- **`ps ... comm` também não é seguro:** `node`/`npm` reescrevem o título do processo e o `comm` passa a trazer os argumentos. Caso real (2026-11-18): três tokens do Supabase e chaves do Google e do Context7 saíram no chat por um `comm=` sem filtro.
- Para olhar processos à mão, use o script, ou cole o resultado num filtro que corta tudo depois do primeiro argumento.
- Não imprima `~/.gemini/config/mcp_config.json` nem `~/.claude.json`: extraia só o nome do servidor e o `command`.
- Segredo impresso = segredo exposto: avise o dono para rotacionar.

## Armadilhas do ambiente
- `grep` é alias de `ugrep`: use `/usr/bin/grep`; com variável de lista de arquivos ele imprime a lista inteira.
- Caminhos com espaço (`0 Padrões`): `find ... -print0 | xargs -0`. No zsh, `--include=*.py` sem aspas falha por glob.
- `wc -l` devolve espaços à esquerda: compare com `[ $((n)) -eq 0 ]`, nunca `[ "$n" = 0 ]`.
- Arquivos gerados poluem a auditoria de código: exclua `catalog.html` (12 MB), `catalog-data.js`, `plans/**/snapshot/`, `tests/`.
- `lsof` que falha não é "0 clientes": trate como desconhecido.
- Um `agy` com 20 conexões locais é hub ativo de uma janela aberta há minutos, não órfão.

## Docker / OrbStack (o script só orienta)
- `docker stats --no-stream` mostra container em loop; o teto de memória da VM do OrbStack costuma ser metade da RAM.
- Parar e desligar o restart: `docker stop <nome>` e `docker update --restart=no <nome>`. `docker rm` sem `-v` não apaga volumes; confira os volumes antes.
- Se o OrbStack estiver fechado, o socket não existe: `orb start` antes, `orb stop` depois.
