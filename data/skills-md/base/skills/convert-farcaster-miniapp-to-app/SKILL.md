---
name: convert-farcaster-miniapp-to-app
description: Converts Farcaster miniapp SDK projects into regular Base/web apps. Starts with an interactive quiz to choose between the default regular-app conversion and a narrowly isolated Farcaster surface when something truly needs to remain separate. Handles wagmi connectors, providers, auth, SDK actions, manifest routes, meta tags, dependencies, and read-only preservation.
---

# Convert Farcaster Miniapp to Base App

Convert a Farcaster miniapp into a normal app on Base. The default outcome is a regular web app that works in the Base app browser and on the open web, with Farcaster Mini App host coupling removed.

If some Farcaster functionality truly needs to survive, keep it separate from the main app surface. Prefer read-only data first. Only preserve Mini App-specific behavior when the user explicitly insists, and isolate it behind a dedicated route or page rather than carrying it through the whole app.

## Core Principle

Always separate these decisions:

1. Remove Mini App host/runtime coupling.
2. Decide whether any Farcaster-facing functionality should remain.
3. If something remains, keep it isolated from the main app and avoid introducing new vendor dependencies by default.

Do **not** automatically turn "keep some Farcaster functionality" into "migrate to Neynar." If a project already uses Neynar and the user wants to keep an isolated Farcaster-only area, you may preserve that existing integration. Do not introduce new Neynar adoption as the default recommendation.

## Quick Start

Follow these five phases sequentially:

0. **Discovery** — Quick scan + quiz to choose a path
1. **Analysis** — Detailed read-only analysis scoped to the chosen path
2. **Conversion** — Remove Mini App SDK patterns and isolate any intentionally preserved Farcaster surface
3. **Cleanup** — Remove dead code, env vars, and dependencies
4. **Verification** — Type check, build, and summarize

## Conversion Paths

The quiz should route the user into one of two paths:

| Path | Name | Who it's for | What happens |
|------|------|-------------|-------------|
| **A** | Regular App Default | Most projects | Strip Farcaster Mini App coupling and become a normal Base/web app |
| **B** | Isolated Farcaster Surface | The app still needs a small Farcaster-specific area | Convert the main app into a normal app, then keep only a separate Farcaster route/page for the remaining functionality |

`Path B` is still biased toward removing complexity:
- Prefer **read-only** Farcaster data.
- Avoid preserving Mini App host/runtime behavior unless the user explicitly asks for it.
- Keep any preserved Farcaster logic out of the main app shell, shared providers, and primary auth flow.

---

## Phase 0: Discovery

### 0A. Quick Scan (automated, no user interaction)

Run a lightweight scan before asking questions. Produce an internal tally:

1. **Detect framework** from `package.json` (`next`, `vite`, `react-scripts`, `@remix-run/*`)
2. **Count Farcaster packages** in `dependencies` and `devDependencies`
3. **Grep source files** (`.ts`, `.tsx`, `.js`, `.jsx`) for:
   - `sdk.actions.*` calls (count total)
   - `sdk.quickAuth` usage (yes/no)
   - `sdk.context` usage (yes/no)
   - `.well-known/farcaster.json` (yes/no)
   - `farcasterMiniApp` / `miniAppConnector` connector (yes/no)
   - Total files with any `@farcaster/` import
   - `@neynar/` imports or `api.neynar.com` fetch calls (yes/no)
4. **Identify the blast radius**:
   - Are Farcaster references spread across the main app shell?
   - Are they already mostly confined to a route like `app/farcaster/`, `pages/farcaster/`, or a small set of components?
   - Are there obvious host-only features such as haptics, notifications, `openMiniApp`, or `sdk.context.client`?

Use this tally to inform quiz suggestions. Do **not** dump raw scan output to the user before asking the quiz.

### 0B. Interactive Quiz

Ask these questions one at a time. Use the quick scan results to suggest the most likely answer.

**Q1** (always ask):

> Based on my scan, your project has [X] files using the Farcaster SDK with [summary of what is used].
>
> Which outcome do you want?
> - **(a) Regular app everywhere** — remove Farcaster-specific behavior and just keep a normal Base/web app
> - **(b) Regular app first, plus a separate Farcaster area** — keep the main app clean, but preserve a small isolated route/page if really needed

**Q2** (always ask):

> How deeply is the Mini App SDK used today?
> - **(a) Minimal** — mostly `sdk.actions.ready()` and a few helpers
> - **(b) Moderate** — some `context`, `openUrl`, profile links, or conditional `isInMiniApp` logic
> - **(c) Heavy** — auth, wallet connector, notifications, compose flows, or host-specific behavior

**Q3** (ask if Q1 = b):

> What is the smallest Farcaster feature set you actually need to preserve?
> - **(a) Read-only only** — profile or cast display, links out to Farcaster profiles, maybe a small social page
> - **(b) Some Farcaster-specific interactions** — there is a separate page/path that still needs more than read-only behavior
> - **(c) Not sure** — analyze what is isolated already and recommend the smallest keep-surface possible

**Q4** (ask if Q1 = b and there is existing isolated Farcaster code or existing Neynar usage):

> Does the project already have an isolated Farcaster-only route/page or integration that you want to keep as-is if possible?
> - **(a) Yes** — preserve only that isolated surface
> - **(b) No** — prefer removing it unless there is a very strong reason to keep it

**Q5** (ask if quick auth or other Mini App auth is present):

> After conversion, what should the main app use for authentication?
> - **(a) SIWE** — wallet-based auth for the regular app
> - **(b) Existing non-Farcaster auth** — keep whatever normal web auth already exists
> - **(c) No auth** — remove auth entirely

### 0C. Path Selection

Map answers to a path:

| Desired outcome | Typical result |
|-----------------|----------------|
| `Q1 = regular app everywhere` | **Path A** — Regular App Default |
| `Q1 = regular app first, plus separate Farcaster area` | **Path B** — Isolated Farcaster Surface |

Then tighten the recommendation:

- If the user chose `Path B`, prefer **read-only preservation** unless they explicitly require something else.
- If the scan shows heavy host/runtime coupling but the user wants `Path A`, warn them that some features will be deleted rather than recreated.
- If the project already uses Neynar, only keep it if it remains inside the isolated Farcaster surface. Do not expand it into the main app.

Announce the chosen path:

> Based on your answers, I'll use **Path [X]: [Name]**. This will [one-sentence description]. I'll now do a detailed analysis of your project.

Record the quiz answers internally. They guide whether the agent should:
- fully remove Farcaster features
- preserve only a read-only isolated surface
- quarantine any unavoidable Farcaster-specific logic to a dedicated route/page

**Proceed to Phase 1.**

---

## Phase 1: Analysis (Read-Only)

### 1A. Detect Framework

Read `package.json`:
- `next` → Next.js
- `vite` → Vite
- `react-scripts` → Create React App
- `@remix-run/*` → Remix

### 1B. Scan for Farcaster Dependencies

List all packages matching:
- `@farcaster/miniapp-sdk`, `@farcaster/miniapp-core`, `@farcaster/miniapp-wagmi-connector`
- `@farcaster/frame-sdk`, `@farcaster/frame-wagmi-connector`
- `@farcaster/quick-auth`, `@farcaster/auth-kit`
- `@neynar/*` (compatibility only; do not assume it stays)

### 1C. Grep for Farcaster Code

Search source files (`.ts`, `.tsx`, `.js`, `.jsx`) for:

**SDK imports:**
```
@farcaster/miniapp-sdk
@farcaster/miniapp-core
@farcaster/miniapp-wagmi-connector
@farcaster/frame-sdk
@farcaster/frame-wagmi-connector
@farcaster/quick-auth
@farcaster/auth-kit
@neynar/
```

**SDK calls:**
```
sdk.actions.ready
sdk.actions.openUrl
sdk.actions.close
sdk.actions.composeCast
sdk.actions.addMiniApp
sdk.actions.requestWalletAddress
sdk.actions.viewProfile
sdk.actions.viewToken
sdk.actions.sendToken
sdk.actions.swapToken
sdk.actions.signIn
sdk.actions.setPrimaryButton
sdk.actions.openMiniApp
sdk.quickAuth
sdk.context
sdk.isInMiniApp
sdk.getCapabilities
sdk.haptics
sdk.back
sdk.wallet
```

**Connectors & providers:**
```
farcasterMiniApp()
miniAppConnector()
farcasterFrame()
MiniAppProvider
MiniAppContext
useMiniApp
useMiniAppContext
```

**Manifest & meta:**
```
.well-known/farcaster.json
fc:miniapp
fc:frame
```

**Environment variables:**
```
NEYNAR_API_KEY
NEXT_PUBLIC_NEYNAR_CLIENT_ID
FARCASTER_
FC_
```

### 1D. Check Existing Web3 Setup

Look for:
- `coinbaseWallet` connector in wagmi config
- SIWE / `siwe` package usage
- `connectkit`, `rainbowkit`, or `@coinbase/onchainkit`
- Existing wallet connection UI

### 1E. Check Separation Boundaries

Map where Farcaster logic currently lives:

- Root providers or app shell
- Shared hooks or auth middleware
- One-off components
- Dedicated routes/pages like `app/farcaster/*`
- Server routes used only by Farcaster functionality

Mark each location with one action:
- **remove**
- **stub**
- **move behind isolated route/page**
- **keep only as read-only**

### 1F. Report Findings

Create a path-scoped summary.

**All paths include:**
```
## Conversion Analysis — Path [X]: [Name]

**Framework:** [detected]
**Farcaster packages:** [list]
**Files with Farcaster code:** [count]

### Wagmi Connector
- File: [path]
- Current connector: [farcasterMiniApp / miniAppConnector / farcasterFrame / none]
- Other connectors: [list]
- Action: [replace with coinbaseWallet / leave existing wallet setup / remove only]

### MiniApp Provider
- File: [path]
- Pattern: [simple / complex]
- Consumers: [files importing from this]
- Action: [stub / remove / isolate]

### SDK Action Calls
[list each: file, what it does, action]

### Manifest & Meta
- Manifest route: [path or N/A]
- Meta tags: [file or N/A]
```

**Path A additionally includes:**
```
### Main App Outcome
- Action: remove Farcaster-specific UI and flows from the main app entirely

### Authentication
- Quick Auth used: [yes/no, file]
- Action: replace with SIWE / keep existing non-Farcaster auth / remove

### Existing Neynar Usage
- Package or files: [list or N/A]
- Action: remove entirely unless the user later re-scopes to Path B

### Environment Variables
[list all FC/Neynar vars that will be removed]
```

**Path B additionally includes:**
```
### Main App Outcome
- Action: convert the main app into a normal web app first

### Isolated Farcaster Surface
- Route/page to keep: [path or proposed path]
- Scope: [read-only / mixed / host-specific]
- Recommended target scope: [prefer read-only / quarantine existing behavior / remove]

### Authentication
- Quick Auth used: [yes/no, file]
- Main app action: replace with SIWE / keep existing non-Farcaster auth / remove
- Isolated Farcaster surface action: [remove auth coupling / preserve existing isolated flow only if explicitly requested]

### Existing Neynar Usage
- Package or files: [list or N/A]
- Action: [remove / keep only inside isolated surface]

### Environment Variables
- Remove from main app: [FC_*, FARCASTER_*, etc.]
- Keep only if isolated surface truly still needs them: [NEYNAR_API_KEY, etc. or N/A]
```

**All paths end with:**
```
### Potential Issues
- [ ] FID used as database primary key
- [ ] Farcaster colors in tailwind config
- [ ] `isInMiniApp` branches with unique else logic
- [ ] Components only meaningful inside Farcaster
- [ ] Farcaster code mixed into shared providers or root layout
```

Ask:

> Does this analysis look correct? Ready to proceed with conversion?

**STOP and wait for user confirmation before Phase 2.**

---

## Phase 2: Conversion

Steps are organized by feature area. Each step notes which paths it applies to and what to do differently for `Path B`.

### 2A. Wagmi Connector (All Paths)

Find the wagmi config file (`lib/wagmi.ts`, `config/wagmi.ts`, `providers/wagmi-provider.tsx`, etc.):

1. Remove import of `farcasterMiniApp` or `miniAppConnector` from `@farcaster/miniapp-wagmi-connector`
2. Remove the `farcasterMiniApp()` / `miniAppConnector()` call from the `connectors` array
3. If no wallet connector remains, add:
   ```typescript
   import { coinbaseWallet } from "wagmi/connectors";

   coinbaseWallet({ appName: "<app name>" })
   ```
4. If `coinbaseWallet` already exists, leave it as-is
5. Clean up empty lines and stale imports

Skip this step if wagmi is not in the project.

### 2B. MiniApp Provider / Context (All Paths)

If the app has a shared Mini App provider, remove host/runtime assumptions from the main app.

**Pattern A: simple provider**

Replace with a safe stub:

```tsx
'use client'

import React, { createContext, useContext, useMemo } from "react";

interface MiniAppContextType {
  context: undefined;
  ready: boolean;
  isInMiniApp: boolean;
}

const MiniAppContext = createContext<MiniAppContextType | undefined>(undefined);

export function useMiniAppContext() {
  const context = useContext(MiniAppContext);
  if (context === undefined) {
    throw new Error("useMiniAppContext must be used within a MiniAppProvider");
  }
  return context;
}

export default function MiniAppProvider({ children }: { children: React.ReactNode }) {
  const value = useMemo(
    () => ({
      context: undefined,
      ready: true,
      isInMiniApp: false,
    }),
    []
  );

  return <MiniAppContext.Provider value={value}>{children}</MiniAppContext.Provider>;
}
```

Preserve export style and hook names so consumers do not break.

**Pattern B: complex provider**

- If many consumers depend on it, stub it first.
- If only a few files use it, remove it and update those imports directly.
- In `Path B`, do not let the isolated Farcaster surface keep this provider wired through the root app shell. If needed, make it local to the isolated route only.

### 2C. Authentication

The main app should use normal web auth, not Mini App auth.

**Default rule for both paths:**
- If `sdk.quickAuth.getToken()` is used, replace it with SIWE or remove it.
- If a normal non-Farcaster auth system already exists, prefer that over adding new auth.
- Do not introduce new Farcaster or Neynar auth as the default conversion target.

#### SIWE Replacement Pattern

**Client-side** (e.g. `useSignIn.ts`):
- Remove `import sdk from "@farcaster/miniapp-sdk"`
- Remove `sdk.quickAuth.getToken()`
- Replace with:
  1. Get wallet address from `useAccount()` (wagmi)
  2. Create a SIWE message with `siwe`
  3. Sign with `useSignMessage()` (wagmi)
  4. Send signature + message to the backend for verification

**Server-side** (e.g. `app/api/auth/sign-in/route.ts`):
- Remove `@farcaster/quick-auth` verification
- Replace with SIWE verification:
  1. Parse the SIWE message
  2. Verify the signature with `siwe` or `viem`
  3. Use recovered wallet address as the normal app identity

**If FID is used as a database primary key:**
- Do not auto-change schema
- Add a TODO comment for later migration
- Warn in Phase 4 summary

**Path B note:**
- If the isolated Farcaster surface already has its own auth or integration flow and the user explicitly wants to keep it, quarantine it there only.
- Do not let that flow remain the default app-wide auth system.

### 2D. SDK Action Calls

#### 2D-1. Main replacements for both paths

| Original | Replacement |
|----------|-------------|
| `sdk.actions.ready()` | Remove entirely |
| `sdk.actions.openUrl(url)` | `window.open(url, "_blank")` |
| `sdk.actions.close()` | `window.close()` or remove |
| `sdk.actions.composeCast(...)` | Remove from the main app |
| `sdk.actions.addMiniApp()` | Remove call and UI |
| `sdk.actions.requestWalletAddress()` | Remove; wagmi handles wallet access |
| `sdk.actions.viewProfile(fid)` | `window.open(\`https://warpcast.com/~/profiles/${fid}\`, "_blank")` |
| `sdk.actions.viewToken(opts)` | `window.open(\`https://basescan.org/token/${opts.token}\`, "_blank")` |
| `sdk.actions.sendToken(opts)` | Replace with wagmi flow if the feature matters, otherwise remove |
| `sdk.actions.swapToken(opts)` | Remove call and UI unless there is a real app-specific swap feature outside Farcaster |
| `sdk.actions.signIn(...)` | Remove; auth handled by normal web auth |
| `sdk.actions.setPrimaryButton(...)` | Remove entirely |
| `sdk.actions.openMiniApp(...)` | Remove from the main app |
| `sdk.isInMiniApp()` | Remove conditional and keep the non-Farcaster branch |
| `sdk.context` | Remove from the main app |
| `sdk.getCapabilities()` | Remove or replace with `async () => []` |
| `sdk.haptics.*` | Remove entirely |
| `sdk.back.*` | Remove entirely |
| `sdk.wallet.*` | Remove; wagmi handles wallet access |

For conditional `isInMiniApp` branches:

```tsx
// BEFORE
if (isInMiniApp) {
  sdk.actions.openUrl(url);
} else {
  window.open(url, "_blank");
}

// AFTER
window.open(url, "_blank");
```

Always keep the normal web branch.

#### 2D-2. Path B overrides

`Path B` does **not** mean "recreate everything." It means "keep the main app clean and preserve the smallest separate Farcaster surface possible."

- `sdk.context`
  - Remove from the main app
  - For the isolated surface, prefer replacing it with read-only fetched data or explicit route params
  - Remove `context.location`, `context.client`, safe area, and other host-derived assumptions unless the user explicitly insists on preserving a host-specific page

- `sdk.actions.composeCast(...)`
  - Remove from the main app
  - If the user only needs read-only, delete it entirely
  - If they insist on preserving it, keep it isolated behind a dedicated page/path and flag it as a manual follow-up rather than rebuilding it by default

- `sdk.actions.openMiniApp(...)`
  - Remove from the main app
  - Only keep it in an isolated route if the user explicitly wants a Farcaster-only surface

- notifications / haptics / host buttons
  - Remove from the main app
  - Preserve only if the isolated route truly depends on them and the user has explicitly opted into that complexity

### 2E. Optional Read-Only Farcaster Data (Path B only)

If the user wants an isolated Farcaster surface, prefer **read-only** data first.

**Create `lib/farcaster-readonly.ts`** (or equivalent) only if the app needs it:

```typescript
const HUB_URL = "https://hub.farcaster.xyz";

export async function getUserData(fid: number) {
  const res = await fetch(`${HUB_URL}/v1/userDataByFid?fid=${fid}`);
  if (!res.ok) throw new Error(`Hub user data fetch failed: ${res.status}`);
  return res.json();
}

export async function getCastsByFid(fid: number, pageSize = 25) {
  const res = await fetch(`${HUB_URL}/v1/castsByFid?fid=${fid}&pageSize=${pageSize}`);
  if (!res.ok) throw new Error(`Hub casts fetch failed: ${res.status}`);
  return res.json();
}
```

Then:
- Keep these calls inside the isolated route/page only
- Do not thread Farcaster data requirements through the main app shell
- If the project already has a small isolated Neynar-based read-only integration, you may keep it only if removing it would create more churn than it saves
- Do not add new Neynar packages for this by default

### 2F. Manifest Route (All Paths)

Delete `.well-known/farcaster.json` route:
- `app/.well-known/farcaster.json/route.ts`
- `public/.well-known/farcaster.json`
- `api/farcaster-manifest.ts` or similar helpers

If the `.well-known` directory becomes empty, delete it.

### 2G. Meta Tags (All Paths)

In root layout or metadata files, remove:
- `<meta>` tags with `property="fc:miniapp*"` or `property="fc:frame*"`
- `Metadata.other` entries that only exist for Farcaster tags
- `generateMetadata` logic that only produces Mini App metadata

### 2H. Dependencies

**All paths — remove:**
- `@farcaster/miniapp-sdk`, `@farcaster/miniapp-wagmi-connector`, `@farcaster/miniapp-core`
- `@farcaster/frame-sdk`, `@farcaster/frame-wagmi-connector`
- `@farcaster/quick-auth`, `@farcaster/auth-kit`

**Path A — also remove:**
- `@neynar/nodejs-sdk`, `@neynar/react`
- any other Neynar packages or helpers

**Path B — remove by default:**
- `@neynar/nodejs-sdk`, `@neynar/react`, and Neynar helpers unless they remain inside the intentionally isolated Farcaster surface

**All paths — add only if truly needed:**
- `siwe` if SIWE auth is introduced and not already present

Do not add new Neynar packages as part of the default conversion.

### 2I. Farcaster-Specific Routes & Components

**Path A:**
- Delete `app/farcaster/`, `pages/farcaster/`, and Farcaster-only components entirely
- Delete Farcaster-only API routes such as `/api/farcaster/*` and `/api/neynar/*`
- Remove any navigation links that point to deleted routes

**Path B:**
- Keep the main app route tree clean
- Move preserved Farcaster UI behind one dedicated route/page if it is not already isolated
- Prefer names like `app/farcaster/` or `app/social/` over spreading Farcaster logic throughout generic shared pages
- Remove any component that has no purpose outside that isolated surface
- Keep any remaining Neynar usage, if any, confined to that isolated route/page and its server helpers only

---

## Phase 3: Cleanup

### 3A. Update `package.json`

**All paths — remove Mini App packages:**
- `@farcaster/miniapp-sdk`, `@farcaster/miniapp-wagmi-connector`, `@farcaster/miniapp-core`
- `@farcaster/frame-sdk`, `@farcaster/frame-wagmi-connector`
- `@farcaster/quick-auth`, `@farcaster/auth-kit`

**Path A — also remove:**
- all `@neynar/*` packages

**Path B — remove unless still isolated and intentionally preserved:**
- `@neynar/*`

**All paths — add if introduced:**
- `siwe`

### 3B. Environment Variables

**Path A — remove from all `.env*` files:**
- `NEYNAR_API_KEY`
- `NEXT_PUBLIC_NEYNAR_CLIENT_ID`
- `FARCASTER_*`
- `FC_*`
- `NEXT_PUBLIC_FC_*`
- `NEXT_PUBLIC_FARCASTER_*`

**Path B — remove from the main app by default:**
- `FARCASTER_*`
- `FC_*`
- `NEXT_PUBLIC_FC_*`
- `NEXT_PUBLIC_FARCASTER_*`

Only keep `NEYNAR_*` vars if the isolated surface explicitly still depends on existing Neynar integration.

Also update env validation schemas (`env.ts`, `env.mjs`, zod schemas, etc.).

### 3C. Dead Code Cleanup

- Remove unused imports from modified files
- Remove unused Farcaster types and helper functions
- Remove empty import statements
- Remove dead hooks or API wrappers that only existed for the Mini App SDK

### 3D. Tailwind Colors

If `tailwind.config.ts` or `tailwind.config.js` includes Farcaster brand colors such as `farcaster: "#8B5CF6"`, remove them unless that branding is intentionally kept inside an isolated Farcaster-only surface.

### 3E. Install Dependencies

Tell the user:

```bash
npm install
```

---

## Phase 4: Verification

### 4A. Search for Remaining References

**All paths — search for:**
```
@farcaster
farcasterMiniApp
miniAppConnector
sdk.actions
sdk.quickAuth
sdk.context
fc:miniapp
fc:frame
```

**Path A — also search for:**
```
@neynar
NEYNAR_API_KEY
NEXT_PUBLIC_NEYNAR_CLIENT_ID
api.neynar.com
```

**Path B — if Neynar was intentionally preserved:**
- verify that remaining `@neynar` imports and env vars exist only inside the isolated Farcaster surface and its server helpers

Report any source matches, ignoring `node_modules`, lock files, and git history.

### 4B. Type Check

```bash
npx tsc --noEmit
```

Report and fix type errors.

### 4C. Build Check

```bash
npm run build
```

Report and fix build errors.

### 4D. Conversion Summary

```
## Conversion Complete — Path [X]: [Name]

**Files modified:** [count]
**Files deleted:** [count]
**Files created:** [count, if any]
**Packages removed:** [list]
**Packages added:** [list, if any]

### What was done
- [x] Removed Farcaster Mini App wagmi connector
- [x] Stubbed or removed Mini App provider/context
- [x] Replaced Mini App auth with normal web auth or removed it
- [x] Removed or replaced SDK action calls
- [x] Deleted manifest route
- [x] Removed Farcaster meta tags
- [x] Cleaned up dependencies and env vars
```

**Path B summary additionally includes:**
```
- [x] Kept the main app as a normal web app
- [x] Confined remaining Farcaster functionality to a dedicated route/page
- [x] Preferred read-only Farcaster data where possible
- [x] Removed Farcaster host/runtime coupling from shared app infrastructure
```

**All paths end with:**
```
### Manual steps
- [ ] Run `npm install`
- [ ] Test wallet connection flow
- [ ] If FID migration is needed, migrate from FID-based identity to wallet address
- [ ] If Path B preserves a Farcaster-only area, verify it stays isolated from the main app shell

### Verification
- TypeScript: [pass/fail]
- Build: [pass/fail]
- Remaining Farcaster references: [none / list]
```

---

## Edge Cases

### No wagmi

Skip Phase 2A. Do not introduce wagmi unless the app actually needs wallet connectivity.

### No auth system

Skip Phase 2C. Do not add SIWE unnecessarily.

### `@farcaster/frame-sdk` (older)

Treat identically to `@farcaster/miniapp-sdk`.

### Monorepo

Ask which workspace(s) to convert. Only modify those.

### FID as database primary key

Do not change schema automatically. Flag it and warn in Phase 4.

### Conditional `isInMiniApp` branches

Always keep the normal web branch and remove the Mini App branch.

### Components with no non-Farcaster purpose

Delete them entirely in `Path A`. In `Path B`, keep them only if they live inside the isolated Farcaster route/page.

### Existing Neynar usage

If the project already uses Neynar:
- remove it in `Path A`
- keep it only if it remains inside the isolated `Path B` surface
- do not add more Neynar usage than already exists unless the user explicitly requests it

### Read-only is usually enough

If the user says they want to "keep Farcaster stuff," bias toward:
- profile links
- read-only profile or cast display
- a dedicated social page

Do not assume they want write access, notifications, or host/runtime behavior.

### Quiz ambiguity

If the scan and quiz conflict, point it out and ask the user to confirm the smaller keep-surface first.

---

## Security

- **Validate wallet setup** — ensure `coinbaseWallet` or the chosen wallet connector is configured correctly
- **FID-based identity** — requires manual database migration if used as a primary key
- **SIWE verification** — verify signatures server-side before trusting them
- **Preserved isolated surface** — do not let a Farcaster-only route/page leak host/runtime assumptions into the main app shell
- **Existing Neynar usage** — keep API keys server-side only, and only if that isolated surface still depends on them