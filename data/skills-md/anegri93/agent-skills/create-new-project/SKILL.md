---
name: create-new-project
description: Scaffold a production-ready Next.js (App Router) + TypeScript + Tailwind + shadcn/ui + Supabase (Postgres/Auth/Storage) boilerplate, deployable to Vercel. Includes Supabase migrations, RLS-ready multi-tenant schema, and example API routes (internal + external).
---

# create-new-project

## When to use
Use this skill whenever the user wants to start a new web app using the standard stack:
- Next.js (App Router) + TypeScript
- Tailwind CSS + shadcn/ui
- Supabase (Postgres, Auth, Storage, Realtime)
- Deploy on Vercel
- API routes in Next.js for internal + third-party integrations

## What you must ask (minimal)
Ask only what is necessary:
1) Project name (kebab-case recommended)
2) Package manager: pnpm (default) / npm
3) Supabase mode:
   - "local-first" (init Supabase locally + migrations)
   - "cloud-only" (create env placeholders; user will link later)

If the user explicitly wants external integrations, confirm:
- "public API for third-party order creation" yes/no (default: yes)

## Execution plan (do this in order)
1) Create the project folder using the script (pick the right OS reminder):
   - macOS/Linux/Git-Bash/WSL: `bash scripts/create-new-project.sh <name>`
   - Windows PowerShell: `powershell -ExecutionPolicy Bypass -File scripts/create-new-project.ps1 -Name <name>`

2) Ensure the scaffold includes:
   - Next.js app (App Router) + Tailwind
   - shadcn/ui initialized
   - Supabase client helpers (server + browser)
   - `.env.example` + `.env.local` placeholders (never commit secrets)
   - Supabase migration file with baseline schema for orders/sales (multi-tenant ready)
   - Example API routes:
     - `/api/v1/orders` (authenticated internal)
     - `/api/v1/public/orders` (API key for third-party callers)

3) After generation, run:
   - install deps (if not already)
   - `pnpm dev` (or npm) quick smoke test
   - if Supabase CLI present and local-first: `supabase init` and confirm migration file exists

4) Output to the user:
   - what was created (high-level)
   - exact next steps to connect Supabase Cloud + Vercel env vars
   - how to call the public API endpoint from another system

## Guardrails
- Do NOT add next-themes/react-day-picker unless versions are compatible with the chosen React/Next baseline.
- Do NOT commit `.env.local`, Supabase service role keys, or Vercel tokens.
- Keep the project "boring": simple, predictable, production-ready defaults.

## References
- See `references/STACK.md` for backend/API model on Vercel + Supabase.
- See `references/DB_SCHEMA.sql` for schema + RLS-ready patterns.
