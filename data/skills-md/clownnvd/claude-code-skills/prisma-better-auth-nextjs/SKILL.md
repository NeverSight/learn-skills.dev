---
name: prisma-better-auth-nextjs
description: "Prisma 7 + Better Auth + Next.js App Router. Email/password, OAuth, 2FA, rate limiting, audit logging. Triggers: add auth, better auth, prisma auth, nextjs login, sign-up/sign-in, auth scaffold."
license: Complete terms in LICENSE.txt
---

# Prisma + Better Auth + Next.js Setup Guide

> Source: prisma.io/docs/guides/authentication/better-auth/nextjs

## Prerequisites

- Node.js 20+, Next.js App Router + TypeScript
- **PostgreSQL** (Neon, Supabase, local) — for MySQL/SQLite swap the adapter

## Steps Overview — Core (Basic Setup)

| Step | Folder | Files | What |
|------|--------|-------|------|
| 1 | `1-setup-project/` | [create-nextjs-app](references/1-setup-project/create-nextjs-app.md) | Create Next.js project |
| 2.1 | `2-setup-prisma/` | [install-dependencies](references/2-setup-prisma/install-dependencies.md) | Install Prisma + pg |
| 2.2 | | [configure-prisma](references/2-setup-prisma/configure-prisma.md) | `prisma.config.ts` |
| 2.3 | | [generate-client](references/2-setup-prisma/generate-client.md) | Generate typed client |
| 2.4 | | [global-client](references/2-setup-prisma/global-client.md) | Singleton `src/lib/db/index.ts` |
| 3.1 | `3-setup-better-auth/` | [install-configure](references/3-setup-better-auth/install-configure.md) | Install + `src/lib/auth.ts` |
| 3.2 | | [add-auth-models](references/3-setup-better-auth/add-auth-models.md) | User, Session, Account (with `@@map`) |
| 3.3 | | [migrate-database](references/3-setup-better-auth/migrate-database.md) | Run migration |
| 4.1 | `4-api-routes/` | [setup-routes](references/4-api-routes/setup-routes.md) | Catch-all + auth client |
| 5.1 | `5-pages/` | [sign-up](references/5-pages/sign-up.md) | Sign up form |
| 5.2 | | [sign-in](references/5-pages/sign-in.md) | Sign in form |
| 5.3 | | [dashboard](references/5-pages/dashboard.md) | Protected dashboard |
| 5.4 | | [home](references/5-pages/home.md) | Landing page |
| 6 | `6-test/` | [test-app](references/6-test/test-app.md) | Test + troubleshoot |

## Steps Overview — Advanced (Production-Grade)

| Step | Folder | Files | What |
|------|--------|-------|------|
| 2.5 | `2-setup-prisma/` | [neon-adapter](references/2-setup-prisma/neon-adapter.md) | Neon serverless adapter + dual URLs |
| 2.6 | | [slow-query-logging](references/2-setup-prisma/slow-query-logging.md) | Structured slow query detection |
| 3.4 | `3-setup-better-auth/` | [oauth-providers](references/3-setup-better-auth/oauth-providers.md) | Google + GitHub OAuth |
| 3.5 | | [two-factor](references/3-setup-better-auth/two-factor.md) | TOTP 2FA plugin |
| 3.6 | | [email-verification](references/3-setup-better-auth/email-verification.md) | Resend + React Email templates |
| 3.7 | | [session-config](references/3-setup-better-auth/session-config.md) | Session, cookies, trustedOrigins |
| 4.2 | `4-api-routes/` | [rate-limiting](references/4-api-routes/rate-limiting.md) | Upstash Redis + account lockout |
| 4.3 | | [audit-logging](references/4-api-routes/audit-logging.md) | Structured auth event logging |

## Key Files

| File | Purpose |
|------|---------|
| `prisma.config.ts` | Datasource URL (Prisma 7: `DIRECT_URL` fallback) |
| `src/lib/db/index.ts` | Global Prisma + Neon adapter + slow query logging |
| `src/lib/auth.ts` | Better Auth config (email, OAuth, 2FA, hooks) |
| `src/lib/auth-client.ts` | React client (`signIn`, `signUp`, `signOut`, `useSession`, `twoFactor`) |
| `src/lib/rate-limit.ts` | Upstash Redis rate limiter + in-memory fallback |
| `src/lib/auth/audit-log.ts` | Structured auth event logger |
| `src/lib/email/resend.ts` | Resend email sender + fire-and-forget variant |
| `src/app/api/auth/[...all]/route.ts` | Auth API + rate limit + account lockout |

## Quick Commands

```bash
# Core
npm install prisma tsx --save-dev
npm install @prisma/client @prisma/adapter-neon better-auth
npx @better-auth/cli@latest secret
npx @better-auth/cli generate
npx prisma migrate dev --name add-auth-models

# Advanced
npm install @upstash/ratelimit @upstash/redis resend react-email
```

## Key Patterns

- **Prisma 7**: `prisma.config.ts` for datasource, NOT `schema.prisma`
- **@@map**: All models use `@@map("lowercase")` — required by Better Auth
- **Neon dual URLs**: `DATABASE_URL` (pooled) for queries, `DIRECT_URL` for migrations
- **trustedOrigins**: Required if port != 3000 or in production
- **Rate limiting**: Upstash Redis (prod) / in-memory (dev), 4 presets
- **Account lockout**: 10 failures in 15 min → 30 min lockout
- **IP extraction**: Last `X-Forwarded-For` IP (proxy-set, not spoofable)
- **OAuth**: Conditional enable via `Boolean(ID && SECRET)`
- **Email verification**: Auto-enable via `Boolean(process.env.RESEND_API_KEY)`
- **Audit log**: JSON in prod, readable in dev, no PII

## Scaffold Script

```bash
python .claude/skills/prisma-better-auth-nextjs/scripts/scaffold.py [target-dir]
```
