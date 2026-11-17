---
# Repository: https://github.com/Felipelbahia/superiaprojects
name: launch-readiness
description: Use when an app or site built with AI is about to be published or launched, or the user asks for a pre-launch, go-live or "antes de lançar" check beyond code security - email deliverability, app store submission, chatbot risk, kill switch and spend caps, broken links, legal and privacy exposure.
author: Super IA Projects / Futuro Mercado
license: MIT
---
# Launch Readiness

Final pass before going live. It checks what code security does not. **Risk triage, not legal advice**: every legal item carries a verification status; confirm with a lawyer before monetizing.

## Triage (ask once, then load only the modules that apply)

| # | Ask | If yes |
|---|-----|--------|
| 1 | Does the project send email? Which sending domain? | `python3 -I scripts/check_email_dns.py <domain> --selector <dkim-selector>` |
| 2 | Public site, form or WhatsApp link? URL? | `python3 -I scripts/check_site_links.py <url>`, then test the form by hand |
| 3 | App for App Store / Play Store? | `store-readiness.md` |
| 4 | Chatbot or conversational AI? | `chatbot-guardrails.md` + `templates/chatbot-guardrails-prompt.md` |
| 5 | Paid API or remote backend? | `ops-resilience.md` |
| 6 | Audience (BR / US / EU), sensitive data, user uploads, minors, subscriptions? | `legal-preflight.md` (one process for all jurisdictions; reads only the `legal-matrix.md` rows the answers switch on) |
| 7 | Sells in or reaches the EU as a downloadable app? | `templates/security.txt` + `templates/runbook-cra.md` |

Answers "no" skip the module entirely. Do not run or recite a module the answers exclude.

## Rules

- Run scripts with `python3 -I` and the path relative to this skill folder.
- Report only FAIL and WARN; PASS is one line.
- A legal item marked `não verificado` is a prompt to check the source, never a fact to repeat.
- Policy or terms text is out of scope: check that they exist and match what the code does.
- Overlaps resolve elsewhere: privacy mechanics in `gdpr-data-handling`, a11y in `accessibility-compliance`, SEO in the marketing hub (`sip-marketing`, project 0 Mkt), speed in `performance-profiling`.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Dumping every module "to be safe" | Triage first; skip what the answers exclude |
| Stating a fine amount as settled | Quote the item's status; unverified means unverified |
| Checking DKIM without a selector | Selector comes from the email provider dashboard; ask for it |
| Trusting a green link check as form test | Scripts cannot prove a lead email arrives; send a real submission |
