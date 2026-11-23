---
# Repository: https://github.com/Felipelbahia/superiaprojects-marketing
# Status: Customizada / Modificada localmente por Felipe Bahia
name: session-handoff
description: Use when ending a session with unfinished work that another session will need to continue, or when starting a session that resumes someone else's (or your own past) handoff — captures task status, decisions, learnings, and next steps without losing context.
author: Futuro Mercado / Felipe Bahia (@felipelbahia) & Felipe Bahia (Futuro Mercado)
license: MIT
metadata:
  author: Futuro Mercado / Felipe Bahia (@felipelbahia) & Felipe Bahia (Futuro Mercado)
  version: 1.0.0
---
# Session Handoff

## Overview

Two directions of the same artifact: **write** a handoff when context is about to end with real work still open; **resume** from one when a fresh session needs to continue it. File-based only — no external sync tool, no ticket system, no script dependency required.

Adapted from the `create_handoff.md`/`resume_handoff.md` agents in this repo, which cite a `thoughts/` folder, a `scripts/spec_metadata.sh`, and a `humanlayer thoughts sync` CLI — none of which exist here. This skill keeps their genuinely good template, dropped everything that doesn't exist in this repo.

## When to Use

- Ending a session/turn with unfinished work (mid-plan, mid-`execution-loop` cycle, mid-debug) that another session will need to pick up.
- Starting a session where the user gives you a path to a previous handoff, or says "continue from where we left off."
- **NOT** for a fully finished task — that just needs a normal summary, not a handoff file.

**Reaching `execution-loop`** (mentioned below for the mid-loop case): if not present in this project's own `.agents/skills/`, it lives at `/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agents/skills/execution-loop/` — resolve via Rule 4 (Fallback Resolution Protocol) / `skill-resolver`, the same way this skill itself was found.

## Where Handoffs Live

`.agents/plans/handoffs/` (next to the loops and plans in `.agents/plans/`). *Legacy:* a project that already has `handoffs/` at its root keeps using it until the owner asks to migrate it (`mv` into `.agents/plans/`, fix the links). Filename: `AAAA-MM-DD_HH-MM_<descrição-curta>.md`. No ticket system, no external sync — the committed file itself is the handoff. If this project already tracks work in an issue tracker, prefixing the filename with its ticket ID is a fine optional adapter — don't require one that doesn't exist here.

**A prompt to continue (the owner asks to resume in another session or at another time):** it is not the handoff. Save it as `.agents/plans/prompts/NNN-<Short Title>.md` (own counter; temporary prompts go there too) and give the owner its path. The prompt points at the handoff file in `handoffs/`; never paste the handoff's content into it.

**If the work being handed off is inside an `execution-loop` run:** the handoff's Artifacts section must point at the exact `.agents/plans/execution-loops/<date>/<goal>/NN Nome.md` files already produced, so resuming continues the loop's numbering instead of restarting it.

## Creating a Handoff

Metadata is computed directly — no script:
- Date/time: system clock.
- `git_commit`: `git rev-parse HEAD`
- `branch`: `git branch --show-current`
- `repository`: the project's folder/repo name

```markdown
---
date: [current date/time, ISO format]
git_commit: [output of git rev-parse HEAD]
branch: [output of git branch --show-current]
repository: [repository name]
status: complete
---

# Handoff: {concise task name}

## Task(s)
{What you were working on and the status of each (completed / in progress / planned). If working from a plan or an execution-loop cycle, name it and which phase/file you're on.}

## Critical References
{2-3 most important file paths — specs, plans, ADRs that must be followed. Leave blank if none.}

## Recent Changes
{What you changed, as file:line references.}

## Learnings
{Patterns, root causes, gotchas the next session needs — explicit file paths where useful.}

## Artifacts
{Every file you produced or updated that the next session should read, in the order to read them.}

## Action Items & Next Steps
{What the next session should do, based on current status.}

## Other Notes
{Anything else worth passing on.}
```

Guidelines: more information beats less; avoid large code blocks/diffs (prefer `path/to/file.ext:line` references an agent can follow later); be precise about phase/status, not just "in progress."

## Resuming from a Handoff

1. Read the handoff file **completely** — no `Read` with limit/offset.
2. Read every file listed in "Artifacts" and "Critical References" — don't skip because the handoff describes them, verify directly.
3. **Never assume the handoff still matches reality.** Check that "Recent Changes" are actually present, that referenced files still exist, that nothing regressed since it was written.
4. Present a short analysis before acting: original tasks + current verification, learnings still valid vs. changed, recommended next action — then confirm with the user or proceed if direction is unambiguous.
5. Track continuity with TodoWrite from the Action Items section. Consider writing a new handoff when your own session ends, if work is still open.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Citing `thoughts/`, `spec_metadata.sh`, or `humanlayer sync` | None of these exist in this repo — use `.agents/plans/handoffs/` and plain `git` commands |
| Trusting the handoff's claims without checking current state | Re-verify every artifact and change — codebases drift between sessions |
| Writing a handoff for a task that's actually done | Done work gets a normal summary; handoffs are for real unfinished work |
| Losing an in-progress `execution-loop`'s file counter on resume | Point the Artifacts section at the loop's existing numbered files so the next session continues numbering instead of restarting |
