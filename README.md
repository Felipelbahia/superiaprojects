<div align="center">
  <img src="assets/logo.png" alt="Futuro Mercado" width="340" />
  <h1>Super IA Projects (<code>superiaprojects</code>)</h1>
  <p><strong>The Agentic Engineering Framework</strong></p>
  <p>Modular Skills, Multi-AI Dual Parity Rules, Autonomous Specialists, and Interactive Visual Catalog.</p>

  <p>
    <a href="https://www.futuromercado.com.br"><img src="https://img.shields.io/badge/Futuro%20Mercado-Website-gold?style=for-the-badge&logo=googlechrome&logoColor=black" alt="Website" /></a>
    <a href="https://instagram.com/felipelbahia"><img src="https://img.shields.io/badge/Instagram-@felipelbahia-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram" /></a>
    <a href="mailto:felipe@futuromercado.com.br"><img src="https://img.shields.io/badge/Contato-felipe@futuromercado.com.br-blue?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" /></a>
    <img src="https://img.shields.io/badge/Vers%C3%A3o-v1.0.0-blueviolet?style=for-the-badge" alt="Versão" />
    <img src="https://img.shields.io/badge/Atualizado-03%2F11%2F2026-informational?style=for-the-badge" alt="Atualizado" />
  </p>

  <p>
    <strong>Português</strong> | <a href="README.en.md">🇺🇸 Read in English</a>
  </p>
</div>

---

> **Autoria:** Criado e mantido por **Felipe Bahia** ([Futuro Mercado](https://www.futuromercado.com.br)).  
> **Versão:** `v1.0.0` · **Última Atualização:** 03 de Novembro de 2026  
> Inspirado na filosofia de fricção zero do [`obra/superpowers`](https://github.com/obra/superpowers) e desenhado para engenharia ágil com **Claude Code**, **Google Antigravity** e **Cursor**.

---

## ⚡ Por que o Super IA Projects?

O desenvolvimento com agentes autônomos de IA frequentemente sofre com contexto instável, regras conflitantes e skills difíceis de portar entre diferentes ferramentas de linha de comando ou IDEs.

O **Super IA Projects** resolve isso fornecendo uma arquitetura unificada:

- 🎯 **Compatibilidade Multi-IA Real (Paridade Dual):** Regras 100% idênticas sincronizadas automaticamente entre `CLAUDE.md`, `GEMINI.md` e `.cursorrules`.
- 🧩 **Skills Modulares & Agnósticas:** Mais de 210 skills prontas cobrindo desenvolvimento web, mobile, web scraping robusto (Firecrawl) e arquitetura.
- 🔄 **Loop de Execução (Execution Loop):** Metodologia rígida de entrega: *Brainstorm → Espec → Plan → Execução → QA (com notas 0 a 10 e evidências verificáveis)*. Se algum critério da Rubrica de QA tirar nota menor que 10, a skill reinicia o ciclo sozinha (Debug → Espec) e tenta de novo — até 5 ciclos — em vez de entregar algo "quase pronto".
- 🏭 **SIPs (Super IA Projects especialistas):** Projetos-hub que concentram toda a inteligência (skills, agents, workflows) de um domínio específico (ex: n8n, marketing) em um único lugar, compartilhada sob demanda com qualquer projeto que precise — sem duplicar conhecimento em cada repositório.
- 📊 **Catálogo Visual Interativo:** Um painel navegável em HTML (`catalog.html`) e índice Markdown (`.agent/CATALOG.md`) atualizados dinamicamente.
- 🛡️ **Privacidade & Isolamento:** Regras pessoais, históricos de execução e dados de clientes isolados por padrão via `.gitignore`.

---

## 📦 O que está incluído

- **130+ Agentes Especialistas** (`.agent/agents/`): Personas focadas em domínios (Frontend, Mobile, Backend, Segurança, DevOps, Auditoria).
- **220+ Skills com Scripts** (`.agent/skills/`): Conhecimento procedural acionável com verificações e testes embutidos.
- **110+ Workflows** (`.agent/workflows/`): Comandos `/slash` rápidos para Claude Code e Cursor.
- **Modelos Agnósticos:**
  - `CLAUDE.example.md` (ou `ClaudeExample.md`): Template agnóstico pronto para ser copiado para `CLAUDE.md`.
  - `prompts-template/`: Coleção de prompts copy-paste testados para criação, migração e sincronização de projetos.
  - `mcp.example.json`: Configuração limpa para servidores MCP.

---

## 🚀 Quickstart & Instalação

### Instalação em 1 Comando:

```bash
git clone https://github.com/seu-usuario/superiaprojects.git
cd superiaprojects
./install.sh
```

O script `./install.sh`:

1. Verifica seu ambiente Python 3.
2. Cria o arquivo `CLAUDE.md` a partir do `CLAUDE.example.md` (se ainda não existir).
3. Cria todos os symlinks para o Claude Code (`.claude/`) e Cursor (`.cursor/`).
4. Gera o catálogo visual unificado em `catalog.html`.

---

## 💻 Como rodar em outra máquina

Os scripts do kit usam só a biblioteca padrão do Python: não há `npm`, `uv` nem arquivo `.env`.

```bash
git clone https://github.com/Felipelbahia/superiaprojects.git
cd superiaprojects
python3 --version                                   # 3.11 ou mais novo
git config core.hooksPath .githooks                 # ativa o hook de commit
python3 .agent/scripts/sync_entrypoints.py --check  # confere skills, agents e workflows
python3 -m unittest discover -s .agent/scripts/tests -q
```

- `.agent/` é a fonte de tudo; `.claude/` e `.cursor/` só têm links para ela. Não copie nem apague os links à mão.
- Os arquivos de regras (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`) ficam fora do git: gere os seus com `CLAUDE.example.md` e `install.sh`.
- Os links `.claude/skills/sip-*` só existem onde o SIP está instalado; o `--check` não os cobra quando o `.gitignore` os ignora.
- Mínimo: Python 3.11 (`pyproject.toml`, `.python-version`; o hook de commit para com erro claro em versão menor).

## 📋 Como usar no dia a dia

### 🤖 Roteamento Inteligente de Agentes

Você não precisa se lembrar do nome de cada especialista. O sistema analisa seu pedido e aplica a persona adequada automaticamente:

```markdown
Você: "Adicione autenticação JWT e proteja as rotas da API"
IA: 🤖 Applying knowledge of @security-auditor + @backend-specialist...
```

### 🔁 O Ciclo de Entrega (Execution Loop)

Para features complexas, refatorações ou novos módulos, ative a skill `execution-loop` — é o que permite à IA **trabalhar sozinha até o resultado ficar realmente bom**, em vez de parar na primeira versão que compila:

1. **00 Brainstorm:** Alinhamento de escopo e perguntas socráticas.
2. **01 Espec:** Documento de requisitos com Rubrica de QA (critérios de aceite numerados).
3. **02 Plan:** Plano de tarefas mapeado item a item.
4. **03 Execução:** Registro rastreável de comandos, código e diffs.
5. **04 QA:** Auditoria estrita com nota 0 a 10 por critério, com evidência re-derivada (não basta "parece certo").

> 🔁 **Se qualquer critério tirar nota menor que 10, o loop não entrega — ele volta sozinho para o Debug/Espec e tenta de novo**, até 5 ciclos. Isso é o que diferencia o `execution-loop` de pedir "faça X": aqui a IA se audita e se corrige antes de te devolver o trabalho.

### 🏭 SIPs: Projetos Especialistas Compartilhados (`superiaprojects-criar-sip`)

Quando mais de um projeto seu usa a mesma tecnologia (ex: n8n, marketing, um banco de dados específico), não faz sentido duplicar skills e conhecimento em cada repositório. A skill `superiaprojects-criar-sip` transforma um repositório em um **SIP (Super IA Projects especialista)**: um hub central que concentra toda a inteligência daquele domínio — skills, agents, workflows, exemplos reais — e fica disponível **sob demanda** para qualquer outro projeto, via uma skill-ponte leve (`sip-<domínio>`) instalada no projeto consumidor.

Na prática: em vez de cada projeto reinventar (ou copiar e desatualizar) o conhecimento de n8n, todos eles consultam o mesmo hub, que aprende e evolui continuamente.

**SIPs existentes:**

- **`SIP - N8N`**: Hub de automações, nós de código, expressões e padrões arquiteturais de n8n. Por isso este repositório (`0 Padrões`) não carrega mais as skills `n8n-*` localmente — elas migraram para o hub dedicado, que em breve ganha seu próprio repositório público no GitHub.
- **[`SIP - Marketing`](https://github.com/Felipelbahia/superiaprojects-marketing)**: Hub de copywriting, SEO, growth e estratégia de conteúdo, já publicado no GitHub.

### 📁 Prompts Reutilizáveis (`prompts-template/`)

Dentro da pasta `prompts-template/`, você encontra roteiros prontos para:

- `01-atualizar-projeto-existente.md`: Alinhar um projeto já existente ao kit, na primeira vez ou depois de atualizações, sem perder as regras locais.
- `02-criar-projeto-do-zero.md`: Inicializar um projeto do zero via `project-initializer`.
- `04-buscar-bibliotecas-prontas.md`: Avaliar reuso de software open source via `oss-scout`.

---

## 🔌 Ferramentas Recomendadas: Servidores MCP & Extensões

O ecossistema opera de forma integrada com ferramentas que potencializam os agentes de IA.

### 🌟 Servidores MCP Selecionados
Modelos prontos no arquivo [`mcp.example.json`](mcp.example.json):
- **`context7`**: Consulta de documentações técnicas oficiais e atualizadas.
- **`firecrawl`**: Web scraping avançado e pesquisas com saída em Markdown limpo.
- **`chrome-devtools`**: Depuração visual no navegador, acessibilidade (a11y) e Core Web Vitals.
- **`testsprite`**: Automação e execução autônoma de planos de testes a partir de PRDs.
- **`stitch`**: Prototipagem de interfaces e geração de design systems.
- **`supabase`**: Consultas SQL, migrações e sincronização de tipos TypeScript.
- **`api-tools`**: Leitura e validação de contratos OpenAPI / Swagger.
- **`notion`**: Sincronização de documentos, notas e PRDs direto no Notion.

### 🧩 Extensões de IDE (VS Code / Antigravity / Cursor)
Recomendadas automaticamente via [`.vscode/extensions.json`](.vscode/extensions.json):
- **IA:** Claude Code, Kilo Code.
- **Produtividade:** Peacock (cores de workspace), Material Icon Theme, Rainbow CSV, Office Viewer, PDF Viewer.
- **Web & APIs:** Thunder Client (requisições REST integradas), CSS Peek, Svelte.
- **Python & Infra:** Suíte oficial Python (Pylance) e Docker.

👉 *Veja o [**Guia Completo de Setup (SETUP.md)**](SETUP.md) para instruções passo a passo e instalação em lote.*

**Hook de commit (uma vez por clone):** `git config core.hooksPath .githooks`. O `.githooks/pre-commit` roda `sync_entrypoints.py --check` e `sync_rules.py --check` (~2 s) e recusa o commit se algum falhar.

---

## 📝 Atualizações Recentes

- **03/11/2026:** As skills `n8n-*` (automações, código JS/Python, expressões, validação) saíram deste repositório e viraram o hub dedicado **`SIP - N8N`** — em breve com repositório próprio no GitHub. Projetos que precisam de n8n passam a consultá-lo via skill-ponte, em vez de duplicar o conhecimento localmente.
- **03/11/2026:** Nova skill **`superiaprojects-criar-sip`**, que padroniza a criação desses hubs especialistas (SIPs) para qualquer domínio.
- **03/11/2026:** Publicado o **[`SIP - Marketing`](https://github.com/Felipelbahia/superiaprojects-marketing)** no GitHub.
- **03/11/2026:** Logo atualizada (wordmark "Futuro" em preto, legível em fundo claro).

---

## 🤝 Como Contribuir

Quer criar novas skills ou agentes? Veja o nosso [Guia de Contribuição (CONTRIBUTING.md)](CONTRIBUTING.md) para entender a metodologia TDD-for-skills e os padrões de validação.

---

## 🙏 Créditos & Agradecimentos

O **Super IA Projects** foi construído e enriquecido a partir de contribuições valiosas do ecossistema open-source:

- **[`obra/superpowers`](https://github.com/obra/superpowers)** por **Jesse Vincent (obra)**: Grande inspiração para a filosofia de skills modulares, meta-skills de bootstrapping, TDD de documentação (`writing-skills`) e estrutura de repositório público.
- **Antigravity Kit** por **Vudovn**: Base inicial de agentes e templates de workflows.
- **Anthropic & Claude Community**: Padrões de engenharia de prompts, segurança e boas práticas de CLI.

---

## 📬 Contato & Comunidade

- **Autor:** Felipe Bahia
- **Empresa:** [Futuro Mercado](https://www.futuromercado.com.br)
- **Email:** [felipe@futuromercado.com.br](mailto:felipe@futuromercado.com.br)
- **Instagram:** [@felipelbahia](https://instagram.com/felipelbahia)

---

## 📄 Licença

Distribuído sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
