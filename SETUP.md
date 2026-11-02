# ⚙️ Guia Completo de Setup — Super IA Projects

> **Ecossistema Multi-IA mantido por Felipe Bahia ([Futuro Mercado](https://www.futuromercado.com.br))**  
> Este guia detalha a configuração dos **Servidores MCP Recomendados** e das **Extensões de IDE** para extrair a máxima produtividade do ecossistema.

---

## 🔌 1. Servidores MCP Recomendados

O Model Context Protocol (MCP) conecta as LLMs às suas ferramentas de terminal, navegadores, bancos de dados e APIs externas.

### Resumo dos 8 Servidores Selecionados

| Servidor MCP | Função Principal | Quando o Agente Utiliza |
| :--- | :--- | :--- |
| **`context7`** | Documentação Técnica Oficial | Sempre antes de escrever código ou configurar novas bibliotecas |
| **`firecrawl`** | Web Scraping & Busca Web | Pesquisa de mercado, benchmarking e extração de sites em Markdown |
| **`chrome-devtools`** | Depuração Visual no Navegador | Inspeção de elementos, acessibilidade (a11y) e Core Web Vitals (LCP) |
| **`testsprite`** | Automação de Testes | Geração de planos de teste a partir de PRDs e execução de suites |
| **`stitch`** | Prototipagem & Design Systems | Criação e edição de telas e variantes de UI |
| **`supabase`** | Gerenciamento de Banco Postgres | Consultas SQL, migrações de schema e tipagem TypeScript automática |
| **`api-tools`** | Contratos de APIs | Leitura e validação de especificações OpenAPI / Swagger |
| **`notion`** | Gestão de Conhecimento | Leitura e sincronização de PRDs e notas direto no Notion |

---

### Como Ativar os MCPs no seu Ambiente

Você pode usar o arquivo modelo [`mcp.example.json`](mcp.example.json) fornecido na raiz:

#### Para Claude Code (CLI)
Copie a configuração para o arquivo global do Claude Code:
```bash
cp mcp.example.json ~/.claude/mcp.json
```
*(Preencha as chaves de API necessárias, como a do Firecrawl ou Supabase, dentro do arquivo).*

#### Para Cursor IDE
No Cursor, acesse **Settings > Features > MCP**, ou adicione diretamente em:
```bash
cp mcp.example.json ~/.cursor/mcp.json
```

#### Para VS Code / Google Antigravity
Copie para a pasta de configurações do seu editor:
```bash
cp mcp.example.json .vscode/mcp.json
```

---

## 🧩 2. Extensões Recomendadas (VS Code / Antigravity / Cursor)

Configuramos o arquivo [`.vscode/extensions.json`](.vscode/extensions.json) com as extensões que utilizamos no dia a dia.

### Instalação em 1 Passo (Terminal):

Se preferir instalar todas de uma vez via linha de comando, basta rodar:

```bash
code --install-extension anthropic.claude-code \
     --install-extension kilocode.kilo-code \
     --install-extension johnpapa.vscode-peacock \
     --install-extension pkief.material-icon-theme \
     --install-extension mechatroner.rainbow-csv \
     --install-extension cweijan.vscode-office \
     --install-extension tomoki1207.pdf \
     --install-extension jasdeepkhalsa.html-md-converter-vscode \
     --install-extension rangav.vscode-thunder-client \
     --install-extension pranaygp.vscode-css-peek \
     --install-extension svelte.svelte-vscode \
     --install-extension ms-python.python \
     --install-extension ms-python.vscode-pylance \
     --install-extension ms-azuretools.vscode-docker
```

---

### Detalhamento das Extensões por Categoria

#### 🤖 IA & Agentes
- **Claude Code (`anthropic.claude-code`):** Integração com o agente de linha de comando da Anthropic.
- **Kilo Code (`kilocode.kilo-code`):** Copiloto inteligente para autocompletar e sugestões de código.

#### 🛠️ Produtividade & Visualização de Arquivos
- **Peacock (`johnpapa.vscode-peacock`):** Altera a cor da moldura do editor para você bater o olho e saber exatamente em qual projeto está trabalhando.
- **Material Icon Theme (`pkief.material-icon-theme`):** Ícones modernos para identificar pastas e extensões rapidamente.
- **Rainbow CSV (`mechatroner.rainbow-csv`):** Colore cada coluna de arquivos CSV com uma cor diferente para inspeção rápida de dados.
- **Office Viewer (`cweijan.vscode-office`):** Visualiza e edita planilhas Excel, tabelas e arquivos doc sem sair do editor.
- **PDF Viewer (`tomoki1207.pdf`):** Abre arquivos PDF diretamente nas abas do VS Code.
- **HTML to Markdown Converter (`jasdeepkhalsa.html-md-converter-vscode`):** Converte blocos HTML em Markdown limpo com 1 atalho.

#### 🌐 APIs, Web & Frontend
- **Thunder Client (`rangav.vscode-thunder-client`):** Cliente de testes REST integrado (alternativa leve e rápida ao Postman).
- **CSS Peek (`pranaygp.vscode-css-peek`):** Permite inspecionar a definição de uma classe CSS diretamente a partir do arquivo HTML/TSX.
- **Svelte (`svelte.svelte-vscode`):** Destaque de sintaxe e autocomplete para componentes Svelte.

#### 🐍 Python & Infraestrutura
- **Python + Pylance (`ms-python.python`, `ms-python.vscode-pylance`):** Intellisense, linting e execução de testes em Python.
- **Docker (`ms-azuretools.vscode-docker`):** Gerenciamento visual de containers, imagens e volumes Docker.

---

**Futuro Mercado** — [www.futuromercado.com.br](https://www.futuromercado.com.br) | [@felipelbahia](https://instagram.com/felipelbahia)
