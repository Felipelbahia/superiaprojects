---
status: draft
approved:
---
# IMPLEMENTATION PLAN

> The project map and state. Protocol: `project-defines/tracker.md`. Born with Phase 1 only; item D-08 writes phases 2+ from the approved documents.

## Panel

- Size: S | M | L
- Current phase: 1 — Define
- Next item: D-01
- **Next exact step:** Ask the sizing questions of the BRIEF, one at a time.
- Blocked: 0
- Progress: Phase 1: 0/8
- **Resume prompt:** "Read `_projectdefines/IMPLEMENTATION-PLAN.md`, the Panel first, and continue with the next exact step."

## Open decisions

Change proposals, questions and unconfirmed premises. Each has a recommended default.

| # | Decision needed | Recommended default | Owner's answer |
|---|---|---|---|

## Mocks

Placeholder data present in the product (must also be visibly marked in the product).

| Where | What is fake | What replaces it | Item |
|---|---|---|---|

## Status legend

⬜ Backlog · 📝 Specified · 🗺️ Planned · 🔨 In execution · 🔍 In QA · ✅ Done · 🐞 In debug · 🚫 Blocked

## Phase 0 — Baseline  (brownfield only; delete this section in a new project)

What already exists and works. ✅ only with evidence re-derived now and the owner's approval.

| ID | Item | Covers | Depends | Status | Spec | Plan | QA |
|---|---|---|---|---|---|---|---|
| B-01 | <existing capability, with the evidence> | F-xx | - | 📝 | | | |

## Phase 1 — Define  (gate: ⬜)

Light approval for size S and M (ARCHITECTURE and SCHEMA run the full loop for M); full loop for size L. Recipes: `project-defines/catalog.md`.

| ID | Item | Covers | Depends | Status | Spec | Plan | QA |
|---|---|---|---|---|---|---|---|
| D-01 | BRIEF | - | - | ⬜ | | | |
| D-02 | PRD | - | D-01 | ⬜ | | | |
| D-03 | ARCHITECTURE | F-xx | D-02 | ⬜ | | | |
| D-04 | APP-FLOW | F-xx | D-02, D-03 | ⬜ | | | |
| D-05 | PATTERNS | S-xx | D-02, D-04 | ⬜ | | | |
| D-06 | SCHEMA | F-xx | D-02, D-03, D-04 | ⬜ | | | |
| D-07 | Consistency check | all | D-02…D-06 | ⬜ | | | |
| D-08 | Expand the plan (phases 2+) | all | D-07 | ⬜ | | | |

*Ready when* (one line per item):
- D-01…D-08: the document meets its *Approved when* in `catalog.md` and the owner approved it.

**Gate of Phase 1:** all D items ✅ · owner's ok.

## Phases 2+

(written by D-08. Each phase: a table with the columns above, a *ready when* line per item, and a gate. The first build phase ends in a runnable skeleton.)

## Size L

Replace the phase tables by the module list and order; each module's items live in `modules/<module>/plan.md`, created when the module's turn comes.

| Order | Module | Status | Plan |
|---|---|---|---|

## How to follow (owner)

Open the Panel. Signs the AI is lost: it asks what to do next, it edits an approved document, it starts a phase without a gate. Say the resume prompt above to bring it back.

## Change log

| Date | What changed | Approved by |
|---|---|---|
