# Document Catalog

Single source of the recipes. Phase 1 of every `IMPLEMENTATION-PLAN.md` is born from the table below (items D-01…D-08).

## 1. Sizing (asked inside the BRIEF)

Ask in plain language, one question per message (style: `brainstorming`):

1. Who will use it, and are there different kinds of users (for example staff and clients)?
2. Will several separate companies or customers use the same system, each seeing only its own data? (multi-tenant)
3. Does it handle money, invoices, tax data, health data or personal data about other people?
4. How many main areas does it have (for example contacts, deals, invoices, reports)?
5. Does it need to talk to other services (payments, e-mail, WhatsApp, tax authority, ERP)?

Propose a size **with the reasons**; the owner confirms. The size can go up later (S→M→L) through the document-first rule in `conformance.md`.

| Size | Starting thresholds (adjust with use) | Structure | Phase 1 rigor |
|---|---|---|---|
| **S** | One kind of user, one main flow, no sensitive data | 7 files | Light: the document's *approved when* is the rubric; its approval record is appended to the document |
| **M** | 2–3 roles, 3–5 areas, some integration | 7 files | Light, except ARCHITECTURE and SCHEMA, which run the full `execution-loop` (costliest to change) |
| **L** | Multi-tenant, or financial/sensitive data, or 6+ modules (CRM/ERP class) | Global files + `modules/<module>/` | Full `execution-loop` on every global document and every module definition |

Light approval record = a final section `## Approval record` (date, criteria met, owner decision). No extra files.

**D-01 (BRIEF) is always light:** it is the document that produces the size, so the rigor column applies from D-02 onward.

## 2. Phase 1 recipes

MCPs are **optional accelerators**: detect which tools exist at run time, never assume one. The manual path always works.

| ID | Document | Created with | Optional MCP → manual path | Needs | Template · Prompt | Approved when | Approver |
|---|---|---|---|---|---|---|---|
| D-01 | `BRIEF.md` | `brainstorming` + `product-owner` | none → conversation | n/a | `BRIEF.md` · `brief.md` | Every section filled, including the Launch profile (`launch-profile.md`); size proposed with reasons; unknowns listed as open questions | Owner |
| D-02 | `PRD.md` | `product-manager` + `spec-writing` | none | BRIEF | `PRD.md` · `prd.md` | Every feature has an F-xx ID, acceptance criteria and error/empty states; v1 / excluded / later split; success criteria; no unmarked open question | Owner |
| D-03 | `ARCHITECTURE.md` | `backend-architect` + `architecture` (ADRs) | **Context7, always before choosing any technology** (rule "Latest Docs First" in CLAUDE.md) → official docs by hand | PRD | `ARCHITECTURE.md` · `architecture.md` | Stack mode chosen (`stack-presets.md`); each dependency justified; security baseline and lean budget present; major choices have an ADR with rejected alternatives | Owner (consequences) + `architect-review` |
| D-04 | `APP-FLOW.md` | `mermaid-expert` + template | none → plain Mermaid/text | PRD, ARCHITECTURE | `APP-FLOW.md` · `app-flow.md` | Every screen S-xx has route, purpose, entry, action → destination, and loading/empty/error/success states; flowchart present; every PRD feature maps to ≥1 screen | Owner |
| D-05 | `PATTERNS.md` | `frontend-specialist` + `ui-ux-pro-max` | Stitch for visual drafts → written description with tokens | PRD, APP-FLOW | `PATTERNS.md` · `patterns.md` | Tokens with exact values; components with states; composition of each core screen; accessibility; always/never rules; i18n | Owner |
| D-06 | `SCHEMA.md` | `database-architect` + `database-design` + `auth-implementation-patterns` | Supabase to inspect/apply → SQL written by hand | PRD, ARCHITECTURE, APP-FLOW | `SCHEMA.md` · `schema.md` | Every table E-xx maps to a feature; auth model and roles; access rules per table (create/read/update/delete); relations and ER diagram; deletion/retention | Owner + `security-auditor` |
| D-07 | Consistency check | `architect-review` + `security-auditor` | none | D-02…D-06 | none · `consistency-check.md` | No blocking contradiction; same names for the same things; every F-xx has a screen and data; findings fixed or explicitly accepted | Owner |
| D-08 | Expand the plan | `project-planner` + `plan-writing` | none | all | `IMPLEMENTATION-PLAN.md` · `expand-plan.md` | Every item has *Covers*, *Depends* and a *ready when* line; first build phase ends in a runnable skeleton; gates defined; no item without coverage | Owner |

Notes:
- **D-02a (optional) Reference study:** after the PRD and before D-03, when the owner wants to learn from open source projects. Skill `oss-scout` (Reference study mode); output: report in `.agent/plans/` and `THIRD_PARTY.md`. In size L it may precede a module definition. Not a gate item.
- **Existing project:** the same documents are drafted **as-built** from the code, and some do not apply to the project type: see `brownfield.md`.
- `ui-ux-pro-max` is documentation-only here (its `search.py --persist` script is not bundled). If the owner installs its CLI in the project, the generated `design-system/` is attached to `PATTERNS.md` as a token appendix; `PATTERNS.md` stays the contract.
- Size L adds, per module, the module templates (`templates/module-*.md`), created when the module's turn comes: its definition is an item of the module's phase in the plan.
- Premises written by the AI are **open questions with a recommended default** until the owner answers; a document with an unanswered question that blocks it cannot be approved.
