---
name: tinyship-deploy
description: >-
  Deploy TinyShip to production: Docker, Vercel, Cloudflare Workers, or VPS
  with PM2/Nginx. Use when the user asks to "deploy", "go to production",
  "deploy to vercel", "docker deploy", "cloudflare workers", "set up server",
  "deploy to VPS", or "production setup".
---

# TinyShip Deployment

Guide for deploying TinyShip to production.

## Choose Platform

Ask the user which deployment target they prefer:

| Platform | Best For | Framework Support |
|----------|----------|-------------------|
| **Docker** | Self-hosted, full control | All 3 frameworks |
| **Vercel** | Next.js projects, zero-config | Next.js (recommended) |
| **Cloudflare Workers** | Edge deployment, global | TanStack Start only |
| **VPS (PM2 + Nginx)** | Traditional hosting | All 3 frameworks |

Then read the relevant reference file and follow the steps.

## Pre-Deployment Checklist (All Platforms)

Before deploying, ensure:

1. **Production database** is ready (PostgreSQL recommended)
2. **Environment variables** are set for production:
   - `APP_BASE_URL` — your production domain (e.g., `https://app.example.com`)
   - `BETTER_AUTH_URL` — same as `APP_BASE_URL`
   - `BETTER_AUTH_SECRET` — a strong random secret (generate with `openssl rand -hex 32`)
   - `DATABASE_URL` — production database connection string
3. **OAuth redirect URIs** updated to production domain
4. **Payment webhook URLs** updated to production domain
5. **Database migrated**: `pnpm db:push` against production database

## Docker Deployment

Read [references/docker-deploy.md](references/docker-deploy.md) for full steps.

Quick summary:
```bash
# Build and run with Docker Compose
docker compose --profile next up -d  # or --profile nuxt / --profile tanstack

# Or build individual image
docker build -f apps/next-app/Dockerfile -t tinyship .
```

## Vercel Deployment

Read [references/vercel-deploy.md](references/vercel-deploy.md) for full steps.

Quick summary:
1. Push to GitHub
2. Import project in Vercel Dashboard
3. Set root directory to `apps/next-app`
4. Configure environment variables
5. Deploy

## Cloudflare Workers

Read [references/cloudflare-deploy.md](references/cloudflare-deploy.md) for full steps.

Only available for TanStack Start. Uses D1 database and Wrangler CLI.
Read `apps/tanstack-app/CF-NOTES.md` for known pitfalls.

## VPS (PM2 + Nginx)

Read `docs/user-guide/deployment/traditional.md` in the TinyShip repo.

Quick summary:
1. Build the app: `pnpm build:next` (or nuxt/tanstack)
2. Install PM2: `npm install -g pm2`
3. Start with PM2: `pm2 start .output/server/index.mjs --name tinyship`
4. Configure Nginx reverse proxy to port 7001
5. Set up SSL with Let's Encrypt

## Post-Deployment

After deploying:

1. Verify health: `curl https://yourdomain.com/api/health`
2. Test login flow
3. Update OAuth redirect URIs for all providers
4. Update payment webhook URLs
5. Run a test payment if payments are configured
6. Set up monitoring/alerting

## Reference Files in TinyShip Repo

- `docs/user-guide/deployment/overview.md` — deployment documentation index
- `docs/user-guide/deployment/docker.md` — Docker deployment guide
- `docs/user-guide/deployment/cloud.md` — cloud platform guide
- `docs/user-guide/deployment/cloudflare-workers.md` — CF Workers guide
- `docs/user-guide/deployment/traditional.md` — VPS/PM2 guide
- `docker-compose.yml` — Docker Compose configuration
- `apps/tanstack-app/CF-NOTES.md` — Cloudflare Workers pitfalls
- `apps/tanstack-app/wrangler.jsonc` — Wrangler configuration
