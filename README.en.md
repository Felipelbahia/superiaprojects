<div align="center">
  <img src="assets/logo.png" alt="Futuro Mercado" width="340" />
  <h1>Super IA Projects (<code>superiaprojects</code>)</h1>
  <p><strong>The Agentic Engineering Framework</strong></p>
  <p>Modular Skills, Multi-AI Dual Parity Rules, Autonomous Specialists, and Interactive Visual Catalog.</p>

---

> **Authorship:** Created and maintained by **Felipe Bahia** ([Futuro Mercado](https://www.futuromercado.com.br)).
> **Version:** `v1.0.0` · **Last Updated:** November 3, 2026
> Inspired by the frictionless design of [`obra/superpowers`](https://github.com/obra/superpowers) and engineered for agile pair programming across **Claude Code**, **Google Antigravity**, and **Cursor**.

---

## ⚡ Why Super IA Projects?

AI-assisted coding frequently suffers from unstable context, contradictory rules, and skills that cannot be easily shared across CLI tools and IDEs.

**Super IA Projects** solves this by providing a unified, battle-tested agentic engineering system:

- 🎯 **True Multi-AI Parity (Dual Rules Engine):** 100% identical rules automatically synchronized between `CLAUDE.md` (Claude Code) and `AGENTS.md` (Antigravity and other tools), both at the root. Coming from an older kit? `GEMINI.md` and `.agent/rules/` are legacy: `python3 .agent/scripts/sync_rules.py --clean-legacy` lists what is left and deletes only after you say yes (anything that differs from `CLAUDE.md` is kept for you to review).
- 🧩 **Modular & Composable Skills:** Over 220 plug-and-play skills covering web & mobile development, automation pipelines, robust web scraping (Firecrawl), and clean architecture.
- 🔄 **The Execution Loop:** A strict, auditable delivery methodology: *Brainstorm → Spec → Plan → Execution → QA (scored 0 to 10 with verifiable proof)*. If any QA criterion scores below 10, the skill restarts the cycle on its own (Debug → Spec) and tries again — up to 5 cycles — instead of shipping something "mostly done".
- 🏭 **SIPs (Specialist Super IA Projects):** Hub projects that concentrate all the intelligence (skills, agents, workflows) of a specific domain (e.g. n8n, marketing) in one place, shared on demand with any project that needs it — without duplicating knowledge across repos.
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

For non-trivial features, refactors, or new modules, invoke the `execution-loop` skill — it's what lets the AI **keep working on its own until the result is actually good**, instead of stopping at the first version that compiles:

1. **00 Brainstorm:** Socratic discovery, scope alignment, and edge-case exploration.
2. **01 Spec:** Product specification with an Acceptance Rubric (criteria numbered).
3. **02 Plan:** Granular task breakdown mapping 1-to-1 with rubric items.
4. **03 Execution:** Traceable execution log of shell commands, files touched, and diffs.
5. **04 QA:** Strict audit graded 0 to 10 per criterion, with evidence re-derived at QA time (not just "looks right").

> 🔁 **If any criterion scores below 10, the loop doesn't ship — it restarts itself (Debug → Spec) and tries again**, up to 5 cycles. That's what sets `execution-loop` apart from just asking the AI to "do X": it audits and corrects itself before handing the work back to you.

### 🏭 SIPs: Shared Specialist Projects (`superiaprojects-criar-sip`)

When more than one of your projects uses the same technology (e.g. n8n, marketing, a specific database), it makes no sense to duplicate skills and knowledge in every repo. The `superiaprojects-criar-sip` skill turns a repository into a **SIP (Specialist Super IA Project)**: a central hub that concentrates all the intelligence of that domain — skills, agents, workflows, real examples — and becomes available **on demand** to any other project, through a lightweight bridge skill (`sip-<domain>`) installed in the consuming project.

In practice: instead of every project reinventing (or copying and letting go stale) n8n knowledge, they all consult the same hub, which keeps learning and evolving.

**Existing SIPs:**

- **`SIP - N8N`**: Hub for n8n automations, code nodes, expressions, and architectural patterns. This is why this repository (`0 Padrões`) no longer ships the `n8n-*` skills locally — they moved to the dedicated hub, which will soon have its own public GitHub repository.
- **[`SIP - Marketing`](https://github.com/Felipelbahia/superiaprojects-marketing)**: Hub for copywriting, SEO, growth, and content strategy, already published on GitHub.

### 📁 Reusable Prompts (`prompts-template/`)

Inside `prompts-template/`, you will find ready-to-use recipes:

- `01-atualizar-projeto-existente.md`: Align an existing project with the kit, the first time or after kit updates, keeping its local rules.
- `02-criar-projeto-do-zero.md`: Scaffold new applications from scratch via `project-initializer`.
- `04-buscar-bibliotecas-prontas.md`: Evaluate open-source library reuse with `oss-scout`.

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

## 📝 Recent Updates

- **11/03/2026:** The `n8n-*` skills (automations, JS/Python code, expressions, validation) left this repository and became the dedicated **`SIP - N8N`** hub — soon with its own GitHub repository. Projects that need n8n now consult it through a bridge skill, instead of duplicating the knowledge locally.
- **11/03/2026:** New skill **`superiaprojects-criar-sip`**, which standardizes the creation of these specialist hubs (SIPs) for any domain.
- **11/03/2026:** Published **[`SIP - Marketing`](https://github.com/Felipelbahia/superiaprojects-marketing)** on GitHub.
- **11/03/2026:** Updated the logo (the "Futuro" wordmark is now black, legible on light backgrounds).

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
