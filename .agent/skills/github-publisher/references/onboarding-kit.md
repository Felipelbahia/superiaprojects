# Onboarding kit: clone and run on another machine

Source: kit inbox item 025 (2026-11-12), reference implementation in Ilazos - Site (`github.com/Felipelbahia/ilazos-lp`, commit `be4067f`). Applies to every project with **runnable code**. A project without runnable code (documents, content, prompts) only needs a README with name and one line.

**When it is required (owner decision 2026-11-12):** the first push to a **private** repository is encouraged early (backup and history) and never waits for this kit. **Sharing** waits for it: making the repository public, adding a collaborator, or sending the link to someone. Before sharing, items 1-7 are in place and the proof of item 8 was run, with its command and result shown.

## The kit (any stack)

1. **Runtime version pinned in a file:** `.nvmrc` (Node), `.python-version` (Python), or the stack's equivalent.
2. **Minimum version that fails early:** Node uses `engines` in `package.json` **plus** `.npmrc` with `engine-strict=true` (without the `.npmrc`, `engines` is only a warning nobody reads). The `.npmrc` is **versioned** and holds configuration only; a registry token goes in `~/.npmrc` or as `${NPM_TOKEN}`, never literal (owner decision 2026-11-12). Python uses `requires-python` in `pyproject.toml`.
3. **Lockfile versioned** (`package-lock.json`, `uv.lock`, `poetry.lock`…), and the README uses the reproducible install (`npm ci`, `uv sync`…).
4. **`.env.example` versioned** with every variable. The project runs without `.env` whenever possible (fallbacks in code), or the README names exactly which variables are required.
5. **README section "Como rodar em outra máquina":**
   - prerequisites with versions;
   - copyable steps: clone → runtime version → install → `.env` → run;
   - the **"it worked" criterion** (e.g. "`npm run build` ends with `Complete!`");
   - a table of common problems (symptom → cause → fix).
6. **Note about the AI folders** (`.agent/`, `CLAUDE.md`, `AGENTS.md`): they cite paths of this machine, are not needed to run the project, and on another machine only the local skills work.
7. **Versioned symlinks documented** (e.g. `.claude/skills/<skill>` → `.agent/skills/<skill>`), with the Windows note: run `git config --global core.symlinks true` before cloning.
8. **Proof:** a clean clone in a temporary folder installs and builds with no extra steps. Run it from the remote (or the local repo), never inside the original folder:
   ```bash
   git clone "<repo url or path>" "<scratch>/clone" && cd "<scratch>/clone" && npm ci && npm run build   # or: uv sync && <run/test command>
   ```
   Report the command and its last lines. To prove the version lock of item 2, run the install with the **real** old runtime (e.g. `npx -p node@20.11.0 npm ci` must stop with `EBADENGINE`); flags like `npm ci --node-version=…` do not simulate it.

## Risk
`engine-strict=true` also blocks dependencies whose `engines` does not match the runtime. If that happens, adjust the runtime version; never remove the lock silently.

## Stack details
Stack SIPs add the stack-specific part (e.g. SIP - Astro, its own inbox item 001). This file is the general rule.
