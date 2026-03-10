---
name: integrating-convex-expo
description: >-
  Sets up and evolves Convex backends for Expo / React Native apps: create deployments, configure EXPO_PUBLIC_CONVEX_URL (and EAS env vars),
  wire up ConvexProvider + ConvexReactClient, use generated api types, and implement queries/mutations/actions, schemas/indexes,
  auth, and file uploads. Use when the user mentions Convex with Expo/React Native, create-expo-app, expo-router, useQuery/useMutation,
  ConvexReactClient, convex dev, deployment URL, EAS builds, or asks for a realtime database/backend in an Expo app.
compatibility: >-
  Intended for Expo (React Native) apps (including expo-router) using Node.js and the Convex CLI via npx.
  Assumes you can run shell commands and edit project files.
metadata:
  version: 1.0.0
  category: mobile-backend
  tags: [convex, expo, react-native, realtime, typescript]
---

# Integrating Convex with Expo (React Native)

## Why this skill exists
Convex setup in React Native is straightforward, but *small* details (Expo environment variables, file locations, keeping `convex dev` running)
regularly cause broken builds or “it returns undefined” confusion. This skill standardises a reliable, end-to-end workflow.

## Non-negotiables (do these every time)
- **Keep `npx convex dev` running** while developing. It syncs functions + generates the `convex/_generated` API/types.
- **Use Expo public env vars**: the client should read `process.env.EXPO_PUBLIC_CONVEX_URL`.
- **Create exactly one Convex client** per app, and wrap the whole tree in `ConvexProvider`.
- **React Native:** set `unsavedChangesWarning: false` on `ConvexReactClient` (the default warning is web-centric).
- **Don’t hand-type API names:** always import from `convex/_generated/api` and call `api.someFile.someExport`.

## First decision: what kind of Expo project is this?
1. **expo-router project** (common with `create-expo-app`):
   - root layout is usually `app/_layout.tsx` or `src/app/_layout.tsx`
2. **classic App.tsx entrypoint**:
   - wrap `App.tsx` with `ConvexProvider`

When unsure, search for `expo-router` in `package.json` and look for an `app/` folder.

---

# Workflow A — Add Convex to an existing Expo app (recommended default)

## A1) Install Convex
From the Expo app root:

```bash
npx expo install convex
```

(If you aren’t using Expo’s installer, `npm i convex` also works.)

## A2) Create a Convex dev deployment + backend folder
```bash
npx convex dev
```

What you should see / get:
- prompts to log in and create a project
- a new `convex/` folder for backend functions
- `.env.local` containing `EXPO_PUBLIC_CONVEX_URL=...`
- the command keeps running to sync changes

## A3) Ensure `EXPO_PUBLIC_CONVEX_URL` is available in development *and* builds
- **Dev (Expo CLI / Metro):** `npx convex dev` writes `.env.local` with `EXPO_PUBLIC_CONVEX_URL`.
- **EAS builds:** copy that value into EAS env vars.

See: [references/eas-env.md](references/eas-env.md)

## A4) Wire up the Convex client + provider (expo-router)
Edit `app/_layout.tsx` *or* `src/app/_layout.tsx`:

```ts
import { ConvexProvider, ConvexReactClient } from "convex/react";
import { Stack } from "expo-router";

const convex = new ConvexReactClient(process.env.EXPO_PUBLIC_CONVEX_URL!, {
  unsavedChangesWarning: false,
});

export default function RootLayout() {
  return (
    <ConvexProvider client={convex}>
      <Stack />
    </ConvexProvider>
  );
}
```

### If the project does not use expo-router
Wrap your top-level component (usually `App.tsx`) similarly:

```ts
import { ConvexProvider, ConvexReactClient } from "convex/react";

const convex = new ConvexReactClient(process.env.EXPO_PUBLIC_CONVEX_URL!, {
  unsavedChangesWarning: false,
});

export default function App() {
  return (
    <ConvexProvider client={convex}>
      {/* your existing navigation / UI */}
    </ConvexProvider>
  );
}
```

## A5) Create a first query + show it in the app
Use the canonical “tasks” example:
- backend: `convex/tasks.ts`
- seed: `sampleData.jsonl`
- import: `npx convex import --table tasks sampleData.jsonl`
- UI: `useQuery(api.tasks.get)`

See: [references/tasks-example.md](references/tasks-example.md)

✅ Quality gate: when the app loads, `useQuery` should initially be `undefined` (loading) and then become an array of tasks.

---

# Workflow B — Add a new feature end-to-end (schema → function → UI)

Use this loop for each feature (it keeps you “in sync” across app/backend/db):

1. **Data model first (schema + indexes)**
   - define/extend tables in `convex/schema.ts`
   - add indexes you’ll query by (before you have 1000+ docs)
   - see: [references/schema-and-indexes.md](references/schema-and-indexes.md)

2. **Backend API (query/mutation/action)**
   - prefer **query** for reads, **mutation** for writes, **action** when you need Node APIs or third-party fetches that don’t fit the normal runtime
   - always validate args with `v.*`
   - see: [references/functions.md](references/functions.md)

3. **Frontend integration**
   - `useQuery(api.file.export)`
   - `useMutation(api.file.export)`
   - consider loading/empty/error states explicitly
   - see: [references/frontend-patterns.md](references/frontend-patterns.md)

4. **Run/verify**
   - keep `npx convex dev` running
   - restart Metro if env vars changed
   - run the validation script: `python scripts/validate_project.py`

---

# Workflow C — Authentication (pick one and stick to it)

Convex supports multiple approaches; the right choice depends on your app’s needs:

- **Convex Auth**: simplest end-to-end if you’re all-in on Convex.
- **Clerk**: common in Expo; Convex provides `<ConvexProviderWithClerk>` for integration.
- **Other OIDC/JWT providers**: generally work by passing JWTs and enforcing access control in functions.

See: [references/auth.md](references/auth.md)

---

# Workflow D — File uploads from Expo / React Native
Use Convex File Storage upload URLs:

1. mutation generates a short-lived upload URL
2. client `fetch(putUrl, { method: "POST", ... })`
3. store the returned `storageId` in your table

See: [references/file-uploads.md](references/file-uploads.md)

---

# Troubleshooting (fast path)
If something breaks, do this in order:

1. **Is `npx convex dev` running?** If not, start it.
2. **Is `process.env.EXPO_PUBLIC_CONVEX_URL` defined at runtime?**
   - if you added/changed `.env*`, restart Metro with cache cleared.
3. **Does the app wrap the entire tree with `ConvexProvider`?**
4. **Are you importing `api` from `convex/_generated/api` and calling `useQuery(api.x.y)`?**
5. Run: `python scripts/validate_project.py`

More cases + fixes: [references/troubleshooting.md](references/troubleshooting.md)

---

# Scripts included
- `scripts/validate_project.py` — checks package.json, env vars, Convex folder, and provider wiring.
- `scripts/scaffold_tasks_example.py` — generates the “tasks” example files (dry-run by default).

---

# References (load only when needed)
- [references/eas-env.md](references/eas-env.md) — `.env.local` vs EAS env vars, Expo gotchas
- [references/tasks-example.md](references/tasks-example.md) — seed + query + UI in Expo
- [references/schema-and-indexes.md](references/schema-and-indexes.md) — schemas, validators, indexes, query perf
- [references/functions.md](references/functions.md) — queries, mutations, actions patterns
- [references/frontend-patterns.md](references/frontend-patterns.md) — hooks patterns, loading/error handling, navigation
- [references/auth.md](references/auth.md) — Convex Auth vs Clerk vs others, access control patterns
- [references/file-uploads.md](references/file-uploads.md) — RN/Expo file URIs → Blob → Convex storage
- [references/troubleshooting.md](references/troubleshooting.md) — common issues and exact fixes
- [references/sources.md](references/sources.md) — upstream docs used to build this skill

