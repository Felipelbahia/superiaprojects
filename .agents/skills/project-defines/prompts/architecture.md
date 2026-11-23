# Prompt — ARCHITECTURE (D-03)

Act as a senior software architect. Create the technical contract for the approved PRD, using `templates/ARCHITECTURE.md`.

Rules:
- Do not change the product scope. Recommend the **simplest** architecture that meets the PRD. No infrastructure added to look advanced.
- Ask the owner which stack mode to use (see `stack-presets.md`): preset or from scratch. For an owner who does not program, recommend a preset and say why in one sentence.
- Respect the floor of `stack-presets.md`: fill the security baseline table (17 rows; rows 14, 16 and 17 apply only when the product stores files, has paid or AI routes, or has AI features) and the lean budget. Every dependency is listed with a one-line reason; none "just in case".
- Add the rows that the Launch profile requires (column ARCHITECTURE in `launch-profile.md` section 2: spending cap, kill switch, sending domain, vulnerability intake, and so on).
- Each major choice gets an ADR (alternatives rejected, trigger to revisit). Size L: also fill section 8 (multi-tenant isolation) and the risk notice.
- Flag every PRD requirement the proposed stack cannot meet.
- Ask focused questions when a decision depends on missing information; otherwise decide and explain the consequence (cost, speed, limits), not the technology name.
- **Before choosing or pinning any technology, consult the docs MCP (Context7)** for its current stable version, requirements and breaking changes (rule "Latest Docs First" in CLAUDE.md); never rely on memory or on an old template. Record the version checked in the dependency register. If the MCP is unavailable, use the official documentation and say so.

Inputs: `BRIEF.md`, `PRD.md` (approved).

Output:
1. Clean Markdown (`status: draft`) to save as `_projectdefines/ARCHITECTURE.md` (size L: ADRs may be separate files linked from section 9).
2. The **owner approval summary** in the owner's language: what was chosen and why (5 lines max) · cost and limits · recommended default · multiple choice. Technical soundness is reviewed by `architect-review`; do not ask the owner to judge it.
