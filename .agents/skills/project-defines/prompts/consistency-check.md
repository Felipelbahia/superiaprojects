# Prompt — Consistency check (D-07)

Act as an independent reviewer (`architect-review` for structure, `security-auditor` for security). Audit the approved documents as **one connected specification** before any code is written.

Inputs: `BRIEF.md`, `PRD.md`, `ARCHITECTURE.md`, `APP-FLOW.md`, `PATTERNS.md`, `SCHEMA.md` (and the module map for size L).

Check for:
- Features in one document missing from another
- Screens without a supporting PRD feature
- Buttons or actions without a destination
- Entities or fields with no product purpose
- PRD features with no screen, data or (after D-08) plan item
- Technical choices that cannot support the approved flow
- Flow states missing from PATTERNS
- Authentication or permission conflicts
- Different names for the same thing
- Security baseline rows (ARCHITECTURE section 5) not handled in SCHEMA or APP-FLOW
- The eight Launch profile checks in `launch-profile.md` section 4 (blocking when the profile answer is yes)
- Unresolved assumptions presented as confirmed decisions
- Size L: tenant isolation gaps (ARCHITECTURE section 8)

Return:
1. Blocking contradictions
2. Important gaps
3. Minor naming inconsistencies
4. Exact corrections required, per file
5. A traceability matrix: feature → screen → entity → (plan item)

Do not rewrite the documents or start coding. Present the corrections in the owner's language with a recommended default for each; apply them to a document only after the owner approves (document-first rule), and record each in that document's *Change log*.
