---
name: nextjs-static
description: Next.js static site template principles. Landing pages, portfolios, marketing.
---

# Next.js Static Site Template

> **Authority:** this file gives the structure and practices. Every version, command and config name is a *lookup*: ask Context7 (rule "Latest Docs First" in CLAUDE.md) **for the version the project uses** (new project: current stable). The *Snapshot* column and the code blocks come from the docs on 2026-10-11 and are hints only: if they differ from Context7, follow Context7, tell the owner and fix this file.
> **Existing project:** follow its `## Stack` block and lockfile, not this template.
> **Projects built from the previous version of this template** (Next.js 14) are not changed by it: upgrade them with the official upgrade guide (consult Context7), never by copying this template over them.
> For content-heavy Astro sites, the dedicated `astro-development` skill (Base Sites - Astro) is newer than the `astro-static` template.

## Tech Stack

| Component | Technology | Look up in Context7 | Snapshot 2026-10-11 (hint only) |
|-----------|------------|---------------------|----------------------------------|
| Framework | Next.js (Static Export) | "Next.js": static export (`output: 'export'`) and its limits | 16.x · Node ≥ 20.9 · TypeScript ≥ 5.1 |
| Language | TypeScript | "TypeScript" | 5.x |
| Styling | Tailwind CSS | "Tailwind CSS": install with Next.js | v4 · `@import "tailwindcss";` + `@tailwindcss/postcss` |
| Animations | Motion | "Motion": package name and React import path | `motion` (formerly Framer Motion) · import from `motion/react` |
| Icons | Lucide React | "Lucide": React package | `lucide-react` · import only the icons used |
| SEO | Next.js Metadata API (built in) | "Next.js": Metadata API, sitemap, robots | no extra package: `metadata`, `generateMetadata`, `sitemap.ts`, `robots.ts`; `next-seo` is not needed in the App Router |

---

## Directory Structure

```
project-name/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx      # Landing (exports `metadata`)
│   │   ├── sitemap.ts
│   │   ├── robots.ts
│   │   ├── about/
│   │   ├── contact/
│   │   └── blog/
│   ├── components/
│   │   ├── layout/       # Header, Footer
│   │   ├── sections/     # Hero, Features, CTA
│   │   └── ui/
│   └── lib/
├── content/              # Markdown content
├── public/
└── next.config.ts
```

---

## Static Export Config

Snapshot of the docs on 2026-10-11; confirm with Context7.

```ts
// next.config.ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  images: { unoptimized: true },   // the default image loader is not compatible with export
  trailingSlash: true,
};

export default nextConfig;
```

The build writes plain HTML/CSS/JS to the `out` folder.

**Not supported with static export (build fails):** Server Actions, intercepting routes, and the default image-optimization loader. Forms need an external service or a client-side call; there is no server.

---

## Landing Page Sections

| Section | Purpose |
|---------|---------|
| Hero | Main headline, CTA |
| Features | Product benefits |
| Testimonials | Social proof |
| Pricing | Plans |
| CTA | Final conversion |

---

## Animation Patterns

| Pattern | Use |
|---------|-----|
| Fade up | Content entry |
| Stagger | List items |
| Scroll reveal | On viewport |
| Hover | Interactive feedback |

Respect reduced motion; keep animation purposeful.

---

## Setup Steps

Versions in these commands are the 2026-10-11 snapshot: confirm each with Context7 first, and use the version the project already has if it exists.

1. `npx create-next-app@latest {{name}} --yes` (TypeScript, Tailwind, ESLint, App Router, Turbopack by default)
2. Install: `npm install motion lucide-react`
3. Configure static export (above)
4. Create sections
5. `npm run dev`

---

## Deployment

| Platform | Method |
|----------|--------|
| Vercel | Auto |
| Netlify | Auto |
| GitHub Pages | gh-pages branch |
| Any host | Upload `out` folder |

---

## Best Practices

- Static export for maximum performance (no server code)
- Motion for animation, only where it helps the user
- Responsive mobile-first design
- SEO metadata on every page through the built-in Metadata API
