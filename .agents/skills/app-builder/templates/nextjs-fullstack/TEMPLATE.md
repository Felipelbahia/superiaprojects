---
name: nextjs-fullstack
description: Next.js full-stack template principles. App Router, Prisma, Tailwind.
---

# Next.js Full-Stack Template

> **Authority:** this file gives the structure and practices. Every version, command and config name is a *lookup*: ask Context7 (rule "Latest Docs First" in CLAUDE.md) **for the version the project uses** (new project: current stable). The *Snapshot* column and the code blocks come from the docs on 2026-10-11 and are hints only: if they differ from Context7, follow Context7, tell the owner and fix this file.
> **Existing project:** follow its `## Stack` block and lockfile, not this template.

## Tech Stack

| Component | Technology | Look up in Context7 | Snapshot 2026-10-11 (hint only) |
|-----------|------------|---------------------|----------------------------------|
| Framework | Next.js (App Router) | "Next.js": current stable, Node and TypeScript requirements, `create-next-app` options, upgrade notes | 16.2.x · Node ≥ 20.9 · TypeScript ≥ 5.1 · Turbopack default |
| Language | TypeScript | "TypeScript": version the framework and libraries require | 5.x (≥ 5.5 for Zod 4) |
| Database | PostgreSQL + Prisma ORM | "Prisma": stable major, install steps, `prisma.config.ts`, generator, driver adapter | ORM 7 stable · ORM 8 only a release candidate (not the default) |
| Styling | Tailwind CSS | "Tailwind CSS": install with Next.js | v4 · CSS-first `@import "tailwindcss";` + `@tailwindcss/postcss` |
| Auth | Clerk (optional) | "Clerk": Next.js quickstart, route-protection file | `@clerk/nextjs` · `proxy.ts` with `clerkMiddleware()` · `<ClerkProvider>` |
| Validation | Zod | "Zod": current major and TypeScript requirement | 4 · `npm install zod@^4` |

---

## Directory Structure

```
project-name/
├── prisma/
│   └── schema.prisma        # generator "prisma-client" + models
├── prisma.config.ts         # Prisma 7: schema path, migrations path, DATABASE_URL
├── src/
│   ├── app/
│   │   ├── layout.tsx       # <ClerkProvider> if Clerk is used
│   │   ├── page.tsx
│   │   ├── globals.css      # @import "tailwindcss";
│   │   └── api/
│   ├── components/
│   │   └── ui/
│   ├── generated/prisma/    # generated client; do not edit; add to .gitignore
│   ├── lib/
│   │   ├── db.ts            # Prisma client singleton (driver adapter)
│   │   └── utils.ts
│   ├── proxy.ts             # replaces middleware.ts (Next.js 16)
│   └── types/
├── AGENTS.md                # created by create-next-app
├── .env.example
└── package.json
```

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| Server Components | Default, fetch data |
| Server Actions | Form mutations (validate input and check authorization inside each one) |
| Route Handlers | API endpoints |
| `proxy.ts` | Runs before routes (the new name of `middleware.ts`); export a function named `proxy` or the Clerk helper |
| Async request APIs | `cookies()`, `headers()`, `params`, `searchParams` are **async only**: always `await` them |
| Prisma 7 | Type-safe ORM; needs a driver adapter (`@prisma/adapter-pg`); client is generated into `src/generated/prisma` |

Key snippets (docs snapshot 2026-10-11; confirm with Context7 before pasting):

```ts
// prisma.config.ts
import "dotenv/config";
import { defineConfig, env } from "prisma/config";

export default defineConfig({
  schema: "prisma/schema.prisma",
  migrations: { path: "prisma/migrations" },
  datasource: { url: env("DATABASE_URL") },
});
```

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client"
  output   = "../src/generated/prisma"
}
```

```ts
// src/lib/db.ts  (note: the import path ends with /client)
import { PrismaClient } from "@/generated/prisma/client";
import { PrismaPg } from "@prisma/adapter-pg";

const adapter = new PrismaPg({ connectionString: process.env.DATABASE_URL! });
const globalForPrisma = global as unknown as { prisma: PrismaClient };

export const prisma = globalForPrisma.prisma || new PrismaClient({ adapter });
if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;
```

---

## Environment Variables

| Variable | Purpose |
|----------|---------|
| DATABASE_URL | Prisma connection (server only) |
| NEXT_PUBLIC_APP_URL | Public URL |
| NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY | Clerk public key (only if Clerk is used) |
| CLERK_SECRET_KEY | Clerk secret (server only; never in git) |

---

## Setup Steps

Versions in these commands are the 2026-10-11 snapshot: confirm each with Context7 first, and use the version the project already has if it exists.

1. `npx create-next-app@latest {{name}} --yes` (default setup: TypeScript, Tailwind CSS, ESLint, App Router, Turbopack, `@/*` alias, `AGENTS.md`). Requires Node.js ≥ 20.9.
2. `npm install zod@^4`
3. `npm install prisma@7 tsx @types/pg --save-dev` and `npm install @prisma/client@7 @prisma/adapter-pg dotenv pg`
4. Create `prisma.config.ts`, `prisma/schema.prisma` and `src/lib/db.ts` (snippets above); add `src/generated/prisma` to `.gitignore`
5. `npx prisma migrate dev --name init` (it also generates the client)
6. Optional auth: `npm install @clerk/nextjs`; create `src/proxy.ts` with `clerkMiddleware()` and wrap `layout.tsx` in `<ClerkProvider>`. Routes are **public by default**: protect them explicitly.
7. `npm run dev`

---

## Best Practices

- Server Components by default
- Server Actions for mutations, always validating with Zod and checking who is calling
- Prisma for type-safe DB access through the single client in `src/lib/db.ts`
- Zod for validation at every boundary
- Node runtime for anything touching the database
- Secrets only in environment variables, never in git
