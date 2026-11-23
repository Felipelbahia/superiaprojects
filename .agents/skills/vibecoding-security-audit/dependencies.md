# Dependencies: vet before you install

Only when a dependency is about to be added, especially one an AI assistant suggested. AI tools sometimes invent package names; attackers register those names with malware ("slopsquatting"). `npm audit` only finds known CVEs in packages you already installed, so it does not cover this.

## Before every new dependency

1. Run the check (network needed):
   ```bash
   python3 -I scripts/vet_package.py npm <name>      # or: pypi <name>
   ```
2. Read the result:

   | Result | Meaning | Action |
   |---|---|---|
   | `FAIL` (exit 1) | The package does not exist on the registry | Do not install. The name was invented; find the real package or write the code |
   | `WARN` young or few downloads | New or obscure | Read its source and repository first; prefer a mature alternative |
   | `WARN` no repository | You cannot read the source | Do not install unless you vetted the code another way |
   | `WARN` runs code on install | `preinstall`/`install`/`postinstall` | Read that script before installing |
   | `WARN` close to a popular name | Possible typo or typosquat | Confirm the exact spelling against the project's official docs |
   | `PASS` | Looks established | Still pin the version and keep the lockfile committed |

3. Record the package in the project's dependency register (ARCHITECTURE section 6: why it is needed, alternative considered).

Defaults: `--min-downloads 1000`, `--min-age-days 30`, `--strict` to make warnings fail a CI step.

## After

- Keep scanning known vulnerabilities in CI (`npm audit`, `pip-audit` or Dependabot).
- Commit the lockfile; install with `npm ci` in CI so the lockfile is the source of truth.
- For deeper supply-chain work, use `vulnerability-scanner` and the Context7 docs for the exact tool versions you run.

Offline tests of the logic: `python3 -I -m unittest discover -s tests` from this skill's folder.
