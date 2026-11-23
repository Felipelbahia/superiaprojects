# Prompt — Adopt the contract in an existing project (brownfield)

Act as a senior engineer adopting `_projectdefines/` in a project that **already exists**. Follow `brownfield.md` of the `project-defines` skill. The owner may not program: talk in plain language, one decision per message.

Hard rules:
- **Read-only on the project.** Do not change, move or delete any existing file. Do not install, run the project or its scripts, or use the network (except Context7 and official docs). Secrets: names only.
- Write only inside `_projectdefines/`. Rules file and `## Stack` block are written **only after** the owner approves ARCHITECTURE.
- Every statement carries a label: `[as-built]` (with the file:line or command that proves it), `[assumption]`, or `[owner]`. Never state what you did not verify.
- Decide which documents apply (`brownfield.md`, section 1). Documents that do not apply are recorded as N/A with the reason; never invent screens or visual rules.

Do, in order:
1. Preflight: project type, manifests and lockfile, `## Stack`, ficha in `0 Padrões/projetos/`, rules files, existing docs, roadmap/backlog, legacy folders.
2. Discover with evidence: topology, routes/screens, data, integrations, env var names, tests, mocks, tech debt, security gaps. Compare the ficha and README against the code and list every divergence.
3. Draft **all applicable documents as-built** from `templates/`, plus the BRIEF with a proposed size and reasons. Unknowns go to *Open questions* with a recommended default.
4. List gaps and divergences under *Open decisions* (both versions and the evidence); security gaps become blocking items.
5. Build `IMPLEMENTATION-PLAN.md`: Phase 0 — Baseline (what exists and works, with evidence), Phase 1 (the adoption), and the existing backlog as later items with its origin.
6. Version check: for each main technology and the runtime, use Context7 (`resolve-library-id` and `query-docs`) for the **installed** version and the current stable; nothing about versions or end of life from memory ("not verified" instead). List the ones behind as backlog items. Never upgrade.
7. Prepare the `## Stack` block and the Gate text inside the ARCHITECTURE draft.

Output:
1. The files created (all `status: draft`).
2. A short table: document → applies / N/A (reason).
3. The top findings and divergences.
4. The **owner approval summary** in the owner's language, for the first document to approve: what it decides (5 lines max), what it limits, the recommended default, multiple choice.

Stop there and wait for the owner's approval. Approve documents one at a time, in order.
