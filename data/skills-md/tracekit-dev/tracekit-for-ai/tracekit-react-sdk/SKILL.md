---
name: tracekit-react-sdk
description: Sets up TraceKit APM in React applications with error boundaries, component performance tracking, and distributed tracing. Use when the user asks to add TraceKit, add observability, instrument a React app, or configure APM in a React/TypeScript project.
---

# TraceKit React SDK Setup

## When To Use

Use this skill when the user asks to:
- Add TraceKit to a React application
- Add observability or APM to a React app
- Instrument a React project with error tracking or distributed tracing
- Configure TraceKit API keys in a React project
- Set up error boundaries with automatic error reporting
- Add performance monitoring to a React app
- Debug production React apps with live breakpoints

**Not React?** If the user is using Vue, Angular, Next.js, Nuxt, or a plain JS/TS project without a framework, use the corresponding skill instead.

## Non-Negotiable Rules

1. **Never hardcode API keys** in code. Always use environment variables or build-time injection (e.g., `import.meta.env.VITE_TRACEKIT_API_KEY`).
2. **Always include a verification step** confirming errors and traces appear in `https://app.tracekit.dev/traces`.
3. **Always enable code monitoring** (`enableCodeMonitoring: true`) — it is TraceKit's differentiator for live debugging.
4. **Always init TraceKit before any other application code** — the provider must wrap the entire app at the root level.

## Detection

Before applying this skill, detect the project type:

1. **Check for `package.json`** — confirms this is a JavaScript/TypeScript project.
2. **Check for `react-dom`** in `dependencies` or `devDependencies` — confirms this is a React project.
3. **Check for Next.js:** If `next` is in dependencies, use the `tracekit-nextjs-sdk` skill instead.
4. **Detect build tool** for env var pattern:
   - CRA (`react-scripts` in dependencies) => `REACT_APP_TRACEKIT_API_KEY` via `process.env`
   - Vite (`vite` in devDependencies) => `VITE_TRACEKIT_API_KEY` via `import.meta.env`
5. **Check for TypeScript:** `tsconfig.json` presence means use `.tsx` snippets.
6. **Only ask the user** if `react-dom` is not found but React-like code exists.

## Step 1: Environment Setup

Set the `TRACEKIT_API_KEY` environment variable. This is the only required secret.

Add to your `.env` file:

**Vite projects:**
```bash
VITE_TRACEKIT_API_KEY=ctxio_your_api_key_here
```

**Create React App projects:**
```bash
REACT_APP_TRACEKIT_API_KEY=ctxio_your_api_key_here
```

Where to get your API key:
1. Log in to [TraceKit](https://app.tracekit.dev)
2. Go to **API Keys** page
3. Generate a new key (starts with `ctxio_`)

Do **not** commit real API keys. Use `.env` files, deployment secret managers, or CI variables.

## Step 2: Install SDK

```bash
npm install @tracekit/react
```

Or with Yarn:

```bash
yarn add @tracekit/react
```

This installs the TraceKit React SDK which wraps `@tracekit/browser` with React-specific integrations: error boundaries, provider pattern, performance hooks, and router breadcrumbs. You only need this one package.

## Step 3: Initialize TraceKit Provider

Wrap your app root in `<TraceKitProvider>`. This initializes the SDK and provides context to all child components.

### Vite + React

```tsx
// src/main.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { TraceKitProvider } from '@tracekit/react';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <TraceKitProvider
      config={{
        apiKey: import.meta.env.VITE_TRACEKIT_API_KEY,
        serviceName: 'my-react-app',
        endpoint: 'https://app.tracekit.dev/v1/traces',
        enableCodeMonitoring: true,
        release: import.meta.env.VITE_APP_VERSION || '0.0.0',
        environment: import.meta.env.MODE,
      }}
    >
      <App />
    </TraceKitProvider>
  </React.StrictMode>
);
```

### Create React App

```tsx
// src/index.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { TraceKitProvider } from '@tracekit/react';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <TraceKitProvider
      config={{
        apiKey: process.env.REACT_APP_TRACEKIT_API_KEY!,
        serviceName: 'my-react-app',
        endpoint: 'https://app.tracekit.dev/v1/traces',
        enableCodeMonitoring: true,
        release: process.env.REACT_APP_VERSION || '0.0.0',
        environment: process.env.NODE_ENV,
      }}
    >
      <App />
    </TraceKitProvider>
  </React.StrictMode>
);
```

**Key points:**
- `TraceKitProvider` must be the outermost wrapper (before Router, Redux, etc.)
- The provider calls `init()` internally — do not call `init()` separately
- `serviceName` should match your app's logical name (e.g., `"dashboard"`, `"checkout"`)

## Step 4: Error Boundary

Wrap component trees with `<TraceKitErrorBoundary>` to capture React render errors. The error boundary automatically calls `captureException` with component stack traces.

```tsx
import { TraceKitErrorBoundary } from '@tracekit/react';

function ErrorFallback({ error, resetError }: { error: Error; resetError: () => void }) {
  return (
    <div role="alert" style={{ padding: '2rem', textAlign: 'center' }}>
      <h2>Something went wrong</h2>
      <p style={{ color: '#666' }}>{error.message}</p>
      <button
        onClick={resetError}
        style={{ marginTop: '1rem', padding: '0.5rem 1rem', cursor: 'pointer' }}
      >
        Try again
      </button>
    </div>
  );
}

// Wrap your app or specific route sections
function App() {
  return (
    <TraceKitErrorBoundary fallback={(error, _componentStack, resetError) => (
      <ErrorFallback error={error} resetError={resetError} />
    )}>
      <Dashboard />
    </TraceKitErrorBoundary>
  );
}
```

**Nesting error boundaries** — wrap different sections for granular recovery:

```tsx
function App() {
  return (
    <div>
      <Header /> {/* Errors here bubble up to root */}
      <TraceKitErrorBoundary fallback={<p>Dashboard failed to load</p>}>
        <Dashboard />
      </TraceKitErrorBoundary>
      <TraceKitErrorBoundary fallback={<p>Sidebar failed to load</p>}>
        <Sidebar />
      </TraceKitErrorBoundary>
    </div>
  );
}
```

**Important:** React error boundaries only catch errors during rendering, lifecycle methods, and constructors. They do NOT catch errors in event handlers, async code, or setTimeout. Use `captureException` for those:

```tsx
import { captureException } from '@tracekit/react';

function SubmitButton() {
  const handleClick = async () => {
    try {
      await submitForm();
    } catch (err) {
      captureException(err as Error, { component: 'SubmitButton' });
    }
  };
  return <button onClick={handleClick}>Submit</button>;
}
```

## Step 5: Custom Performance Spans

Use the `useTraceKitSpan` hook to measure component-level operations:

```tsx
import { useTraceKitSpan } from '@tracekit/react';

function Dashboard() {
  const { startSpan } = useTraceKitSpan();

  useEffect(() => {
    const span = startSpan('load-dashboard-data');
    fetchDashboardData()
      .then((data) => {
        setData(data);
        span.end();
      })
      .catch((err) => {
        captureException(err as Error);
        span.end();
      });
  }, []);

  return <div>{/* dashboard content */}</div>;
}
```

**Measuring route transitions:**

```tsx
import { useTraceKitSpan } from '@tracekit/react';
import { useLocation } from 'react-router-dom';

function RouteTracker() {
  const location = useLocation();
  const { startSpan } = useTraceKitSpan();

  useEffect(() => {
    const span = startSpan('route-transition', {
      'route.path': location.pathname,
    });
    // End span after page renders
    requestAnimationFrame(() => span.end());
  }, [location.pathname]);

  return null;
}
```

## Step 6: Distributed Tracing

Configure `tracePropagationTargets` in the provider config to attach trace headers to outbound fetch/XHR requests. This connects frontend spans to backend traces.

```tsx
<TraceKitProvider
  config={{
    apiKey: import.meta.env.VITE_TRACEKIT_API_KEY,
    serviceName: 'my-react-app',
    endpoint: 'https://app.tracekit.dev/v1/traces',
    enableCodeMonitoring: true,
    tracePropagationTargets: [
      'https://api.myapp.com',
      'https://auth.myapp.com',
      /^https:\/\/.*\.myapp\.com/,
    ],
  }}
>
  <App />
</TraceKitProvider>
```

**How it works:**
1. Fetch/XHR requests to matching URLs receive a `traceparent` header
2. Your backend SDK reads this header and links the backend span to the frontend trace
3. The full request lifecycle appears as a single trace in the TraceKit dashboard

**Important:** Your backend CORS configuration must accept the `traceparent` and `tracestate` headers.

## Step 7: Session Replay (Optional)

Enable session replay via the provider config to record user sessions for visual debugging:

```tsx
import { replayIntegration } from '@tracekit/replay';

const replay = replayIntegration({
  sessionSampleRate: 0.1,
  errorSampleRate: 1.0,
  maskAllText: true,
  blockAllMedia: true,
});

<TraceKitProvider
  config={{
    apiKey: import.meta.env.VITE_TRACEKIT_API_KEY,
    serviceName: 'my-react-app',
    endpoint: 'https://app.tracekit.dev/v1/traces',
    enableCodeMonitoring: true,
    addons: [replay],
  }}
>
  <App />
</TraceKitProvider>
```

## Step 8: Source Maps (Optional)

Upload source maps so stack traces show original file names and line numbers.

Add to your `.env`:

```bash
TRACEKIT_AUTH_TOKEN=your_auth_token_here
```

After building:

```bash
tracekit sourcemaps upload --release=1.0.0 ./build
```

**Build integration** — add to `package.json`:

```json
{
  "scripts": {
    "build": "vite build",
    "postbuild": "tracekit sourcemaps upload --release=$npm_package_version ./dist"
  }
}
```

Ensure the `release` value matches the `release` option in your provider config.

## Step 9: Verification

After integrating, verify errors and traces are flowing:

1. **Start your application** with the API key env var set.
2. **Trigger a test error** — add this temporarily inside a component:
   ```tsx
   import { captureException } from '@tracekit/react';

   function TestError() {
     useEffect(() => {
       captureException(new Error('TraceKit React test error'));
     }, []);
     return null;
   }
   ```
3. **Open** `https://app.tracekit.dev/traces`.
4. **Confirm** the test error and your service name appear within 30-60 seconds.
5. **Remove the test component** once verified.

To test the ErrorBoundary:

```tsx
function BuggyComponent() {
  throw new Error('ErrorBoundary test');
  return null;
}

// Wrap with TraceKitErrorBoundary and render — should show fallback UI
// and report error to dashboard
```

## Complete Working Example

Full `App.tsx` with TraceKitProvider, ErrorBoundary, router wrapping, and all features:

```tsx
// src/App.tsx
import React, { useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import {
  TraceKitProvider,
  TraceKitErrorBoundary,
  useTraceKitSpan,
  captureException,
  setUser,
  setTag,
} from '@tracekit/react';
import { replayIntegration } from '@tracekit/replay';

// --- Session Replay ---
const replay = replayIntegration({
  sessionSampleRate: 0.1,
  errorSampleRate: 1.0,
  maskAllText: true,
  blockAllMedia: true,
});

// --- Error Fallback ---
function ErrorFallback({ error, resetError }: { error: Error; resetError: () => void }) {
  return (
    <div role="alert" style={{ padding: '2rem', textAlign: 'center' }}>
      <h2>Something went wrong</h2>
      <p style={{ color: '#666' }}>{error.message}</p>
      <button onClick={resetError} style={{ marginTop: '1rem', padding: '0.5rem 1rem' }}>
        Try again
      </button>
    </div>
  );
}

// --- Dashboard with performance span ---
function Dashboard() {
  const [data, setData] = useState(null);
  const { startSpan } = useTraceKitSpan();

  useEffect(() => {
    const span = startSpan('load-dashboard');
    fetch('/api/dashboard')
      .then((r) => r.json())
      .then((d) => { setData(d); span.end(); })
      .catch((err) => { captureException(err as Error); span.end(); });
  }, []);

  return <div>{data ? JSON.stringify(data) : 'Loading...'}</div>;
}

// --- App Root ---
export default function App() {
  useEffect(() => {
    // Set user context after auth
    setUser({ id: 'user-123', email: 'alice@example.com' });
    setTag('plan', 'pro');
  }, []);

  return (
    <TraceKitProvider
      config={{
        apiKey: import.meta.env.VITE_TRACEKIT_API_KEY,
        serviceName: 'my-react-app',
        release: import.meta.env.VITE_APP_VERSION || '0.0.0',
        environment: import.meta.env.MODE,
        endpoint: 'https://app.tracekit.dev/v1/traces',
        enableCodeMonitoring: true,
        tracePropagationTargets: [
          'https://api.myapp.com',
          /^https:\/\/.*\.myapp\.com/,
        ],
        addons: [replay],
      }}
    >
      <BrowserRouter>
        <nav>
          <Link to="/">Home</Link> | <Link to="/dashboard">Dashboard</Link>
        </nav>
        <TraceKitErrorBoundary
          fallback={(error, _stack, resetError) => (
            <ErrorFallback error={error} resetError={resetError} />
          )}
        >
          <Routes>
            <Route path="/" element={<h1>Home</h1>} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </TraceKitErrorBoundary>
      </BrowserRouter>
    </TraceKitProvider>
  );
}
```

## Troubleshooting

### ErrorBoundary not catching errors

- **Event handlers:** Error boundaries only catch errors during rendering. Errors in `onClick`, `onChange`, etc. must use `try/catch` with `captureException`.
- **Async code:** Errors in `async` functions, `setTimeout`, or Promises are not caught by error boundaries. Use `captureException` in catch blocks.
- **Server components:** Error boundaries do not work in React Server Components. Use `error.tsx` files in Next.js App Router instead.

### Traces not connecting to backend

- **Check `tracePropagationTargets`:** URLs must match your API endpoints. Verify `traceparent` headers appear in the browser Network tab.
- **Check CORS:** Your backend must accept `traceparent` and `tracestate` in `Access-Control-Allow-Headers`.
- **Check backend SDK:** The backend must be instrumented with a TraceKit SDK that reads `traceparent`.

### HMR double-init in development

- **React Strict Mode:** In development, Strict Mode double-renders components. The `TraceKitProvider` handles this gracefully by checking for existing initialization.
- **Vite HMR:** If you see duplicate init warnings during hot reload, this is normal in development and does not affect production.

### Source maps not resolving

- **Check release version:** The `release` in provider config must match the `--release` flag during upload.
- **CRA output:** Upload from `./build`, not `./dist`.
- **Vite output:** Upload from `./dist`.

## Next Steps

Once your React app is traced, consider:
- **Code Monitoring** — Set live breakpoints and capture snapshots in production without redeploying (already enabled via `enableCodeMonitoring: true`)
- **Session Replay** — Visual debugging with full session recordings (see `tracekit-session-replay` skill)
- **Source Maps** — Readable stack traces with original source code (see `tracekit-source-maps` skill)
- **Backend Tracing** — Add `@tracekit/node-apm` or another backend SDK for end-to-end distributed traces (see `tracekit-node-sdk`, `tracekit-go-sdk`, and other backend skills)
- **Browser SDK** — For advanced browser-level configuration, see the `tracekit-browser-sdk` skill

## References

- React SDK docs: `https://app.tracekit.dev/docs/frontend/frameworks/react`
- TraceKit docs root: `https://app.tracekit.dev/docs`
- Dashboard: `https://app.tracekit.dev`
- Quick start: `https://app.tracekit.dev/docs/quickstart`
