---
status: draft
approved:
---
# ARCHITECTURE — Technical Requirements

> The technical contract. Keep it as simple as the PRD allows. Anything not listed here (dependency, service, env var) cannot be added to the code until it is listed here.

## 1. Overview
- Architecture in two or three sentences:
- Platforms:
- Main constraints:

## 2. Stack
- **Mode:** A (preset: P1 / P2 / P3) or B (from scratch). See `stack-presets.md`.
- If a preset was left or altered: link to the ADR.
- **Stack record:** mirror the stack (names only) in the `## Stack` block of the project's rules file; the versions live in the lockfile.

| Layer | Choice | Reason | Rejected alternatives |
|---|---|---|---|
| Frontend | | | |
| Backend | | | |
| Database | | | |
| Authentication | | | |
| File storage | | | |
| Hosting | | | |
| Testing | | | |

- **Capabilities (reuse scan, skill `oss-scout`):** one row per PRD capability, classified reuse / platform / build. Search only the `reuse` ones; format in `oss-scout/templates/CAPABILITIES.md`.

| Capability | Class | Decision | Candidate (version checked) | Reason | Source and date | Owner approval |
|---|---|---|---|---|---|---|

## 3. Responsibilities
Client · server · database · external services.

## 4. APIs and integrations
For each: purpose · data sent and received · authentication · usage limits and cost · failure handling.

## 5. Security baseline (mandatory; mark each as done / planned in item T-xx)

| # | Requirement | Where it is handled |
|---|---|---|
| 1 | Authentication and authorization defined for every route and resource | |
| 2 | Access rule per table or resource enforced on the server side | |
| 3 | Secrets only in environment variables; never in git; `.gitignore` before the first commit | |
| 4 | All input validated; queries parameterized; user content escaped | |
| 5 | Mass assignment blocked (explicit allow-lists on writes) | |
| 6 | Session cookies protected; passwords hashed with a modern algorithm | |
| 7 | Rate limit on login and critical routes; bot protection where public | |
| 8 | File uploads restricted by type and size | |
| 9 | API responses return only the fields needed | |
| 10 | HTTPS, HSTS and security headers | |
| 11 | Dependency scanning in CI | |
| 12 | Sensitive data identified, encrypted or kept out | |
| 13 | Admin and dashboard accounts (hosting, database, DNS, CMS) protected with two-factor | |
| 14 | If the product stores files: buckets private by default; backups, dumps and secrets never in the web root; views and functions respect the row rules | |
| 15 | Every new dependency checked before install (exists, age, downloads, install scripts) | |
| 16 | If the product has paid or AI routes: per-user quota, provider hard cap, kill switch, fail closed | |
| 17 | If the product has AI features: model input and output treated as untrusted; no destructive action without human confirmation | |

## 6. Lean budget
- Targets measured at the gates: LCP ≤ 2.5 s · INP ≤ 200 ms · CLS ≤ 0.1.
- Dependency register (every library justified; none "just in case"):

| Dependency | Version checked (date, source) | Why it is needed | Alternative considered |
|---|---|---|---|

## 7. Environments and deployment
Local · staging · production · environment variables (names only) · CI checks · deploy approach · backup and restore.

## 8. Multi-tenant isolation (size L, or any project with several customers' data)
- [ ] Tenant identity comes only from the authenticated session, never from forms, URLs or unchecked cookies.
- [ ] Every business table has a non-null tenant column and enforced row rules; the app role cannot bypass them.
- [ ] References between records include the tenant (a record cannot point into another tenant); uniqueness and counters are per tenant.
- [ ] Files, cache, queues, search, logs, e-mails, PDFs, exports and public links carry and verify the tenant.
- [ ] A record from another tenant answers exactly like a missing one.
- [ ] Automated tests with tenants A, B and canary data attack IDs, search, exports, reports and links; a check fails CI when a new table lacks the rules; disabling one rule must make the suite fail.
- [ ] Risk notice shown at the gate: leak between customers · financial/tax calculation · data migration.

## 9. ADR index
| ADR | Decision | Status |
|---|---|---|

## 10. Risks and open questions
| # | Question | Recommended default | Owner's answer |
|---|---|---|---|

## Change log

| Date | What changed | Approved by |
|---|---|---|

## Approval record

Date · criteria met · owner decision · reviewer agents
