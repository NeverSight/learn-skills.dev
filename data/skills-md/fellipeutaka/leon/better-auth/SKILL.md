---
name: better-auth
description: |
  Better Auth — framework-agnostic TypeScript authentication & authorization library.
  Covers setup, email/password, social OAuth (40+ providers), passkeys, magic links,
  2FA, organizations, sessions, plugins, admin, hooks, and security hardening.
  Use when implementing auth with Better Auth: configuring auth instances, adding
  providers, setting up database adapters (Prisma, Drizzle, PostgreSQL, MySQL, SQLite,
  MongoDB), integrating with frameworks (Next.js, Nuxt, SvelteKit, Astro, Hono, Express,
  Elysia, Fastify, Expo), managing sessions, or extending with plugins.
---

# Better Auth

Framework-agnostic TypeScript auth library. Plugin-based architecture, 40+ OAuth providers, 18+ framework integrations.

## Quick Start

### Install

```bash
npm install better-auth
```

Scoped packages (as needed):

| Package | Use case |
|---------|----------|
| `@better-auth/passkey` | WebAuthn/Passkey auth |
| `@better-auth/sso` | SAML/OIDC enterprise SSO |
| `@better-auth/stripe` | Stripe payments |
| `@better-auth/expo` | React Native/Expo |

### Environment Variables

```env
BETTER_AUTH_SECRET=<32+ chars, generate: openssl rand -base64 32>
BETTER_AUTH_URL=http://localhost:3000
DATABASE_URL=<connection string>
```

### Server Config (`lib/auth.ts`)

```ts
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: process.env.DATABASE_URL,  // or adapter instance
  emailAndPassword: { enabled: true },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  },
  plugins: [], // add plugins here
});

export type Session = typeof auth.$Infer.Session;
```

### Client Config (`lib/auth-client.ts`)

```ts
import { createAuthClient } from "better-auth/react"; // or /vue, /svelte, /solid, /client

export const authClient = createAuthClient({
  plugins: [], // add client plugins here
});
```

### Route Handler

| Framework | File | Handler |
|-----------|------|---------|
| Next.js App Router | `app/api/auth/[...all]/route.ts` | `toNextJsHandler(auth)` → export `{ GET, POST }` |
| Next.js Pages | `pages/api/auth/[...all].ts` | `toNextJsHandler(auth)` → default export |
| Express | any | `app.all("/api/auth/*splat", toNodeHandler(auth))` |
| Hono | route | `app.on(["POST","GET"], "/api/auth/**", (c) => auth.handler(c.req.raw))` |
| SvelteKit | `hooks.server.ts` | `svelteKitHandler({ auth, event })` |
| Astro | `pages/api/auth/[...all].ts` | `toAstroHandler(auth)` |
| Elysia | plugin | `new Elysia().mount(auth.handler)` |

See [references/framework-integrations.md](references/framework-integrations.md) for all frameworks.

### CLI Commands

```bash
npx @better-auth/cli@latest migrate          # Apply schema (built-in adapter)
npx @better-auth/cli@latest generate          # Generate for Prisma/Drizzle
npx @better-auth/cli@latest generate --output prisma/schema.prisma
npx @better-auth/cli@latest generate --output src/db/auth-schema.ts
```

**Re-run after adding/changing plugins.**

## Core Concepts

- **Server instance** (`auth`): handles all auth logic, DB, sessions
- **Client instance** (`authClient`): framework-specific hooks (`useSession`, `signIn`, `signUp`, `signOut`)
- **Plugins**: extend both server and client — add endpoints, DB tables, hooks
- **Type inference**: `auth.$Infer.Session`, `auth.$Infer.Session.user` for full type safety
- For separate client/server projects: `createAuthClient<typeof auth>()`

## Authentication Methods

| Method | Package | Config/Plugin | Reference |
|--------|---------|---------------|-----------|
| Email/Password | built-in | `emailAndPassword: { enabled: true }` | [authentication.md](references/authentication.md) |
| Social OAuth | built-in | `socialProviders: { google: {...} }` | [authentication.md](references/authentication.md) |
| Magic Link | built-in | `magicLink()` plugin | [authentication.md](references/authentication.md) |
| Passkey | `@better-auth/passkey` | `passkey()` plugin | [authentication.md](references/authentication.md) |
| Username | built-in | `username()` plugin | [authentication.md](references/authentication.md) |
| Email OTP | built-in | `emailOtp()` plugin | [authentication.md](references/authentication.md) |
| Phone Number | built-in | `phoneNumber()` plugin | [authentication.md](references/authentication.md) |
| Anonymous | built-in | `anonymous()` plugin | [authentication.md](references/authentication.md) |

## Plugin Quick Reference

Import from dedicated paths for tree-shaking: `import { twoFactor } from "better-auth/plugins/two-factor"` NOT `from "better-auth/plugins"`.

| Plugin | Server Import | Client Import | Purpose |
|--------|---------------|---------------|---------|
| `twoFactor` | `better-auth/plugins/two-factor` | `twoFactorClient` | TOTP, OTP, backup codes |
| `organization` | `better-auth/plugins/organization` | `organizationClient` | Multi-tenant orgs, teams, RBAC |
| `admin` | `better-auth/plugins/admin` | `adminClient` | User management, impersonation |
| `passkey` | `@better-auth/passkey` | `passkeyClient` | WebAuthn/FIDO2 |
| `magicLink` | `better-auth/plugins/magic-link` | `magicLinkClient` | Passwordless email links |
| `emailOtp` | `better-auth/plugins/email-otp` | `emailOtpClient` | Email one-time passwords |
| `username` | `better-auth/plugins/username` | `usernameClient` | Username-based auth |
| `phoneNumber` | `better-auth/plugins/phone-number` | `phoneNumberClient` | Phone-based auth |
| `anonymous` | `better-auth/plugins/anonymous` | `anonymousClient` | Guest sessions |
| `apiKey` | `better-auth/plugins/api-key` | `apiKeyClient` | API key management |
| `bearer` | `better-auth/plugins/bearer` | — | Bearer token auth |
| `jwt` | `better-auth/plugins/jwt` | `jwtClient` | JWT tokens |
| `multiSession` | `better-auth/plugins/multi-session` | `multiSessionClient` | Multiple active sessions |
| `oauthProvider` | `better-auth/plugins/oauth-provider` | — | Become OAuth provider |
| `oidcProvider` | `better-auth/plugins/oidc-provider` | — | Become OIDC provider |
| `sso` | `@better-auth/sso` | `ssoClient` | SAML/OIDC enterprise SSO |
| `openAPI` | `better-auth/plugins/open-api` | — | API documentation |
| `customSession` | `better-auth/plugins/custom-session` | — | Extend session data |
| `genericOAuth` | `better-auth/plugins/generic-oauth` | `genericOAuthClient` | Custom OAuth providers |
| `oneTap` | `better-auth/plugins/one-tap` | `oneTapClient` | Google One Tap |

Pattern: server plugin in `auth({ plugins: [...] })` + client plugin in `createAuthClient({ plugins: [...] })` + re-run CLI migrations.

See [references/plugins.md](references/plugins.md) for detailed usage and custom plugin creation.

## Database Setup

| Adapter | Setup |
|---------|-------|
| SQLite | Pass `better-sqlite3` or `bun:sqlite` instance |
| PostgreSQL | Pass `pg.Pool` instance |
| MySQL | Pass `mysql2` pool |
| Prisma | `prismaAdapter(prisma, { provider: "postgresql" })` from `better-auth/adapters/prisma` |
| Drizzle | `drizzleAdapter(db, { provider: "pg" })` from `better-auth/adapters/drizzle` |
| MongoDB | `mongodbAdapter(db)` from `better-auth/adapters/mongodb` |
| Connection string | `database: process.env.DATABASE_URL` (uses built-in Kysely) |

**Critical:** Config uses ORM model name, NOT DB table name. Prisma model `User` mapping to table `users` → use `modelName: "user"`.

Core schema tables: `user`, `session`, `account`, `verification`. Plugins add their own tables.

See [references/setup.md](references/setup.md) for full database setup details.

## Session Management

Key options:

```ts
session: {
  expiresIn: 60 * 60 * 24 * 7,  // 7 days (default)
  updateAge: 60 * 60 * 24,       // refresh every 24h (default)
  freshAge: 60 * 60 * 24,        // require re-auth after 24h for sensitive ops
  cookieCache: {
    enabled: true,
    maxAge: 300,                  // 5 min
    strategy: "compact",          // "compact" | "jwt" | "jwe"
  },
}
```

- **`secondaryStorage`** (Redis/KV): sessions go there by default, not DB
- **Stateless mode**: no DB + cookieCache = session in cookie only
- **`customSession` plugin**: extend session with custom fields

See [references/sessions.md](references/sessions.md) for full session management details.

## Security Checklist

| DO | DON'T |
|----|-------|
| Use 32+ char secret with high entropy | Commit secrets to version control |
| Set `baseURL` with HTTPS in production | Disable CSRF check (`disableCSRFCheck`) |
| Configure `trustedOrigins` for all frontends | Disable origin check |
| Enable rate limiting (on by default in prod) | Use `"memory"` rate limit storage in serverless |
| Configure `backgroundTasks.handler` on serverless | Skip email verification setup |
| Use `"jwe"` cookie cache for sensitive session data | Store OAuth tokens unencrypted if used for API calls |
| Set `revokeSessionsOnPasswordReset: true` | Return specific error messages ("user not found") |

See [references/security.md](references/security.md) for complete security hardening guide.

## Common Gotchas

1. **Model vs table name** — config uses ORM model name, not DB table name
2. **Plugin schema** — re-run CLI after adding/changing plugins
3. **Secondary storage** — sessions go there by default, not DB. Set `session.storeSessionInDatabase: true` to persist both
4. **Cookie cache** — custom session fields NOT cached, always re-fetched from DB
5. **Callback URLs** — always use absolute URLs with origin (not relative paths)
6. **Express v5** — use `"/api/auth/*splat"` not `"/api/auth/*"` for catch-all routes
7. **Next.js RSC** — add `nextCookies()` plugin to auth config for server component session access

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "Secret not set" | Add `BETTER_AUTH_SECRET` env var |
| "Invalid Origin" | Add domain to `trustedOrigins` |
| Cookies not setting | Check `baseURL` matches domain; enable secure cookies in prod |
| OAuth callback errors | Verify redirect URIs in provider dashboard match exactly |
| Type errors after adding plugin | Re-run CLI generate/migrate |
| Session null in RSC | Add `nextCookies()` plugin |
| 2FA redirect not working | Add `twoFactorClient` with `onTwoFactorRedirect` to client |

## Reference Index

| File | When to read |
|------|-------------|
| [setup.md](references/setup.md) | Setting up new project, configuring DB, route handlers |
| [authentication.md](references/authentication.md) | Implementing any auth method (email, social, passkey, magic link, etc.) |
| [sessions.md](references/sessions.md) | Configuring session expiry, caching, stateless mode, secondary storage |
| [security.md](references/security.md) | Hardening for production — rate limiting, CSRF, cookies, OAuth security |
| [plugins.md](references/plugins.md) | Using or creating plugins, plugin catalog |
| [framework-integrations.md](references/framework-integrations.md) | Framework-specific setup (Next.js, Nuxt, SvelteKit, Hono, Express, etc.) |
| [two-factor.md](references/two-factor.md) | Implementing 2FA (TOTP, OTP, backup codes, trusted devices) |
| [organizations.md](references/organizations.md) | Multi-tenant orgs, teams, invitations, RBAC |
| [admin.md](references/admin.md) | User management, roles, banning, impersonation |
| [hooks-and-middleware.md](references/hooks-and-middleware.md) | Custom logic via before/after hooks, DB hooks, middleware |
