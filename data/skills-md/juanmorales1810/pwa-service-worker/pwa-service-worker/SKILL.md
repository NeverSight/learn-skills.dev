---
name: pwa-service-worker
description: Implement, debug, and optimize Progressive Web Apps in Next.js (App Router) with service workers, push notifications, offline support, caching strategies, and installability. Use when requests mention Next.js PWA setup, app/manifest.ts, public/sw.js, navigator.serviceWorker.register, updateViaCache, cache strategies (Cache First, Network First, Stale-While-Revalidate), offline fallback pages, App Shell pattern, precaching, Background Sync, web-push with Server Actions, VAPID keys, service worker lifecycle (skipWaiting, clients.claim), update notification UX, HTTPS local testing, security headers in next.config.js, Serwist/Workbox integration, maskable icons, iOS PWA quirks, or Lighthouse PWA issues in Next.js. Also use when users troubleshoot stale caches, registration failures, scope conflicts, or cache versioning problems.
---

# Service Worker PWA (Next.js)

## Overview

Use this skill to build or fix a production-ready PWA in Next.js App Router with explicit service worker lifecycle, robust caching strategies, offline support, push notifications, and safe deployment behavior.

## Workflow

1. Inspect existing Next.js PWA files and routing mode.
2. Implement manifest, icon set, and platform-specific meta tags.
3. Implement service worker registration, lifecycle management, and `public/sw.js`.
4. Choose and implement caching strategies based on resource types.
5. Implement offline fallback and, optionally, Background Sync.
6. Implement push subscriptions with Server Actions when needed.
7. Add update notification UX so users get new versions.
8. Secure service worker delivery and validate in HTTPS.
9. Debug and troubleshoot with DevTools.

---

## 1) Inspect Project State

Check these paths first:

- `app/manifest.ts` or `app/manifest.json`
- `app/layout.tsx` for `<meta>` tags (viewport, theme-color, apple-touch-icon)
- `public/sw.js`
- Client component that registers the service worker
- `app/actions.ts` (if push notifications are required)
- `next.config.js` or `next.config.ts` for headers

If `pages/` and `app/` coexist, keep changes isolated to App Router conventions unless the user asks for Pages Router support.

---

## 2) Implement Manifest and Installability

Prefer `app/manifest.ts` (MetadataRoute) for typed configuration.

### Minimum fields

- `name`, `short_name`, `description`
- `start_url`, `display` (use `standalone` for app feel, `minimal-ui` when you need the back button)
- `background_color`, `theme_color`
- `icons` array (see icon guidance below)

### Icons

Provide at minimum:

- `192×192` PNG — used as the home-screen icon
- `512×512` PNG — used as the splash-screen icon
- `512×512` PNG with `"purpose": "maskable"` — for Android adaptive icons (the safe zone is the inner 80% circle, so center the important art)

Optionally add `apple-touch-icon` in `app/layout.tsx` `<head>` for iOS:

```tsx
<link rel="apple-touch-icon" href="/apple-touch-icon-180.png" />
```

### iOS/Safari considerations

iOS has specific PWA limitations that affect real users:

- `beforeinstallprompt` does not fire — install is only via Safari's "Add to Home Screen" menu. Do not build install banners that depend on this event on iOS.
- Push notifications require iOS 16.4+ and the user must add the app to the home screen first.
- `standalone` mode on iOS has no back gesture by default — ensure in-app navigation is always available.
- Splash screens on iOS are generated from `apple-touch-startup-image` media queries, not from manifest icons. If the user requests iOS splash screens, provide the relevant `<link>` tags.
- Persistent storage quotas on iOS are lower (~50 MB default) and get evicted after ~7 days of inactivity.

### Install UX

If an install prompt is requested, use progressive enhancement: listen for `beforeinstallprompt` to show a custom install button on Android/Desktop, and fall back to instructions text for iOS. Never block the app waiting for this event.

---

## 3) Implement Service Worker in Next.js

### Registration

Register from a client component with `scope: '/'` and `updateViaCache: 'none'`.

`updateViaCache: 'none'` matters because browsers can cache `sw.js` itself. Setting this to `'none'` guarantees the browser always fetches `sw.js` fresh from the network on every navigation, so new deployments of the service worker are detected immediately.

### Lifecycle: install → waiting → activate

Understanding the lifecycle prevents subtle bugs:

1. **install** — The new SW downloads and fires `install`. This is the right time to precache static assets.
2. **waiting** — If there's already an active SW controlling the page, the new one enters `waiting` state. It will not activate until all tabs using the old SW are closed.
3. **activate** — The new SW takes control. This is the right time to clean up old caches.

#### `skipWaiting()` and `clients.claim()` — when to use and when not to

- `self.skipWaiting()` makes the new SW skip the waiting state and activate immediately, even while other tabs still run the old version. This is convenient but can cause subtle issues: the new SW might handle fetch events from pages that were loaded with assets from the old SW. Use it when your SW only handles push/notification and doesn't do complex caching. Avoid it (or pair it with a page reload) when the SW manages cached assets that change between versions.
- `self.clients.claim()` in the `activate` handler makes the newly activated SW take control of already-open pages immediately instead of waiting for the next navigation. Useful for first-time registration so the user doesn't need to reload. For updates, combine with a "new version available" reload prompt.

### Cache Versioning

Name caches with a version prefix so that old entries can be cleaned up on activate:

```js
const CACHE_VERSION = "v2";
const CACHE_NAME = `app-cache-${CACHE_VERSION}`;
```

In the `activate` handler, delete any caches that don't match the current version. This avoids unbounded disk usage and stale assets. See the snippets reference for the complete pattern.

---

## 4) Caching Strategies

Choose the right strategy per resource type. Using the wrong strategy causes either stale content (bad UX) or unnecessary network requests (bad performance).

### Cache First (Cache, falling back to Network)

Best for: versioned static assets (`/_next/static/`, fonts, images with hashed filenames).
Why: these assets are immutable once deployed — serving from cache is always correct and fast.

### Network First (Network, falling back to Cache)

Best for: HTML pages, API responses that must be fresh.
Why: the user always gets the latest content when online, and still gets something useful when offline.

### Stale-While-Revalidate

Best for: assets that should be fast but eventually consistent (non-critical API responses, avatar images, non-hashed CSS).
Why: serves the cached version instantly (fast) while fetching a fresh copy in the background for next time.

### Network Only

Best for: analytics pings, POST/PUT/DELETE requests, any non-idempotent operations.
Why: caching these would cause incorrect behavior (duplicate submissions, stale mutations). Never cache non-idempotent requests.

### Cache Only

Best for: explicitly precached assets during install that you know are always available.
Why: avoids network round-trips entirely for known resources.

### Recommended mapping for Next.js

| Resource pattern                 | Strategy                                                        |
| -------------------------------- | --------------------------------------------------------------- |
| `/_next/static/**`               | Cache First                                                     |
| HTML pages (`/`, `/about`, etc.) | Network First with offline fallback                             |
| API routes (`/api/**`)           | Network Only (GET can be Stale-While-Revalidate if appropriate) |
| Images in `public/`              | Cache First or Stale-While-Revalidate                           |
| Fonts                            | Cache First                                                     |
| Third-party scripts              | Network First or Stale-While-Revalidate                         |

See `references/strategies-and-snippets.md` for the full fetch handler implementation.

---

## 5) Offline Support

### Offline Fallback Page

Create `app/offline/page.tsx` with a user-friendly message. Precache `/offline` during the `install` event so it's always available. In the `fetch` handler, when a navigation request fails (both network and cache miss), respond with the cached `/offline` page.

This is the minimum offline story — the user sees a branded page instead of Chrome's dinosaur.

### App Shell Pattern

For richer offline experiences, precache the app shell (layout, navigation, critical CSS) so the structure loads instantly and only the dynamic content requires the network. In Next.js App Router, the layout is the natural app shell — precache the root layout's critical assets.

### Precaching vs Runtime Caching

- **Precaching** happens during `install`. List the URLs you know ahead of time (offline page, app shell assets, critical fonts). These are available immediately after install.
- **Runtime caching** happens on the fly during `fetch` events. Resources are cached as the user encounters them, using the strategies from section 4.

Use precaching sparingly — every precached resource adds to install time and storage. Only precache assets that are essential for the offline experience.

---

## 6) Background Sync (Optional)

When the user performs an action offline (form submission, saving data), the request fails. Background Sync retries the request automatically when connectivity returns.

Flow:

1. In the client component, detect the failed fetch and register a sync event tag.
2. In the SW, listen for the `sync` event and replay the queued request.
3. Store pending requests in IndexedDB (not localStorage, which is unavailable in service workers).

This requires the Background Sync API, which is supported in Chromium browsers but not in Safari/Firefox as of now. Provide a fallback: store the pending action and retry on next page load if sync is unavailable.

See `references/strategies-and-snippets.md` for the implementation pattern.

---

## 7) Implement Push Notifications (Optional)

When push is requested:

- Manage subscription in a client component.
- Use Server Actions (`app/actions.ts`) with `web-push` to send notifications.
- Require env vars:
    - `NEXT_PUBLIC_VAPID_PUBLIC_KEY`
    - `VAPID_PRIVATE_KEY`

### Permission UX

Never call `Notification.requestPermission()` on page load — this results in high denial rates because the user has no context for why they should allow notifications. Instead:

1. Show a custom in-app prompt explaining the value of notifications.
2. Only call `requestPermission()` after the user clicks "Enable notifications" in your UI.
3. Handle all three states: `granted`, `denied` (show explanation, no retry possible), `default` (can ask again).

### Subscription lifecycle

- On subscribe: send the `PushSubscription` object to the server and persist it in a real datastore.
- On unsubscribe: remove the subscription server-side.
- Handle `pushsubscriptionchange` in the SW to re-subscribe automatically when the browser refreshes the subscription.

Persist subscriptions in a real datastore for production (in-memory examples are demo-only).

---

## 8) Update Notification UX

When a new service worker is deployed, users on the old version need a way to update without losing their work. The pattern:

1. In the registration component, listen for `registration.onupdatefound`.
2. When the new SW enters the `installed` state (meaning it's waiting), show a banner: "A new version is available. Reload to update."
3. When the user clicks the banner, post a message to the waiting SW telling it to `skipWaiting()`.
4. Listen for `controllerchange` and reload the page.

This is better than calling `skipWaiting()` unconditionally because it lets the user finish their current action before the page reloads. See snippets for the complete component.

---

## 9) Security, Testing, and Delivery

### Headers

Apply headers in `next.config.js`:

- Global hardening headers (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`).
- Service worker headers on `/sw.js`:
    - `Content-Type: application/javascript; charset=utf-8`
    - `Cache-Control: no-cache, no-store, must-revalidate`
    - restrictive `Content-Security-Policy`

### Validation checklist

- Run local HTTPS with `next dev --experimental-https`.
- Validate registration/scope/update in DevTools → Application → Service Workers.
- Validate manifest + installability under Application → Manifest.
- Test push subscribe/send/unsubscribe flows.
- Run Lighthouse → PWA audit and fix reliability and installability issues.
- Test the update flow: change `sw.js`, reload, verify the update banner appears.
- Test offline: go to Network tab → toggle Offline → verify fallback page or cached content.

### Debugging and Troubleshooting

Common issues and how to resolve them:

| Symptom                                      | Likely cause                                               | Fix                                                                      |
| -------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------ |
| SW never registers                           | Not serving over HTTPS (or localhost)                      | Use `next dev --experimental-https` or plain `localhost`                 |
| SW registers but doesn't control the page    | Missing `clients.claim()` or user hasn't navigated         | Add `clients.claim()` in activate, or reload after first registration    |
| New SW is stuck in "waiting" state           | Another tab has the old SW active                          | Close all tabs, or implement the update notification UX from section 8   |
| Stale cached content after deploy            | Old cache name still active, no versioning                 | Implement cache versioning and clean up old caches on activate           |
| Push works in dev but not in production      | VAPID keys mismatch or wrong `mailto:`                     | Verify env vars match between local and production                       |
| `fetch` handler returns unexpected responses | SW scope is wider than intended, catching unrelated routes | Check `scope` in registration and add URL filtering in the fetch handler |
| Lighthouse PWA fails "start_url not cached"  | The start_url from manifest isn't precached                | Add `start_url` value to the precache list in `install`                  |
| iOS doesn't show install prompt              | Expected — iOS doesn't support `beforeinstallprompt`       | Guide users to use Safari's Share → Add to Home Screen                   |

For deeper debugging:

- Chrome: `chrome://serviceworker-internals/` shows all registered SWs across all origins.
- DevTools → Application → Cache Storage lets you inspect individual cached entries.
- DevTools → Application → Service Workers has "Update on reload" checkbox for development (forces install+activate on every page load).

---

## 10) Serwist Integration

When the user needs advanced offline capabilities (complex precaching manifests, runtime caching routes with expiration, automatic SW generation), use [Serwist](https://serwist.pages.dev/) — the actively maintained successor to Workbox's Next.js integrations.

### When to use Serwist vs manual SW

- **Manual `public/sw.js`**: best for simple cases — push-only, basic offline fallback, or when the user wants full control over every line of the worker.
- **Serwist**: best when you need build-time precaching (inject a manifest of hashed assets), runtime caching with TTL/max-entries, or navigational preloading. The build plugin generates the SW automatically.

### Setup

1. Install: `npm install @serwist/next @serwist/precaching @serwist/strategies`
2. Configure the Next.js plugin in `next.config.js` wrapping the existing config.
3. Create the SW entry file (e.g., `app/sw.ts`) using Serwist's API instead of raw `self.addEventListener`.
4. Serwist's plugin handles injecting the precache manifest at build time.

Note: Serwist's Next.js plugin currently requires Webpack mode (the default). If the project uses Turbopack for production builds, check compatibility before proceeding.

---

## Decision Notes

- **Static export** (`output: 'export'`): move away from Server Actions and move header control to your proxy/CDN. Push notification subscription management must happen via external API endpoints.
- **Middleware and SW coexistence**: Next.js Middleware runs on the server (edge runtime). The service worker runs in the browser. They don't conflict, but be aware that Middleware redirects and rewrites happen before the response reaches the SW's `fetch` handler. If Middleware rewrites `/about` to `/about-v2`, the SW sees the request to `/about` but the response comes from `/about-v2`.
- **ISR and caching**: If using Incremental Static Regeneration, be careful with Cache First strategy on HTML pages — you might serve a stale cached page that ISR has already regenerated on the server. Use Network First for ISR pages so the revalidated version is always preferred.
- **Multi-zone or micro-frontend**: Each zone gets its own SW scope. Plan scope boundaries carefully to avoid one zone's SW intercepting another's requests.

## References

Load as needed:

- [references/strategies-and-snippets.md](references/strategies-and-snippets.md): Code templates for caching strategies, offline fallback, update notification component, Background Sync, cache versioning, Serwist config, iOS meta tags, and full troubleshooting checklist.
