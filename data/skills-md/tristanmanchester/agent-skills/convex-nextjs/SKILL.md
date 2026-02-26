---
name: convex-nextjs
description: >-
  Builds, integrates, and deploys Convex backends in Next.js (App Router by
  default, Pages Router supported). Covers running `npx convex dev`, defining
  Convex schema/indexes, writing queries/mutations/actions, wiring
  ConvexReactClient + ConvexProvider hooks (useQuery/useMutation), optional SSR
  preloading and Server Actions via convex/nextjs, authentication patterns, and
  deployment (including Vercel + preview deployments). Use when the user
  mentions Convex, convex.dev, Next.js + Convex, real-time database updates,
  Convex functions, schema/indexes, NEXT_PUBLIC_CONVEX_URL, convex dev/deploy,
  or troubleshooting Convex in a Next.js app.
compatibility: >-
  Intended for Next.js 13+ (App Router) with TypeScript. Requires Node.js and the
  Convex CLI via the `convex` npm package (typically run with `npx convex ...`).
allowed-tools: "Read,Write,Bash(npm:*),Bash(npx:*),Bash(node:*),Bash(python:*)"
metadata:
  version: 1.0.0
  ecosystem: convex
  framework: nextjs
---

# Convex + Next.js skill

## What this skill optimises for
- **End-to-end features**: schema → functions → UI wiring, with type safety.
- **Correct Next.js boundaries**: keep reactive Convex hooks in Client Components; use `convex/nextjs` helpers for SSR/server code.
- **Low surprise deployments**: predictable environment variables and `convex deploy` flows.

## Default choices (override if the user says otherwise)
- **Next.js App Router + TypeScript** (Pages Router still supported).
- **Reactive UI** via `ConvexReactClient` + `<ConvexProvider>` + hooks.
- **Validation-first** Convex functions: always define `args` validators and basic access control for any public function.

---

## Workflow 0 — Decide the starting point
1. **Brand new project?** Prefer `npm create convex@latest` (template-based scaffolding).
2. **Existing Next.js app?** Add Convex via `npm install convex` + `npx convex dev`.
3. **Cloud coding agent / no login possible?** Use Agent Mode or local deployments (see [references/07-agent-mode-and-local-dev.md](references/07-agent-mode-and-local-dev.md)).

---

## Workflow 1 — Add Convex to a Next.js app (App Router)

### Step 1: Install and initialise Convex
Run:
```bash
npm install convex
npx convex dev
```

Expected results:
- Prompts you to log in, create/select a project, and writes your deployment URLs.
- Creates a `convex/` directory for backend functions.
- Keeps running to sync code to your dev deployment.

### Step 1b (optional): Seed sample data + expose a first query
If you want a known-good end-to-end smoke test:

1) Create `sampleData.jsonl`:
```jsonl
{"text":"Buy groceries","isCompleted":true}
{"text":"Go for a swim","isCompleted":true}
{"text":"Integrate Convex","isCompleted":false}
```

2) Import it into a `tasks` table:
```bash
npx convex import --table tasks sampleData.jsonl
```

3) Add a query at `convex/tasks.ts`:
```ts
import { query } from "./_generated/server";

export const get = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.db.query("tasks").collect();
  },
});
```

### Step 2: Create a client provider (Client Component)
Create `app/ConvexClientProvider.tsx`:

```tsx
"use client";

import { ConvexProvider, ConvexReactClient } from "convex/react";
import type { ReactNode } from "react";

const convex = new ConvexReactClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

export function ConvexClientProvider({ children }: { children: ReactNode }) {
  return <ConvexProvider client={convex}>{children}</ConvexProvider>;
}
```

### Step 3: Wrap your app layout
In `app/layout.tsx`, wrap the `children`:

```tsx
import { ConvexClientProvider } from "./ConvexClientProvider";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <ConvexClientProvider>{children}</ConvexClientProvider>
      </body>
    </html>
  );
}
```

### Step 4: Call your first query from a Client Component
- **Only** call `useQuery/useMutation/useAction` in files with `"use client"`.
- Use the generated `api` object from `convex/_generated/api`.

Example:
```tsx
"use client";
import { useQuery } from "convex/react";
import { api } from "@/convex/_generated/api";

export function Tasks() {
  const tasks = useQuery(api.tasks.get);
  if (tasks === undefined) return <div>Loading…</div>;
  return <ul>{tasks.map((t) => <li key={t._id}>{t.text}</li>)}</ul>;
}
```

---

## Workflow 2 — Build a feature end-to-end (schema → functions → UI)

Copy/paste checklist:
- [ ] Define or update tables and indexes in `convex/schema.ts`.
- [ ] Implement **queries** for reads and **mutations** for writes (use `args` validators).
- [ ] Keep `npx convex dev` running to regenerate `convex/_generated/*`.
- [ ] Call functions from UI using `useQuery` / `useMutation`.
- [ ] Add access control and validate user input for any function callable from clients.

### Minimal table + query + mutation pattern
- Schema and indexes: see [references/02-schema-and-indexes.md](references/02-schema-and-indexes.md)
- Function patterns: see [references/03-functions.md](references/03-functions.md)

---

## Workflow 3 — SSR, Server Components, Server Actions (optional)

Use this when you need a faster first paint or want server-only routes:
- **Reactive after load**: `preloadQuery` in a Server Component + `usePreloadedQuery` in a Client Component.
- **Server-only (non-reactive)**: `fetchQuery` in a Server Component.
- **Server Actions / Route Handlers**: `fetchMutation` / `fetchAction`.

Key constraints:
- `convex/nextjs` helpers assume `NEXT_PUBLIC_CONVEX_URL` is set, or you pass an explicit `url` option.
- Avoid multiple `preloadQuery` calls in the same page if you need consistency (see docs caveat).

Details + copy/paste examples:
- [references/04-nextjs-ssr-and-server.md](references/04-nextjs-ssr-and-server.md)

---

## Workflow 4 — Authentication (client-only vs server+client)

1. **Client-only auth (simplest)**:
   - Wrap the provider with your auth provider + a `ConvexProviderWith…` adapter.
   - Use `<Authenticated>`, `<Unauthenticated>`, `<AuthLoading>` from `convex/react` for UI gates.

2. **Server + client auth (App Router SSR / Server Actions)**:
   - Use your provider’s Next.js SDK to obtain a JWT on the server.
   - Pass `{ token }` as the third argument to `preloadQuery` / `fetchQuery`.

Details:
- [references/05-auth.md](references/05-auth.md)

---

## Workflow 5 — Deploy (production + previews)

### Default production deploy
```bash
npx convex deploy
```

### Vercel (recommended)
Set Vercel Build Command to:
```bash
npx convex deploy --cmd 'npm run build'
```
and configure `CONVEX_DEPLOY_KEY` in Vercel environment variables.

Details:
- [references/06-deployment-vercel.md](references/06-deployment-vercel.md)

---

## Validation loop (fast sanity checks)
When working in an existing repo:
1. Make changes
2. Run the validator:
   ```bash
   python {baseDir}/scripts/validate_project.py --root .
   ```
3. Fix any errors/warnings before moving on.

---

## THE EXACT PROMPT — Implement a Convex-backed feature in Next.js
Copy/paste into a coding agent:

```
You are implementing a feature using Convex in a Next.js (App Router) app.

Requirements:
1) Update convex/schema.ts (tables + indexes) as needed.
2) Add Convex functions (queries/mutations/actions) with argument validators.
3) Keep reactive data fetching in Client Components using convex/react hooks.
4) If SSR is requested, use convex/nextjs preloadQuery + usePreloadedQuery.
5) Include basic access control for any function callable from the client.
6) Ensure convex/_generated is up-to-date (assume npx convex dev is running).

Deliver:
- Exact file paths + code diffs
- Short usage notes (how to run, what env vars are needed)
- Quick test plan (1-3 smoke tests)
```

---

## Quick search (when debugging)
```bash
# Find Convex calls in the frontend
rg "useQuery\(|useMutation\(|useAction\(" .

# Find Convex functions
ls convex
```
