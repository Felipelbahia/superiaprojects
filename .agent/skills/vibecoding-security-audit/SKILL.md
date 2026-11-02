---
name: vibecoding-security-audit
description: Use when an app built or edited with AI needs a security pass before shipping - exposed secrets, Supabase row level security, auth and sessions, user uploads, a new dependency an AI suggested, or AI and usage-priced routes that could run up a bill. Also for "auditoria de segurança" or "vibecoding security audit" requests.
---

# Vibecoding Security Audit

Security pass for AI-generated apps. It adds what the baseline scanners miss; it does not replace them. The owner's checklist is `Vibecoding - Segurança - Checagem` (20 points + AI extras).

## Triage (ask once, load only what applies)

| Ask | If yes |
|---|---|
| Always | Prompt 1 (secrets) in `prompts.md`; run `vulnerability-scanner` (`security_scan.py`) first |
| Does it have accounts or sessions? | Prompt 2 |
| Supabase or a database reachable by the public key? | `supabase-rls.md` + `scripts/rls_audit.sql` + prompt 3 |
| Any user input or file upload? | Prompt 4; uploads: `uploads.md` + `templates/magic-bytes.ts` |
| LLM, e-mail, SMS or other usage-priced routes? | `ai-routes.md` + prompt 5 |
| About to add a dependency, especially one an AI named? | `dependencies.md` + `python3 -I scripts/vet_package.py <npm\|pypi> <name>` |

A "no" skips the module. Do not recite modules the answers exclude.

## Rules

- Audit is read-only: report first, fix as a separate, reviewed change.
- Report format: where | what is wrong | how an attacker uses it | severity | exact fix. The fix is the corrected SQL or code, runnable as written (never "use X" in prose); a finding with no runnable fix says why. Fix order: public storage and unprotected tables, then secrets, then authorization, then the rest.
- A key that ever touched a commit is burned: rotate it, hiding it is not enough.
- Facts about a technology come from its current docs (Context7 or the vendor); the Supabase facts in `supabase-rls.md` carry their check date.
- Overlaps live elsewhere: static scans in `vulnerability-scanner`, review and scan prompts in `claude-security-scan` and `security-guidance-plugin`, Supabase mechanics in `supabase`, secrets handling in `secrets-management`, kill switch and spend caps in `launch-readiness/ops-resilience.md`.
- Never aim offensive security skills at systems you do not own.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Trusting `npm audit` to catch an invented package | Run `vet_package.py` before installing |
| RLS enabled but policies filter on client input | Query 04 and prompt 3; policies must use `auth.uid()` |
| Checking the file extension for uploads | Detect the type from the bytes |
| A rate limit that fails open | Quota errors must deny |
| Fixing while auditing | Report, then fix in a migration |
