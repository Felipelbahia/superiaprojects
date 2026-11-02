<div align="center">
  <img src="assets/logo.png" alt="Futuro Mercado" width="340" />
  <h1>Super IA Projects (<code>superiaprojects</code>)</h1>
  <p><strong>The Agentic Engineering Framework</strong></p>
  <p>Modular Skills, Multi-AI Dual Parity Rules, Autonomous Specialists, and Interactive Visual Catalog.</p>

  <p>
    <a href="https://www.futuromercado.com.br"><img src="https://img.shields.io/badge/Futuro%20Mercado-Website-gold?style=for-the-badge&logo=googlechrome&logoColor=black" alt="Website" /></a>
    <a href="https://instagram.com/felipelbahia"><img src="https://img.shields.io/badge/Instagram-@felipelbahia-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram" /></a>
    <a href="mailto:felipe@futuromercado.com.br"><img src="https://img.shields.io/badge/Contact-felipe@futuromercado.com.br-blue?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" /></a>
    <img src="https://img.shields.io/badge/Version-v1.0.0-blueviolet?style=for-the-badge" alt="Version" />
    <img src="https://img.shields.io/badge/Updated-Nov%201%2C%202026-informational?style=for-the-badge" alt="Updated" />
  </p>

  <p>
    <a href="README.md">🇧🇷 Leia em Português</a> | <strong>English</strong>
  </p>
</div>

---

> **Authorship:** Created and maintained by **Felipe Bahia** ([Futuro Mercado](https://www.futuromercado.com.br)).  
> **Version:** `v1.0.0` · **Last Updated:** November 1, 2026  
> Inspired by the frictionless design of [`obra/superpowers`](https://github.com/obra/superpowers) and engineered for agile pair programming across **Claude Code**, **Google Antigravity**, and **Cursor**.

---

## ⚡ Why Super IA Projects?

AI-assisted coding frequently suffers from unstable context, contradictory rules, and skills that cannot be easily shared across CLI tools and IDEs.

**Super IA Projects** solves this by providing a unified, battle-tested agentic engineering system:

- 🎯 **True Multi-AI Parity (Dual Rules Engine):** 100% identical rules automatically synchronized across `CLAUDE.md`, `GEMINI.md`, and `.cursorrules`.
- 🧩 **Modular & Composable Skills:** Over 220 plug-and-play skills covering web & mobile development, automation pipelines, robust web scraping (Firecrawl), and clean architecture.
- 🔄 **The Execution Loop:** A strict, auditable delivery methodology: *Brainstorm → Spec → Plan → Execution → QA (scored 0 to 10 with verifiable proof)*.
- 📊 **Interactive Visual Dashboard:** A responsive HTML catalog (`catalog.html`) and markdown directory (`.agent/CATALOG.md`) dynamically generated from your codebase.
- 🛡️ **Zero Data Leakage:** Private project sheets, execution loop run histories, and machine-specific configs are completely isolated via `.gitignore`.

---

## 📦 What's Included

- **130+ Specialist Personas** (`.agent/agents/`): Domain experts (Frontend, Mobile, Backend, Security, DevOps, QA, Product).
- **220+ Procedural Skills** (`.agent/skills/`): Actionable workflows with embedded scripts and verification routines.
- **110+ Workflows** (`.agent/workflows/`): Quick `/slash` commands for Claude Code and Cursor.
- **Agnostic Starter Templates:**
  - `CLAUDE.example.md` (or `ClaudeExample.md`): Clean, machine-agnostic template ready to copy to `CLAUDE.md`.
  - `prompts-template/`: Curated copy-paste prompts for scaffolding, syncing, and refactoring projects.
  - `mcp.example.json`: Pre-configured server list for Model Context Protocol integrations.

---

## 🚀 Quickstart & Setup

### 1-Step Installation:

```bash
git clone https://github.com/your-username/superiaprojects.git
cd superiaprojects
./install.sh
```

The `./install.sh` script automatically:
1. Detects your Python 3 environment.
2. Initializes your `CLAUDE.md` from `CLAUDE.example.md` (without overwriting if you already have one).
3. Creates symlinks for **Claude Code** (`.claude/`) and **Cursor** (`.cursor/`).
4. Generates the unified visual catalog in `catalog.html`.

---

## 📋 Daily Workflow

### 🤖 Intelligent Agent Routing
You never have to memorize individual specialist names. The system analyzes your prompt and auto-applies the right persona:

```markdown
User: "Add JWT authentication and protect all backend API routes"
AI: 🤖 Applying knowledge of @security-auditor + @backend-specialist...
```

### 🔁 The Execution Loop
For non-trivial features, refactors, or new modules, invoke the `execution-loop` skill:

1. **00 Brainstorm:** Socratic discovery, scope alignment, and edge-case exploration.
2. **01 Spec:** Product specification with an Acceptance Rubric (criteria numbered).
3. **02 Plan:** Granular task breakdown mapping 1-to-1 with rubric items.
4. **03 Execution:** Traceable execution log of shell commands, files touched, and diffs.
5. **04 QA:** Strict audit graded 0 to 10 per criterion with verifiable evidence. *(Any grade < 10 restarts the cycle via automated debug).*

### 📁 Reusable Prompts (`prompts-template/`)
Inside `prompts-template/`, you will find ready-to-use recipes:
- `01-atualizar-projeto-existente.md`: Adopt multi-AI standards in brownfield projects without breaking existing code (Merge & Preserve).
- `02-criar-projeto-do-zero.md`: Scaffold new applications from scratch via `project-initializer`.
- `04-buscar-bibliotecas-prontas.md`: Evaluate open-source library reuse with `oss-scout`.
- `08-sincronizar-com-o-kit.md`: Keep projects synchronized with updates from the central kit.
- `template-inteligencia.md`: Inject market intelligence routines (Trends, RSS, hook mining).

---

## 🔌 Recommended Tools: MCP Servers & Extensions

Super IA Projects is built to leverage Model Context Protocol servers and curated IDE extensions.

### 🌟 Selected MCP Servers
Configured in [`mcp.example.json`](mcp.example.json):
- **`context7`**: Consults the latest official library documentation for installed versions (eliminates hallucinations).
- **`firecrawl`**: Deep web searches, site crawls, and markdown extraction.
- **`chrome-devtools`**: Visual browser inspection, accessibility (a11y) audits, and Core Web Vitals profiling.
- **`testsprite`**: Autonomous PRD-to-test-plan generation and execution.
- **`stitch`**: Screen prototyping and design system generation.
- **`supabase`**: SQL queries, database migrations, and TypeScript type sync.
- **`api-tools`**: OpenAPI / Swagger contract validation.
- **`notion`**: Syncs documentation, notes, and PRDs with Notion.

### 🧩 Recommended Extensions (VS Code / Antigravity / Cursor)
Pre-configured in [`.vscode/extensions.json`](.vscode/extensions.json) for 1-click installation:
- **AI & Agents:** Claude Code, Kilo Code.
- **Productivity & File Viewing:** Peacock (workspace coloring), Material Icon Theme, Rainbow CSV, Office Viewer, PDF Viewer.
- **Web & APIs:** Thunder Client (integrated REST client), CSS Peek, Svelte.
- **Python & Infra:** Python Suite (Pylance, Debugpy), Docker.

👉 *Read the [**Complete Setup Guide (SETUP.md)**](SETUP.md) for batch install commands and detailed instructions.*

---

## 🤝 Contributing

We welcome community contributions! Please check our [Contributing Guide (CONTRIBUTING.md)](CONTRIBUTING.md) to learn about our TDD-for-skills methodology, naming standards, and PR requirements.

---

## 🙏 Credits & Acknowledgements

**Super IA Projects** is built upon and inspired by pioneering work in the open-source agent community:

- **[`obra/superpowers`](https://github.com/obra/superpowers)** by **Jesse Vincent (obra)**: Core inspiration for modular skills, documentation-as-TDD (`writing-skills`), and frictionless open-source distribution.
- **Antigravity Kit** by **Vudovn**: Foundational personas and workflow templates.
- **Anthropic & Claude Community**: Prompt engineering patterns, CLI best practices, and security guidelines.

---

## 📬 Contact & Community

- **Author:** Felipe Bahia
- **Company:** [Futuro Mercado](https://www.futuromercado.com.br)
- **Email:** [felipe@futuromercado.com.br](mailto:felipe@futuromercado.com.br)
- **Instagram:** [@felipelbahia](https://instagram.com/felipelbahia)

---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.
