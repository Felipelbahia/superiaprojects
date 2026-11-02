# Conformance (Docs Gate)

How every build step obeys `_projectdefines/`.

## Switch and scope

- The folder `_projectdefines/` in the project root is the switch. No folder: nothing here applies and `execution-loop` behaves as before.
- Only documents with `status: approved` bind. Drafts are working material. A partial set is valid: check only what is approved.
- Applies to the work `execution-loop` is offered for (new feature, build, refactor, significant change).

## Reading map (read only what the work touches)

Always read the **Panel** of `IMPLEMENTATION-PLAN.md` first, then:

| Work | Read |
|---|---|
| New or changed screen or component | `PATTERNS.md`, `APP-FLOW.md` |
| Route or navigation | `APP-FLOW.md` |
| Database, login, permissions | `SCHEMA.md`, `ARCHITECTURE.md` |
| Dependency, integration, env var | `ARCHITECTURE.md`, the project's `## Stack` block and lockfile; Context7 for the **installed** version |
| New feature | `PRD.md` and the plan item |

Size L: read the master Panel and the **current module's** files only.

## Nothing unlisted

No screen, route, table, dependency or environment variable enters the code unless an approved document lists it. In the Espec, every rubric row that comes from a document cites its ID (F-xx, S-xx, E-xx, ADR).

## When a request conflicts with a document (document-first)

1. **Stop** the conflicting part. Parts that do not conflict may proceed.
2. **Do not edit** the approved document, and do not add plan items out of order.
3. Write a **Change Proposal** in plain language in the owner's language: what the request needs, which document and ID it contradicts, impact, the options and a recommended default. If the owner can be asked now, ask. If not, add it under *Open decisions* in `IMPLEMENTATION-PLAN.md` and say so in the final report. The proposal is the question.
4. After explicit approval: update the document (keep `approved`, add a line in its *Change log*: date, what, who approved), then add or reorder plan items through the structure-change rule in `tracker.md`, then build.

A deadline or "I can't ask" never turns an assumption into an approval.

## Baseline violations cannot be deferred silently

The security baseline and lean budget in `ARCHITECTURE.md` are not optional features. If the work cannot meet one (for example a route without the required login), it becomes a **blocking** plan item or an approved exception in the document, never a note in a report.

## Mocks and placeholder data

Placeholder data must be visibly marked as such **inside the product** (label or banner) and listed under *Mocks* in `IMPLEMENTATION-PLAN.md`. It is never presented as real. If it cannot be marked, do not build it.

## Bugs

A small bug fix is a simple task: no plan item, but it must still conform and be logged in `memory.md` if it teaches something. A "fix" that changes documented behavior is a document-first change.

## Evidence

A rubric row earns its grade by evidence re-derived at QA time (command output, test, diff), never from a previous log. See the ✅ rule in `tracker.md`.

## Rationalizations (all wrong)

| Thought | Reality |
|---|---|
| "The owner obviously wants it; I'll update the document and tell them afterwards" | The document is the owner's decision. Propose and stop. |
| "I can't ask, so I'll assume and continue" | Not being able to ask means the proposal goes in the report. It does not mean approving yourself. |
| "It's only 10 minutes / a demo" | Urgency does not change who approves. Build the non-conflicting part. |
| "No login system exists yet, so this route can stay open" | A missing prerequisite is a blocking item, not permission. |
| "It's only sample data" | Mark it in the product or do not build it. |
| "The log says 10/10, and I was told to close" | Re-derive the evidence. Mismatch means 🐞, and tell the owner. |
| "A note under the Panel is enough" | A problem lives in the item's status, not in a loose note. |
