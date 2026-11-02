---
name: project-defines
description: Use when a new application or system must be planned, specified and built step by step, when a project contains a _projectdefines/ folder and anything is about to be built, changed or reviewed, or when an owner who does not program needs a safe, lean build path.
---

# Project Defines

## Overview

Contract-first building, designed for owners who may not program. `_projectdefines/` holds documents the owner approves one by one; `IMPLEMENTATION-PLAN.md` inside it is both the map and the state of the project.

**Core principle: code obeys approved documents; only the owner's approval changes a document.**

## When to Use

- `project-initializer` offers this after its setup phase 3 (never forced; default No).
- A project has `_projectdefines/` and something is about to be built, changed or reviewed: apply `conformance.md`.
- Not for one-line fixes, questions, or projects without the folder (unless the owner opts in).

## Flow

1. **Size** the project (S/M/L) with plain-language questions in the BRIEF. Propose with reasons; the owner confirms. See `catalog.md`.
2. **Define** (Phase 1 of the plan), one document at a time, each approved before the next: BRIEF (with the mandatory Launch profile) → PRD → ARCHITECTURE → APP-FLOW → PATTERNS → SCHEMA → consistency check → expand the plan. Recipe, template and prompt per document are in `catalog.md`, `templates/`, `prompts/`. Stack: preset or from scratch, see `stack-presets.md`.
3. **Build** phase by phase; one item = one `execution-loop` run. See `tracker.md`.
4. **Every** build step obeys `conformance.md`.

## Approval Gate

The owner is never asked to judge technology. One decision per message, in the owner's language, no jargon:

- what this document decides (5 lines max)
- what it costs or limits
- the recommended default
- multiple choice

Technical soundness is checked by the catalog's approval criteria and reviewer agents. Questioning style: use `brainstorming`.

## Language

Documents are written in English by default, in the owner's language only if the owner asks. Approval summaries and change proposals are always in the owner's language.

## Quick Reference

| Need | Read |
|---|---|
| Size, recipes, approval criteria per document | `catalog.md` |
| Obeying or changing documents, mocks, bugs | `conformance.md` |
| Statuses, the ✅ rule, gates, edit rights, large projects | `tracker.md` |
| Presets and from-scratch stack | `stack-presets.md` |
| Launch profile (mandatory BRIEF section), where its seeds land, the launch phase | `launch-profile.md` |
| Session start; rules-file block for a project that lacks the gate | `prompts/handoff.md` |
| Adopting the contract in an **existing** project | `brownfield.md` |

## Hard Rules

1. Approved documents change only by the owner's explicit approval. On conflict, write the change proposal and **stop**.
2. Nothing enters code that is not in the documents: screen, route, table, dependency, env var.
3. ✅ only with re-derived evidence. An order to close does not replace evidence.
4. A premise is not a decision: unconfirmed assumptions are open questions with a recommended default.
5. Size L: define a module's documents only when its turn comes.
6. Before choosing or pinning any technology, consult the docs MCP (Context7) for its current stable version and setup ("Latest Docs First" in CLAUDE.md; details in `stack-presets.md`).

## Sources

Adapted (rewritten and extended) from the public guide "The 6 Documents You Need Before Vibe Coding Any App" and the Claude artifact "Vibe Coding — 6 Documents".
