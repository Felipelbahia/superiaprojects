# Tracker Protocol (`IMPLEMENTATION-PLAN.md`)

The project map and state. A waterfall of phases; inside each phase, items; each item is one `execution-loop` run. Detailed spec and plan of an item are created later by its loop and **linked** here.

## Structure (template: `templates/IMPLEMENTATION-PLAN.md`)

1. **Panel** (about 10 lines): current phase, next item, **next exact step** (one line), blocked items, progress counts per phase, and the resume prompt.
2. **Open decisions**: change proposals, questions and unconfirmed premises, each with a recommended default.
3. **Mocks**: placeholder data present in the product.
4. **Phases**: one table each, with its gate. Finished phases collapse to one line.

Item columns: `ID · Item · Covers · Depends · Status · Spec · Plan · QA`, plus one *ready when* line per item. *Covers* lists F-xx / S-xx / E-xx (or a cited origin). An item without coverage is refused.

## Statuses

⬜ Backlog → 📝 Specified → 🗺️ Planned → 🔨 In execution → 🔍 In QA → ✅ Done. Also 🐞 In debug and 🚫 Blocked. The statuses mirror the loop phases; Spec, Plan and QA columns stay empty until the loop creates the file, then hold the link.

## Who may edit what

| Who | May change |
|---|---|
| `execution-loop`, alone | Status, Spec/Plan/QA links, date, grade, Panel counters and next exact step, rows of *Mocks*, and **new entries** in *Open decisions* (proposals, questions) |
| Owner approval required | Create, remove or reorder items; *Depends*; *Covers*; *ready when*; gates; anything in *Open decisions* being resolved |

The loop's rubric always contains the fixed row **"Tracker updated with status and links"**, graded with evidence at QA.

## Rules

- **✅ rule:** an item becomes ✅ only when its QA grades are all 10 **and each grade's evidence was re-derived** now. The QA column links the evidence file. If re-derived evidence does not match the log, the item becomes 🐞 on its own row and the owner is told. An owner may order an explicit override: record it on the row as "closed by owner override", with the date.
- **One 🔨 at a time** unless the owner allows parallel items.
- **Cascade:** do not start items of phase N+1 until the gate of phase N is ✅. An item whose *Depends* is not ✅ does not start.
- **Gate of a phase** = automated checks pass **and** the owner's ok. Checks: `checklist.py` (order: Security → Lint → Schema → Tests → UX → SEO → Lighthouse/E2E) from the project's `.agents/scripts/`, or the absolute path `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agents/scripts/checklist.py` when the project has no copy. Final phase: also the owner's lists `Vibecoding - Segurança - Checagem` and `Vibecoding - Lançamento - Checagem` when present. Each gate shows "how to see it working" in plain steps (skill `run`).
- **Commit per ✅ item:** one commit whose message starts with the item ID, so any item can be undone.
- **Loop folders** are named `<ID> <Title>` (for example `T-007 Login and session`) so the row finds its files.
- **Born small:** a new tracker is created together with the BRIEF, as soon as the owner starts the pipeline, and contains only Phase 1 (D-01…D-08). D-08 writes phases 2+ from the approved documents; after the Phase 1 gate the structure is frozen and changes only through the document-first rule.
- **Premise ≠ decision:** unconfirmed premises live under *Open decisions* with a recommended default.

## Brownfield (existing project)

The plan may start with **Phase 0 — Baseline**: items that describe what already exists and works. They become ✅ only with evidence re-derived now **and** the owner's approval. Phase 1 is the adoption itself (documents approved as-built = baseline contract). The existing backlog (for example `BackLog/Roadmap.md`) becomes items of later phases and keeps its origin in *Covers*. After the Phase 1 gate the structure freezes as usual. Procedure: `brownfield.md`.

## Size L layout

- `IMPLEMENTATION-PLAN.md` is the **master**: Panel (current module only), the module list with order, phase summaries.
- Each module has `_projectdefines/modules/<module>/` with its PRD, APP-FLOW, SCHEMA fragment and `plan.md` (item table), created **when the module's turn comes** as the first item of that module's phase.
- Order of phases: platform core (tenancy, login, roles and permissions, audit) → visual base → **one minimal module end to end** to validate the architecture → remaining modules by dependency → integrations → hardening (security, performance, tests) → launch.
- Gates of the platform core and of SCHEMA-core carry a **risk notice** (leak between customers, financial/tax calculation, data migration), the review of `security-auditor` and `architect-review`, and the owner's recorded acceptance. A **tenant-isolation test** (customer A never reads customer B, with canary data and attacks on IDs, search, exports, reports and links) is a mandatory gate item. Human expert review is recommended in the notice, not required.
- The AI reads the master Panel and the current module's files, never the whole project.

## For the owner (include in the template)

How to follow: open the Panel. Signs the AI is lost: it asks what to do next, it edits an approved document, it starts a new phase without a gate. Resume prompt: "Read `_projectdefines/IMPLEMENTATION-PLAN.md`, the Panel first, and continue with the next exact step."
