---
# Repository: https://github.com/Felipelbahia/superiaprojects
name: claude-code-review
description: Use when setting up, tuning or running Claude Code Review (managed GitHub PR review, REVIEW.md, @claude review) or the local /code-review command, when review findings are noisy, missing or costly, or when gating merges on automated review severity. Also for revisão de PR automatizada and ultrareview requests.
author: Super IA Projects / Futuro Mercado
license: MIT
---
# Claude Code Review

## Overview

Two surfaces, one goal: find correctness bugs before merge.

- **Managed Code Review** `[Claude Code only]` — GitHub App. A fleet of agents reviews each PR on Anthropic infrastructure, a verification step filters false positives, and results arrive as inline comments plus a **Claude Code Review** check run. Research preview, Team and Enterprise only; unavailable with Zero Data Retention or the HIPAA configuration.
- **Local `/code-review`** `[Claude Code only]` — reviews your branch's commits ahead of upstream plus uncommitted changes, in a background subagent. No GitHub App, works on any plan.

Default scope is **correctness** (bugs that would break production), not formatting or missing tests. Findings **never approve or block** a PR.

## Relationship to existing skills (precedence)

Complements `code-review-excellence` (human review etiquette), `code-review-checklist`, `requesting-code-review` / `receiving-code-review` (subagent review loop) and `vulnerability-scanner`. **When in doubt or in conflict, this skill prevails** (owner decision, 2026-10-11). Keep using the others for what this one does not cover: etiquette, checklists, OWASP.

- **The emojis do not mean the same thing.** Here: 🔴 Important · 🟡 Nit · 🟣 Pre-existing. Older skills: 🔴 blocking · 🟡 important/suggestion · 🟢 nit. Always print the word next to the emoji; a 🟡 here is *not* "important".
- Default scope is correctness. Add style or test-coverage rules only when the repo asks for them (`REVIEW.md` / `CLAUDE.md`).

## When to Use

- Enabling or tuning Code Review for a repo, writing `REVIEW.md`, choosing a trigger.
- Reviewing a diff before pushing (`/code-review`) or escalating (`/code-review ultra`).
- Findings missing, too noisy or too expensive; CI must gate on severity.
- **NOT:** etiquette for human reviewers → `code-review-excellence`; scanning a repo for vulnerabilities → `claude-security-scan`; in-session guardrails → `security-guidance-plugin`.

## Quick Reference

| Marker | Severity | Meaning |
|---|---|---|
| 🔴 | Important | Bug to fix before merging |
| 🟡 | Nit | Minor, worth fixing, not blocking |
| 🟣 | Pre-existing | Bug already in the codebase, not introduced by this PR |

| Trigger (per repo) | Behavior |
|---|---|
| Once after PR creation | One review when the PR opens or is marked ready |
| After every push | Review per push; auto-resolves threads when fixed; **cost × pushes** |
| Manual | Nothing automatic; comment `@claude review` |

`@claude review` = one review · `@claude review always` = also subscribe to pushes · `@claude review once` = same as bare. It must be a **top-level** PR comment, command first on the line, by someone with write/maintain/admin; the PR must be open. Fork PRs only start by comment. Details and troubleshooting: `reference.md`.

**Local flags:** `/code-review [low|medium|high|xhigh|max|ultra] [target] [--fix] [--comment] [--post] [--max-findings n|all|default]`. Target = path, PR number, branch or range like `main...feature`. `low` = fewest, highest-confidence findings; `medium`–`max` broaden; `ultra` = cloud multi-agent, billed and triggered by the user (ask them to run it; do not launch it yourself). `--fix` edits the working tree (revert with git, not `/rewind`). `/review` is an alias; `/simplify` is cleanup-only and finds no bugs.

**Guidance files:** `CLAUDE.md` = project context, newly introduced violations become Nits. `REVIEW.md` (repo root) = review-only rules for severity, nit cap, skip paths, repo checks, verification bar, re-review convergence, summary shape. **Local `/code-review` does not read `REVIEW.md`.** Template in `reference.md`.

**Cost:** averages US$15–25 per review (20 min), billed separately through usage credits; cap at `claude.ai/admin-settings/usage`.

**Gate CI:** the check run always ends *neutral*. Read the `bughunter-severity` JSON on the last line of its Details text; `normal` > 0 means at least one Important finding (command in `reference.md`).

## Portable Method (any AI)

1. Review from the diff plus surrounding code in a **fresh context**, not the author's session.
2. One pass per class of issue (logic, security, edge cases, regressions), then a **verification pass** that checks each candidate against real behavior and cites `file:line`; drop what cannot be shown.
3. Deduplicate and rank: Important (breaks behavior, leaks data, blocks rollback) · Nit · Pre-existing.
4. Cap nits; skip generated, lock and vendored files and anything CI already enforces.
5. On re-review, report only new Important findings.
6. Open with a one-line tally, then findings with `file:line`, why flagged, how verified. Fix in code; replies do not dismiss anything.

Write a `REVIEW.md` even outside Claude Code and point other tools at it.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Expecting `/code-review` to follow `REVIEW.md` | It does not; put must-have rules in `CLAUDE.md` or in the target text |
| Expecting Code Review to block merges | Check run is neutral; gate in CI on `bughunter-severity` |
| `@claude review` as an inline diff comment, or with a private org membership | Top-level comment; make membership public or add the user as collaborator |
| Using `always` casually | Every push is billed; use the bare command for a one-off second opinion |
| Replying to a finding to dismiss it | Resolve the thread, or fix and push |
| Habit from before July 2026 that bare `@claude review` subscribes the PR | It no longer does; use `always` |
| Scheduling `/code-review ultra` | Scheduled tasks never launch the cloud review; schedule plain `/code-review` |
| Using `/simplify` to hunt bugs | It only cleans up; use `/code-review --fix` |

**Related:** `security-guidance-plugin` (in-session) · `claude-security-scan` (deep scan, and the full layered-tools table).

**Source:** https://code.claude.com/docs/en/code-review — verified 2026-10-11. Flags depend on the Claude Code version (see `reference.md`); re-read the page when the installed version differs.
