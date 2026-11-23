# Prompt — APP-FLOW (D-04)

Act as a senior product designer. Create the App Flow for the approved PRD and ARCHITECTURE, using `templates/APP-FLOW.md`. Use the `mermaid-expert` agent for the diagram.

Rules:
- Map every screen with an ID (S-01…): route, purpose, the PRD feature it supports, entry conditions, main content, primary and secondary actions with their destination, and the states loading, empty, error and success.
- Fill the **action matrix** (screen · trigger/button · condition · feedback · next screen). No button without a destination.
- Include the primary journey, secondary journeys, authentication, decision points, edge cases and navigation rules (protected routes, back behavior, deep links).
- Add the screens and actions that the Launch profile requires (column APP-FLOW in `launch-profile.md` section 2); each must map to a PRD feature.
- Do not add screens the PRD does not support. Flag missing or contradictory flows instead of guessing.
- Add the traceability table (feature → screens). Every F-xx maps to at least one screen.

Inputs: `PRD.md`, `ARCHITECTURE.md` (approved).

Output:
1. Clean Markdown (`status: draft`) with a plain-language journey summary, the screen inventory, a Mermaid flowchart and the screen-by-screen detail; save as `_projectdefines/APP-FLOW.md`.
2. The **owner approval summary** in the owner's language: the main path in 5 lines · what is deliberately not in v1 · recommended default · multiple choice.
