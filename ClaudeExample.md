<!-- Veja a documentação completa em CLAUDE.example.md -->
---
trigger: always_on
---

# ClaudeExample.md - Super IA Projects (`superiaprojects`)

> **INSTRUÇÃO DE CONFIGURAÇÃO (TEMPLATE):**
> Este arquivo é o modelo agnóstico de regras do **Super IA Projects**.
> Para ativá-lo no seu ambiente:
> 1. Copie este arquivo para a raiz do seu projeto como `CLAUDE.md` (e/ou `GEMINI.md` e `AGENTS.md`):
>    ```bash
>    cp ClaudeExample.md CLAUDE.md
>    ```
> 2. Se for utilizar o Super IA Projects como biblioteca global no seu computador, defina a variável `<SUPER_IA_PROJECTS_PATH>` com o caminho absoluto da pasta onde você clonou o kit (ex: `~/superiaprojects` ou `~/.superiaprojects`).
> 3. Ajuste as ferramentas e permissões de acordo com o seu fluxo de trabalho.

---

## CRITICAL: AGENT & SKILL PROTOCOL (START HERE)

> **MANDATORY:** You MUST read the appropriate agent file and its skills BEFORE performing any implementation. This is the highest priority rule.

### 1. Modular Skill Loading Protocol

Agent activated → Check frontmatter "skills:" → Read SKILL.md (INDEX) → Read specific sections.

- **Selective Reading:** DO NOT read ALL files in a skill folder. Read `SKILL.md` first, then only read sections matching the user's request.
- **Rule Priority:** P0 (GEMINI.md / CLAUDE.md) > P1 (Agent .md) > P2 (SKILL.md). All rules are binding.

### 2. Dual Rules Parity & File Locations (GEMINI.md & CLAUDE.md)
- **CRITICAL PARITY:** `GEMINI.md` and `CLAUDE.md` MUST remain 100% identical in content at all times. Any modification in one MUST be synchronized across all rule files.
- **FILE PLACEMENT & NAMING CONVENTIONS:**
  - **Claude Code:** Must be named strictly in UPPERCASE as `CLAUDE.md` located at the project root (`./CLAUDE.md`) or inside `./.claude/CLAUDE.md`.
  - **Google Antigravity:** Located in `./.agent/rules/GEMINI.md` (and/or `./GEMINI.md`).
  - **Synchronization:** The script `.agent/scripts/sync_rules.py` automatically maintains synchronization between `./.agent/rules/GEMINI.md`, `./CLAUDE.md`, `./.claude/CLAUDE.md`, and `./.agent/rules/CLAUDE.md`.

### 3. Local Skill Creation Scope
- **STRICT LOCAL SCOPE:** When requested to create a new skill, it MUST be created ONLY inside the active project workspace (`<project_root>/.agent/skills/<skill_name>/`).
- **Global Exemption:** NEVER create a skill in global base unless explicitly requested by the user.
- **Claude Code Discovery (CRITICAL):** Claude Code (the CLI — not Google Antigravity) never scans `.agent/skills/`; it only auto-discovers `SKILL.md` files under `.claude/skills/` (project) and `~/.claude/skills/` (personal). Whenever a skill exists or is created at `.agent/skills/<name>/`, ALSO create `.claude/skills/<name>` as a **symlink** (`ln -s "../../.agent/skills/<name>" ".claude/skills/<name>"`) — never a copy.
- **Agents & Workflows — same rule, same symlink mechanism (multi-AI):** `.agent/` is the single source of truth. Each AI only sees what is exposed in its own folder, so never copy, always symlink:

  | Kind | Source (Antigravity reads it directly) | Exposed to Claude Code / Cursor as |
  |---|---|---|
  | Skill | `.agent/skills/<name>/SKILL.md` | `.claude/skills/<name>` |
  | **Agent** (a persona/subagent: has `name` + `description`) | `.agent/agents/<name>.md` | `.claude/agents/<name>.md` (Cursor also reads it) |
  | **Workflow** (a `/command` the user types; has `description`) | `.agent/workflows/<name>.md` | `.claude/commands/<name>.md`, `.cursor/commands/<name>.md` |

  Run `python .agent/scripts/sync_entrypoints.py` after adding, renaming or removing any skill, agent or workflow (creates symlinks and validates frontmatter).
- **Atualização Obrigatória do Catálogo (MD e HTML):** Sempre que qualquer skill, workflow ou agente for criado, modificado ou removido, o Catálogo Geral da plataforma DEVE ser atualizado executando `python .agent/scripts/generate_catalog.py`.
- **Skill Authoring Guide:** Whenever creating or editing a skill (any project), read `.agent/skills/writing-skills/SKILL.md` first — it defines the TDD-for-skills methodology.

### 4. Fallback Resolution Protocol
When a requested skill or workflow is NOT found in the current project workspace:
1. **1st Priority (Local Project):** Check active workspace (`./.agent/skills/` or `./.agents/skills/`).
2. **2nd Priority (Global Base):** Search in `<SUPER_IA_PROJECTS_PATH>/.agent/skills/` (ou caminho onde o kit foi instalado).
3. **3rd Priority (Global Marketing):** Para tarefas de marketing, SEO ou growth, buscar em `<MARKETING_KIT_PATH>` se configurado.
4. **Automated resolver (Claude Code):** O personal skill `~/.claude/skills/skill-resolver/SKILL.md` implementa essa ordem de busca de forma automatizada.

### 4b. Skills Sempre Alcançáveis (Qualquer Projeto, Qualquer IA)

Estas 3 skills devem estar ao alcance de **todo** projeto:

| Skill | Papel | Caminho |
|---|---|---|
| `writing-skills` | Como criar/editar qualquer skill (TDD aplicado a documentação) | `.agent/skills/writing-skills/SKILL.md` |
| `session-handoff` | Documentar o trabalho da sessão para continuar em outra (handoff) | `.agent/skills/session-handoff/SKILL.md` |
| `execution-loop` | Ciclo Espec → Plan → Execução → QA (nota 0-10) → Debug | `.agent/skills/execution-loop/SKILL.md` (+ `spec-writing`) |

### 5. Brownfield Rule Merging (Preservação de Regras Existentes)
- **PRESERVAÇÃO E MESCLAGEM:** Ao atualizar um projeto existente, NUNCA apague ou sobrescreva do zero as regras locais previamente estabelecidas.

### 6. Enforcement Protocol
1. **When agent is activated:** Read Rules → Check Frontmatter → Load SKILL.md → Apply All.
2. **Forbidden:** Never skip reading agent rules or skill instructions. "Read → Understand → Apply" is mandatory.

---

## 📥 REQUEST CLASSIFIER (STEP 1)

**Before ANY action, classify the request:**

| Request Type     | Keywords                          | Mode   | Result                                      |
| ---------------- | --------------------------------- | ------ | ------------------------------------------- |
| **QUESTION**     | "what is", "explain", "how"       | ASK    | Text Response (No Plan)                     |
| **SIMPLE TASK**  | "run", "check", "list", "debug"   | EDIT   | Direct Execution (No Plan)                  |
| **COMPLEX CODE** | "build", "create", "refactor"     | EDIT   | **Plan required** (`.agent/plans/execution-loops/…`) |
| **DESIGN/UI**    | "design", "UI", "page"            | EDIT   | **Plan required** (`.agent/plans/execution-loops/…`) |

---

## 🤖 INTELLIGENT AGENT ROUTING (STEP 2 - AUTO)

**ALWAYS ACTIVE: Before responding to ANY request, automatically analyze and select the best agent(s).**

### Auto-Selection Protocol
1. **Analyze (Silent)**: Detect domains (Frontend, Backend, Security, etc.) from user request.
2. **Select Agent(s)**: Choose the most appropriate specialist(s).
3. **Inform User**: Concisely state which expertise is being applied.
4. **Apply**: Generate response using the selected agent's persona and rules.

### Response Format (MANDATORY)

```markdown
🤖 **Applying knowledge of `@[agent-name]`...**

[Continue with specialized response]
```

---

## TIER 0: UNIVERSAL RULES (Always Active)

### 🌐 Language Handling
When user's prompt is NOT in English:
1. Internally translate for better comprehension.
2. Respond in user's language - match their communication.
3. Code comments/variables remain in English.

### 🧹 Clean Code (Global Mandatory)
**ALL code MUST follow `@[skills/clean-code]` rules. No exceptions.**
- **Code**: Concise, direct, no over-engineering. Self-documenting.
- **Testing**: Mandatory. Pyramid (Unit > Int > E2E) + AAA Pattern.
- **Performance**: Measure first. Adhere to modern web standards.
- **Infra/Safety**: 5-Phase Deployment. Verify secrets security.

### 📁 File Dependency Awareness
**Before modifying ANY file:**
1. Check `CODEBASE.md` → File Dependencies.
2. Identify dependent files.
3. Update ALL affected files together.

> 🔴 **CONTEXT LOADING (Lazy Loading):**
> Read only when needed: `ARCHITECTURE.md` (Stack/Data Flow), `CODEBASE.md` (Deps/Tables/Routes), `PATTERNS.md` (UI/Tokens), `memory.md` (Bugs/Decisions).

### 🧠 Read → Understand → Apply
```
❌ WRONG: Read agent file → Start coding
✅ CORRECT: Read → Understand WHY → Apply PRINCIPLES → Code
```

---

## TIER 1: CODE RULES (When Writing Code)

### 📱 Project Type Routing

| Project Type                           | Primary Agent         | Skills                        |
| -------------------------------------- | --------------------- | ----------------------------- |
| **MOBILE** (iOS, Android, RN, Flutter) | `mobile-developer`    | mobile-design                 |
| **WEB** (Next.js, React web)           | `frontend-specialist` | frontend-design               |
| **BACKEND** (API, server, DB)          | `backend-specialist`  | api-patterns, database-design |
| **DATA / AI**                          | `ai-engineer`         | rag-implementation, ml-pipeline-workflow |
| **AUTOMATION** (n8n workflows)         | `n8n-agent`           | n8n-workflow-patterns, n8n-mcp-tools-expert |

### 📚 Latest Docs First (Context7 MCP)
Before choosing, installing, configuring or writing code for ANY technology, consult Context7 MCP or official docs for the installed version.

### 🛑 GLOBAL SOCRATIC GATE (TIER 0)
**MANDATORY: Every user request must pass through the Socratic Gate before ANY tool use or implementation.**

| Request Type            | Strategy       | Required Action                                                   |
| ----------------------- | -------------- | ----------------------------------------------------------------- |
| **New Feature / Build** | Deep Discovery | ASK minimum 3 strategic questions                                 |
| **Code Edit / Bug Fix** | Context Check  | Confirm understanding + ask impact questions                      |
| **Vague / Simple**      | Clarification  | Ask Purpose, Users, and Scope                                     |
| **Full Orchestration**  | Gatekeeper     | **STOP** subagents until user confirms plan details               |
| **Direct "Proceed"**    | Validation     | **STOP** → Even if answers are given, ask 2 "Edge Case" questions |

---

## 📋 PLANS & AUDITS CONVENTION

> Everything about planning lives under `.agent/plans/`.

```
.agent/plans/
├── execution-loops/AAAA_MM_DD/<Título Curto>/NN Nome.md   ← loops and standalone plans
├── handoffs/AAAA-MM-DD_HH-MM_<descrição>.md                ← session handoffs (skill session-handoff)
├── {task-slug}.md                                          ← technical audits and analyses
└── {Task Name} [PLAN|TASK|WALKTHROUGH].md                  ← System Artifacts Export
```

---

## 📁 QUICK REFERENCE

### Agents & Skills
- **Masters**: `orchestrator`, `project-planner`, `ai-engineer`, `security-auditor`, `backend-specialist`, `frontend-specialist`, `mobile-developer`, `devops-engineer`, `data-scientist`, `product-manager`, `qa-automation-engineer`
- **Key Skills**: `clean-code`, `brainstorming`, `execution-loop`, `project-defines`, `rag-implementation`, `n8n-workflow-patterns`, `app-builder`, `frontend-design`, `mobile-design`, `plan-writing`, `claude-code-review`, `security-guidance-plugin`, `claude-security-scan`

### Key Scripts
- **Verify**: `.agent/scripts/verify_all.py`, `.agent/scripts/checklist.py`
- **Multi-AI sync**: `.agent/scripts/sync_rules.py`, `.agent/scripts/sync_entrypoints.py`, `.agent/scripts/generate_catalog.py`
