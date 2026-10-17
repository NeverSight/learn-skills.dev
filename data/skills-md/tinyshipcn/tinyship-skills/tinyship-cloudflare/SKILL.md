---
name: tinyship-cloudflare
description: >-
  One-stop Cloudflare setup for TinyShip: Workers + D1/Hyperdrive + R2 + Email Sending +
  Turnstile. Use when the user asks to "set up cloudflare", "all-in cloudflare", "deploy to
  workers", "configure d1", "configure r2", "cf setup", "cloudflare full stack", or wants
  to use the Cloudflare ecosystem for their TinyShip project.
---

# TinyShip Cloudflare Setup

One-stop wizard to configure the full Cloudflare stack for TinyShip (TanStack Start).

**This is a conversational, step-by-step wizard. You MUST ask the user at each
decision point and wait for their answer before proceeding. NEVER make choices
on the user's behalf.**

## Step 0: Detect Template & Route

First, read [../../references/template-detection.md](../../references/template-detection.md)
and detect which template the current project is.

### If the project is tinyship-cf (Cloudflare-only template)

The project is already Cloudflare-native — bindings, D1, and the Workers setup are
preconfigured. Do NOT run framework cleanup or wrangler scaffolding. Go directly to
the **Fast Path** below.

### If the project is shipeasy (multi-framework)

**⛔ STOP — You MUST tell the user and ask before proceeding.**

> TinyShip now has a dedicated Cloudflare template (**tinyship-cf**) that ships
> preconfigured for Workers (no hacks, no framework cleanup needed). For NEW
> Cloudflare projects, starting from tinyship-cf is recommended.
>
> - **Continue here** — configure Cloudflare in this shipeasy project (makes sense
>   if you already built features on it)
> - **Switch to tinyship-cf** — start fresh from the dedicated template and migrate
>   your changes manually

If the user chooses to continue, follow the **Full Wizard** below.

---

## Fast Path (tinyship-cf projects)

### 1. Wrangler Login

```bash
cd apps/tanstack-app
npx wrangler login
npx wrangler whoami   # capture the Account ID
```

If already logged in, skip and tell the user.

### 2. Local env

```bash
cp apps/tanstack-app/.dev.vars.example apps/tanstack-app/.dev.vars
```

Set `BETTER_AUTH_SECRET` (`openssl rand -hex 32`). Verify local dev:

```bash
pnpm dev   # http://localhost:7001
```

### 3. Remote database

The D1 database is already bound in `wrangler.jsonc`. Apply migrations and verify:

```bash
npx wrangler d1 migrations apply tinyship-db --remote
```

For Hyperdrive + PostgreSQL instead of D1, read and follow
[references/hyperdrive-setup.md](references/hyperdrive-setup.md).

### 4. Secrets

**⛔ STOP — ask the user which features they use, then set only those secrets.**

```bash
npx wrangler secret put BETTER_AUTH_SECRET      # required
# Payments (as needed): STRIPE_SECRET_KEY, PAYPAL_CLIENT_ID/SECRET,
#   DODO_PAYMENTS_API_KEY/WEBHOOK_KEY, CREEM_API_KEY/WEBHOOK_SECRET
# AI image/video (as needed): QWEN_API_KEY, FAL_API_KEY,
#   GOOGLE_GENERATIVE_AI_API_KEY, VOLCENGINE_ACCESS_KEY_ID
# Email: RESEND_API_KEY
```

Notes:
- **Chat AI needs no secret** — it runs on Workers AI + AI Gateway. Third-party
  chat keys (OpenAI/DeepSeek) are managed in the AI Gateway dashboard (BYOK).
- `AI_GATEWAY_ID` defaults to `default`; if the user's gateway has a different
  name, set it in `wrangler.jsonc` `vars`.
- Payment webhook URLs in each provider dashboard must point to the production domain.

### 5. Optional extras

Ask about each, then read and follow the matching reference:
- **R2 storage** — [references/r2-setup.md](references/r2-setup.md) (bucket already bound)
- **Email Sending** — [references/email-setup.md](references/email-setup.md)
- **Turnstile** — [references/turnstile-setup.md](references/turnstile-setup.md)

### 6. Deploy

```bash
pnpm deploy:cf
```

Verify: home page 200, `/en/pricing` 200, login works. If `pricing_plan` table is
empty and `PRICING_MODE=dynamic`, log in as admin → Admin → Pricing Plans →
**Import Static** to populate plans.

Go to **Step 8: Summary**.

---

## Full Wizard (shipeasy projects)

> **Scope:** This wizard configures TanStack Start (`apps/tanstack-app`) for Cloudflare
> Workers deployment. Next.js and Nuxt.js are designed for Node.js environments and
> do not deploy to Workers.

### Prerequisites

1. **Node.js >= 22.20.0** — run `node -v`
2. **pnpm >= 9.0.0** — run `pnpm -v`
3. **Dependencies installed** — if `node_modules/` is missing, run `pnpm install`
4. **A Cloudflare account** — https://dash.cloudflare.com/sign-up

### Step 1: Wrangler Login

Run the following to authenticate with Cloudflare:

```bash
cd apps/tanstack-app
npx wrangler login
```

This opens a browser for authorization. After success, verify:

```bash
npx wrangler whoami
```

Capture the **Account ID** from the output — it will be reused for R2 and Email.

If the user is already logged in (`wrangler whoami` shows account info), skip this step
and tell the user.

### Step 2: Framework Cleanup

**⛔ STOP — You MUST ask the user before proceeding.**

Since Cloudflare Workers only supports TanStack Start, the Next.js and Nuxt.js apps
are not needed for a Cloudflare-only deployment. Ask the user:

**You've chosen the all-in Cloudflare path, which uses TanStack Start exclusively.
Do you want to remove the Next.js and Nuxt.js apps from the project?**

| Option | Action |
|--------|--------|
| **Yes — clean up** | Remove `apps/next-app` and `apps/nuxt-app`, update workspace config |
| **No — keep them** | Leave them in place (useful if you also plan Node.js deployments) |

#### If the user chooses Yes:

Follow the cleanup procedure from the `tinyship-setup` skill:
read and follow [../tinyship-setup/references/framework-cleanup.md](../tinyship-setup/references/framework-cleanup.md)
using **TanStack Start** as the kept framework.

Summary of what to do:
1. `rm -rf apps/next-app apps/nuxt-app`
2. Update `turbo.json` — remove `.nuxt/**`, `.output/**`, `.next/**` from build outputs
3. Update root `package.json` — remove `dev:next`, `build:next`, `dev:nuxt`, `build:nuxt` etc.,
   rename `dev:tanstack` → `dev`, `build:tanstack` → `build`, etc.
4. Update `docker-compose.yml` — remove `next-app` and `nuxt-app` services
5. Update `.github/workflows/ci.yml` — remove build steps for deleted apps
6. Run `pnpm install` to clean up the lockfile

After cleanup, run `pnpm typecheck` and `pnpm build` (which now point to TanStack) to verify.

#### If the user chooses No:

Skip this step. The other apps remain in the project but won't be deployed to Workers.

### Step 3: Database — D1 or Hyperdrive

**⛔ STOP — You MUST ask the user before proceeding.**

Present these options and wait for the user's response:

| Option | Database | Best For |
|--------|----------|----------|
| **A** | **Cloudflare D1** (SQLite) | All-in Cloudflare, zero external deps, low cost |
| **B** | **Hyperdrive + PostgreSQL** | Reuse existing PG, high write concurrency, data parity with Next/Nuxt |

Explain the trade-offs:
- **D1**: Fully managed, included in Workers billing, 5-10 GB limit, single-writer constraint
- **Hyperdrive**: Needs an external PostgreSQL, but no storage limits, same DB across all 3 apps

#### If the user chooses D1:

Read and follow [references/d1-setup.md](references/d1-setup.md).

#### If the user chooses Hyperdrive:

Read and follow [references/hyperdrive-setup.md](references/hyperdrive-setup.md).

**After database is configured, verify locally:**

```bash
cd apps/tanstack-app
pnpm dev:cf
```

Check that the app loads and database-dependent pages work. Tell the user the results.

### Step 4: R2 Storage (Optional)

**⛔ STOP — You MUST ask the user before proceeding.**

Ask: **Do you want to set up Cloudflare R2 for file storage (images, uploads)?**

- **Yes** — read and follow [references/r2-setup.md](references/r2-setup.md)
- **No** — skip (can be configured later)

### Step 5: Email Sending (Optional)

**⛔ STOP — You MUST ask the user before proceeding.**

Ask: **Do you want to use Cloudflare Email Sending for transactional emails
(verification codes, password resets)?**

- **Yes** — read and follow [references/email-setup.md](references/email-setup.md)
- **No** — skip (default is Resend, or configure later)

### Step 6: Turnstile Bot Protection (Optional)

**⛔ STOP — You MUST ask the user before proceeding.**

Ask: **Do you want to enable Cloudflare Turnstile (CAPTCHA) for login/signup protection?**

- **Yes** — read and follow [references/turnstile-setup.md](references/turnstile-setup.md)
- **No** — skip (disabled by default, safe to add later)

### Step 7: Deploy to Workers

**⛔ STOP — You MUST ask the user before proceeding.**

Ask: **Do you want to deploy to Cloudflare Workers now, or just finish the local setup?**

- **Deploy now** — read and follow [references/workers-deploy.md](references/workers-deploy.md)
- **Later** — tell the user they can deploy anytime with `cd apps/tanstack-app && pnpm run deploy:cf`

### Step 8: Summary

After setup is complete, provide a summary of what was configured:

```
✅ Cloudflare Setup Complete
─────────────────────────────
Template:   [tinyship-cf (fast path) / shipeasy (full wizard)]
Frameworks: TanStack Start only [Next/Nuxt removed / kept]
Workers:    TanStack Start on Cloudflare Workers
Database:   [D1 / Hyperdrive+PG] — configured and verified
Storage:    [R2 / skipped]
Email:      [Cloudflare Email / skipped]
Turnstile:  [enabled / skipped]
Deployment: [deployed to <url> / ready for deploy]

Next steps:
- tinyship-cf: `pnpm dev` for local dev, `pnpm deploy:cf` to deploy
- shipeasy: `cd apps/tanstack-app && pnpm dev:cf` / `pnpm run deploy:cf`
- Use `npx wrangler tail` to view live logs
```

## Reference Files in TinyShip Repo

When executing this skill, read these files from the user's project for context:

- `apps/tanstack-app/wrangler.jsonc` — current Wrangler config
- `apps/tanstack-app/CF-NOTES.md` — known Cloudflare pitfalls
- `apps/tanstack-app/.dev.vars.example` — local dev vars template (tinyship-cf)
- `env.example` — all environment variables (shipeasy only)
- `apps/tanstack-app/vite.config.ts` — CF plugin conditional loading
- `docs/user-guide/deployment/cloudflare-workers.md` — full deployment guide
- `config/storage.ts` — R2 config structure
- `config/email.ts` — Email config structure
- `config/captcha.ts` — Turnstile config structure
