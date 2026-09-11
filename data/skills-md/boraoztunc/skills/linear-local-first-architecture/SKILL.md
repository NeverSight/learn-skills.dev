---
name: linear-local-first-architecture
description: "Use when building a web app that must feel instant, when users complain about spinners or perceived slowness despite acceptable latency, or when designing a local-first sync architecture with optimistic updates."
---

## When to use this skill

- You're building a productivity tool where perceived speed is critical to user experience
- Users report the app "feels slow" despite reasonable network latency
- You need to eliminate loading spinners and skeleton states from user workflows
- You're architecting a local-first application with offline capabilities
- You want to implement optimistic updates that feel instant
- You're designing a keyboard-first interface for power users

## Core principles

1. **The network is the bottleneck—eliminate it wherever possible.** Every network request costs hundreds of milliseconds; the best optimization is to avoid the request entirely by reading from local state.

2. **Treat the browser as the database for each user.** Store the full workspace in IndexedDB and hydrate into an in-memory observable graph; the UI reads from local state, not the server.

3. **Mutations apply locally first, sync asynchronously.** Update the local observable immediately so the UI re-renders synchronously, then queue the transaction for background sync to the server.

4. **Render first, authenticate second.** If local data exists, render it immediately and verify the session in the background; only redirect to login if the server rejects.

5. **Ship less code in more pieces.** Aggressive code splitting, modern-only targets, and per-package vendor chunks reduce initial payload and improve cache granularity.

6. **Animate only composited properties.** Restrict animations to `transform` and `opacity` to keep work on the GPU; never animate layout-triggering properties like `width`, `height`, or `margin`.

## Tactics

### Set up local-first data architecture

Store the workspace in IndexedDB and hydrate into an in-memory observable store (MobX in Linear's case). The UI queries the local store, not the server.

```typescript
// A traditional web app updating the server
async function updateIssue({ issue }) {
  showSpinner();
  const response = await fetch(`/api/issues/${issue.id}`, {
    method: "PATCH",
    body: JSON.stringify({ title: issue.title }),
  });
  const updated = await response.json();
  setIssue(updated)
  hideSpinner();
}

// vs Linear
issue.title = "Faster app launch";
issue.save();
```

The first line updates an in-memory datastore (MobX observable). The second line queues a transaction that the sync engine batches and flushes to the server. The UI re-renders synchronously off the local update—no spinners, no waiting.

### Implement optimistic updates with standard libraries

If you're not building a custom sync engine, use libraries like Tanstack Query or SWR with optimistic updates:

```typescript
// optimistic mutation with SWR
mutate(
  `/api/issues/${issue.id}`,
  { ...issue, title: "Faster app launch" },
  false
);

// vs Linear
issue.title = "Faster app launch";
issue.save();
```

The key: UI responsiveness should not depend on network latency. Users perceive speed based on how quickly the interface reacts, not how quickly the server responds.

### Reduce bundle size with modern-only builds

Target only modern browsers, drop legacy polyfills, and use aggressive code splitting:

```typescript
// vite.config.ts (reconstruction; matches observed chunk graph)
export default defineConfig({
  plugins: [react()],
  build: {
    target: "esnext",            // no legacy syntax, no polyfills
    cssMinify: "lightningcss",
    modulePreload: { polyfill: false },
    rollupOptions: {
      output: {
        // One chunk per npm package > ~3 KB. Cache invalidation
        // becomes per-library instead of per-app-revision.
        manualChunks(id) {
          if (id.includes("node_modules")) {
            const pkg = id.match(/node_modules\/([^/]+)/)?.[1];
            if (pkg) return `vendor-${pkg}`;
          }
        },
      },
    },
  },
});
```

Split every npm package into its own chunk. A traditional `vendor.js` invalidates the entire dependency graph on any bump; per-package chunking makes cache invalidation fine-grained.

### Preload critical chunks in parallel

Eliminate the waterfall of fetch → parse → fetch imports by declaring all critical chunks in `<head>`:

```html
<script type=module crossorigin
  src="https://static.linear.app/client/assets/html.2_JBQs3Q.js"></script>
<link rel=modulepreload crossorigin
  href="https://static.linear.app/client/assets/vendor-mobx.Crhy2qQc.js">
<link rel=modulepreload crossorigin
  href="https://static.linear.app/client/assets/SyncWebSocket.Djw6l_Op.js">
<link rel=modulepreload crossorigin
  href="https://static.linear.app/client/assets/DatabaseManager.DKssGAN8.js">
<!-- ...around many more -->
```

The `crossorigin` attribute on each preload matches the `crossorigin` on the entry script, so the browser reuses the cached fetch. The cold-load timeline collapses from a sequential waterfall into a single parallel batch.

### Precache remaining assets with a service worker

After the first page load, use a service worker to precache route-level chunks in the background:

```javascript
// The service worker has a precache manifest baked into its source,
// around 1,200 hashed assets covering route chunks, icons, and fonts.
// It pulls them down lazily after the first page load.
```

Within seconds of hitting the login screen, the full app sits in cache. Subsequent navigations skip the network entirely; the service worker answers directly from cache. Combined with IndexedDB, the app works offline.

### Inline critical CSS and boot logic

Avoid an external stylesheet fetch by inlining just enough CSS to paint the loading state:

```css
<style>
  :root {
    --bg-color: #f5f5f5;
    --bg-base-color: #fcfcfd;
    --bg-border-color: #e0e0e0;
    --sidebar-width: 244px;
  }
  html { background: var(--bg-color); height: 100%; }
  body { font-family: "Inter Variable", Arial, Helvetica, sans-serif; }

  #appBorders {
    border: 1px solid var(--bg-border-color);
    background: var(--bg-base-color);
    margin: 8px 8px 8px var(--sidebar-width);
    border-radius: 12px;
  }

  #logo { transform: translateZ(0); }

  @keyframes logoBackgroundPulse {
    0%   { opacity: 0; transform: scale(0.8); }
    70%  { opacity: 1; }
    100% { opacity: 0; transform: scale(1.0); }
  }
</style>
<script>performance.mark("appStart");</script>
```

Inline JavaScript restores last-known shell tokens (sidebar bg, width, dark mode) before paint:

```javascript
<script>
// Electron context — lets CSS branch on native chrome.
if (navigator.userAgent.includes("Electron") && navigator.userAgent.includes("Linear")) document.documentElement.classList.add("electron");

// No local store → no workspace data → render the auth layout.
if (localStorage.getItem("ApplicationStore") === null) document.documentElement.classList.add("logged-out");

// Restore last-known shell tokens (sidebar bg, width, dark mode) before paint.
const c = JSON.parse(localStorage.getItem("splashScreenConfig") || "{}");
if (c.bgSidebarColor) document.documentElement.style.setProperty("--bg-sidebar-color", c.bgSidebarColor);
if (c.sidebarWidth) document.documentElement.style.setProperty("--sidebar-width", c.sidebarWidth + "px");
if (c.darkMode) document.documentElement.classList.add("dark");

// Compact sidebar to a sliver when the user opens links in the desktop app.
if (JSON.parse(localStorage.getItem("userSettings") || "{}").openLinksInDesktop) document.documentElement.style.setProperty("--sidebar-width", "8px");

</script>
```

By the time the first JavaScript bundle arrives, the loading screen is already correctly themed, sized, and positioned.

### Optimize font loading

Preload variable fonts with correct CORS mode to avoid double-fetching:

```html
<!-- in <head> of index.html -->
<link rel="preload"
      href="https://static.linear.app/fonts/InterVariable.woff2?v=4.1"
      as="font" type="font/woff2" crossorigin="anonymous">
<link rel="preconnect" href="https://static.linear.app" crossorigin>
```

```css
@font-face {
  font-family: "Inter Variable";
  font-weight: 100 900;
  font-display: swap;
  src: url(https://static.linear.app/fonts/InterVariable.woff2?v=4.1)
       format("woff2");
}
/* Italic and Berkeley Mono follow the same shape, single woff2 each. */
```

Variable fonts cover the full 100–900 weight axis in a single woff2. `font-display: swap` renders the fallback stack immediately and swaps to Inter when it loads. `crossorigin="anonymous"` on the preload makes the browser reuse the cached font when CSS references it.

### Assume authentication, verify in background

Instead of blocking on session validation, check if local data exists:

```javascript
if (localStorage.getItem("ApplicationStore") === null) {
  document.documentElement.classList.add("logged-out");
}
```

If `ApplicationStore` exists, the user has used the app before and their workspace is in IndexedDB. Render it immediately. The actual session token sits in a cookie; let the next request (WebSocket handshake, sync delta, any HTTP call) fail with a 401 if the session is stale, then redirect to login.

The flow is "do we have anything to show you," not "do you have a valid session."

### Use granular observables for surgical re-renders

Make every property on every model its own observable. When a delta arrives from the server, write to the corresponding observable. The framework (MobX) knows exactly which components depend on which fields and re-renders only those components.

A change that updates one field of one issue re-renders exactly the components that read that field—not the parent list, not the sidebar, one cell. A 50-issue update is 50 cell re-renders, not a list re-render.

### Design for keyboard-first interaction

Every common action should have a shortcut. Single letters edit the focused issue. Two-letter combos navigate. Modifiers act globally. Make shortcuts visible everywhere in the UI.

Implement a global command palette (`⌘ k`) that searches over actions, issues, projects, labels, status changes, navigation, settings. Search runs against the local MobX object pool—no server request, instant results.

### Animate only composited properties

Browsers have three tiers of property changes:

- **Composited properties** (`transform`, `opacity`): GPU-accelerated, independent of main thread
- **Paint-triggering properties** (`color`, `background-color`, `border-color`, `fill`): skip layout but redraw pixels
- **Layout-triggering properties** (`width`, `height`, `top`, `left`, `margin`, `padding`): force recomputation of every subsequent element

Never animate layout-triggering properties:

```css
/* What Linear does */
.row:hover {
  background-color: var(--color-bg-hover);
  transition: background-color 0.12s;
}
.icon-arrow {
  transform: translateX(0);
  transition: transform 0.15s;
}

/* What you'd write if you didn't know better */
.row:hover {
  margin-left: 2px;       /* triggers layout for every row beneath */
  transition: all 0.2s;   /* and now you're animating margin */
}
```

### Keep animation durations short

Default to shorter transitions than industry norms:

```css
/* variables form Linear's stylesheet */

--speed-highlightFadeIn: 0s;
--speed-highlightFadeOut: .15s;
--speed-quickTransition: .1s;
--speed-regularTransition: .25s;
--speed-slowTransition: .35s;
```

Use asymmetric timing: appear instantly when summoned, fade out over 150ms when dismissed. This makes the interface feel responsive to user intent.

## Anti-patterns

❌ **Don't wait for network requests before updating the UI.** Apply mutations locally first, sync in the background, and rollback only if the server rejects.

❌ **Don't animate layout-triggering properties** like `width`, `height`, `margin`, `padding`, `top`, or `left`. Stick to `transform` and `opacity`.

❌ **Don't block initial render on authentication.** If local data exists, render it immediately and verify the session asynchronously.

❌ **Don't bundle all vendor code into a single chunk.** Split each npm package into its own chunk so cache invalidation is per-library, not per-app-revision.

❌ **Don't use long animation durations (>250ms) for frequent interactions.** Shorter transitions make the app feel faster; reserve longer durations for infrequent, high-impact moments.

❌ **Don't fetch data on every navigation if it's already local.** Hydrate from IndexedDB on boot, lazy-load heavy tables on demand, and treat the server as a sync target, not a source of truth for the UI.

## Source

[How's Linear so fast? A technical breakdown](https://performance.dev/how-is-linear-so-fast-a-technical-breakdown)
