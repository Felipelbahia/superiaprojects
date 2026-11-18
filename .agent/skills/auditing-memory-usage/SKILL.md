---
# Repository: https://github.com/Felipelbahia/superiaprojects
name: auditing-memory-usage
description: Use when the owner says the machine or an app feels heavy, slow or memory-hungry, memory keeps growing, or asks to check a project's code for memory leaks or unnecessary memory use.
author: Super IA Projects / Felipe Bahia
license: MIT
---
# Auditing Memory Usage

## Overview
Static audit of a project's **code** for memory that grows and never returns. Every finding has evidence (`file:line`) and a **how to fix**. Fixes are proposed, never applied without the owner's ok.

Not for: clearing macOS RAM (`purge` and cleaners backfire) or tuning the OS. High "compressed" memory with green pressure is normal.

## Steps
1. **Stack:** detect languages in the project (`ls`, manifests). Read only the matching section of `references/checklists.md`.
2. **Scan:** run the greps of each checklist section on source dirs only (skip `node_modules`, `.git`, `.venv`, generated files).
3. **Confirm each hit** by reading the surrounding code. A hit is a finding only if the resource is never released, or the structure has no bound. Discard the rest.
4. **Rank** by impact: runs forever (servers, watchers, loops) > per-request/per-event growth > one-off scripts.
5. **Report** (table, one row per finding):

| # | file:line | What grows | Why it is a leak | How to fix |
|---|---|---|---|---|

6. **Ask** which fixes to apply. Apply only those, then re-run the same greps and show the result.

## Rules
- No evidence (path + line), no finding.
- Short-lived scripts that exit are low severity: say so, don't inflate.
- Nothing found? Say "no findings", list the greps run and the sections covered. Don't invent.
- If the leak is not visible in code, suggest measuring: heap snapshot (JS), `tracemalloc` (Python), `leaks <pid>` (macOS), AddressSanitizer (C/C++). Measure before and after the fix.

## Common mistakes
- Flagging every `setInterval` or global list: check for `clear`/bound first.
- Fixing without measuring: confirm memory actually stops growing.
