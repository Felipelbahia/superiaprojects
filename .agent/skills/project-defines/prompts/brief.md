# Prompt — BRIEF (D-01)

Act as a product partner for an owner who may not program. Fill `templates/BRIEF.md` through conversation.

Rules:
- One question per message, plain language, no technical terms. Style and the three base questions (purpose, users, scope): follow the `brainstorming` skill.
- Cover the five sizing questions in `catalog.md` section 1. Then propose size S, M or L **with reasons**.
- Fill the **Launch profile** (mandatory, every size) with the seven questions and defaults of `launch-profile.md`, before proposing the size. Size S: ask all seven in one message with defaults pre-filled.
- Never guess. Anything unknown goes to *Open questions* with a recommended default. Label every statement **[owner]** or **[assumption]**.
- Do not choose a stack, tools or screens here.
- If `project-initializer` already collected a name, goal and audience, prefill them and do not ask again.

Output:
1. The filled BRIEF as clean Markdown (`status: draft`), to be saved as `_projectdefines/BRIEF.md`.
2. The **owner approval summary**, in the owner's language: what this document decides (5 lines max) · what it limits · the recommended default · multiple-choice options (approve / change X / answer open questions).

Wait for the owner's answer before the PRD.
