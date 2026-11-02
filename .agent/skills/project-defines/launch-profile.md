# Launch Profile

Mandatory section of the BRIEF, every size. It decides which launch points are born in the documents (not at the end). The facts behind each point live in the skill `launch-readiness`; this file only says **when to ask, where each answer lands, and how the launch phase is built**. Never copy its legal or technical content here.

## 1. The seven questions (BRIEF section "Launch profile")

Plain language, one message, yes/no plus the detail in parentheses. Each has a recommended default; an unknown goes to *Open questions* with that default.

| Q | Ask the owner | If yes, note | Default |
|---|---|---|---|
| Q1 | Will it send e-mails from your own domain (confirmations, receipts, reminders)? | the sending domain | yes if the product has accounts |
| Q2 | Will it have a public site with a contact form or WhatsApp button? | the address | yes if platforms include web |
| Q3 | Will it be published in the phone app stores? | which stores | yes if platforms include phone |
| Q4 | Will it have an assistant or chat that answers with AI? | what it may answer | no |
| Q5 | Will it use a service that charges by usage, or a server that runs by itself? | which services | yes if Q4 or accounts |
| Q6 | Who will use it (Brazil, USA, Europe), and will it have sign-up, recurring charges, file or photo uploads, or users under 18? | tick each | from the BRIEF audience |
| Q7 | Will people in Europe download it as an app? | - | yes if Q3 and Europe |

Size S: ask all seven in one message with the defaults pre-filled from the rest of the BRIEF; the owner corrects what is wrong. Size M and L: same questions, one at a time if the owner prefers.

A deliberate "no" that carries risk (for example "adults only" in Q6) is recorded in *Open decisions* as a decision with its default, so the choice is visible and not silent.

The BRIEF cannot be approved with an unanswered question that blocks a document; use *Open questions* for the rest.

## 2. Where each answer lands

Each landing is a **seed**: a line the document author must write or consciously reject (rejection is recorded in *Open decisions*). The detail of each point is in the named `launch-readiness` file.

| Answer | PRD (features and criteria) | ARCHITECTURE | APP-FLOW | SCHEMA | Launch phase item |
|---|---|---|---|---|---|
| Q1 | - | sending provider and domain; transactional separate from marketing | - | - | L: e-mail DNS check (`scripts/check_email_dns.py`) |
| Q2 | contact form feature: the lead must really arrive | - | 404 screen, thank-you screen | - | L: link check (`scripts/check_site_links.py`) + manual form test |
| Q3 | in-app account deletion; restore purchases if anything is sold | production keys, store review notes, fast-fix path for phone apps | account deletion screen, restore action | - | L: store submission (`store-readiness.md`) |
| Q4 | safety criteria on the assistant feature: says it is AI, no promises about prices/refunds/policies, crisis response, human hand-off | usage limit per user, spending cap, kill switch for the assistant | permanent AI notice, hand-off action | keep/erase policy for conversations | L: assistant tests (`chatbot-guardrails.md`) |
| Q5 | - | hard spending cap, kill switch, restored-backup rehearsal, paid plan that never pauses | - | - | L: operations (`ops-resilience.md`) |
| Q6 | sign-up: account and data deletion; recurring charge: cancel as easy as subscribing, renewal terms beside the buy button; uploads: report-and-remove route; under 18: age check | - | cancel path no longer than the subscribe path; report action | uploads: real deletion and private-by-default storage; consent records | L: legal pre-flight (`legal-preflight.md`: one process for every audience; output is the project's legal register) |
| Q7 | - | vulnerability intake row | - | - | L: vulnerability intake (`templates/security.txt`, `templates/runbook-cra.md`) |

## 3. The launch phase (written by D-08)

- It is the phase just before the final gate (size L: the last module-independent phase).
- One `L-xx` item per **yes** in section 2, plus `L-00`. *Covers* cites the origin (`profile Q3`) and the F-xx/S-xx/E-xx seeds it verifies. *Depends*: the build items that implement those seeds. *Ready when*: the named script passes or the named test list is done, with evidence.
- `L-00 Launch gate`: run `checklist.py` with the flags that apply (`--url`, `--check-links`, `--email-domain`, `--dkim-selector`), then the owner's list `Vibecoding - Lançamento - Checagem`, then the owner's ok. All "no" answers still produce `L-00`.
- Items are verification and submission work. Anything that adds behavior to the product must already exist as an F-xx/S-xx/E-xx; if it does not, stop and propose the document change (document-first).

## 4. Extra checks for the consistency check (D-07)

Each is a blocking finding when the profile answer is yes:

1. Q3 and no feature plus screen for in-app account deletion.
2. Q4 and the assistant feature lacks the safety criteria, or APP-FLOW lacks the permanent AI notice.
3. Q4 or Q5 and ARCHITECTURE lacks the spending cap and kill switch rows.
4. Q6 recurring charge and the cancel path is longer than the subscribe path.
5. Q6 uploads and SCHEMA lacks real deletion and private-by-default storage.
6. Q1 and ARCHITECTURE has no sending provider and domain.
7. Q7 and ARCHITECTURE has no vulnerability intake row.
8. A launch-phase item without a seed it verifies, or a seed without an item.

## 5. Brownfield

Answer the seven questions as-built (label **[as-built]** with evidence); an unmet seed becomes an item of the baseline gap list, not a silent pass.

## 6. Security audit modules

The security baseline is mandatory in every ARCHITECTURE (section 5, 17 rows). The hardening item of the plan runs skill `vibecoding-security-audit`, loading only the modules the product needs. The profile answers and the stack choose them:

| Signal | Module of `vibecoding-security-audit` |
|---|---|
| Always | secrets prompt and the static scan |
| Accounts or sessions exist | authentication prompt |
| The stack uses Supabase or a database reachable by the public key | row-level-security audit (`supabase-rls.md`, `scripts/rls_audit.sql`) |
| Q6 uploads, or any user input | inputs and uploads (`uploads.md`) |
| Q4 assistant, or Q5 usage-priced services | AI and paid routes (`ai-routes.md`) |
| A dependency is added during the build | dependency vetting (`dependencies.md`), before each install |

The consistency check (D-07) also blocks when Q4 or Q5 is yes and ARCHITECTURE rows 16 and 17 are missing, or when the stack stores files and row 14 is missing.
