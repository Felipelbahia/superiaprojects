## Code rules

- Code, comments and identifiers in English.
- **`ponytail`:** on every coding task (write, fix, refactor, review, pick a dependency) apply skill `ponytail`: the smallest complete change, and a reply a busy human reads in one pass. Default level `full`.
- Clean code (`clean-code`): concise, no over-engineering. Every logic change comes with tests (unit > integration > E2E, AAA).
- **Tests accumulate:** every bug fix starts with a test that reproduces the bug and fails; then the fix; the test stays in the suite for good (skill `test-driven-development`). Show the failing run before the fix and the passing run after.
- **Never weaken the suite:** do not delete, skip, or loosen a failing test (or its expected value) to get a green run without the owner's approval. A test that was already in the suite and already failing in a baseline run made before your first edit (output shown) is reported with its name and cause, and stays failing until the owner decides. A test that passed in the baseline and fails now is a regression you caused and blocks; the new bug test must pass after the fix. Ask the owner in the same reply. Until then, those named tests are the only accepted failures: `checklist.py` and the execution loop's closing gate count as green only if every other check passes, and the change is reported as "done except known failing test <name> (owner decision pending)". Never bypass the hook (`--no-verify`) for them: commits wait for the owner.
- **A failing test is never accepted without detail:** its name, cause and the command to reproduce it go in a new item in the tested project's `inbox/`. Skipped tests and checks left "not verified" (they need another environment) also become an inbox item of that project, with the command to run where it works.
- **Lint what you touch:** every code file you create or edit passes the project's linter (and type checker, when it has one) with no new findings. Old findings in files you did not touch are not fixed in passing.
- **Where tests run:** the fast part of the suite (seconds) in the pre-commit hook `.githooks/pre-commit`; the full suite in `checklist.py` and before closing a significant change. No hook in the project and a fast check exists (about 5 s or less): propose installing it (step "Hook de commit" of `project-initializer`).
- **Docs first (Context7 MCP, mandatory):** before choosing, installing, configuring or writing code for any technology — framework, library, SDK, API, CLI, and also CSS/UI libraries, component kits and design tokens — consult Context7 (`resolve-library-id` → `query-docs`) and say which library ID was used. New project: current stable version. Existing project: the version in the lockfile. Docs win over memory and templates on facts. Context7 unavailable: use official docs and say so.
- **`## Stack` block** in this file, names only, no frozen versions. Missing? Write it the first time a technology is touched (read the lockfile, consult Context7).
  ```
  ## Stack
  - Language/runtime: <name>
  - Framework: <name>
  - Main libraries: <names>
  - Last checked: AAAA-MM-DD (Context7)
  ```
- **Shareable by clone:** a project with runnable code keeps the onboarding kit (skill `github-publisher`, `references/onboarding-kit.md`: runtime version file, a minimum version that fails early, versioned lockfile, `.env.example`, README section "Como rodar em outra máquina"). Push to a private repository early; share it (public, collaborator, link sent) only after the clean-clone proof, with the command and result shown.
- **Reuse before build:** skill `oss-scout` before building a capability a mature library may cover.
- **No new dependency without asking:** before adding a package, say what it solves and which one the project already has that could do it; install only after the owner says yes. Follow the folders, names and libraries already in the code (`STANDARDS.md`, `PATTERNS.md`, `CODEBASE.md`).

## Code done means

A significant change is not finished until `python .agent/scripts/checklist.py .` passes (add `--url <URL>` before deploy). Show its output. The whole test suite and the linter run, not only the tests of the file you touched; an old test that now fails is a regression: show its name and the error, then fix it or ask. The checklist also runs `scope_check.py` and `env_diff_check.py` (see *Change discipline* and *Safety and handoff*). Also run it when the user asks for "final checks" / "checagem final". Order: Security → Lint → Schema → Tests → UX → SEO → Lighthouse/E2E; fix Critical blockers first. Review and security: `claude-code-review`, `security-guidance-plugin`, `claude-security-scan` win over `code-review-*`, `vulnerability-scanner`, `sast-configuration`.
