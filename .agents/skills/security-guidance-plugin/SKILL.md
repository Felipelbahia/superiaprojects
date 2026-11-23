---
# Repository: https://github.com/Felipelbahia/superiaprojects
name: security-guidance-plugin
description: Use when enabling, tuning or debugging the Claude Code security-guidance plugin that reviews Claude's own edits for vulnerabilities during a session, when adding custom security rules or patterns to it, or when writing code that uses eval or exec, unsafe deserialization, raw DOM injection or CI workflow files. Also for avisos de segurança durante a edição.
author: Super IA Projects / Futuro Mercado
license: MIT
---
# Security Guidance Plugin

## Overview

`[Claude Code only]` A plugin built entirely on hooks that makes Claude review **its own** code changes for common vulnerabilities while it works and fix what it finds in the same session. Nothing to invoke after install. It is the in-session companion to Code Review (`claude-code-review`): it reduces what reaches the PR, Code Review catches what still does.

It reviews at three depths. **None of them block a write or a commit** — findings reach Claude as instructions and the review model can miss issues. One layer of defense in depth, not a complete security solution.

## Relationship to existing skills (precedence)

Complements `vulnerability-scanner` (OWASP checklist), `sast-configuration` (deterministic CI scanners), `secrets-management` and the `security-auditor` agent. **When in doubt or in conflict, this skill prevails** for anything about Claude's in-session security checks (owner decision, 2026-10-11). It never replaces CI static analysis or dependency scanning.

## When to Use

- Installing the plugin, enabling it for a team, or turning layers on and off.
- Encoding a repo's threat model: rules in plain language and regex patterns.
- A warning appeared, a layer silently skipped, or cost needs trimming.
- Writing code in the risky categories below, with or without the plugin.
- **NOT:** scanning existing code → `claude-security-scan`; PR review → `claude-code-review`.

## Quick Reference

| Layer | Trigger | What it does | Limits |
|---|---|---|---|
| Per edit | `PostToolUse` on Edit / Write / NotebookEdit | Pattern match, **no model call, no cost**; warning goes into Claude's next-step context | Once per pattern per file per session |
| End of turn | `Stop` | Separate Claude, fresh context, reviews the `git diff` of everything the turn changed (edits, Bash, subagents) in the background; Claude is re-prompted with findings | ≤ 30 files per turn; ≤ 3 re-prompts in a row |
| Commit / push | `PostToolUse` on Bash (`git commit`, `git push`) | Agentic review that reads callers, sanitizers and related files before calling a finding real | Only commits Claude makes via Bash (not your shell or `!`); ≤ 20 per rolling hour |

Per-edit categories: dynamic execution (`eval(`, `new Function`, `os.system`, `child_process.exec`) · unsafe deserialization (`pickle`) · DOM injection (`dangerouslySetInnerHTML`, `.innerHTML =`, `document.write`) · edits under `.github/workflows/`. The model-backed layers also catch authorization bypass, IDOR, injection, SSRF and weak cryptography.

**Install:** `/plugin install security-guidance@claude-plugins-official` (first `/plugin marketplace add anthropics/claude-plugins-official` if the marketplace is missing). Team-wide: `enabledPlugins` in the project's `.claude/settings.json`. Needs Python 3.7+ (3.10+ for the agentic commit review) and a git repo for the two model-backed layers. Available on all plans.

**Add rules (additive only):** `.claude/claude-security-guidance.md` (plain-language threat model, advisory) and `.claude/security-patterns.yaml` / `.yml` / `.json` (deterministic per-edit rules). User, project and `.local` scopes are merged. Schema, caps and examples: `reference.md`.

**Turn off:** `ENABLE_PATTERN_RULES=0` · `ENABLE_STOP_REVIEW=0` · `ENABLE_COMMIT_REVIEW=0` · `ENABLE_CODE_SECURITY_REVIEW=0` (both model layers) · `SECURITY_GUIDANCE_DISABLE=1` (all). Models: `SECURITY_REVIEW_MODEL`, `SG_AGENTIC_MODEL`.

**Debug first:** `~/.claude/security/log.txt`.

## Portable Method (any AI)

Do by hand what the hooks do:

1. **After each edit,** scan your own diff for the per-edit categories above plus string-built SQL or shell commands, hard-coded credentials and unscoped queries; fix before moving on.
2. **At the end of a task,** review the full `git diff` in a **fresh context** with a security-only prompt (authorization bypass, IDOR, injection, SSRF, weak crypto). Fix, then report done.
3. **Before committing or pushing,** do a deeper pass: read callers and sanitizers before calling something a vulnerability, to keep false positives low.
4. Keep the repo's threat-model rules in a short guidance file; anything that must *always* hold goes into a blocking hook or a CI check, because guidance is advisory.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Treating the guidance file as a guardrail | It is advisory; enforce with a hook that blocks the edit, or CI |
| Writing "ignore X" rules | Additive only; a rule cannot suppress a vulnerability class |
| `security-patterns.yaml` silently ignored | PyYAML is not importable; use `security-patterns.json` |
| Project-relative `paths` never match | Globs match the full path; prefix with `**/` |
| Expecting review of commits made with `!` or your own shell | Only Claude's Bash `git commit` / `git push` are reviewed |
| No findings outside a repo, or without auth | Model layers need git state and Anthropic auth or a provider; only the per-edit check runs |
| Third-party provider with old Python | Model-backed reviews need the SDK and Python 3.10+; they skip with a one-time notice |
| Expecting a clean commit to print something | A clean commit, or one duplicating the end-of-turn findings, is silent |

**Related:** `claude-code-review` (PR time) · `claude-security-scan` (deep scan, and the full layered-tools table).

**Source:** https://code.claude.com/docs/en/security-guidance — verified 2026-10-11. Default review model is named in the page (Opus 4.7 at that date); re-check when models change.
