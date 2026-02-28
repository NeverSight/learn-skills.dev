---
name: nextjs-pwa
description: "Build Progressive Web Apps with Next.js: service workers, offline support, caching strategies, push notifications, install prompts, and web app manifest. Use when creating PWAs, adding offline capability, configuring service workers, implementing push notifications, handling install prompts, or optimizing PWA performance. Triggers: PWA, progressive web app, service worker, offline, cache strategy, web manifest, push notification, installable app, Serwist, next-pwa, workbox, background sync."
---

# Next.js PWA Skill

## Quick Reference

| Task | Approach | Reference |
|------|----------|-----------|
| Add PWA to Next.js app | Serwist (recommended) | This file → Quick Start |
| Add PWA without dependencies | Manual SW | references/service-worker-manual.md |
| Configure caching | Serwist defaultCache or custom | references/caching-strategies.md |
| Add offline support | App shell + IndexedDB | references/offline-data.md |
| Push notifications | VAPID + web-push | references/push-notifications.md |
| Fix iOS issues | Safari/WebKit workarounds | references/ios-quirks.md |
| Debug SW / Lighthouse | DevTools + common fixes | references/troubleshooting.md |
| Migrate from next-pwa | Serwist migration | references/serwist-setup.md |

---

## Quick Start — Serwist (Recommended)

Serwist is the actively maintained successor to next-pwa, built for App Router.

### 1. Install

```bash
npm install @serwist/next && npm install -D serwist
```

### 2. Create `app/manifest.ts`

```ts
import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "My App",
    short_name: "App",
    description: "My Progressive Web App",
    start_url: "/",
    display: "standalone",
    background_color: "#ffffff",
    theme_color: "#000000",
    icons: [
      { src: "/icon-192.png", sizes: "192x192", type: "image/png" },
      { src: "/icon-512.png", sizes: "512x512", type: "image/png" },
    ],
  };
}
```

### 3. Create `app/sw.ts` (service worker)

```ts
import { defaultCache } from "@serwist/next/worker";
import type { PrecacheEntry, SerwistGlobalConfig } from "serwist";
import { Serwist } from "serwist";

declare global {
  interface WorkerGlobalScope extends SerwistGlobalConfig {
    __SW_MANIFEST: (PrecacheEntry | string)[] | undefined;
  }
}

declare const self: ServiceWorkerGlobalScope;

const serwist = new Serwist({
  precacheEntries: self.__SW_MANIFEST,
  skipWaiting: true,
  clientsClaim: true,
  navigationPreload: true,
  runtimeCaching: defaultCache,
});

serwist.addEventListeners();
```

### 4. Update `next.config.ts`

```ts
import withSerwist from "@serwist/next";

const nextConfig = {
  // your existing config
};

export default withSerwist({
  swSrc: "app/sw.ts",
  swDest: "public/sw.js",
  disable: process.env.NODE_ENV === "development",
})(nextConfig);
```

That's it — 4 files for a working PWA. Run `next build` and test with Lighthouse.

---

## Quick Start — Manual (No Dependencies)

Use this when you want zero dependencies or are using `output: "export"`.

### 1. Create `app/manifest.ts`

Same as above.

### 2. Create `public/sw.js`

```js
const CACHE_NAME = "app-v1";
const PRECACHE_URLS = ["/", "/offline"];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(PRECACHE_URLS))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  if (event.request.mode === "navigate") {
    event.respondWith(
      fetch(event.request).catch(() => caches.match("/offline"))
    );
    return;
  }
  event.respondWith(
    caches.match(event.request).then((cached) => cached || fetch(event.request))
  );
});
```

### 3. Register SW in layout

```tsx
// app/components/ServiceWorkerRegistration.tsx
"use client";

import { useEffect } from "react";

export function ServiceWorkerRegistration() {
  useEffect(() => {
    if ("serviceWorker" in navigator) {
      navigator.serviceWorker.register("/sw.js");
    }
  }, []);
  return null;
}
```

Add `<ServiceWorkerRegistration />` to your root layout.

---

## Decision Framework

| Scenario | Recommendation |
|----------|---------------|
| App Router, wants caching out of the box | **Serwist** |
| Static export (`output: "export"`) | **Manual SW** |
| Migrating from next-pwa | **Serwist** (drop-in successor) |
| Need push notifications | Either — see references/push-notifications.md |
| Need granular cache control | Serwist with custom routes |
| Zero dependencies required | **Manual SW** |
| Minimal PWA (just installable) | **Manual SW** |

---

## Web App Manifest

Next.js 13.3+ supports `app/manifest.ts` natively. This generates `/manifest.webmanifest` at build time.

### Key fields

```ts
{
  name: "Full App Name",              // install dialog, splash screen
  short_name: "App",                  // home screen label (≤12 chars)
  description: "What the app does",
  start_url: "/",                     // entry point on launch
  display: "standalone",              // standalone | fullscreen | minimal-ui | browser
  orientation: "portrait",            // optional: lock orientation
  background_color: "#ffffff",        // splash screen background
  theme_color: "#000000",             // browser chrome color
  icons: [
    { src: "/icon-192.png", sizes: "192x192", type: "image/png" },
    { src: "/icon-512.png", sizes: "512x512", type: "image/png" },
    { src: "/icon-maskable.png", sizes: "512x512", type: "image/png", purpose: "maskable" },
  ],
  screenshots: [                      // optional: richer install UI
    { src: "/screenshot-wide.png", sizes: "1280x720", type: "image/png", form_factor: "wide" },
    { src: "/screenshot-narrow.png", sizes: "640x1136", type: "image/png", form_factor: "narrow" },
  ],
}
```

### Manifest tips
- Always include both 192x192 and 512x512 icons (Lighthouse requirement)
- Add a `maskable` icon for Android adaptive icons
- `screenshots` enable the richer install sheet on Android/desktop Chrome
- `theme_color` should match your `<meta name="theme-color">` in layout

---

## Service Worker Essentials

### Lifecycle

1. **Install** — SW downloaded, `install` event fires, precache assets
2. **Waiting** — New SW waits for all tabs to close (unless `skipWaiting`)
3. **Activate** — Old caches cleaned up, SW takes control
4. **Fetch** — SW intercepts network requests

### Update flow

When a new SW is detected:
- `skipWaiting: true` — immediately activates (may break in-flight requests)
- Without `skipWaiting` — waits for all tabs to close, then activates
- Notify users of updates with `workbox-window` or manual `controllerchange` listener

### Registration scope

- SW at `/sw.js` controls all pages under `/`
- SW at `/app/sw.js` only controls `/app/*`
- Always place SW at root unless you have a specific reason not to

---

## Caching Strategies Quick Reference

| Strategy | Use For | Serwist Class |
|----------|---------|--------------|
| **Cache First** | Static assets, fonts, images | `CacheFirst` |
| **Network First** | API data, HTML pages | `NetworkFirst` |
| **Stale While Revalidate** | Semi-static content (CSS/JS) | `StaleWhileRevalidate` |
| **Network Only** | Auth endpoints, real-time data | `NetworkOnly` |
| **Cache Only** | Precached content only | `CacheOnly` |

Serwist's `defaultCache` provides sensible defaults. For custom strategies, see references/caching-strategies.md.

---

## Offline Support Basics

### App shell pattern

Precache the app shell (layout, styles, scripts) so the UI loads instantly offline. Dynamic content loads from cache or shows a fallback.

### Online/offline detection hook

```tsx
"use client";
import { useSyncExternalStore } from "react";

function subscribe(callback: () => void) {
  window.addEventListener("online", callback);
  window.addEventListener("offline", callback);
  return () => {
    window.removeEventListener("online", callback);
    window.removeEventListener("offline", callback);
  };
}

export function useOnlineStatus() {
  return useSyncExternalStore(
    subscribe,
    () => navigator.onLine,
    () => true // SSR: assume online
  );
}
```

### Offline fallback page

Create `app/offline/page.tsx` and precache `/offline` in your SW. When navigation fails, serve this page.

For IndexedDB, background sync, and advanced offline patterns, see references/offline-data.md.

---

## Install Prompt Handling

### `beforeinstallprompt` (Chrome/Edge/Android)

```tsx
"use client";
import { useState, useEffect } from "react";

export function InstallPrompt() {
  const [deferredPrompt, setDeferredPrompt] = useState<any>(null);

  useEffect(() => {
    const handler = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e);
    };
    window.addEventListener("beforeinstallprompt", handler);
    return () => window.removeEventListener("beforeinstallprompt", handler);
  }, []);

  if (!deferredPrompt) return null;

  return (
    <button
      onClick={async () => {
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        if (outcome === "accepted") setDeferredPrompt(null);
      }}
    >
      Install App
    </button>
  );
}
```

### iOS detection

iOS doesn't fire `beforeinstallprompt`. Detect iOS and show manual instructions:

```ts
function isIOS() {
  return /iPad|iPhone|iPod/.test(navigator.userAgent) && !(window as any).MSStream;
}

function isStandalone() {
  return window.matchMedia("(display-mode: standalone)").matches
    || (navigator as any).standalone === true;
}
```

Show a banner: "Tap Share then Add to Home Screen" for iOS Safari users.

---

## Push Notifications Quick Start

### 1. Generate VAPID keys

```bash
npx web-push generate-vapid-keys
```

### 2. Subscribe in client

```ts
async function subscribeToPush() {
  const reg = await navigator.serviceWorker.ready;
  const sub = await reg.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY,
  });
  await fetch("/api/push/subscribe", {
    method: "POST",
    body: JSON.stringify(sub),
  });
}
```

### 3. Handle in SW

```ts
self.addEventListener("push", (event) => {
  const data = event.data?.json() ?? { title: "Notification" };
  event.waitUntil(
    self.registration.showNotification(data.title, {
      body: data.body,
      icon: "/icon-192.png",
    })
  );
});
```

For server-side sending, VAPID setup, and full implementation, see references/push-notifications.md.

---

## Troubleshooting Cheat Sheet

| Problem | Fix |
|---------|-----|
| SW not updating | Add `skipWaiting: true` or hard refresh (Shift+Cmd+R) |
| App not installable | Check manifest: needs `name`, `icons`, `start_url`, `display` |
| Stale content after deploy | Bump cache version or use content-hashed URLs |
| SW registered in dev | Disable in dev: `disable: process.env.NODE_ENV === "development"` |
| iOS not showing install | iOS has no install prompt — show manual instructions |
| Lighthouse PWA fails | Check HTTPS, valid manifest, registered SW, offline page |
| Next.js rewrite conflicts | Ensure SW is served from `/sw.js`, not rewritten |

For detailed debugging steps, see references/troubleshooting.md.

---

## Assets & Templates

- `assets/manifest-template.ts` — Complete app/manifest.ts with all fields
- `assets/sw-serwist-template.ts` — Serwist SW with custom routes and offline fallback
- `assets/sw-manual-template.js` — Manual SW with all strategies
- `assets/next-config-serwist.ts` — next.config.ts with withSerwist

## Generator Script

```bash
python scripts/generate_pwa_config.py <project-name> --approach serwist|manual [--push] [--offline]
```

Scaffolds PWA files based on chosen approach and features.
