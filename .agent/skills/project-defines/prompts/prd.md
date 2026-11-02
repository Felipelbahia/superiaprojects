# Prompt — PRD (D-02)

Act as a senior product manager. Create the PRD for the first usable version, using `templates/PRD.md` and the approved BRIEF.

Rules:
- No code and no technical stack. Describe what the user sees and gets.
- Every feature gets an ID (F-01…), a user need, inputs, expected output, checkable acceptance criteria and error/empty states.
- Keep version 1 realistic: separate must-have from nice-to-have; fill *Included*, *Explicitly excluded* and *Possible later*. Excluded items are a promise: code will not include them.
- Add measurable success criteria and the non-functional requirements that matter (privacy, accessibility, devices).
- Seed the features and acceptance criteria that the BRIEF's Launch profile requires (column PRD in `launch-profile.md` section 2); a seed you reject goes to *Assumptions and open questions*.
- Size L: add the module map (module, purpose, dependencies, order); do not detail modules here.
- Do not silently invent important requirements. Missing information goes to *Assumptions and open questions* with a recommended default; ask focused questions if it blocks the document.

Inputs: `_projectdefines/BRIEF.md` (approved).

Output:
1. Clean Markdown (`status: draft`) to save as `_projectdefines/PRD.md`.
2. The **owner approval summary** in the owner's language: what the product will and will not do in v1 (5 lines max) · what it costs in scope · recommended default · multiple choice.
