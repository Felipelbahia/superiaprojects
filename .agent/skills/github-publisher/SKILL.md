---
# Repository: https://github.com/Felipelbahia/superiaprojects
name: github-publisher
description: Use when the user asks to publish, upload or push a local folder or project to GitHub for the first time, create a new GitHub repository from existing code, or "subir o projeto pro GitHub" / "criar repositório", and when a repository is about to be shared (made public, a collaborator added, the link sent to someone) - including when they say it is already clean or they are in a hurry.
author: Futuro Mercado / Felipe Bahia (@felipelbahia)
license: MIT
---
# GitHub Publisher

## Overview

Publishing is irreversible: once a key or a private file reaches GitHub, deleting it later does not unpublish it (forks, caches, clones). So nothing is staged before the folder is audited, and nothing is pushed before the staged list is checked. "Already clean", "já testei" and "tô com pressa" change none of the steps.

Push early: the first push to a **private** repository is encouraged as soon as the audit passes (backup and history from day one) and never waits for the onboarding kit. **Sharing** does: a project with runnable code is made public, gets a collaborator or has its link sent only after Step 9.

## Step 1 — Ask once, in one message

Before running anything that writes, ask together (offer the defaults so a one-word reply works):

| Question | Default |
|---|---|
| Repository name | folder name |
| Owner (personal account or org) | personal |
| Visibility | **private** (public only if the user says "public") |
| One-line description | none |
| License (MIT, Apache-2.0…) | none |
| Basic CI (lint/test on push) | none |

## Step 2 — Pre-flight (read-only)

```bash
git --version && gh --version
gh auth status            # not logged in → ask the user to run: ! gh auth login   (never script a login)
git -C "<dir>" rev-parse --show-toplevel 2>/dev/null   # repository boundary, see Step 3
```

## Step 3 — Repository boundary (REQUIRED)

| `--show-toplevel` prints | Meaning | Action |
|---|---|---|
| nothing (error) | not inside any repo | `git init -b main` in `<dir>` (Step 6) |
| exactly `<dir>` | `<dir>` is its own repo | check `git remote -v`. **No `origin`:** go on, and also run the history check of Step 4. **`origin` exists and the request is only to share it** (make public, add a collaborator, send the link): run Step 4 in full (files, content and history scan), then go to Step 9; skip Steps 5 to 8. **`origin` exists for any other request:** stop and ask |
| **a parent of `<dir>`** | `<dir>` is a folder **inside another repo** | **STOP and ask.** `git status`/`git log` here describe the PARENT, and `gh repo create --source=.` would publish the PARENT. Show the parent path and whether it tracks files of `<dir>` (`git -C "<dir>" ls-files . \| head`). Options: (a) make `<dir>` its own repo (`git init -b main` inside it, then add `<dir>/` to the parent's `.gitignore`); (b) the user really meant the parent. Never decide alone. |

## Step 4 — Audit before any `git add` (run all, from `<dir>`)

```bash
# secret files and MCP configs with embedded API keys by name
find . -path ./node_modules -prune -o -path ./.git -prune -o -type f \( -name '.env' -o -name '.env.*' -o -name '*.env' -o -name '*.pem' -o -name '*.key' -o -name '*.p12' -o -name 'id_rsa*' -o -name '*service-account*.json' -o -name 'credentials*.json' -o -name '.mcp.json' -o -name 'opencode.json' -o -path './.cursor/mcp.json' -o -path './.vscode/mcp.json' -o -path './.gemini/settings.json' -o -path './.codex/config.toml' -o -path './.zed/settings.json' -o -path './config/mcporter.json' \) ! -name '.env.example' ! -name '*.env.example' -print
# secret CONTENT inside ordinary files (names alone miss keys pasted into code)
grep -rIlE --exclude-dir={node_modules,.git,.venv,venv,dist,build} -- 'sk_live_[0-9A-Za-z]{10,}|sk-(proj-)?[0-9A-Za-z_-]{20,}|AKIA[0-9A-Z]{16}|gh[pousr]_[0-9A-Za-z]{30,}|npm_[0-9A-Za-z]{36}|xox[abpr]-[0-9A-Za-z-]{10,}|AIza[0-9A-Za-z_-]{35}|-----BEGIN [A-Z ]*PRIVATE KEY-----' .
# .npmrc is versioned (config such as engine-strict=true) but must not hold a literal token (read the output: a printed path is a hit; the exit code means nothing)
find . \( -name node_modules -o -name .git \) -prune -o -name '.npmrc' -type f -print0 | xargs -0 grep -lE '(_authToken|_auth|_password)[[:space:]]*=[[:space:]]*["'\'']?[^$"'\''[:space:]]' 2>/dev/null
# large files (GitHub warns at 50 MB, rejects at 100 MB)
find . -path ./node_modules -prune -o -path ./.git -prune -o -type f -size +50M -print
# dependencies, builds, caches
ls -d node_modules dist build .next out __pycache__ .venv venv .DS_Store 2>/dev/null
```

| Finding | Action |
|---|---|
| Secret **file** (`.env`, key, service account) | add to `.gitignore`; tell the user it stays local |
| `.npmrc` with a literal token | **STOP.** Do not ignore the file: it carries the version lock. Move the token to `~/.npmrc` or write `${NPM_TOKEN}` in its place (owner decision 2026-11-12), rotate the token if it was ever shared |
| Secret **inside a source file** | **STOP.** Ignoring the file is not a fix (it is code the project needs). The user moves the value to an env var and rotates the key if it was ever shared. Publish only after the grep returns nothing |
| File > 50 MB | ask: exclude, or Git LFS |
| Deps / build / cache folders | `.gitignore` |
| Existing repo (Step 3, own repo) | `git log --all --name-only --format= \| sort -u` and the content grep on history (`git log --all -p \| grep -E '<same regex>'`). A hit → **STOP**: history rewrite + key rotation is the user's decision |

`.gitignore`: extend or create it for the stack (`gh repo gitignore view Node` / `Python` prints a template), always listing every secret file found above.

## Step 5 — README, plus optional files (license and CI only if asked in Step 1)

- License: `gh repo license view <key> > LICENSE` (e.g. `mit`, `apache-2.0`), then fill the year and owner.
- CI: one minimal workflow in `.github/workflows/ci.yml` running the project's existing lint/test commands; see skill `github-actions-templates`.
- `README.md` (always, not only if asked): project with runnable code → the section "Como rodar em outra máquina" and the files of `references/onboarding-kit.md` (items 1-7); without runnable code → name + one line. A missing piece of the kit is reported, and does not block a private push.

## Step 6 — Stage and verify, then commit

```bash
git init -b main                         # only if Step 3 said "not inside any repo" (or option a)
echo "<dir name>/" >> "<parent>/.gitignore"   # option (a) only: the parent stops seeing this folder
git add -A
git diff --cached --name-only            # must contain none of the files flagged in Step 4
git diff --cached | grep -E '<same regex as Step 4>'   # must print nothing
git commit -m "feat: initial commit"
git branch -M main
```

## Step 7 — Create and push (non-interactive)

```bash
gh repo create <owner>/<name> --private --source=. --remote=origin --push --description "<desc>"
```

Use `--public` only with the user's explicit "public", and for a project with runnable code only after Step 9 (public at creation is sharing). Do not add `--license`/`--gitignore`/`--add-readme` here: with `--source` the files come from the local repo (Step 5).

## Step 8 — Verify the result

```bash
gh repo view <owner>/<name> --json url,visibility,defaultBranchRef
git status -sb                                        # main tracks origin/main
git ls-tree -r --name-only origin/main | grep -E '(^|/)(\.env|.*service-account.*\.json|.*\.pem|.*\.key)$'   # must print nothing
```

Report the URL, the visibility and what was kept local (ignored files), with the commands' output as evidence.

## Step 9 — Before sharing (REQUIRED for runnable code)

Before `gh repo edit --visibility public`, `gh repo create --public`, adding a collaborator (`gh api repos/<owner>/<name>/collaborators/<user> -X PUT`) or sending the link:

1. Items 1-7 of `references/onboarding-kit.md` are in the repository (list the files and quote the README section title).
2. Run the clean-clone proof (item 8) in a temporary folder and show the command and its last lines.
3. Proof failed or kit incomplete → **do not share**: fix, commit, push, prove again. The private repository stays as it is.

Project without runnable code: no proof needed; say so in the report.

## Never

- `git add` before Step 4, or `git push --force`, or a `master` branch.
- Publish from inside a parent repo without the user's choice (Step 3).
- Treat "already clean" as evidence: run the audit.
- Script `gh auth login`.
- Share a project with runnable code (public, collaborator, link) without the clean-clone proof of Step 9.

## Common Mistakes

| Mistake | Fix |
|---|---|
| "The folder is already a git repo" because `git status` works | Compare `--show-toplevel` with the folder: it may be the parent |
| Only checking file names for secrets | Run the content grep; keys get pasted into `config.js` |
| Ignoring a source file that contains a key | Move the key out and rotate it; ignoring breaks the project and the key stays in your hands |
| Declaring success after `gh repo create` | Step 8: list the remote files and confirm the URL and visibility |
| Holding the first private push until the README is perfect | Push privately as soon as the audit passes; the onboarding kit gates sharing, not backup |
| Proving the version lock with `npm ci --node-version=…` | It does not simulate the old runtime; run the install with the real old runtime (onboarding kit, item 8) |
