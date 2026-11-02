# Prompt — Expand the plan (D-08)

Act as a senior technical lead (`project-planner`, with `plan-writing`). Write phases 2+ of `IMPLEMENTATION-PLAN.md` from the approved documents. Do not write implementation code.

Rules:
- Inspect the existing project, if any. Reuse its stack and conventions unless ARCHITECTURE explicitly requires a change.
- Waterfall phases; inside each, small items. **One item = one `execution-loop` run.** Each item has: ID (T-xx), title, *Covers* (F-xx / S-xx / E-xx), *Depends*, and one *ready when* line. An item without coverage is refused; a feature without an item is a gap.
- Do not put detailed specs or plans in the tracker. Specs and plans of each item are created later by its loop and linked.
- Suggested order (adapt): project foundation and environment → shared visual base → **a runnable skeleton** → authentication → core data → primary journey → secondary features → error/empty states → responsive and accessibility pass → tests and performance → security hardening → launch readiness.
- Build the **launch phase** from the BRIEF's Launch profile, exactly as `launch-profile.md` section 3 says: one `L-xx` item per yes, plus `L-00` (gate). Place it just before the final gate; the seeds it verifies must already be build items.
- Tag every item `reuso: buscar | plataforma | construir` from the ARCHITECTURE capabilities table. A capability that is not in the table: add the line "search before the Espec" (skill `oss-scout`).
- The foundation item writes the `## Stack` block (format in CLAUDE.md) in the project's rules file, after consulting Context7, and runs `sync_rules.py`.
- Each phase ends with a gate: automated checks (`checklist.py`) plus the owner's ok, and a plain-language "how to see it working".
- Security baseline rows (ARCHITECTURE section 5) must each land in a named item. The security hardening item runs skill `vibecoding-security-audit` (modules per `launch-profile.md` section 6) and reports its findings. Mocks, if any, are listed under *Mocks*.
- Size L: write the master only (platform core → visual base → one minimal module end to end → remaining modules by dependency → integrations → hardening → launch). Each module's definition is the first item of its phase. Add the tenant-isolation test as a mandatory gate item.
- Identify contradictions or missing information before presenting the plan.

Inputs: all approved documents.

Output:
1. The updated `_projectdefines/IMPLEMENTATION-PLAN.md` (Panel, Open decisions, Mocks, phases 2+ with gates) as `status: draft`.
2. A traceability table: feature → screen → entity → item.
3. The **owner approval summary** in the owner's language: the phases in order, 1 line each · what will be visible first · recommended default · multiple choice. After approval the structure is frozen.
