---
name: templates
description: Project scaffolding templates for new applications. Use when creating new projects from scratch. Contains 13 templates for various tech stacks.
allowed-tools: Read, Glob, Grep
---

# Project Templates

> Quick-start templates for scaffolding new projects.

---

## 🎯 Selective Reading Rule

**Read ONLY the template matching user's project type!**

> 📚 **Latest Docs First.** A template is a starting point, not the truth about versions. Before scaffolding, consult the docs MCP (Context7) for every technology in it, follow what the docs say today, and update the template when it is outdated (rule in CLAUDE.md). The *Verified* column shows the last time a template was checked; **"not verified" means the versions in it must be checked before use.** Who wins: for facts about a technology, Context7 (for the version the project uses; new project: current stable); for structure and practices, the template. An existing project's `## Stack` block and lockfile come first.

| Template | Tech Stack | When to Use | Verified (Context7) |
|----------|------------|-------------|---------------------|
| [nextjs-fullstack](nextjs-fullstack/TEMPLATE.md) | Next.js + Prisma | Full-stack web app | 2026-10-11 |
| [nextjs-saas](nextjs-saas/TEMPLATE.md) | Next.js + Stripe | SaaS product | 2026-10-11 |
| [nextjs-static](nextjs-static/TEMPLATE.md) | Next.js + Motion | Landing page | 2026-10-11 |
| [nuxt-app](nuxt-app/TEMPLATE.md) | Nuxt + Pinia (Vue) | Full-stack app with Vue (the Vue counterpart of Next.js) | not verified |
| [express-api](express-api/TEMPLATE.md) | Express + JWT | REST API | not verified |
| [python-fastapi](python-fastapi/TEMPLATE.md) | FastAPI | Python API | not verified |
| [react-native-app](react-native-app/TEMPLATE.md) | Expo + Zustand | Mobile app | not verified |
| [flutter-app](flutter-app/TEMPLATE.md) | Flutter + Riverpod | Cross-platform | not verified |
| [electron-desktop](electron-desktop/TEMPLATE.md) | Electron + React | Desktop app | not verified |
| [chrome-extension](chrome-extension/TEMPLATE.md) | Chrome MV3 | Browser extension | not verified |
| [cli-tool](cli-tool/TEMPLATE.md) | Node.js + Commander | CLI app | not verified |
| [monorepo-turborepo](monorepo-turborepo/TEMPLATE.md) | Turborepo + pnpm | Monorepo | not verified |
| [astro-static](astro-static/TEMPLATE.md) | Astro + MDX | Blog / Docs. For Astro sites prefer the newer `astro-development` skill (Base Sites - Astro) | not verified (says Astro 4.x) |

---

## Usage

1. User says "create [type] app"
2. Match to appropriate template
3. Read ONLY that template's TEMPLATE.md
4. Consult Context7 for each technology in it (see the note above) and fix the template if outdated
5. Follow its tech stack and structure
