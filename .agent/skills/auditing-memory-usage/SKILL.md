---
# Repository: https://github.com/Felipelbahia/superiaprojects
name: auditing-memory-usage
description: Use when the owner says the Mac or an app feels heavy, slow or memory-hungry, swap or compressed memory is high after hours of IDE use, orphan processes from Antigravity, Gemini, Claude, Kilo or codex pile up, memory keeps growing, or asks to check a project's code for memory leaks or unnecessary memory use.
author: Super IA Projects / Felipe Bahia
license: MIT
---
# Auditing Memory Usage

## Overview
Two phases, in order: **Phase 0** the machine (processes that pile up), **Phase 1** the project's **code** (memory that grows and never returns). Every finding has evidence and a fix. Nothing is killed or fixed without the owner's ok. Never `purge` or RAM cleaners: they backfire.

## Phase 0: the machine
Run `python3 .agent/scripts/check_memoria.py` (read-only). Not in this project: run the kit's copy, path in `.agent/SIPS-CONSUMIDOS.md`.

1. Read the traffic light and "Como resolver". Show the owner the findings, never raw `ps`.
2. Orphans or stopped hosts: offer `--limpar` (lists targets, asks ok, `SIGTERM`; `SIGKILL` only for survivors, after a second ok). Then re-run the check.
3. No orphans, memory still high: the weight is in open windows. From "Mais pesados" (up to 5, shown when something is yellow or red; age and live processes inside) name the oldest, emptiest Antigravity window and ask the owner to close that conversation. Then restart Antigravity; if it persists, reboot. Phase 1 only if one app's memory keeps growing.
4. Docker/OrbStack: the script only advises; ask before touching containers.

Run it after closing Antigravity windows or conversations and at the end of long sessions. In the Claude terminal, leave with `/exit`.

Hard rules: never kill the session's own terminal, host or `claude`; never print `ps` `command` or `comm` (title-rewritten processes carry tokens), `mcp_config.json` or `.claude.json`. Criteria and macOS traps: `references/ambiente-macos.md`.

## Phase 1: the code
1. Detect languages; read only the matching section of `references/checklists.md`.
2. Run its greps on source dirs only (skip `node_modules`, `.git`, `.venv`, generated files).
3. Confirm each hit by reading the code: a finding only if the resource is never released or has no bound.
4. Rank: runs forever (servers, watchers, loops) > per-request growth > one-off scripts.
5. Report one row per finding: `# | file:line | What grows | Why it is a leak | How to fix`.
6. Ask which fixes to apply, apply only those, re-run the greps.

## Rules
- No evidence (path + line), no finding. Nothing found: "no findings" plus the greps run.
- Short-lived scripts that exit are low severity.
- Leak not visible in code: measure before and after (heap snapshot for JS, `tracemalloc` for Python, `leaks <pid>` on macOS, AddressSanitizer for C/C++).

## Common mistakes
- Flagging every `setInterval` or global list: check for `clear`/bound first.
- Killing a process because it is `ppid=1`: an active hub also is; check its clients.
- Reading `ps -o rss` as real use: it misses what went to the compressor.
