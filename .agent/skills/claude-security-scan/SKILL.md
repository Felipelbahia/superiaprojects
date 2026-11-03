---
# Repository: https://github.com/Felipelbahia/superiaprojects
name: claude-security-scan
description: Use when scanning a repository, branch diff, pull request or commit for vulnerabilities with the Claude Security plugin (/claude-security), reading CLAUDE-SECURITY reports (md, jsonl, SARIF), turning findings into reviewed patches, or choosing between security-review, deep scan, Code Review and CI scanners. Also for varredura de vulnerabilidades.
author: Super IA Projects / Futuro Mercado
license: MIT
---
# Claude Security Scan

## Overview

`[Claude Code only]` The **Claude Security plugin** adds one command, `/claude-security`, that runs a multi-agent vulnerability scan inside your session: agents map the architecture, build a threat model, hunt for vulnerabilities, and **independently verify every finding** before it reaches the report. It scans a whole repo or only a set of committed changes, then turns chosen findings into patches **you** review and apply.

Runs locally on your session's model; no separate key; each scan counts toward usage. Distinct from the managed **Claude Security** product (Enterprise plan, hosted monitoring of connected repos); the plugin also reaches GitLab/Bitbucket repos and networks that block inbound connections.

## Relationship to existing skills (precedence)

Complements `vulnerability-scanner` (OWASP / CVSS checklist), `sast-configuration` (deterministic CI scanners), `stride-analysis-patterns`, `attack-tree-construction`, `security-requirement-extraction` and the `security-auditor` / `penetration-tester` agents. **When in doubt or in conflict, this skill prevails** for deep scans, report format and patch handling (owner decision, 2026-10-11). Severity vocabulary here is the report's own (severity + confidence per finding); map to CVSS only when another tool needs it. It never replaces static analysis or dependency scanners.

## When to Use

- "Scan the repo / my branch / PR #N / commit abc1234 for vulnerabilities".
- Reading or triaging `CLAUDE-SECURITY-*` output; "fix finding F3".
- Choosing the right layer for a security question (table below).
- **NOT:** checks while writing code → `security-guidance-plugin`; PR review → `claude-code-review`; setting up CI scanners → `sast-configuration`.

## Quick Reference

**Prerequisites:** a paid plan, Anthropic API access or a third-party provider (the scan uses dynamic workflows; on Pro enable *Dynamic workflows* in `/config`) · `python3` 3.9+ (stdlib only) · Git for change scans and patches (a full scan works in any directory). Install: `/plugin install claude-security@claude-plugins-official`. Best in **auto mode**.

**Jobs** (`/claude-security` menu, arguments, or plain language):

| Job | How | Notes |
|---|---|---|
| Scan codebase | menu → *Scan codebase* | Plugin reads the repo, offers whole repo or a focused area with file counts and cost; asks to confirm; Claude Code must stay open |
| Scan changes | `/claude-security scan my branch`, "scan commit abc1234", an open PR | **Committed changes only**; commit or stash first. PR lookup needs `gh` signed in and permission |
| Suggest patches | menu → *Suggest patches*, "fix finding F3" | See patch flow below |

**Output:** `CLAUDE-SECURITY-<timestamp>/` in the repo, with its own `.gitignore` (delete that one file to commit it as an audit trail). It is the scan's only change to your checkout. Files and fields: `reference.md`.

**Patch flow:** drafted in a scratch copy → reviewed by an agent independent of the writer (runs the project's tests if any, reads the diff for anything new) → a patch is written **only** if the review vouches that it fixes the one finding, adds no new vulnerability and leaves behavior unchanged; otherwise you get a note. `git apply CLAUDE-SECURITY-<timestamp>/patches/F1.patch`, **one patch per pull request**. Never applied automatically. A stale report (code changed since) is skipped; the plugin offers a fresh scan.

**Large repos:** scan one area at a time (API layer, auth…); the report's coverage section says what was and was not examined.

### Where each tool fits

| Stage | Tool | Covers |
|---|---|---|
| In session | `security-guidance-plugin` | Common vulnerabilities in code Claude writes, fixed in the same session |
| On demand, single pass | `/security-review` | One-time security pass on the current branch's changes |
| On demand, deep scan | **this plugin** | Multi-agent scan of a repo or diff, verified findings, patches |
| On pull request | `claude-code-review` (Team / Enterprise) | Multi-agent correctness and security review with full codebase context |
| Managed | Claude Security product (Enterprise) | Hosted scanning that monitors connected repositories |
| In CI | existing SAST and dependency scanners → `sast-configuration` | Language rules, supply-chain checks, policy enforcement |

All of them read **source in your checkout**, not a running site or deployed service.

## Portable Method (any AI)

1. **Map** entry points, trust boundaries, authn/authz, data stores, secrets. Scope large repos by area.
2. **Threat-model** (`stride-analysis-patterns`, `attack-tree-construction`).
3. **Hunt** per area and class of weakness.
4. **Verify independently:** a second pass tries to refute each finding by reading callers and sanitizers; keep only survivors, each with impact, exploit scenario, severity, confidence, CWE and recommendation.
5. **Patch separately:** draft in a scratch copy; a different pass runs tests and checks the patch fixes only that finding, adds nothing new, changes no other behavior; if it cannot vouch for all three, write a note instead. Never auto-apply; one PR per patch.
6. **Stamp the report** with the commit and settings it covered; re-scan after changes. Scans are nondeterministic, so repeat them on a schedule. Emit SARIF 2.1.0 for tools that read it.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Expecting uncommitted work in a change scan | Commit or stash; a full scan reads the working tree |
| Patching from an old report | Rescan; patches target committed code described by the report |
| Applying all patches in one change | Each in its own PR so it is reviewed and tested alone |
| Expecting identical results on repeat scans | Nondeterministic by design; use the revision stamp to attribute each report |
| Treating the plugin as a SAST replacement | It complements deterministic scanners |
| `git add .` sweeping the report in | The report dir ships its own `.gitignore`; remove it only to keep an audit trail |
| Alarm at "safeguards flagged this message" on a Fable model | Expected: the request re-runs on an Opus model through automatic fallback |
| Menu shows a Python warning | Need `python3` 3.9+ first on `PATH`; open a new session |

**Related:** `security-guidance-plugin` (in-session) · `claude-code-review` (PR time).

**Source:** https://code.claude.com/docs/en/claude-security — verified 2026-10-11. Check the page for current model and plan requirements.
