# Checklists por linguagem

Cada item: **o que buscar** → **como resolver**.

## JavaScript / TypeScript / React
- `addEventListener(` / `.on(` / `.subscribe(` sem `removeEventListener` / `.off(` / `unsubscribe` → remover no cleanup (`return () => ...` do `useEffect`, `disconnectedCallback`).
- `setInterval(` / `setTimeout(` recorrente sem `clearInterval` → guardar o id e limpar ao destruir.
- `new Map()` / `{}` / `[]` em escopo de módulo que só recebe `.set` / `.push` → limite de tamanho, LRU, `WeakMap`/`WeakRef` ou `delete` ao fim do uso.
- Closures que seguram objetos grandes (callbacks guardados em listas) → guardar só o necessário e soltar a referência.
- `new IntersectionObserver` / `MutationObserver` / `ResizeObserver` sem `.disconnect()` → desconectar no cleanup.
- `fs.watch` / `chokidar` / `WebSocket` / `EventSource` abertos sem `close()` → fechar ao terminar.
- `fetch` / streams sem `AbortController` em componentes desmontados → abortar no cleanup.
- Ler arquivo grande inteiro (`readFileSync`, `JSON.parse` de GBs) → stream/linha a linha.

## Python
- `lru_cache` sem `maxsize` (`@lru_cache(maxsize=None)`), dict/list global que só cresce → `maxsize` ou `cachetools.TTLCache`.
- `open(` sem `with` → `with open(...) as f`.
- `.read()` / `.readlines()` em arquivo grande, `list(...)` de gerador enorme → iterar linha a linha / manter gerador.
- Listas acumuladas em loop longo (`results.append` sem fim) → processar em lotes, `yield`.
- Referências circulares com `__del__`, callbacks registrados e nunca removidos → `weakref`, desregistrar.
- Threads/processos/sessões (`requests.Session`, conexões de DB) sem fechar → `with` ou `try/finally`.
- `subprocess.Popen` sem `wait()`/`communicate()` → zumbis; usar `subprocess.run`.

## Bash
- `cmd &` sem `wait` nem `trap ... EXIT` para matar filhos → `trap 'kill $(jobs -p)' EXIT`.
- `while true` sem `sleep`, acumulando variável/array → limitar e esvaziar.
- `tail -f` / watchers deixados em background → registrar PID e matar no fim.
- Ler arquivo grande com `$(cat arq)` → `while read -r linha`.
- Arquivos em `/tmp` criados e nunca removidos → `mktemp` + `trap 'rm -f' EXIT`.

## HTML / CSS / JS puro (catálogos, páginas)
- Mesmos itens de JS acima; atenção a `innerHTML +=` em loop e nós DOM removidos mas ainda referenciados em arrays.
- Dados gigantes embutidos (`catalog-data.js`) carregados inteiros → paginar ou carregar sob demanda.

## C / C++
- `malloc`/`new` sem `free`/`delete` em todos os caminhos (inclui retorno antecipado e erro) → RAII, `std::unique_ptr`, `goto cleanup`.
- Ferramenta: AddressSanitizer (`-fsanitize=address`), Valgrind, `leaks` no macOS.

## Como medir (antes e depois)
- Chrome DevTools → Memory → heap snapshots comparados.
- Python: `tracemalloc` (`take_snapshot()` antes/depois).
- macOS: `leaks <pid>`, `ps -o rss= -p <pid>` em intervalos.
