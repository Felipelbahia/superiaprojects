---
name: nextjs-saas
description: Next.js SaaS template principles. Auth, payments, email.
---

# Next.js SaaS Template

> **Authority:** this file gives the structure and practices. Every version, command and config name is a *lookup*: ask Context7 (rule "Latest Docs First" in CLAUDE.md) **for the version the project uses** (new project: current stable). The *Snapshot* column and the code blocks come from the docs on 2026-10-11 and are hints only: if they differ from Context7, follow Context7, tell the owner and fix this file.
> **Existing project:** follow its `## Stack` block and lockfile, not this template.
> **Projects built from the previous version of this template** (Next.js 14) are not changed by it: upgrade them with the official upgrade guide (consult Context7), never by copying this template over them.
> Base setup (Next.js 16, Prisma 7 with driver adapter, Tailwind v4, Zod 4, `proxy.ts`): see `nextjs-fullstack/TEMPLATE.md`. Only what is specific to a SaaS is below.

## Tech Stack

| Component | Technology | Look up in Context7 | Snapshot 2026-10-11 (hint only) |
|-----------|------------|---------------------|----------------------------------|
| Framework | Next.js (App Router) | "Next.js": as in `nextjs-fullstack` | 16.x · `proxy.ts` replaces `middleware.ts` |
| Auth | **ASK USER** (options below) | the chosen option's library | Do not pick for the user: present the options, with consequences, and record the choice as an ADR |
| Payments | Stripe | "Stripe Node": current major, webhook signature verification | `stripe` v22 · verify the signature with the **raw** request body |
| Database | PostgreSQL + Prisma ORM | "Prisma": as in `nextjs-fullstack` | ORM 7 stable · ORM 8 only a release candidate |
| Email | Resend | "Resend": send from a Route Handler with a React template | `resend` · templates as React components · `from` on a verified domain |
| UI | Tailwind + **ASK USER**: shadcn/ui / Headless UI / Custom | "shadcn/ui": init with Tailwind v4 | `npx shadcn@latest init`, then `add <component>` |

---

## Auth options (ASK USER)

Before choosing, **ask the owner and bring these possibilities** in plain language: what it is, who holds the users' data, the effort, the cost and dependency, and the risk. Say which one you would recommend **for this project and why**, but let the owner decide, then record it as an ADR in `ARCHITECTURE.md`. Check each option in Context7 right before use (facts below were verified on 2026-10-11).

| Option | What it is | Maturity in the docs | Where the users live | Fits when | Watch out |
|---|---|---|---|---|---|
| **Auth.js v5** (NextAuth) | Open-source library that runs inside your app | The official guide installs it with the **`beta` tag** (`next-auth@beta`) | Your own database (Prisma adapter `@auth/prisma-adapter`) | You want control and no vendor | A beta tag is not the default in this kit: confirm status first; you maintain the security updates |
| **Better Auth** | Open-source TypeScript auth framework with plugins (2FA, SSO, passkeys…) | 1.x line (v1.6.x in the docs index) | Your own database (Prisma adapter); handler mounted at `/api/auth/[...all]` | You want control plus rich features | Newer ecosystem: read its Next.js integration page before use |
| **Clerk** | Managed service: ready-made screens and user management | `@clerk/nextjs` with `proxy.ts` (see `nextjs-fullstack`) | Clerk's servers | You want the least auth code and the least to maintain | External dependency and a pricing model: check both with the owner; routes are public until protected |
| **Supabase Auth** | Auth of the Supabase backend, used through `@supabase/ssr` | `@supabase/ssr` replaces the deprecated `auth-helpers` packages | Supabase's servers | The project already uses Supabase as its backend | Ties the project to Supabase; the proxy/middleware that refreshes the session is mandatory |

---

## Directory Structure

```
project-name/
├── prisma/
├── prisma.config.ts           # Prisma 7
├── src/
│   ├── app/
│   │   ├── (auth)/            # Login, register
│   │   ├── (dashboard)/       # Protected routes
│   │   ├── (marketing)/       # Landing, pricing
│   │   └── api/
│   │       ├── auth/[...nextauth]/   # only with Auth.js
│   │       └── webhooks/stripe/
│   ├── components/
│   │   ├── auth/
│   │   ├── billing/
│   │   └── dashboard/
│   ├── lib/
│   │   ├── db.ts              # Prisma client singleton
│   │   ├── auth.ts            # Auth.js config (if used)
│   │   ├── stripe.ts          # Stripe client
│   │   └── email.ts           # Resend client
│   ├── proxy.ts               # route protection (Next.js 16)
│   └── config/
│       └── subscriptions.ts
└── package.json
```

---

## SaaS Features

| Feature | Implementation |
|---------|---------------|
| Auth | Auth.js (OAuth/email) or Clerk |
| Subscriptions | Stripe Checkout (`mode: 'subscription'`) |
| Billing Portal | Stripe customer portal |
| Webhooks | Stripe events, signature verified server-side |
| Email | Transactional via Resend |

---

## Database Schema

| Model | Fields |
|-------|--------|
| User | id, email, stripeCustomerId, subscriptionId |
| Account | OAuth provider data (Auth.js) |
| Session | User sessions (Auth.js, database strategy) |

---

## Environment Variables

| Variable | Purpose |
|----------|---------|
| DATABASE_URL | Prisma (server only) |
| AUTH_SECRET | Only with Auth.js v5 (`npx auth secret`); the `NEXTAUTH_` prefix is no longer used. Other auth options: variables per their docs (consult Context7) |
| STRIPE_SECRET_KEY | Payments (server only) |
| STRIPE_WEBHOOK_SECRET | Webhooks (server only) |
| RESEND_API_KEY | Email (server only) |

Clerk instead of Auth.js: `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` and `CLERK_SECRET_KEY`.

---

## Setup Steps

Versions in these commands are the 2026-10-11 snapshot: confirm each with Context7 first, and use the version the project already has if it exists.

1. `npx create-next-app@latest {{name}} --yes` (Node.js ≥ 20.9). Then the Prisma 7, Zod 4 and Tailwind steps from `nextjs-fullstack`.
2. Install: `npm install stripe resend`; then the auth option the owner chose, following its docs (consult Context7): for example `npm install next-auth@beta @auth/prisma-adapter` (Auth.js) or `npm install @clerk/nextjs` (Clerk)
3. Setup Stripe products/prices
4. Configure environment (secrets only in env vars, never in git)
5. `npx prisma migrate dev --name init`
6. Stripe CLI `stripe listen` forwarding to `/api/webhooks/stripe` (local webhooks)
7. `npm run dev`

---

## Best Practices

- Route groups for layout separation
- Stripe webhooks are the source of truth for subscription state; verify the signature using the raw body
- Check authorization on the server in every Server Action and Route Handler, not only in `proxy.ts`
- Auth with the Prisma adapter (`@auth/prisma-adapter`) when Auth.js is chosen
- Email templates as React components (React Email)
