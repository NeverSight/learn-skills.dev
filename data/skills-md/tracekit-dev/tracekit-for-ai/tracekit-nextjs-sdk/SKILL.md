---
name: tracekit-nextjs-sdk
description: Sets up TraceKit APM in Next.js applications with multi-runtime support, error boundaries, and distributed tracing. Covers both App Router and Pages Router architectures.
---

# TraceKit Next.js SDK Setup

## When To Use

Use this skill when the user asks to:
- Add TraceKit to a Next.js application
- Add observability, error tracking, or APM to a Next.js project
- Instrument a Next.js app with distributed tracing
- Set up error monitoring in a Next.js app (App Router or Pages Router)
- Configure server-side and client-side error capture in Next.js
- Debug production Next.js applications with live breakpoints

If the user has a vanilla JavaScript/TypeScript project without Next.js, use the `tracekit-browser-sdk` skill instead. If the user has a plain React SPA (no Next.js), use the `tracekit-react-sdk` skill instead.

## Non-Negotiable Rules

1. **Never hardcode API keys** in code. Use `NEXT_PUBLIC_TRACEKIT_API_KEY` for client-side and `TRACEKIT_API_KEY` for server-side via `.env.local`.
2. **Always include a verification step** confirming errors appear in `https://app.tracekit.dev`.
3. **Always enable code monitoring** (`enableCodeMonitoring: true`) -- it is TraceKit's differentiator.
4. **Always initialize TraceKit before app bootstrap** -- use Next.js instrumentation files for both client and server init.

## Detection

Before applying this skill, detect the project type:

1. **Check `package.json`** for `next` in dependencies -- confirms this is a Next.js project.
2. **Detect router architecture** by directory structure:
   - `app/` directory exists => App Router (Next.js 13+)
   - `pages/` directory exists => Pages Router
   - Both may exist (hybrid) -- cover both patterns
3. **Only ask the user** if neither `app/` nor `pages/` directory is found.

## Step 1: Environment Setup

Set API keys in `.env.local` (Next.js convention -- never committed to git):

```bash
# .env.local
NEXT_PUBLIC_TRACEKIT_API_KEY=ctxio_your_api_key_here
TRACEKIT_API_KEY=ctxio_your_server_api_key_here
APP_VERSION=1.0.0
NEXT_PUBLIC_APP_VERSION=1.0.0
```

- `NEXT_PUBLIC_` prefix makes the variable available to client-side code (browser bundle).
- Without the prefix, the variable is only available server-side.
- Use the same key for both, or separate keys for client vs server if your security model requires it.

Where to get your API key:
1. Log in to [TraceKit](https://app.tracekit.dev)
2. Go to **API Keys** page
3. Generate a new key (starts with `ctxio_`)

## Step 2: Install SDK

```bash
npm install @tracekit/nextjs
```

Or with Yarn:

```bash
yarn add @tracekit/nextjs
```

This installs the TraceKit Next.js wrapper with multi-runtime support (client + server), error boundary components, navigation breadcrumbs, and source map upload tooling.

## Step 3: Server-Side Init

Create `instrumentation.ts` at the project root. Next.js calls the `register()` function during server startup.

```typescript
// instrumentation.ts
import { initServer, captureRequestError } from '@tracekit/nextjs';

export function register() {
  initServer({
    apiKey: process.env.TRACEKIT_API_KEY!,
    release: process.env.APP_VERSION,
    environment: process.env.NODE_ENV,
    apiEndpoint: 'https://app.tracekit.dev',
    enableCodeMonitoring: true,
  });
}

// Capture server-side request errors (App Router + Pages Router)
export const onRequestError = captureRequestError;
```

`captureRequestError` matches the Next.js `onRequestError` signature. It receives error context including `routerKind` ("App Router" or "Pages Router"), `routePath`, and `routeType` ("page", "route", or "middleware"). Errors are sent to TraceKit via HTTP POST (fire-and-forget, never throws).

## Step 4: Client-Side Init

Create `instrumentation-client.ts` at the project root. Next.js loads this file in the browser.

```typescript
// instrumentation-client.ts
import { initClient, onRouterTransitionStart } from '@tracekit/nextjs';

initClient({
  apiKey: process.env.NEXT_PUBLIC_TRACEKIT_API_KEY!,
  release: process.env.NEXT_PUBLIC_APP_VERSION,
  environment: process.env.NODE_ENV,
  endpoint: 'https://app.tracekit.dev/v1/traces',
  enableCodeMonitoring: true,
  tracePropagationTargets: [
    process.env.NEXT_PUBLIC_API_URL || 'https://api.example.com',
  ],
});

// Next.js 15.3+ navigation breadcrumbs
export { onRouterTransitionStart };
```

`initClient()` initializes the `@tracekit/browser` SDK for client-side error capture, breadcrumbs, and distributed tracing.

`onRouterTransitionStart` is a Next.js 15.3+ hook that captures client-side route transitions as breadcrumbs with from/to URLs and navigation type (push, replace, traverse).

## Step 5: Error Boundary

### App Router

Create `app/global-error.tsx` to capture errors in the root layout:

```typescript
// app/global-error.tsx
export { GlobalError as default } from '@tracekit/nextjs';
```

Or customize the error UI:

```typescript
// app/global-error.tsx
'use client';

import { useEffect } from 'react';
import { captureException } from '@tracekit/nextjs';

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    captureException(error);
  }, [error]);

  return (
    <html>
      <body>
        <h2>Something went wrong!</h2>
        <button onClick={reset}>Try again</button>
      </body>
    </html>
  );
}
```

For per-route error boundaries, create `error.tsx` files in route directories:

```typescript
// app/dashboard/error.tsx
'use client';

import { useEffect } from 'react';
import { captureException } from '@tracekit/nextjs';

export default function DashboardError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    captureException(error);
  }, [error]);

  return (
    <div>
      <h2>Dashboard error</h2>
      <button onClick={reset}>Retry</button>
    </div>
  );
}
```

### Pages Router

Wrap your custom error page with `withTraceKitErrorPage`:

```typescript
// pages/_error.tsx
import { withTraceKitErrorPage } from '@tracekit/nextjs';

function CustomErrorPage({ statusCode }: { statusCode?: number }) {
  return (
    <div>
      <h1>{statusCode ? statusCode + ' - Server Error' : 'Client Error'}</h1>
      <p>An unexpected error occurred.</p>
    </div>
  );
}

CustomErrorPage.getInitialProps = ({ res, err }: any) => {
  const statusCode = res ? res.statusCode : err ? err.statusCode : 404;
  return { statusCode, err };
};

export default withTraceKitErrorPage(CustomErrorPage);
```

## Step 6: Custom Error Capture and Performance Spans

**Client-side** (client components, event handlers):

```typescript
import { captureException, setUser } from '@tracekit/nextjs';

// Capture errors manually
try {
  await riskyOperation();
} catch (err) {
  captureException(err as Error, { context: 'checkout' });
}

// Set user context after authentication
setUser({ id: user.id, email: user.email });
```

**Server-side** (API routes, server components) -- use `captureRequestError` for automatic capture, or import from Node SDK for manual spans in API routes:

```typescript
// app/api/orders/route.ts
import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const order = await processOrder(body);
    return NextResponse.json(order);
  } catch (err) {
    // Server errors are automatically captured via captureRequestError
    return NextResponse.json({ error: 'Failed' }, { status: 500 });
  }
}
```

**Re-exported functions** available from `@tracekit/nextjs` (client-side only):

```typescript
import {
  captureException,
  captureMessage,
  setUser,
  setTag,
  setExtra,
  addBreadcrumb,
  getClient,
} from '@tracekit/nextjs';
```

These re-exports are client-side functions from `@tracekit/browser`. Do not use them in server-side code (API routes, server components). For server-side error capture, use `captureRequestError`.

## Step 7: Distributed Tracing

Client-side distributed tracing is configured via `tracePropagationTargets` in the `initClient()` call (Step 4). The SDK automatically adds trace headers (`tracekit-trace-id`, `baggage`) to outgoing `fetch` requests matching the targets.

```typescript
// instrumentation-client.ts
initClient({
  apiKey: process.env.NEXT_PUBLIC_TRACEKIT_API_KEY!,
  endpoint: 'https://app.tracekit.dev/v1/traces',
  enableCodeMonitoring: true,
  tracePropagationTargets: [
    'https://api.example.com',
    /^\/api\//,  // Same-origin API routes
  ],
});
```

Server-side API routes are automatically traced via `captureRequestError` with route context (`routerKind`, `routePath`, `routeType`).

## Step 8: Session Replay (Optional)

Enable session replay in the client-side init (browser only):

```typescript
// instrumentation-client.ts
initClient({
  apiKey: process.env.NEXT_PUBLIC_TRACEKIT_API_KEY!,
  endpoint: 'https://app.tracekit.dev/v1/traces',
  enableCodeMonitoring: true,
  replay: {
    enabled: true,
    sampleRate: 0.1,
    errorSampleRate: 1.0,
    maskAllText: true,
    blockAllMedia: false,
  },
});
```

Session replay captures DOM mutations, network requests, and console logs in the browser. It does not affect server-side rendering.

## Step 9: Source Maps (Optional)

Add the TraceKit webpack plugin to `next.config.js` for automatic source map upload during builds:

```javascript
// next.config.js
const { withTraceKit } = require('@tracekit/nextjs/webpack-plugin');

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Your existing config
};

module.exports = withTraceKit(nextConfig, {
  apiKey: process.env.TRACEKIT_API_KEY,
  release: process.env.APP_VERSION || '1.0.0',
  // Source maps are uploaded during build, not at runtime
});
```

Or upload manually after building:

```bash
tracekit sourcemaps upload \
  --api-key $TRACEKIT_API_KEY \
  --release 1.0.0 \
  --dist .next/static
```

## Step 10: Verification

After integrating, verify both client-side and server-side errors are captured:

1. **Client-side:** Add a button that throws an error in a client component:
   ```typescript
   'use client';
   export default function TestPage() {
     return <button onClick={() => { throw new Error('TraceKit Next.js client test'); }}>Test Error</button>;
   }
   ```

2. **Server-side:** Create an API route that throws:
   ```typescript
   // app/api/test-error/route.ts
   export async function GET() {
     throw new Error('TraceKit Next.js server test');
   }
   ```

3. **Open** `https://app.tracekit.dev`.
4. **Confirm** both errors appear within 30-60 seconds -- client errors show browser context, server errors show route context.

## Complete Working Example (App Router)

All files needed for a full Next.js App Router setup:

```bash
# .env.local
NEXT_PUBLIC_TRACEKIT_API_KEY=ctxio_your_api_key_here
TRACEKIT_API_KEY=ctxio_your_server_api_key_here
APP_VERSION=1.0.0
NEXT_PUBLIC_APP_VERSION=1.0.0
```

```typescript
// instrumentation-client.ts
import { initClient, onRouterTransitionStart } from '@tracekit/nextjs';

initClient({
  apiKey: process.env.NEXT_PUBLIC_TRACEKIT_API_KEY!,
  release: process.env.NEXT_PUBLIC_APP_VERSION,
  environment: process.env.NODE_ENV,
  endpoint: 'https://app.tracekit.dev/v1/traces',
  enableCodeMonitoring: true,
  tracePropagationTargets: [
    process.env.NEXT_PUBLIC_API_URL || 'https://api.example.com',
  ],
  replay: {
    enabled: true,
    sampleRate: 0.1,
    errorSampleRate: 1.0,
  },
});

export { onRouterTransitionStart };
```

```typescript
// instrumentation.ts
import { initServer, captureRequestError } from '@tracekit/nextjs';

export function register() {
  initServer({
    apiKey: process.env.TRACEKIT_API_KEY!,
    release: process.env.APP_VERSION,
    environment: process.env.NODE_ENV,
    enableCodeMonitoring: true,
  });
}

export const onRequestError = captureRequestError;
```

```typescript
// app/global-error.tsx
export { GlobalError as default } from '@tracekit/nextjs';
```

```typescript
// app/layout.tsx
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

## Troubleshooting

### Server errors not appearing

- **Check `instrumentation.ts`:** Ensure `register()` calls `initServer()` and `onRequestError` is exported at the top level.
- **Check `TRACEKIT_API_KEY`** is set in `.env.local` (without `NEXT_PUBLIC_` prefix for server-side).
- **Check outbound access:** Server must reach `https://app.tracekit.dev`. Test with: `curl -X POST https://app.tracekit.dev/v1/traces` (expect 401).

### Client errors not appearing

- **Check `instrumentation-client.ts`:** Ensure `initClient()` is called with `NEXT_PUBLIC_TRACEKIT_API_KEY`.
- **Check browser console** for initialization errors or network failures to the TraceKit endpoint.

### Server vs client init confusion

- **Server:** `instrumentation.ts` with `initServer()` -- runs in Node.js/Edge runtime
- **Client:** `instrumentation-client.ts` with `initClient()` -- runs in the browser
- Do not import server functions in client code or vice versa.

### Edge runtime compatibility

- `captureRequestError` uses `fetch()` internally, which is available in both Node.js and Edge runtimes.
- `initServer()` stores config in a module-scoped variable -- safe for both runtimes.

### Hydration errors

- TraceKit captures React recoverable hydration errors automatically via `onRecoverableError` in the client-side init.
- These appear as "handled" errors with mechanism `react.onRecoverableError`.

### Navigation breadcrumbs not appearing

- `onRouterTransitionStart` requires Next.js 15.3+. On older versions, breadcrumbs are captured via the base `@tracekit/browser` navigation integration.
- Ensure `onRouterTransitionStart` is re-exported from `instrumentation-client.ts`.

## Next Steps

Once your Next.js app is traced, consider:
- **Browser SDK** -- For non-Next.js pages, use the `tracekit-browser-sdk` skill
- **React SDK** -- For plain React SPAs, use the `tracekit-react-sdk` skill
- **Session Replay** -- Record and replay user sessions with linked traces
- **Source Maps** -- Upload source maps for readable production stack traces
- **Backend SDKs** -- Connect frontend traces to backend services for full distributed tracing

## References

- Next.js SDK docs: `https://app.tracekit.dev/docs/frontend/frameworks/nextjs`
- Browser SDK docs: `https://app.tracekit.dev/docs/frontend/browser-sdk`
- TraceKit docs root: `https://app.tracekit.dev/docs`
- Dashboard: `https://app.tracekit.dev`
