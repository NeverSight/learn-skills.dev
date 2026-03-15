---
name: cloudsignal-websocket
description: >
  Generate a production-grade React MQTT context for CloudSignal real-time
  notifications over WebSocket. Supports Clerk, Supabase, Auth0, Firebase,
  and custom OIDC auth providers. Use when implementing real-time notifications,
  live updates, job progress tracking, or WebSocket messaging with CloudSignal.
disable-model-invocation: true
license: MIT
metadata:
  author: cloudsignal
  version: "1.0.0"
---

# CloudSignal WebSocket — React MQTT Context Generator

Generate a production-grade React context provider for real-time messaging over CloudSignal's MQTT broker using WebSocket. The generated code handles the full connection lifecycle: authentication via external auth providers, reconnection, proactive token refresh, message routing, and cleanup.

## What You Generate

1. **`mqtt-context.tsx`** — React context provider with:
   - Auth-provider token exchange (Clerk, Supabase, Auth0, Firebase, or custom OIDC)
   - WebSocket connection to CloudSignal MQTT broker
   - Auth error circuit-breaker (max 3 retries, 10s delay)
   - Proactive token refresh at 50 minutes (before 60-min TTL expiry)
   - Exact topic routing with safe JSON parsing
   - React StrictMode double-mount protection
   - Tab visibility reconnection
   - Typed subscription hooks (jobs, notifications, transactions, or custom)

2. **`cloudsignal.d.ts`** — TypeScript declarations for `@cloudsignal/mqtt-client` (the npm package does not ship types)

## Before You Start

Ask the user for these inputs (use defaults if not provided):

| Input | Example | Default |
|-------|---------|---------|
| Auth provider | Clerk, Supabase, Auth0, Firebase | Ask (required) |
| Organization ID | `org_k7xm4pqr2n5t` | Ask (required) |
| Topic namespace | `myapp` | App name from package.json |
| Message types needed | notifications, jobs, transactions | All three |
| Target directory | `src/lib/` or `src/contexts/` | `src/lib/` |

## Generation Steps

### Step 1: Read the Reference Implementation

Read `references/mqtt-context.tsx` in this skill's directory. This is the canonical reference — a production-tested context provider extracted from a live SaaS. Use it as the base for all generated code.

### Step 2: Adapt the Auth Provider Hooks

The reference contains two placeholder functions that MUST be replaced based on the user's auth provider:

**`useCurrentUser()`** — must return `{ id: string } | null`:

| Provider | Implementation |
|----------|---------------|
| **Clerk** | `import { useUser } from "@clerk/nextjs"; const { user } = useUser(); return user ? { id: user.id } : null;` |
| **Supabase** | `import { useSession } from "@supabase/auth-helpers-react"; const session = useSession(); return session ? { id: session.user.id } : null;` |
| **Auth0** | `import { useAuth0 } from "@auth0/auth0-react"; const { user, isAuthenticated } = useAuth0(); return isAuthenticated && user ? { id: user.sub! } : null;` |
| **Firebase** | `import { useAuthState } from "react-firebase-hooks/auth"; import { auth } from "@/lib/firebase"; const [user] = useAuthState(auth); return user ? { id: user.uid } : null;` |

**`useGetToken()`** — must return `() => Promise<string | null>`:

| Provider | Implementation |
|----------|---------------|
| **Clerk** | `import { useAuth } from "@clerk/nextjs"; const { getToken } = useAuth(); return getToken;` |
| **Supabase** | `import { useSupabaseClient } from "@supabase/auth-helpers-react"; const supabase = useSupabaseClient(); return async () => { const { data } = await supabase.auth.getSession(); return data.session?.access_token ?? null; };` |
| **Auth0** | `import { useAuth0 } from "@auth0/auth0-react"; const { getAccessTokenSilently } = useAuth0(); return async () => { try { return await getAccessTokenSilently(); } catch { return null; } };` |
| **Firebase** | `import { auth } from "@/lib/firebase"; return async () => auth.currentUser?.getIdToken() ?? null;` |

### Step 3: Customize Message Types

Replace the reference message interfaces with the user's domain. Keep the structure (interface + handler type + registry pattern) but adapt field names and types.

Default message types from reference: `ProgressMessage`, `StatusMessage`, `TransactionMessage`, `NotificationMessage`.

### Step 4: Set Configuration Constants

```tsx
const CLOUDSIGNAL_ORG_ID = process.env.NEXT_PUBLIC_CLOUDSIGNAL_ORG_ID;
const CLOUDSIGNAL_HOST = process.env.NEXT_PUBLIC_CLOUDSIGNAL_HOST || "wss://connect.cloudsignal.app:18885/";
const TOPIC_ROOT = "{user's namespace}";
```

### Step 5: Write the Type Declarations

Read `references/cloudsignal.d.ts` and write it to the user's `types/` directory (or wherever their project keeps type declarations). This file is required because `@cloudsignal/mqtt-client` does not ship `.d.ts` files.

### Step 6: Write the Context Provider

Combine the adapted auth hooks, customized message types, and the full provider logic from the reference into the final `mqtt-context.tsx`. Preserve ALL of these production patterns:

- **Stable ref pattern**: `connectRef` updated every render, used by timers
- **Auth error circuit-breaker**: `authErrorCountRef` with `MAX_AUTH_ERRORS = 3`
- **Proactive token refresh**: `scheduleTokenRefresh()` at 50 minutes
- **StrictMode guard**: `connectingRef` + `mountedRef` prevent double connections
- **Exact topic matching**: `topic === \`${prefix}/notifications\`` not `.includes()`
- **Safe JSON parsing**: try/catch around `JSON.parse` in message handler
- **Client destruction on auth error**: Stops SDK's stale-token reconnect loop
- **Tab visibility reconnect**: `visibilitychange` event listener

### Step 7: Show Usage

Provide a usage example showing:
1. Provider wrapping in `app/providers.tsx` (nested inside the auth provider)
2. A consumer component using `useMQTT()` hook
3. Environment variable setup (`.env.local`)

## Critical SDK Pitfalls

Read `references/sdk-pitfalls.md` for the full list. These MUST be handled in generated code:

1. **Token expiry reconnect loop**: Destroy client on `onAuthError`, don't rely on SDK reconnect
2. **`externalToken` not `idToken`**: Use `externalToken` in `connectWithToken()`
3. **No TypeScript declarations**: Always generate `cloudsignal.d.ts`
4. **React StrictMode double-mount**: Use `connectingRef` + `mountedRef` guards
5. **Token service version**: SDK v2.x expects `/v2/tokens/exchange`
6. **CJS `require()` breaks `mqtt.connect()`**: Always use ESM `import`, never `require()`

## Environment Variables

Tell the user to add these to `.env.local`:

```bash
NEXT_PUBLIC_CLOUDSIGNAL_ORG_ID=org_xxxxxxxxxxxxx    # From CloudSignal dashboard
NEXT_PUBLIC_CLOUDSIGNAL_HOST=wss://connect.cloudsignal.app:18885/  # Optional, this is default
```

## CloudSignal Dashboard Setup

Remind the user they need to configure their CloudSignal organization:
1. Create an organization at https://dashboard.cloudsignal.app
2. Configure an External Auth Provider integration (select their provider, enter JWKS URL)
3. Note the `org_xxx` ID for the environment variable

## npm Dependency

The user needs to install the CloudSignal MQTT client:

```bash
npm install @cloudsignal/mqtt-client
```
