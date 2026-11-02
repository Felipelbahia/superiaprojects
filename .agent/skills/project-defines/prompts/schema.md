# Prompt — SCHEMA (D-06)

Act as a senior backend and database architect. Design the data and access model for the approved PRD, ARCHITECTURE and APP-FLOW, using `templates/SCHEMA.md`. Consult `database-architect`, `database-design` and `auth-implementation-patterns`.

Rules:
- Do not invent features. Every entity (E-01…) must support a named feature (F-xx) or screen (S-xx).
- Define: authentication and session model, roles and permissions, every entity with columns, types, required/default, validation, unique constraints, indexes and references; relationships with delete behavior; **access rules per entity (create, read, update, delete)** enforced on the server side or by row rules; core operations and transaction boundaries; file storage; sensitive data handling; retention and deletion; migrations and seed data.
- Block mass assignment (explicit allow-lists on writes). Every ownership check must tie a record to the signed-in user (or tenant).
- Size L: this document is the **core only** (tenants, users, roles, permissions, audit). Every entity carries the tenant column; module entities come later in `modules/<module>/SCHEMA.md`.
- Return a plain-English data overview, a table-by-table schema, a Mermaid ER diagram, the access-control table and the traceability list (entity → features).
- Apply the data rules that the Launch profile requires (column SCHEMA in `launch-profile.md` section 2: real deletion, private-by-default storage, consent records, conversation retention).
- Apply `ARCHITECTURE.md` section 5 (security baseline). Flag anything it cannot satisfy.

Inputs: `PRD.md`, `ARCHITECTURE.md`, `APP-FLOW.md` (approved). With the Supabase MCP available you may inspect an existing project; otherwise write the SQL by hand.

Output:
1. Clean Markdown (`status: draft`) to save as `_projectdefines/SCHEMA.md`.
2. The **owner approval summary** in the owner's language: what information the app stores and who can see or change it (5 lines max) · what is kept out or deleted · recommended default · multiple choice. Technical soundness is reviewed by `security-auditor`.
