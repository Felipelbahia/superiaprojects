# Prompt — Handoff to the coding agent

Use at the start of any session in a project that has `_projectdefines/`. If the project's rules file (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`) does not carry the "Project Defines Gate", paste this block into it as well.

```
Read the Panel of _projectdefines/IMPLEMENTATION-PLAN.md first, then only the documents the next item touches (reading map in project-defines/conformance.md).

Treat the approved documents as the contract:
- PRD for product scope, ARCHITECTURE for technical decisions, APP-FLOW for navigation and states, PATTERNS for visual behavior, SCHEMA for data, IMPLEMENTATION-PLAN for order and status.

Do not add anything that is not listed in the documents: no screen, route, table, dependency or environment variable. If the request conflicts with a document, stop that part, write a change proposal in plain language with a recommended default, and wait for my approval. Never edit an approved document yourself.

Work on one item at a time through the execution-loop. Mark an item done only with evidence you re-derived now. Update the tracker (status and links) as part of the item. Tell me the next exact step when you finish.
```
