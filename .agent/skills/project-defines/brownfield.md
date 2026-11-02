# Brownfield mode: adopting the contract in an existing project

Use when the project **already exists** (code, docs, history) and the owner wants `_projectdefines/`. The documents first describe **what exists**; what the owner wants to change comes later through the document-first rule. Ready prompt: `prompts/brownfield.md`.

## Safety (non-negotiable)
- Read-only on everything that exists. **Never change, move or delete code or docs.** No installs, no running the project or its scripts, no network except Context7/official docs.
- Secrets: list variable **names** only, never values.
- The only things this mode writes: `_projectdefines/`, and (after the owner's approval) the `## Stack` block and the Gate text in the project's rules file.
- Anything that needs a code change becomes a plan item, never an edit.

## 1. Which documents apply (by project type)

| Project type | BRIEF | PRD | ARCHITECTURE | APP-FLOW | PATTERNS | SCHEMA |
|---|---|---|---|---|---|---|
| App with an interface (web/mobile/desktop) | yes | yes | yes | yes | yes | yes, if it has data |
| API / backend / service | yes | yes | yes | **N/A** | **N/A** | yes |
| Scripts / CLI / data pipeline | short | short | yes | **N/A** | **N/A** | only if there are persistent data or file contracts (CSV, JSONL, tables) |
| Automation (n8n) / content / rules-only workspace | short | N/A | light | N/A | N/A | N/A |

A document that does not apply is recorded **as N/A with the reason** in the plan. Never invent screens, routes or visual rules to fill a template. Inside applicable documents, rows that do not apply (login, web headers, web performance targets) are marked N/A with the reason.

## 2. Labels (every statement carries one)
- `[as-built]`: found in the code or files, **with the evidence on the same line** (file:line or the command that proved it).
- `[assumption]`: inferred, not confirmed. Becomes a decision only when the owner answers.
- `[owner]`: said by the owner.
Never state a fact you did not verify; write "not verified" instead.

## 3. Procedure
1. **Preflight.** Type of project; `## Stack` block; lockfile and manifests; the ficha in `0 Padrões/projetos/`; rules files; existing docs (`ARCHITECTURE.md`, `CODEBASE.md`, `PATTERNS.md`, README, roadmap/backlog, past loops); legacy placement (`execution-loops/`, `handoffs/` at the root).
2. **Discover with evidence.** Real commands, greps, file reads: topology, scripts, routes/screens, data (types, tables, files), integrations, env var names, tests, tech debt, mocks, security gaps. Also compare the **ficha and README against the code** (if the ficha is not reachable, write "ficha not compared" as an open question) and record every divergence (for example a ficha that names a framework the manifest does not contain).
3. **Draft every applicable document at once, as-built** (the facts already exist in the code, so they do not wait for the owner). Use `templates/`. Propose the size (S/M/L) with reasons. Put unknowns in *Open questions* with a recommended default. Fill the BRIEF's Launch profile as-built (`launch-profile.md` section 5).
4. **Gaps and divergences** (mocks, route without login, no tests, docs that describe things that do not exist, counts that disagree between documents) go to *Open decisions* or backlog, each with both versions and the evidence. A baseline security gap becomes a **blocking** item or a written exception; never only a note.
5. **Approval, one document at a time, in order** (BRIEF → PRD → ARCHITECTURE → APP-FLOW → PATTERNS → SCHEMA), in the gate format of `SKILL.md`. Approved as-built documents become the **baseline contract**.
6. **Plan** (`templates/IMPLEMENTATION-PLAN.md`): add **Phase 0 — Baseline** (see `tracker.md`), keep Phase 1 as the adoption itself, and turn the existing backlog (for example `BackLog/Roadmap.md`) into items of the next phases, keeping its origin in *Covers*.
7. **Version check** (section 5).
8. **Stack block and rules** (section 6).

## 4. Existing documentation
- **Never delete.** `ARCHITECTURE.md` and `PATTERNS.md` at the root are **absorbed** by the new documents; the root file gets a pointer only with the owner's authorization. `CODEBASE.md` stays as the code inventory.
- Ficha, README, roadmap, old loops and handoffs are **evidence, not truth**: when they disagree with the code, the code wins and the divergence is listed.
- Legacy `execution-loops/` and `handoffs/` at the root keep working (kit legacy rule). Offer the migration to `.agent/plans/`; never do it unasked.
- If the project's `.gitignore` hides `.agent/plans/` or loop folders, list it as a backlog item (it hides the project history).

## 5. Version check (replaces a separate "upgrade" job)
Read the manifests and lockfile. For each main technology **and the runtime itself** (Python, Node, etc.), consult Context7 with `resolve-library-id` **and** `query-docs`: the docs of the **installed** version (versioned doc IDs) and the current stable. Resolving the ID is not enough, and nothing about "current", "stable" or "end of life" may come from memory: if the lookup is impossible, write "not verified" and make the check a backlog item. A technology behind the current stable becomes a **backlog item** with the official upgrade guide as source (skills `dependency-upgrade`, `react-modernization` help when it is executed). **Never upgrade during adoption.** Projects with only the standard library or no dependencies: record "no external dependencies".

## 6. Stack block and rules file
- Prepare the `## Stack` block (format in CLAUDE.md, names only, no frozen versions) and the Gate text in the draft ARCHITECTURE (*Stack record*).
- After the owner approves ARCHITECTURE, write them into the rules file (create a minimal one from `prompts/handoff.md` if none exists) and run `sync_rules.py`. If the project's rules files differ from each other, **choose the source with the owner first**, so no local rule is lost.
- Until then, the block lives only in the draft.

## 7. Closing the adoption
Phase 1 gate: all applicable documents approved, plan frozen, rules updated, owner's ok. From then on the Docs Gate applies as in any project.
