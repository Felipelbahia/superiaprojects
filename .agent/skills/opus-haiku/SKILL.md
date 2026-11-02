---
name: opus-haiku
description: Use when the user invokes /opus-haiku or asks to save plan usage by delegating code writing to a cheaper model while the main model plans and reviews, and in the Execução phase of the execution-loop.
---

# Opus plans, Haiku writes

## Overview

The main (strong) model thinks: it clarifies, plans, briefs, reviews and grades. Subagents on the cheapest model write the code. Measured in Experimentações (2026-10-21, same to-do app): ~61% lower API-equivalent cost than the strong model alone, comparable quality, **but a requirement lost in the briefing was silently dropped** (filters never built). The saving is real only when the briefing is faithful.

Scope: this session only. Nothing is left in the project.

## When to Use

Delegate when the hard part is typing, not deciding:
- Screens and components from a closed spec, CRUD, scaffolding, migrations, renames, mechanical refactors, tests and types.
- A Plan item that already has files, expected result and acceptance criteria.
- Inside the execution-loop: the **Execução** phase uses this skill.

Do NOT delegate:
- The main model is already the cheap one.
- A 1-2 line edit (the briefing costs more than doing it).
- Open-ended investigation, unknown-cause debugging, architecture or design decisions, ambiguous requirements.
- Shared integrations, auth, secrets, data migrations and anything hard to undo: keep on the strong model (or at most `sonnet`).
- The user says "sem Haiku" / "faça direto".

## Core Pattern

1. **Split** the request into small tasks; independent ones run in parallel (several calls in one message).
2. **Spawn** each as a `general-purpose` subagent and **pass `model: "haiku"` on every call**. Without it the subagent inherits the main model and the saving disappears.
3. **Brief literally.** Copy the user's requirements (and, in the loop, the Espec rubric items) verbatim, never a summary. Add: files involved, what NOT to touch, how to verify (build/test), and ask for a short report: what changed, which files, what is pending or failed.
4. **Check before moving on.** Compare the reports against the full original requirement list; anything unaccounted for goes back to the subagent.
5. **Review on the strong model.** The writer never grades its own work. On a failure, the strong model sends the correction to a subagent instead of rewriting.
6. **Retry cap:** the same item failing twice on Haiku → the strong model does it, or re-delegates with `model: "sonnet"`.

## Other AI runtimes

`model: "haiku"` is a Claude Code parameter. On Gemini / Antigravity / Cursor / Codex, apply the same split with the cheapest equivalent model or sub-agent the runtime offers (e.g. a Flash-class model); if it offers none, skip the delegation and work normally. Never claim a cheaper model was used without evidence.

## Verifying it worked

- Delegation: an `Agent`/`Task` block appears in the conversation, with `model: "haiku"` in its input.
- Real model: `~/.claude/projects/<project>/<session>/subagents/*.jsonl`, field `"model"` (expect `claude-haiku-*`). Prefer this over trusting the model's own statement.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Spawning the subagent without `model: "haiku"` | Pass it on every call |
| Summarizing the requirements in the briefing | Copy them verbatim; check reports against the full list |
| Letting the writer grade the result | QA/review stays on the strong model |
| Looping on the same failing item | Two failures → strong model or `sonnet` |
| Delegating tiny or ambiguous work | Do it directly |
