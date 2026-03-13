---
name: tracekit-browser-sdk
description: Sets up TraceKit APM in vanilla JavaScript/TypeScript applications for automatic error capture, breadcrumbs, performance monitoring, and distributed tracing. Use when the user has a plain HTML/JS, Web Components, or vanilla TypeScript project without a framework like React, Vue, or Angular.
---

# TraceKit Browser SDK Setup

## When To Use

Use this skill when the user asks to:
- Add TraceKit to a JavaScript or TypeScript application
- Add observability or APM to a vanilla JS project
- Instrument a browser app with error tracking or distributed tracing
- Configure TraceKit API keys in a frontend project
- Set up error monitoring in a plain HTML/JS or Web Components app
- Add performance monitoring to a vanilla TypeScript project

**Framework users:** If the user is using React, Vue, Angular, Next.js, or Nuxt, use the corresponding framework wrapper skill instead (`tracekit-react-sdk`, `tracekit-vue-sdk`, `tracekit-angular-sdk`, `tracekit-nextjs-sdk`, `tracekit-nuxt-sdk`). Framework wrappers provide tighter integration with error boundaries, router breadcrumbs, and SSR support.

**Svelte/Solid users:** These frameworks do not have dedicated wrapper skills. Use this browser SDK skill directly — it works in any JavaScript environment.

## Non-Negotiable Rules

1. **Never hardcode API keys** in code. Always use environment variables or build-time injection (e.g., `import.meta.env.VITE_TRACEKIT_API_KEY`).
2. **Always include a verification step** confirming errors and traces appear in `https://app.tracekit.dev/traces`.
3. **Always enable code monitoring** (`enableCodeMonitoring: true`) — it is TraceKit's differentiator for live debugging.
4. **Always init TraceKit before any other application code** — the SDK must be the first thing that runs to capture all errors.

## Detection

Before applying this skill, detect the project type:

1. **Check for `package.json`** — confirms this is a JavaScript/TypeScript project.
2. **Confirm NO framework detected** — scan `package.json` dependencies for:
   - `react-dom` => use `tracekit-react-sdk` skill instead
   - `vue` => use `tracekit-vue-sdk` skill instead
   - `@angular/core` => use `tracekit-angular-sdk` skill instead
   - `next` => use `tracekit-nextjs-sdk` skill instead
   - `nuxt` => use `tracekit-nuxt-sdk` skill instead
3. **Check for TypeScript:** `tsconfig.json` presence means use TypeScript snippets.
4. **Detect build tool** for env var injection pattern:
   - `vite.config.*` => Vite (`import.meta.env.VITE_TRACEKIT_API_KEY`)
   - `webpack.config.*` => Webpack (`process.env.TRACEKIT_API_KEY`)
   - Neither => plain script tag setup
5. **Only ask the user** if `package.json` is missing or multiple frameworks are detected.

## Step 1: Environment Setup

Set the `TRACEKIT_API_KEY` environment variable. This is the only required secret.

Add to your `.env` file:

```bash
TRACEKIT_API_KEY=ctxio_your_api_key_here
```

**Build tool injection** — how the env var reaches your code depends on your bundler:

| Build Tool | Env Var Name | Access Pattern |
|------------|-------------|----------------|
| Vite | `VITE_TRACEKIT_API_KEY` | `import.meta.env.VITE_TRACEKIT_API_KEY` |
| Webpack | `TRACEKIT_API_KEY` | `process.env.TRACEKIT_API_KEY` |
| Parcel | `TRACEKIT_API_KEY` | `process.env.TRACEKIT_API_KEY` |
| None (script tag) | N/A | Pass key directly in init config |

Where to get your API key:
1. Log in to [TraceKit](https://app.tracekit.dev)
2. Go to **API Keys** page
3. Generate a new key (starts with `ctxio_`)

Do **not** commit real API keys. Use `.env` files, deployment secret managers, or CI variables.

## Step 2: Install SDK

```bash
npm install @tracekit/browser
```

Or with Yarn:

```bash
yarn add @tracekit/browser
```

This installs the TraceKit browser SDK with automatic error capture, breadcrumb tracking, distributed tracing support, and code monitoring.

## Step 3: Initialize TraceKit

Create a `tracekit.ts` (or `tracekit.js`) file and import it as the **first module** in your application entry point.

### TypeScript (Vite)

```typescript
// src/tracekit.ts — import this FIRST in main.ts
import { init } from '@tracekit/browser';

init({
  apiKey: import.meta.env.VITE_TRACEKIT_API_KEY,
  serviceName: 'my-frontend-app',
  endpoint: 'https://app.tracekit.dev/v1/traces',
  enableCodeMonitoring: true,
  release: import.meta.env.VITE_APP_VERSION || '0.0.0',
  environment: import.meta.env.MODE,
});
```

### JavaScript (Webpack)

```javascript
// src/tracekit.js — import this FIRST in index.js
const { init } = require('@tracekit/browser');

init({
  apiKey: process.env.TRACEKIT_API_KEY,
  serviceName: 'my-frontend-app',
  endpoint: 'https://app.tracekit.dev/v1/traces',
  enableCodeMonitoring: true,
  release: process.env.APP_VERSION || '0.0.0',
  environment: process.env.NODE_ENV,
});
```

Then in your entry point:

```typescript
// src/main.ts
import './tracekit'; // MUST be first import
import { startApp } from './app';

startApp();
```

**What auto-captures after init:**
- Uncaught errors (`window.onerror`)
- Unhandled promise rejections (`unhandledrejection`)
- Console errors (`console.error`, `console.warn`)
- Click and navigation breadcrumbs (DOM interactions, `pushState`/`popState`)
- Network request breadcrumbs (fetch and XHR)

## Step 4: Error Capture

Capture errors explicitly in catch blocks:

```typescript
import { captureException, captureMessage } from '@tracekit/browser';

// Capture caught errors
try {
  await riskyOperation();
} catch (err) {
  captureException(err as Error, { component: 'Dashboard' });
}

// Capture informational messages
captureMessage('User completed onboarding', 'info');
captureMessage('Payment retry limit exceeded', 'warning');
```

### User Context

Attach user identity to all subsequent events:

```typescript
import { setUser } from '@tracekit/browser';

// After login
setUser({ id: 'user-123', email: 'alice@example.com', username: 'alice' });

// On logout
setUser(null);
```

### Custom Tags and Extra Data

```typescript
import { setTag, setExtra, addBreadcrumb } from '@tracekit/browser';

setTag('tenant', 'acme-corp');
setExtra('cart_items', 3);

addBreadcrumb({
  type: 'user',
  category: 'cart',
  message: 'Added item to cart',
  level: 'info',
  data: { productId: 'prod-456', price: 29.99 },
});
```

## Step 5: Custom Performance Spans

Measure specific operations like API calls, rendering, or user interactions:

```typescript
import { getClient } from '@tracekit/browser';

const client = getClient();

// Measure an async operation
const span = client.startSpan('load-dashboard', null, {
  'component': 'Dashboard',
  'user.id': currentUser.id,
});

try {
  const data = await fetchDashboardData();
  renderDashboard(data);
  span.end();
} catch (err) {
  client.captureException(err as Error);
  span.end();
}
```

## Step 6: Distributed Tracing

Connect frontend requests to backend traces by configuring `tracePropagationTargets`. The SDK automatically injects `traceparent` headers into fetch and XHR requests matching these patterns.

```typescript
import { init } from '@tracekit/browser';

init({
  apiKey: import.meta.env.VITE_TRACEKIT_API_KEY,
  serviceName: 'my-frontend-app',
  endpoint: 'https://app.tracekit.dev/v1/traces',
  enableCodeMonitoring: true,
  tracePropagationTargets: [
    'https://api.myapp.com',           // Exact match
    'https://auth.myapp.com',          // Another backend
    /^https:\/\/.*\.myapp\.com/,       // Regex: all subdomains
  ],
});
```

**How it works:**
1. Frontend fetch/XHR requests to matching URLs receive a `traceparent` header
2. Your backend SDK reads this header and links the backend span to the frontend trace
3. The full request lifecycle appears as a single trace in the TraceKit dashboard

**Important:** Your backend CORS configuration must accept the `traceparent` and `tracestate` headers:

```javascript
// Express.js backend example
app.use(cors({
  origin: 'https://your-app.com',
  allowedHeaders: ['Content-Type', 'Authorization', 'traceparent', 'tracestate'],
}));
```

## Step 7: Session Replay (Optional)

Record user sessions for visual debugging. Replay shows exactly what the user saw when an error occurred.

```typescript
import { init } from '@tracekit/browser';
import { replayIntegration } from '@tracekit/replay';

const replay = replayIntegration({
  sessionSampleRate: 0.1,   // Record 10% of sessions
  errorSampleRate: 1.0,     // Always record sessions with errors
});

init({
  apiKey: import.meta.env.VITE_TRACEKIT_API_KEY,
  serviceName: 'my-frontend-app',
  endpoint: 'https://app.tracekit.dev/v1/traces',
  enableCodeMonitoring: true,
  addons: [replay],
});
```

**Privacy settings** — mask sensitive content by default:

```typescript
const replay = replayIntegration({
  sessionSampleRate: 0.1,
  errorSampleRate: 1.0,
  maskAllText: true,       // Replace text with asterisks
  blockAllMedia: true,     // Block images and videos
});
```

## Step 8: Source Maps (Optional)

Upload source maps so stack traces show original file names and line numbers instead of minified code.

Add to your `.env`:

```bash
TRACEKIT_AUTH_TOKEN=your_auth_token_here
```

After building your application, upload source maps:

```bash
tracekit sourcemaps upload --release=1.0.0 ./dist
```

**Build integration** — add to your build script in `package.json`:

```json
{
  "scripts": {
    "build": "vite build",
    "postbuild": "tracekit sourcemaps upload --release=$npm_package_version ./dist"
  }
}
```

Ensure the `release` value matches the `release` option in your `init()` config. The TraceKit backend uses this to map errors to the correct source maps.

## Step 9: Verification

After integrating, verify errors and traces are flowing:

1. **Start your application** with the API key env var set.
2. **Trigger a test error** — add this temporarily to your code:
   ```typescript
   import { captureException } from '@tracekit/browser';
   setTimeout(() => {
     captureException(new Error('TraceKit test error'));
   }, 2000);
   ```
3. **Open** `https://app.tracekit.dev/traces`.
4. **Confirm** the test error and your service name appear within 30-60 seconds.
5. **Remove the test error code** once verified.

If errors do not appear, see Troubleshooting below.

## Complete Working Example

A full `tracekit.ts` init file with all features wired together:

```typescript
// src/tracekit.ts
import {
  init,
  captureException,
  captureMessage,
  setUser,
  setTag,
  setExtra,
  addBreadcrumb,
  getClient,
} from '@tracekit/browser';
import { replayIntegration } from '@tracekit/replay';

// --- Session Replay ---
const replay = replayIntegration({
  sessionSampleRate: 0.1,
  errorSampleRate: 1.0,
  maskAllText: true,
  blockAllMedia: true,
});

// --- SDK Init (must run before any app code) ---
init({
  apiKey: import.meta.env.VITE_TRACEKIT_API_KEY,
  serviceName: 'my-frontend-app',
  release: import.meta.env.VITE_APP_VERSION || '0.0.0',
  environment: import.meta.env.MODE,
  endpoint: 'https://app.tracekit.dev/v1/traces',
  enableCodeMonitoring: true,
  tracePropagationTargets: [
    'https://api.myapp.com',
    /^https:\/\/.*\.myapp\.com/,
  ],
  beforeSend: (event) => {
    // Drop noisy browser errors
    if (event.message?.includes('ResizeObserver')) return null;
    if (event.stackTrace?.includes('chrome-extension://')) return null;
    return event;
  },
  addons: [replay],
});

// --- Exported helpers for use throughout the app ---
export { captureException, captureMessage, setUser, setTag, setExtra, addBreadcrumb, getClient };
```

Usage in application code:

```typescript
// src/main.ts
import './tracekit'; // MUST be first import

import { setUser, captureException, addBreadcrumb } from './tracekit';

// After login
function onLogin(user: { id: string; email: string; name: string }) {
  setUser({ id: user.id, email: user.email, username: user.name });
}

// In business logic
async function loadDashboard() {
  addBreadcrumb({
    type: 'navigation',
    category: 'route',
    message: 'Navigated to dashboard',
    level: 'info',
  });

  try {
    const data = await fetch('/api/dashboard').then(r => r.json());
    renderDashboard(data);
  } catch (err) {
    captureException(err as Error, { component: 'Dashboard' });
    showErrorFallback();
  }
}
```

## Troubleshooting

### Errors not appearing in dashboard

- **Check API key:** Ensure the env var is set and accessible. Enable `debug: true` in init config to see SDK logs in the browser console.
- **Check CSP headers:** Your Content Security Policy must allow connections to `https://app.tracekit.dev`. Add `connect-src https://app.tracekit.dev` to your CSP header.
- **Check init order:** `init()` must be called before any other application code. If init happens after errors, they are not captured.
- **Check `sampleRate`:** A value below `1.0` drops a percentage of events. Set to `1.0` during testing.
- **Check `beforeSend`:** Your filter callback might be returning `null` for the test error.

### Source maps not resolving

- **Check release version:** The `release` value in `init()` must exactly match the `--release` flag used during upload.
- **Check upload succeeded:** Run `tracekit sourcemaps list --release=1.0.0` to verify maps are uploaded.
- **Check build output:** Source maps must exist in the upload directory (`.js.map` files alongside `.js` files).

### Distributed tracing not connecting

- **Check `tracePropagationTargets`:** URLs must match your backend endpoints. Use the browser Network tab to verify `traceparent` headers are being sent.
- **Check CORS:** Your backend must accept `traceparent` and `tracestate` headers in `Access-Control-Allow-Headers`.
- **Check backend SDK:** Your backend must be instrumented with a TraceKit SDK that reads the `traceparent` header.

### Session replay not recording

- **Check sampling rate:** `sessionSampleRate: 0.1` means only 10% of sessions are recorded. Set to `1.0` during testing.
- **Check `@tracekit/replay` is installed:** Session replay requires a separate package.
- **Check privacy settings:** `maskAllText: true` and `blockAllMedia: true` are recommended defaults. Adjust if replay content appears blank.

## Next Steps

Once your browser app is traced, consider:
- **Code Monitoring** — Set live breakpoints and capture snapshots in production without redeploying (already enabled via `enableCodeMonitoring: true`)
- **Session Replay** — Visual debugging with full session recordings (see `tracekit-session-replay` skill)
- **Source Maps** — Readable stack traces with original source code (see `tracekit-source-maps` skill)
- **Backend Tracing** — Add `@tracekit/node-apm` or another backend SDK for end-to-end distributed traces (see `tracekit-node-sdk`, `tracekit-go-sdk`, and other backend skills)

## References

- Browser SDK docs: `https://app.tracekit.dev/docs/frontend/browser-sdk`
- TraceKit docs root: `https://app.tracekit.dev/docs`
- Dashboard: `https://app.tracekit.dev`
- Quick start: `https://app.tracekit.dev/docs/quickstart`
