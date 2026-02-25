---
name: gainforest-oauth-setup
description: Implement ATProto OAuth authentication in a Next.js App Router application using gainforest-sdk-nextjs. Use when adding login, logout, session management, or authentication flows that integrate with GainForest, Hypercerts, or ATProto PDSes (climateai.org, gainforest.id).
compatibility: Requires Next.js App Router, Supabase project, Node.js
metadata:
  author: gainforest
  version: "2.0"
---

# GainForest OAuth Implementation

Step-by-step instructions for implementing ATProto OAuth in a Next.js (App Router) application using `gainforest-sdk-nextjs`.

## When to Apply

Use this skill when:
- Adding OAuth/authentication to a Next.js app using `gainforest-sdk-nextjs`
- Setting up login/logout flows for ATProto PDS accounts
- Integrating with climateai.org or gainforest.id PDS servers
- Configuring session management with iron-session + Supabase

## Prerequisites

Before starting, verify:
- The project is a **Next.js App Router** application
- `gainforest-sdk-nextjs` and `@supabase/supabase-js` are installed (if not, run `npm install gainforest-sdk-nextjs @supabase/supabase-js`)
- A Supabase project exists with two required tables: `atproto_oauth_session` and `atproto_oauth_state`. **If these tables do not exist yet, create them first** using the SQL in [references/supabase-tables.md](references/supabase-tables.md)

## Critical API Rules

These are non-obvious gotchas. Violating any of these will cause runtime failures.

1. **`storage` nesting**: `sessionStore` and `stateStore` must be nested under `storage: { ... }` in `createATProtoSDK()` config. They are NOT top-level properties.
2. **`OAuthSession` has no `handle`**: The session returned by `callback()` only has `sub`/`did`. You MUST resolve the handle separately via `Agent` + `com.atproto.repo.describeRepo()`.
3. **`GainForestSDK` constructor takes 2 arguments**: `new GainForestSDK(domains, atprotoSDK)`. Not just domains.
4. **`getServerCaller()` takes 0 arguments**: The SDK instance is injected at construction time.
5. **`createContext` is NOT a standalone export**: Use `gainforestSDK.createContext()` instance method instead.
6. **Logout requires two steps**: Call `sdk.revokeSession(did)` to invalidate tokens in Supabase, THEN `clearAppSession()` to clear the cookie. Skipping `revokeSession()` leaves tokens valid.
7. **`COOKIE_SECRET` must be >= 32 characters**: iron-session will throw otherwise.
8. **All OAuth/session helpers are server-side only**: They use `cookies()` from `next/headers`.

## Required Environment Variables

Ensure `.env.local` contains:

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# OAuth Client Configuration
# For local development, use 127.0.0.1 (see references/local-development.md for loopback details)
NEXT_PUBLIC_APP_URL=http://127.0.0.1:3000
# Private key - no "use" field (deprecated), no "key_ops" needed for private keys
OAUTH_PRIVATE_KEY='{"kty":"EC","crv":"P-256","x":"...","y":"...","d":"...","kid":"key-1","alg":"ES256"}'

# Session Cookie
COOKIE_SECRET=your-secret-key-at-least-32-characters-long
COOKIE_NAME=your_app_session
```

| Variable | Required | Notes |
|---|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` | Yes | Your Supabase project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Yes | Server-side only. Never expose to client. |
| `NEXT_PUBLIC_APP_URL` | Yes | Public URL of your app. Use `http://127.0.0.1:3000` for local dev (not `localhost`). |
| `OAUTH_PRIVATE_KEY` | Yes | ES256 JWK. Generate with [scripts/generate-oauth-key.js](scripts/generate-oauth-key.js) if needed. |
| `COOKIE_SECRET` | Yes | Min 32 characters. Used by iron-session for cookie encryption. |
| `COOKIE_NAME` | No | Unique per app (e.g., `greenglobe_session`). Defaults to `climateai_session`. |

## Implementation Steps

Follow these steps in order. Each step produces one file.

### Step 1: Generate OAuth Private Key (if needed)

Only if the user doesn't already have an `OAUTH_PRIVATE_KEY`.

Run the bundled script:

```bash
node scripts/generate-oauth-key.js
```

Or copy the script from [scripts/generate-oauth-key.js](scripts/generate-oauth-key.js) into the user's project and run it there. The script requires `jose` as a dependency (`npm install jose`).

### Step 2: Create ATProto SDK Instance

**Important**: For local development loopback configuration (localhost vs 127.0.0.1, RFC 8252 requirements, scope handling), see [references/local-development.md](references/local-development.md).

Create `lib/atproto.ts`:

```typescript
import {
  createATProtoSDK,
  createSupabaseSessionStore,
  createSupabaseStateStore,
} from "gainforest-sdk-nextjs/oauth";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
);

const APP_ID = "your-app-name"; // Unique per app, e.g., "greenglobe", "bumicerts"
const PUBLIC_URL = process.env.NEXT_PUBLIC_APP_URL!;
const isDev = process.env.NODE_ENV === "development";

// Loopback clients require "atproto transition:generic" scope
const scope = isDev ? "atproto transition:generic" : "atproto";

export const atprotoSDK = createATProtoSDK({
  oauth: {
    // Loopback: client ID embeds scope and redirect URI (no port)
    // Production: client ID is URL to metadata endpoint
    clientId: isDev
      ? `http://localhost?scope=${encodeURIComponent(scope)}&redirect_uri=${encodeURIComponent(`${PUBLIC_URL}/api/oauth/callback`)}`
      : `${PUBLIC_URL}/client-metadata.json`,
    redirectUri: `${PUBLIC_URL}/api/oauth/callback`,
    jwksUri: `${PUBLIC_URL}/.well-known/jwks.json`,
    jwkPrivate: process.env.OAUTH_PRIVATE_KEY!,
    scope,
  },
  servers: {
    pds: "https://climateai.org", // or "https://gainforest.id"
  },
  storage: {
    sessionStore: createSupabaseSessionStore(supabase, APP_ID),
    stateStore: createSupabaseStateStore(supabase, APP_ID),
  },
});
```

### Step 3: Client Metadata Route

Create `app/client-metadata.json/route.ts`:

```typescript
import { NextResponse } from "next/server";

const PUBLIC_URL = process.env.NEXT_PUBLIC_APP_URL!;
const isDev = process.env.NODE_ENV === "development";

// Loopback clients require "atproto transition:generic" scope
const scope = isDev ? "atproto transition:generic" : "atproto";

export async function GET() {
  const metadata = {
    // Loopback: client ID embeds scope and redirect URI
    // Production: client ID is this metadata endpoint URL
    client_id: isDev
      ? `http://localhost?scope=${encodeURIComponent(scope)}&redirect_uri=${encodeURIComponent(`${PUBLIC_URL}/api/oauth/callback`)}`
      : `${PUBLIC_URL}/client-metadata.json`,
    client_name: "Your App Name",
    client_uri: PUBLIC_URL,
    logo_uri: `${PUBLIC_URL}/logo.png`,
    tos_uri: `${PUBLIC_URL}/terms`,
    policy_uri: `${PUBLIC_URL}/privacy`,
    redirect_uris: [`${PUBLIC_URL}/api/oauth/callback`],
    grant_types: ["authorization_code", "refresh_token"],
    response_types: ["code"],
    scope,
    // Loopback uses "none", production uses "private_key_jwt"
    token_endpoint_auth_method: isDev ? "none" : "private_key_jwt",
    token_endpoint_auth_signing_alg: isDev ? undefined : "ES256",
    // Loopback is "native", production is "web"
    application_type: isDev ? "native" : "web",
    dpop_bound_access_tokens: true,
    jwks_uri: `${PUBLIC_URL}/.well-known/jwks.json`,
  };

  return NextResponse.json(metadata, {
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "public, max-age=3600",
    },
  });
}
```

### Step 4: JWKS Endpoint

Create `app/.well-known/jwks.json/route.ts`:

```typescript
import { NextResponse } from "next/server";

export async function GET() {
  const privateKey = JSON.parse(process.env.OAUTH_PRIVATE_KEY!);
  const { d, ...publicKey } = privateKey;
  
  // Add key_ops for public key verification (replaces deprecated "use" field)
  const jwk = {
    ...publicKey,
    key_ops: ["verify"],
  };
  
  // Remove deprecated "use" field if present in source key
  delete jwk.use;

  return NextResponse.json({ keys: [jwk] }, {
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "public, max-age=3600",
    },
  });
}
```

**Note**: The `key_ops: ["verify"]` field replaces the deprecated `use: "sig"` field per current JWK specifications. Only public keys in the JWKS endpoint need `key_ops`; private keys do not.

### Step 5: Authorization Route

Create `app/api/oauth/authorize/route.ts` (or implement as a server action):

```typescript
import { NextRequest, NextResponse } from "next/server";
import { atprotoSDK } from "@/lib/atproto";

export async function POST(request: NextRequest) {
  try {
    const { handle } = await request.json();

    if (!handle) {
      return NextResponse.json(
        { error: "Handle is required" },
        { status: 400 }
      );
    }

    const authUrl = await atprotoSDK.authorize(handle);
    return NextResponse.json({ authorizationUrl: authUrl.toString() });
  } catch (error) {
    console.error("Authorization error:", error);
    return NextResponse.json(
      { error: "Failed to initiate authorization" },
      { status: 500 }
    );
  }
}
```

### Step 6: Callback Route

Create `app/api/oauth/callback/route.ts`:

**IMPORTANT**: `OAuthSession` does NOT have a `handle` property. You must resolve it from the DID using an `Agent`.

```typescript
import { NextRequest } from "next/server";
import { redirect } from "next/navigation";
import { atprotoSDK } from "@/lib/atproto";
import { saveAppSession, Agent } from "gainforest-sdk-nextjs/oauth";

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const oauthSession = await atprotoSDK.callback(searchParams);

    // Resolve handle from DID -- OAuthSession only has sub/did, NOT handle
    const agent = new Agent(oauthSession);
    const { data: profile } = await agent.com.atproto.repo.describeRepo({
      repo: oauthSession.did,
    });

    await saveAppSession({
      did: oauthSession.did,
      handle: profile.handle,
      isLoggedIn: true,
    });

    redirect("/dashboard");
  } catch (error) {
    console.error("OAuth callback error:", error);
    redirect("/login?error=auth_failed");
  }
}
```

### Step 7: Logout Route

Create `app/api/oauth/logout/route.ts` (or implement as a server action):

**IMPORTANT**: Must call `revokeSession()` before `clearAppSession()`. Otherwise OAuth tokens remain valid in Supabase.

```typescript
import { NextResponse } from "next/server";
import { clearAppSession, getAppSession } from "gainforest-sdk-nextjs/oauth";
import { atprotoSDK } from "@/lib/atproto";

export async function POST() {
  try {
    const appSession = await getAppSession();
    if (appSession.did) {
      await atprotoSDK.revokeSession(appSession.did);
    }
    await clearAppSession();

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error("Logout error:", error);
    return NextResponse.json(
      { error: "Failed to logout" },
      { status: 500 }
    );
  }
}
```

### Step 8: Session Check Route

Create `app/api/oauth/session/route.ts`:

```typescript
import { NextResponse } from "next/server";
import { getAppSession } from "gainforest-sdk-nextjs/oauth";
import { atprotoSDK } from "@/lib/atproto";

export async function GET() {
  try {
    const appSession = await getAppSession();

    if (!appSession.isLoggedIn || !appSession.did) {
      return NextResponse.json({ authenticated: false });
    }

    const oauthSession = await atprotoSDK.restoreSession(appSession.did);

    if (!oauthSession) {
      return NextResponse.json({ authenticated: false });
    }

    return NextResponse.json({
      authenticated: true,
      did: appSession.did,
      handle: appSession.handle,
    });
  } catch (error) {
    console.error("Session check error:", error);
    return NextResponse.json({ authenticated: false });
  }
}
```

### Step 9: Login UI Component

Create a client component (e.g., `components/login-form.tsx`):

```tsx
"use client";

import { useState } from "react";

export function LoginForm() {
  const [handle, setHandle] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await fetch("/api/oauth/authorize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ handle }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Authorization failed");
      }

      window.location.href = data.authorizationUrl;
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="handle">Your Handle</label>
        <input
          id="handle"
          type="text"
          value={handle}
          onChange={(e) => setHandle(e.target.value)}
          placeholder="username.climateai.org"
          required
        />
      </div>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <button type="submit" disabled={loading}>
        {loading ? "Redirecting..." : "Sign in with ATProto"}
      </button>
    </form>
  );
}
```

### Step 10 (Optional): tRPC Integration

If the app uses the SDK's built-in tRPC routers:

**`lib/trpc.ts`**:
```typescript
import { GainForestSDK } from "gainforest-sdk-nextjs";
import { atprotoSDK } from "@/lib/atproto";

// Two arguments: domains array AND the atprotoSDK instance
const gainforestSDK = new GainForestSDK(
  ["climateai.org", "gainforest.id"],
  atprotoSDK
);

// Zero arguments -- SDK already injected at construction
export const serverCaller = gainforestSDK.getServerCaller();
```

**`app/api/trpc/[trpc]/route.ts`**:
```typescript
import { fetchRequestHandler } from "@trpc/server/adapters/fetch";
import { GainForestSDK } from "gainforest-sdk-nextjs";
import { atprotoSDK } from "@/lib/atproto";

const gainforestSDK = new GainForestSDK(
  ["climateai.org", "gainforest.id"],
  atprotoSDK
);

const handler = (req: Request) =>
  fetchRequestHandler({
    endpoint: "/api/trpc",
    req,
    router: gainforestSDK.appRouter,
    // Instance method -- createContext is NOT a standalone export
    createContext: () => gainforestSDK.createContext({ req }),
  });

export { handler as GET, handler as POST };
```

## Making Authenticated API Calls

After OAuth is set up, use this pattern for authenticated server-side calls:

```typescript
import { atprotoSDK } from "@/lib/atproto";
import { getAppSession, Agent } from "gainforest-sdk-nextjs/oauth";

export async function getAuthenticatedAgent(): Promise<Agent> {
  const appSession = await getAppSession();

  if (!appSession.isLoggedIn || !appSession.did) {
    throw new Error("Not authenticated");
  }

  const oauthSession = await atprotoSDK.restoreSession(appSession.did);

  if (!oauthSession) {
    throw new Error("Session expired");
  }

  return new Agent(oauthSession);
}
```

## Import Reference

| Import Path | Exports |
|---|---|
| `gainforest-sdk-nextjs` | `GainForestSDK` |
| `gainforest-sdk-nextjs/oauth` | `createATProtoSDK`, `createSupabaseSessionStore`, `createSupabaseStateStore`, `cleanupExpiredStates`, `getAppSession`, `saveAppSession`, `clearAppSession`, `Agent`, `HypercertsATProtoSDK`, `SessionStore`, `StateStore`, `ATProtoSDKConfig`, `AppSessionData` |
| `gainforest-sdk-nextjs/session` | `getAppSession`, `saveAppSession`, `clearAppSession`, `AppSessionData` |
| `gainforest-sdk-nextjs/client` | `createTRPCClient` (tRPC client) |

## Expected File Structure

After implementation, the app should have:

```text
your-app/
├── .env.local
├── lib/
│   ├── atproto.ts                       # SDK instance
│   └── trpc.ts                          # tRPC setup (optional)
├── app/
│   ├── client-metadata.json/
│   │   └── route.ts                     # OAuth client metadata
│   ├── .well-known/
│   │   └── jwks.json/
│   │       └── route.ts                 # Public JWKS endpoint
│   ├── api/
│   │   ├── oauth/
│   │   │   ├── authorize/
│   │   │   │   └── route.ts             # Initiate OAuth flow
│   │   │   ├── callback/
│   │   │   │   └── route.ts             # Handle OAuth callback
│   │   │   ├── logout/
│   │   │   │   └── route.ts             # Revoke session + clear cookie
│   │   │   └── session/
│   │   │       └── route.ts             # Check session status
│   │   └── trpc/
│   │       └── [trpc]/
│   │           └── route.ts             # tRPC handler (optional)
│   └── login/
│       └── page.tsx                     # Login page
└── components/
    └── login-form.tsx                   # Login form component
```

## Further Reading

- [Supabase table setup](references/supabase-tables.md) -- SQL DDL for the required tables
- [Local development](references/local-development.md) -- Loopback URLs, dev mode, env overrides
- [Troubleshooting](references/troubleshooting.md) -- Common errors, security checklist, cleanup
