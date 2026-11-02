# Stack: presets or from scratch

`ARCHITECTURE.md` asks which mode to use. For an owner who does not program, the recommended default is a preset.

## The floor (both modes, non-negotiable)

- **Security baseline:** authentication and authorization defined; access rule per table or resource enforced on the server side (row-level rules or equivalent), never only in the browser; secrets only in environment variables and never in git; all input validated; database queries parameterized; user content escaped; sensitive data identified; rate limit on login and critical routes; HTTPS and security headers; dependency scanning; two-factor on admin accounts; private storage by default; dependencies vetted before install; and, when the product has paid or AI routes, quota, hard spend cap, kill switch and untrusted model input/output. Source: the owner's list `Vibecoding - Segurança - Checagem`.
- **Lean budget:** every dependency has a one-line justification in `ARCHITECTURE.md`; no library "just in case"; prefer platform features; measured targets at the gates: LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 (Core Web Vitals "good").
- **Nothing outside the document:** adding a dependency means updating `ARCHITECTURE.md` first (document-first).
- **Latest docs first:** before choosing a stack or scaffolding a preset, consult the docs MCP (Context7) for every technology: current stable version (release candidates are never the default), requirements, breaking changes, recommended setup. Presets and `app-builder` templates are starting points: re-verify their versions and update the template when outdated. Record the version checked in the dependency register. No MCP: official documentation, and say so. **Who wins:** facts about a technology come from the docs, for the version the project actually uses; kit rules and process come from the kit. The project records its stack (names only, no frozen versions) in the `## Stack` block of its rules file (format in CLAUDE.md).

## Mode A: presets

Reference by path; never copy. Templates live in `.agent/skills/app-builder/templates/<name>/TEMPLATE.md` (resolve through the fallback order if the project has no local copy).

| Preset | Use for | Template |
|---|---|---|
| **P1 Content site** | Landing pages, blogs, documentation, static sites | For Astro sites use the `astro-development` skill (Base Sites - Astro: `/Users/macbookpro/Documents/IA Projects/_Plataforma/Base Sites - Astro/.agent/skills/astro-development/SKILL.md`), which is newer than the `astro-static` template (still says Astro 4.x). Without Astro: `nextjs-static`. |
| **P2 Web app with login and data** | Internal tools, small CRMs, dashboards | `nextjs-fullstack` |
| **P3 SaaS with payments** | Subscriptions, several paying customers, e-mail | `nextjs-saas` (the auth choice, and the fact that Auth.js v5 is installed with the `beta` tag, are noted there; ask the owner) |

Other templates exist (mobile, desktop, API, CLI, browser extension, monorepo) for owners who name that need; they are not presets. Note: the index in `app-builder/templates/SKILL.md` omits `nuxt-app`, which exists as a folder; do not rely on the index alone.

Leaving a preset, or swapping one of its parts, requires an ADR in `ARCHITECTURE.md`.

## Mode B: from scratch

1. Read the `architecture` skill (context discovery and trade-off analysis).
2. Compare at least two options against the PRD and the floor; keep the simplest that meets them.
3. Write an ADR per major choice, including rejected alternatives and the trigger to revisit.
4. The same floor applies. A from-scratch stack that cannot meet it is rejected.
5. Explain the choice to the owner by its consequences (cost, speed, limits), not by technology names.
