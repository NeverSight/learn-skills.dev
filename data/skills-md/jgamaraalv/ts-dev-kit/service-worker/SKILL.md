---
name: service-worker
description: "Service Worker API implementation guide — registration, lifecycle management, caching strategies, push notifications, and background sync. Use when: (1) creating or modifying service worker files (sw.js), (2) implementing offline-first caching (cache-first, network-first, stale-while-revalidate), (3) setting up push notifications or background sync, (4) debugging service worker registration, scope, or update issues, (5) implementing navigation preload, (6) user mentions 'service worker', 'sw.js', 'offline support', 'cache strategy', 'push notification', 'background sync', 'workbox alternative', or 'PWA caching'."
---

# Service Worker

## Table of Contents

- [Constraints](#constraints)
- [Lifecycle](#lifecycle)
- [Registration](#registration)
- [Install Event — Pre-cache Assets](#install-event--pre-cache-assets)
- [Activate Event — Clean Up Old Caches](#activate-event--clean-up-old-caches)
- [Fetch Event — Intercept Requests](#fetch-event--intercept-requests)
- [Navigation Preload](#navigation-preload)
- [Updating a Service Worker](#updating-a-service-worker)
- [Communicating with Pages](#communicating-with-pages)
- [Common Pitfalls](#common-pitfalls)
- [Push Notifications & Background Sync](#push-notifications--background-sync)
- [API Quick Reference](#api-quick-reference)
- [Next.js Integration](#nextjs-integration)
- [DevTools](#devtools)

## Constraints

- HTTPS required (localhost exempt for dev)
- No DOM access — runs on separate thread
- Fully async — no synchronous XHR, no localStorage
- No dynamic `import()` — only static `import` statements
- Scope defaults to the directory containing the SW file
- `self` refers to `ServiceWorkerGlobalScope`

## Lifecycle

```
register() → Download → Install → [Wait] → Activate → Fetch control
```

1. **Register** from main thread via `navigator.serviceWorker.register()`
2. **Install** event fires once — use to pre-cache static assets
3. **Wait** — new SW waits until all tabs using old SW are closed (skip with `self.skipWaiting()`)
4. **Activate** event fires — use to clean up old caches
5. **Fetch** events start flowing — SW controls page network requests

A document must reload to be controlled (or call `clients.claim()` during activate).

## Registration

```js
// main.js — register from the page
if ("serviceWorker" in navigator) {
  const reg = await navigator.serviceWorker.register("/sw.js", { scope: "/" });
  // reg.installing | reg.waiting | reg.active
}
```

**Scope rules:**

- SW at `/sw.js` can control `/` and all subpaths
- SW at `/app/sw.js` can only control `/app/` by default
- Broaden scope with `Service-Worker-Allowed` response header

## Install Event — Pre-cache Assets

```js
// sw.js
const CACHE_NAME = "v1";
const PRECACHE_URLS = ["/", "/index.html", "/style.css", "/app.js"];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(PRECACHE_URLS)));
});
```

`waitUntil(promise)` — keeps install phase alive until the promise settles. If rejected, installation fails and the SW won't activate.

## Activate Event — Clean Up Old Caches

```js
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))),
      ),
  );
});
```

## Fetch Event — Intercept Requests

```js
self.addEventListener("fetch", (event) => {
  event.respondWith(caches.match(event.request).then((cached) => cached || fetch(event.request)));
});
```

`respondWith(promise)` — must be called synchronously (within the event handler, not in a microtask). The promise resolves to a `Response`.

For caching strategy patterns (cache-first, network-first, stale-while-revalidate), see [references/caching-strategies.md](references/caching-strategies.md).

## Navigation Preload

Avoid the startup delay when a SW boots to handle a navigation:

```js
self.addEventListener("activate", (event) => {
  event.waitUntil(self.registration?.navigationPreload.enable());
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    (async () => {
      const cached = await caches.match(event.request);
      if (cached) return cached;

      const preloaded = await event.preloadResponse;
      if (preloaded) return preloaded;

      return fetch(event.request);
    })(),
  );
});
```

## Updating a Service Worker

- Browser byte-compares the SW file on each navigation (or every 24h)
- New version installs in background while old version still serves
- Increment the cache name (e.g., `v1` → `v2`) in the new version
- Delete old caches in the `activate` handler
- Call `self.skipWaiting()` in `install` to activate immediately
- Call `self.clients.claim()` in `activate` to take control of open pages

## Communicating with Pages

```js
// Page → SW
navigator.serviceWorker.controller.postMessage({ type: "SKIP_WAITING" });

// SW → Page (via Clients API)
const clients = await self.clients.matchAll({ type: "window" });
clients.forEach((client) => client.postMessage({ type: "UPDATED" }));

// SW listens
self.addEventListener("message", (event) => {
  if (event.data?.type === "SKIP_WAITING") self.skipWaiting();
});
```

## Common Pitfalls

1. **Response cloning** — `response.clone()` before both caching and returning, since body streams can only be read once
2. **Opaque responses** — cross-origin fetches without CORS return opaque responses (status 0). `cache.add()` will refuse them. Use `cache.put()` but you can't inspect the response
3. **waitUntil timing** — call `event.waitUntil()` synchronously within the event handler, not inside an async callback
4. **Scope ceiling** — a SW cannot control URLs above its own directory unless `Service-Worker-Allowed` header is set
5. **No state persistence** — the SW may terminate at any time when idle. Don't store state in global variables — use Cache API or IndexedDB

## Push Notifications & Background Sync

For push subscription, handling push events, and background sync implementation, see [references/push-and-sync.md](references/push-and-sync.md).

## API Quick Reference

For detailed interfaces (`Cache`, `CacheStorage`, `FetchEvent`, `Clients`, `ServiceWorkerRegistration`, `ServiceWorkerGlobalScope`), see [references/api-reference.md](references/api-reference.md).

## Next.js Integration

In Next.js, place the service worker file in `public/sw.js`. `public/sw.js` is intentionally plain JS (not processed by Next.js build pipeline). Register it from a client component:

```tsx
"use client";
import { useEffect } from "react";

export function ServiceWorkerRegistrar() {
  useEffect(() => {
    if ("serviceWorker" in navigator) {
      navigator.serviceWorker.register("/sw.js");
    }
  }, []);
  return null;
}
```

Add to root layout. Next.js serves `public/` files at the root, so `/sw.js` scope covers `/`.

## DevTools

- **Chrome**: `chrome://inspect/#service-workers` or Application > Service Workers
- **Firefox**: `about:debugging#/runtime/this-firefox` or Application > Service Workers
- **Edge**: `edge://inspect/#service-workers` or Application > Service Workers

Unregister, update, and inspect caches from the Application panel. Use "Update on reload" checkbox during development.
