---
name: execution-loop
description: Use when starting a non-trivial new feature, build, refactor, or significant change that needs a documented, quality-gated development cycle — also called "Loop de Execução" — before writing implementation code.
---

# Execution Loop
*(a.k.a. "Loop de Execução")*

## Overview

A repeatable, documented cycle — Specify → Plan → Execute → QA (scored 0-10 per item) → Debug if any item scores below 10, restarting from Specify — that keeps a demand honest against its own stated objectives instead of declaring victory on vibes. Every phase writes a numbered markdown file to a per-run folder, so the whole cycle is auditable after the fact.

This pattern already worked once, ad hoc, in `.agent/plans/auditoria-skill-de-criacao-de-skills.md`: 7 rubric items, cycle 1 found 3 items below 10, cycle 2 closed all 7 at 10/10. This skill generalizes that into a repeatable, discoverable procedure.

## When to Use

- A new feature, build, refactor, or "significant change" (CLAUDE.md's Request Classifier: COMPLEX CODE / DESIGN-UI / New Feature-Build).
- Any task that benefits from an explicit, gradeable definition of "done" instead of an implicit one.
- **NOT** for one-line fixes, pure Q&A, or SIMPLE TASK requests (run/check/list/known-issue debug) — the overhead isn't worth it.
- CLAUDE.md's Global Socratic Gate decides *when* to offer this skill to the user; this skill defines *how* the loop runs once accepted.

## Core Pattern

```
Orchestrate (this skill; dispatch workflow `/orchestrate` only if Execução needs
             several specialists in parallel)
 └─ 00 Brainstorm  → skill: brainstorming              (once — clarify the ask)
 └─ 01 Espec       → skill: spec-writing + rubric here  ⎫
 └─ 02 Plan        → skill: plan-writing                ⎬  cycle 1
 └─ 03 Execução    → skill: executing-plans             ⎪
 └─ 04 QA          → graded here + code-review-checklist⎭
     any item < 10?
        └─ 05 Debug → workflow: /debug + skill: systematic-debugging
        └─ 06 Espec → repeat (cycle 2, counter keeps climbing)
     all items = 10  → loop ends
     5 cycles done, still < 10 → STOP, hand the decision to the human
```

**Reaching the sub-skills/agents/workflows above:** every REQUIRED SUB-SKILL lives at `.agent/skills/<name>/SKILL.md`, every agent at `.agent/agents/<name>.md` (a specialist role, e.g. `code-reviewer`, `qa-automation-engineer`) and every workflow at `.agent/workflows/<name>.md` (a `/command`, e.g. `/orchestrate`, `/debug`, `/tdd-cycle`). If this project doesn't have one locally (the common case — most projects only reference the global base), it's in the same global base this skill itself came from: `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/skills/`, `.../.agent/agents/` or `.../.agent/workflows/`. Resolve it via Rule 4 (Fallback Resolution Protocol) / the personal `skill-resolver` skill — don't assume a bare name means local-only just because this skill doesn't spell out a path for it. Agent vs workflow: an agent is *who* does the work; a workflow is *a procedure you run by typing `/name`*; never look for a workflow inside `agents/`.

## Quick Reference

**Folder & file convention**

| Level | Path | Rule |
|---|---|---|
| Root | `.agent/plans/execution-loops/` (inside the project's `.agent/plans/`, next to its audits and artifact exports; plural name so it never collides with this skill's own folder in `.agent/skills/execution-loop/`) | One per project, created once. **Legacy:** a project that still has `execution-loops/` at its root keeps using it (one history per project) until the owner asks to migrate it (`mv` into `.agent/plans/`, fix the links). |
| Date | `.../AAAA_MM_DD/` | Date the loop **started**. Reuse the existing folder when resuming a loop already in progress — a new day does not mean a new folder. Only a genuinely new demand gets today's date folder. |
| Goal | `.../<Título Curto do Objetivo>/` | Short, human-readable title (same style as CLAUDE.md's `{Task Name}` convention — not a slug). |
| Phase file | `.../NN Nome.md` | Two-digit counter, **never resets** for the life of the run — it keeps climbing across every cycle and restart. |

Phase names, in order: `Brainstorm` → `Espec` → `Plan` → `Execução` → `QA` → `Debug` (Debug only exists for cycles that failed QA).

**Phase contents**

| Phase | Produces | Sub-skill / agent |
|---|---|---|
| Brainstorm | Clarified objective, scope, assumptions, out-of-scope, open questions answered | **REQUIRED SUB-SKILL:** brainstorming |
| Espec | The Problem/Solution/User Stories/Decisions doc, plus a numbered QA rubric appended at the end (see template below), no scores yet. Also: check this project's `.agent/skills/` and the global `0 Padrões/.agent/skills/` (Fallback Resolution Protocol / skill-resolver) for a domain skill the objective needs (e.g. `database-architect`, `mobile-developer`) and name it here for Plan/Execução to use. When the objective adds a new capability (login, payments, PDF, dates, editor...): check the ARCHITECTURE capabilities table; if absent, run skill `oss-scout` (Reuse) before this Espec. When the objective touches a technology: read the project's `## Stack` block and lockfile, then consult Context7 for the **installed** version (CLAUDE.md, "Latest Docs First"). | **REQUIRED SUB-SKILL:** spec-writing (the rubric appendix is this skill's own addition — spec-writing itself is tracker-agnostic) |
| Plan | Step-by-step plan that satisfies every rubric item | **REQUIRED SUB-SKILL:** plan-writing |
| Execução | Log of what was actually done — commands run, files touched, diffs — the evidence trail QA checks against | **REQUIRED SUB-SKILL:** executing-plans (nest workflow `/tdd-cycle` inside this phase for code-heavy items that need strict red-green-refactor) |
| QA | Re-grades the SAME rubric from the latest Espec (see template below). A score is earned by verifiable evidence — a command output, a diff, a passing test — never by self-assessment. | Run skill `code-review-checklist` as a baseline quality gate under every code-shaped item. Dispatch agent `code-reviewer` for a deeper security/performance pass on non-trivial code, and agent `qa-automation-engineer` when an item's evidence requires an E2E/browser flow. None of these replace the rubric grading — they're evidence sources for it. |
| Debug | Only for items scoring < 10: root-cause hypothesis → investigation → fix decision that feeds the next Espec | **REQUIRED SUB-SKILL:** systematic-debugging (and/or workflow `/debug`) |

## Implementation

**Espec rubric template:**
```markdown
| # | Item | Critério de aceite |
|---|------|---------------------|
| 1 | ...  | ...                 |
```

**QA grading template (same items, now scored):**
```markdown
| # | Nota (0-10) | Evidência |
|---|-------------|-----------|
| 1 | ...         | ...       |
```

**Grading rule (non-negotiable):**
- 10/10 = fully met with cited proof. Anything below 10 means "not done yet" — no partial credit for "almost."
- One item below 10 is enough to restart the whole cycle from Espec.
- Never grade Execução from memory — re-derive evidence the same way (`grep`, `diff`, run the actual test/command), exactly as CLAUDE.md's own "never affirm without verifying" rule already requires project-wide.

**Safety valve:** after 5 full cycles still leave any item below 10, STOP. Do not open a 6th Espec automatically. Add a closing note to that QA file naming the remaining gaps, then present them to the user and ask how to proceed (narrow scope, accept a lower bar, bring in a different specialist skill, etc.).

**Resuming vs. starting fresh:** before creating anything, check whether this continues a loop already in progress (the user references it, or an incomplete goal-folder already exists for this exact objective). If so, reuse its date+goal folder and keep the file counter climbing — do not create a new date folder. Only a genuinely new demand gets a fresh date folder.

## Execução Model Rule (Haiku delegation)

**REQUIRED SUB-SKILL:** `opus-haiku` is the single source of this rule (it applies to Execução only). By default the main session keeps Brainstorm, Espec, Plan, QA and Debug diagnosis, and delegates the *writing* of each Plan item to subagents on the cheapest model (`model: "haiku"` on every call).

Loop-specific points (details, retry cap and skip conditions live in the skill):
- The briefing copies the Espec rubric items and the user's requirements **verbatim**; before leaving Execução, compare the subagent reports against the full rubric list.
- QA is never done by the writer. Debug: strong model diagnoses, a cheap subagent applies the fix.
- The Execução log records which items went to which subagent/model.
- Skip the delegation when the user says "sem Haiku" / "faça direto", or per the skill's "Do NOT delegate" list.

## Docs Gate (only when the project has `_projectdefines/`)

No `_projectdefines/` folder: skip this whole section, the loop is unchanged. With the folder, **REQUIRED SUB-SKILL:** project-defines (`conformance.md` for obeying the documents, `tracker.md` for the plan file).

| Phase | Added step |
|---|---|
| Espec | Read the Panel of `_projectdefines/IMPLEMENTATION-PLAN.md`, then only the documents the work touches (reading map in `conformance.md`). Rubric rows that come from a document cite its ID (F-xx, S-xx, E-xx, ADR). Add the fixed row **"Tracker updated with status and links"**. |
| Plan | If the request conflicts with an approved document, the first step is a change proposal for the owner (document-first). Do not edit the document and do not add plan items out of order. |
| Execução / QA | Nothing unlisted enters the code (screen, route, table, dependency, env var). QA re-derives the evidence of every conformance row and of the tracker row; a mismatch means 🐞, never ✅. |
| Close | Update the item's row: status, Spec/Plan/QA links, grade, Panel counters and next exact step. ✅ only at 10/10 with re-derived evidence; one commit whose message starts with the item ID. |

When the loop serves a plan item, name the goal folder `<ID> <Title>` (for example `T-007 Login and session`) so the row finds its files.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Resetting the file counter each cycle (`01 Espec` again in cycle 2) | Counter is global to the run — cycle 2 starts wherever cycle 1 left off |
| Grading QA against a rubric written from memory | Rubric = the numbered items from the most recent Espec, verbatim |
| Creating a new date folder every time you touch an already-running loop | Reuse the existing date+goal folder; only fresh demands get a fresh date |
| Letting the loop run past 5 cycles unattended | Hard stop at 5, hand off to the human |
| Delegating Execução to a subagent without `model: "haiku"`, or with a summarized briefing | Pass the model on every call and copy the rubric/requirements verbatim (see Execução Model Rule) |
| Skipping Brainstorm because "the ask is obvious" | It still runs once — it's what the Socratic Gate already requires before any build |
