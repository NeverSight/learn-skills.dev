---
name: nextjs-webflow-to-vercel
description: "Migrate a Next.js application from Webflow Cloud to Vercel. Use this skill when a user wants to move, migrate, or port a Next.js app off Webflow Cloud onto Vercel. This covers removing the OpenNext Cloudflare adapter (@opennextjs/cloudflare) and the initOpenNextCloudflareForDev dev hook, uninstalling Wrangler, deleting the Webflow Cloud config files (webflow.json, wrangler.json, open-next.config.ts, cloudflare-env.d.ts), dropping the base path the app mounted under on a Webflow site (basePath and assetPrefix in next.config.ts), removing the Edge runtime directive (export const runtime = 'edge') from Route Handlers and middleware, repointing Cloudflare storage bindings read through getCloudflareContext().env (Object Storage/R2, Key Value Store/Workers KV, SQLite/D1) to Vercel storage, recreating environment variables, and deploying. Next.js runs natively on Vercel, so no adapter replaces OpenNext. Triggers include phrases like 'migrate to Vercel', 'move off Webflow Cloud', 'Next.js Webflow Cloud to Vercel', or the presence of webflow.json, wrangler.json, @opennextjs/cloudflare, open-next.config.ts, or getCloudflareContext in a Next.js project. Do not use for non-Next.js frameworks or for migrations in the opposite direction (Vercel to Webflow Cloud)."
license: Apache-2.0
compatibility: Requires git or the Vercel CLI, and access to the internet
allowed-tools: Bash(git:*) Bash(vercel:*) Read
metadata:
  author: vercel
  version: "1.0.0"
  one-liner: "Migrate a Next.js app from Webflow Cloud to Vercel"
  guide: "https://vercel.com/kb/guide/migrate-a-next-js-app-from-webflow-cloud-to-vercel"
---

# Migrate Next.js from Webflow Cloud to Vercel

## What this skill does

Moving a Next.js app from Webflow Cloud to Vercel mostly means removing the deployment layer that adapted the app to the Cloudflare Workers runtime. On Webflow Cloud the app runs as a Cloudflare Worker through the `@opennextjs/cloudflare` adapter, served from a mount path inside a Webflow site. On Vercel the same app runs natively on Vercel Functions with Fluid compute on by default, in a full Node.js runtime, served from the root, so it scales with traffic on its own and supports the framework's full feature set.

Unlike a framework that needs a platform adapter, Next.js runs natively on Vercel, so **no adapter replaces OpenNext** — you just take it out. The app code (pages, components, Route Handlers) mostly stays the same. The work sits in a few places: the OpenNext adapter and its dev hook in `next.config.ts`, the Webflow Cloud and Wrangler config files that get deleted, the base path the app mounted under, the Edge runtime directive on routes and middleware, and any server code that read storage bindings through `getCloudflareContext().env`.

## The Vercel Plugin

The user will have installed the [Vercel Plugin](https://vercel.com/docs/agent-resources/vercel-plugin.md) already, which among other things includes a number of helpful skills that can assist you and the user with this migration. Prefer those skills for current, detailed product guidance, and let this skill drive the order of work. The ones that line up with these steps:

- `vercel-storage` and `marketplace`: step 5 (Blob, Edge Config, Neon, Upstash, and Marketplace provisioning).
- `env-vars`: steps 5 and 6 (`vercel env`, `.env` files, OIDC tokens).
- `vercel-cli` and `deployments-cicd`: steps 6 and 7 (env vars and deploy).
- `vercel-functions`: step 5 (Route Handlers on Vercel Functions) and the Best practices section (`maxDuration`, regions, ISR).

There are other skills included that may assist with the migration.

## Steps the user completes manually

You handle most of the migration directly by editing files and running commands. A few actions need the Vercel dashboard, a Vercel account, or secret values, so the user has to do those:

- Creating the Vercel account (see Before you start).
- Creating and connecting the backing stores in step 5.
- Adding environment variables in step 6.
- Deploying in step 7.

Guide the user through each of these. Give clear, specific instructions, then wait for them to confirm before moving on. Do not report any of them as done while the user still has to do it.

If you are unsure about a dashboard flow or whether a detail is still current, use an applicable Vercel skill when one is available (see "The Vercel Plugin" above), and check the latest with a web search scoped to the vercel.com domain (for example, `site:vercel.com vercel blob oidc token`).

## Service mapping (quick reference)

| Webflow Cloud | Vercel |
| --- | --- |
| Cloudflare Workers runtime (`workerd`) | [Vercel Functions](https://vercel.com/docs/functions) (Fluid compute) |
| OpenNext Cloudflare adapter (`@opennextjs/cloudflare`) | Native Next.js support, no adapter |
| `initOpenNextCloudflareForDev()` in `next.config.ts` | Not needed |
| `webflow.json` | Not needed, Next.js is auto-detected |
| `wrangler.json` | `vercel.json` (optional) |
| `open-next.config.ts` | Not needed |
| `cloudflare-env.d.ts` | Not needed |
| `basePath` and `assetPrefix` (mount path) | Served from the root; remove unless you want a base path |
| `getCloudflareContext().env` | `process.env` |
| `webflow cloud deploy` or GitHub push | Git push or the `vercel` CLI |
| `npm` only | npm, pnpm, Yarn, or Bun |
| Object Storage (R2 binding) | [Vercel Blob](https://vercel.com/docs/vercel-blob) |
| Key Value Store (Workers KV binding) | [Redis on the Vercel Marketplace](https://vercel.com/marketplace?search=Redis), or [Edge Config](https://vercel.com/docs/edge-config) for read-heavy config |
| SQLite (D1 binding) | [Postgres on the Vercel Marketplace](https://vercel.com/marketplace?search=postgres) |
| Edge runtime middleware only | Full Next.js middleware support |
| `export const runtime = 'edge'` on routes | Remove it to run on Node.js (recommended) |
| No scheduled jobs, queues, or workflows | New on Vercel: [Cron Jobs](https://vercel.com/docs/cron-jobs), [Queues](https://vercel.com/docs/queues), and [Workflows](https://vercel.com/workflows) |

## Before you start

Check the repo for these, and ask the user to confirm anything the repo cannot show:

- A working Next.js app deployed on Webflow Cloud. Look for `next` in `package.json` and the `@opennextjs/cloudflare` adapter (in `package.json`, `next.config.ts`, or `open-next.config.ts`) to confirm the framework and platform before changing anything.
- Node.js 20 or later.
- A Vercel account (the user confirms this; you cannot create one).
- The Vercel CLI, for the env and deploy steps: `npm i -g vercel`.

Do not use this skill for a different framework, a brand-new app (set it up for Vercel directly instead), or a move in the other direction (Vercel to Webflow Cloud).

## Steps

Work through these in order. Step 0 tells you which of steps 3 and 5 apply, so you can skip what the app does not use.

### Step 0: Audit the current Webflow Cloud setup

Run the audit script from the project root:

```bash
bash scripts/audit.sh /path/to/project
```

It reports the Webflow Cloud and Wrangler config files, the `@opennextjs/cloudflare` adapter and its `initOpenNextCloudflareForDev()` dev hook, the base path (`basePath` and `assetPrefix`) and likely manual prefixing, any `export const runtime = 'edge'` directives on routes and middleware, every `getCloudflareContext()` access, and which storage bindings are declared in `wrangler.json` (Object Storage, Key Value Store, SQLite). Use the output to pick which later steps apply, then show the user a short checklist. Skipping this leads to missed bindings and runtime errors.

### Step 1: Remove the OpenNext Cloudflare adapter

Vercel runs Next.js natively, so there is no adapter to install — you just remove OpenNext. Uninstall the adapter and Wrangler:

```bash
npm uninstall @opennextjs/cloudflare wrangler
```

Then remove the OpenNext dev hook from `next.config.ts`. The `create-cloudflare` setup adds these lines so `getCloudflareContext()` works in `next dev`, and they no longer apply on Vercel:

```ts
// Remove these lines
import { initOpenNextCloudflareForDev } from "@opennextjs/cloudflare";
initOpenNextCloudflareForDev();
```

### Step 2: Remove the Webflow Cloud configuration files

Delete the Cloudflare- and Webflow-specific files that no longer apply on Vercel:

- `webflow.json`, which told Webflow Cloud your framework. Vercel detects Next.js automatically.
- `wrangler.json`, including its `compatibility_date`, `nodejs_compat` flag, `assets` binding, and storage bindings. Vercel Functions run on Node.js, so the compatibility flags have no equivalent.
- `open-next.config.ts`, the adapter configuration.
- `cloudflare-env.d.ts` (sometimes `cloudflare.env.ts`), the generated binding types.

Your storage bindings live in `wrangler.json`. Before deleting the file, note which bindings the app uses (Object Storage, Key Value Store, or SQLite) so you can recreate them on Vercel in step 5.

### Step 3: Remove the base path and Edge runtime settings

On Webflow Cloud the app is served from a mount path such as `/app`, so `basePath` and `assetPrefix` are set in `next.config.ts` to match. On Vercel the app is served from the root, so remove both options unless you intend to keep serving the app under a subpath:

```ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Remove basePath and assetPrefix when serving from the root
  // basePath: "/app",
  // assetPrefix: "/app",
};

export default nextConfig;
```

Because the base path is gone, remove the manual prefixing Webflow Cloud required in client-side `fetch` calls and asset references. Change `fetch(${basePath}/api/users)` back to `fetch("/api/users")`, and drop the asset prefix from plain `<img>` tags.

Webflow Cloud also runs API routes and middleware on the Edge runtime. On Vercel, remove the `export const runtime = 'edge'` directive from your Route Handlers and `middleware.ts` so they run on the default Node.js runtime. Migrating from the Edge runtime to Node.js is recommended for performance and reliability, both runtimes run on [Fluid compute](https://vercel.com/fluid) with [Active CPU pricing](https://vercel.com/docs/functions/usage-and-pricing#active-cpu), and Node.js gives your routes the full Node.js API surface and access to npm packages that depend on Node.js built-ins.

### Step 4: Update your build scripts

Replace the Webflow Cloud preview script in `package.json` with the standard Next.js commands. Vercel runs the build for you, so you no longer need the `opennextjs-cloudflare` preview command:

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  }
}
```

Vercel auto-detects Next.js on import and sets the build command and output directory, so these scripts mainly support local development.

### Step 5: Replace Webflow Cloud bindings with Vercel storage

This is the main code change. On Webflow Cloud you read storage through bindings on the Cloudflare `env`, accessed in a Route Handler with `getCloudflareContext()`. On Vercel you read connection details from `process.env` and talk to each store through its SDK or client. Remove every `getCloudflareContext()` call and replace the binding operations. Read `references/service-mapping.md` for the before and after code for each binding, then install the SDK you need, for example:

```bash
npm i @vercel/blob
```

Have the user create and connect the backing stores. This is what adds the env vars the code reads, so it has to be done before the app will run:

- Object Storage to Blob: create a Blob store on the [Storage page](https://vercel.com/d?to=%2F%5Bteam%5D%2F%7E%2Fstores), then connect it to the project from the store's Projects tab. Vercel adds the store's environment variables, including a short-lived `VERCEL_OIDC_TOKEN` that it rotates, and the SDK uses them automatically, so `put()` needs no token in code. This [OIDC approach](https://vercel.com/docs/vercel-blob/using-blob-sdk#oidc-tokens-recommended) is recommended over the long-lived `BLOB_READ_WRITE_TOKEN`, which is only for code that runs outside Vercel.
- Key Value Store to Redis: add a Redis integration such as [Upstash Redis](https://vercel.com/marketplace/upstash) for caching and session data, or use [Edge Config](https://vercel.com/docs/edge-config) for small, read-heavy config.
- SQLite to Postgres: add a Postgres database such as [Neon](https://vercel.com/marketplace/neon) from the Marketplace.

Provisioning a store from the Marketplace adds its connection string and credentials as env vars, which the code reads from `process.env`.

### Step 6: Move environment variables and secrets

Recreate your Webflow Cloud environment variables as Vercel environment variables. Webflow Cloud stores these per environment in your app's settings and injects them at runtime only. Vercel stores them per environment (production, preview, and development) in project settings and makes them available at both build time and runtime.

> **Never handle the user's secrets.** Do not ask the user for secret values, and do not accept secrets pasted into the chat. Do not offer to save, enter, or store environment variables or secrets for the user, and refuse if asked to do so. Setting the actual values is the user's job, done in the dashboard or in their own terminal. Your part is to prepare the list of variable names and the exact commands.

You can list every variable and secret to recreate and write out the exact commands, but you cannot supply secret values or sign the CLI in, and you must not make up values.

The user adds each variable, either on the [project's Environment Variables page](https://vercel.com/d?to=%2F%5Bteam%5D%2F%5Bproject%5D%2Fsettings%2Fenvironment-variables) or with the CLI after `vercel login`:

```bash
vercel env add DATABASE_URL production
```

Once the user has signed in, you can link the project and pull the values into a local `.env`:

```bash
vercel link
vercel env pull
```

A variable added to production is not available in preview or development unless it is added there too. Because Vercel exposes environment variables during the build, you can re-enable any build-time validation you had to disable on Webflow Cloud, where variables aren't available at build time.

### Step 7: Deploy

You cannot import a project, confirm the framework preset, sign in, or select Deploy, so walk the user through one of these paths. Both run the app on Vercel Functions.

Deploy with Git (recommended):

1. Push the project to GitHub, GitLab, or Bitbucket.
2. In the [Vercel dashboard](https://vercel.com), select Add New > Project, then import the repo.
3. Vercel detects Next.js and sets the build command and output directory. Confirm the framework preset, add the environment variables from step 6, and select Deploy.

After the first import, every push to the production branch creates a production deploy, and every pull request gets its own preview URL.

Deploy with the CLI: after `vercel login`, run `vercel` for a preview or `vercel --prod` for production.

If the `vercel-deploy` skill is available, you can use it to create a preview deploy and a claim URL without the user signing in first, which is a good way to check the build before wiring up a connected project.

## After the move: check these

You can grep for the code issues; ask the user to check anything in the dashboard. See `references/troubleshooting.md` for fixes.

- No `@opennextjs/cloudflare` import or `initOpenNextCloudflareForDev()` call remains in `next.config.ts` or anywhere else.
- No `getCloudflareContext()` access remains anywhere in server code.
- No leftover base path: `basePath` and `assetPrefix` are gone from `next.config.ts`, and client-side `fetch` calls and `<img>` tags no longer prefix a base path.
- No `export const runtime = 'edge'` remains on Route Handlers or in `middleware.ts`.
- Each env var exists in the right environment, not only production.

## Tune after migrating (optional)

- Tune function resources per route: set `export const maxDuration = 60` in a route's segment config for routes that need more time, or configure memory and regions in `vercel.json`.
- Put functions near the data: set the function region close to the Marketplace database to cut latency.
- Take advantage of features that were limited on Webflow Cloud: Incremental Static Regeneration, on-demand and tag-based revalidation, the `use cache` directive, and Node.js middleware all work on Vercel without extra configuration. For scheduled and background work Webflow Cloud didn't offer, look at [Cron Jobs](https://vercel.com/docs/cron-jobs), [Queues](https://vercel.com/docs/queues), and [Workflows](https://vercel.com/workflows).

## References

- [service-mapping](references/service-mapping.md): Before and after code for replacing each Webflow Cloud binding (Object Storage to Blob, Key Value Store to Redis or Edge Config, SQLite to Postgres), plus the store setup notes. Read before step 5.
- [troubleshooting](references/troubleshooting.md): The common errors after the move and how to fix them.
