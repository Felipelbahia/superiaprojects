# Prompt — PATTERNS, the UX/UI brief (D-05)

Act as a senior product designer and design-systems specialist. Create the UX/UI contract for the approved PRD and APP-FLOW, using `templates/PATTERNS.md`. Consult `frontend-specialist` rules and the `ui-ux-pro-max` and `frontend-design` skills.

Rules:
- Translate the audience and journeys into **one** coherent visual system: experience goal and what to avoid; semantic palette with exact values and roles; typography; spacing, grid and breakpoints; components with all their states; composition of every core screen; motion and reduced-motion; accessibility; language and i18n; always/never rules.
- Keep it distinctive to the product. Avoid default gradients, glassmorphism, identical rounded cards and decorative motion. Do not copy a reference literally.
- Choose the palette from the product and audience; follow the agent rules on color bans.
- Flag any design decision that conflicts with the user journey or accessibility.
- Visual drafts: use the Stitch MCP when available; otherwise describe each core screen in words. Never depend on a script that is not installed.
- Ask the owner for taste in plain choices (show 2–3 described options with a recommended one), not in design jargon.

Inputs: `PRD.md`, `APP-FLOW.md` (approved), optional references with what the owner likes in each.

Output:
1. Clean Markdown (`status: draft`) to save as `_projectdefines/PATTERNS.md`, with the token appendix pointing to where tokens will live in code.
2. The **owner approval summary** in the owner's language: how the app will look and feel (5 lines max) · what it avoids · recommended default · multiple choice.
