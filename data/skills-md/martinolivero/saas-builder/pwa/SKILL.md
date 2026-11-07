---
name: pwa
description: This skill should be used when turning a web app into a Progressive Web App — making it installable, work offline, cache assets, or send push notifications. Trigger phrases include "make it a PWA", "installable app", "work offline", "offline mode", "service worker", "web push", "push notifications", "add to home screen", "app manifest", "cache assets", "make it feel like a native app". It sets up vite-plugin-pwa with the right caching strategy and avoids the stale-service-worker trap.
---

# PWA

This skill makes a React + Vite app installable and offline-capable — the realistic middle ground between a plain website and a full native app. For a web-SaaS builder, this is the common mobile need; full React Native is rare and better served by Expo's own skills.

Analogy: a PWA is a food truck. It's the same kitchen as the restaurant (your web app), but it can park on the user's home screen and keep serving when the main location's network is down. You don't need to build a second restaurant (a native app) to get there.

## When to use this vs going native

- **PWA (this skill)** → installable, offline, push for an existing web app. Covers most "we need mobile" requests.
- **Full React Native** → only when you need deep native APIs, app-store presence, or heavy device integration. Delegate to **`expo/skills`** (official, ~2k⭐) rather than rebuilding it here. At most, share TS types/API client via a monorepo `packages/shared`.

## Discovery (max 3 questions, only if unknown)

1. What's the goal — installable, offline reads, offline writes, or push notifications?
2. Is this an existing Vite app, or starting fresh?
3. Do you need push on iOS? (It only works for *installed* PWAs, Safari 16.4+.)

## Step 1 — Install and configure

Add **`vite-plugin-pwa`** (~4k⭐, Workbox-based). Start with `registerType: 'autoUpdate'` and the `generateSW` strategy to precache the app shell + static assets. This plus a Web App Manifest and HTTPS = installable.

## Step 2 — Author the manifest

Web App Manifest: `name`, `short_name`, `theme_color`, `background_color`, **192px and 512px maskable icons**, `display: standalone`, `start_url`. The plugin can generate it from config.

## Step 3 — Caching strategy

- **Cache-first** for hashed static assets (they never change without a new hash).
- **Stale-while-revalidate** for API/data (instant from cache, refresh in background).
- Set `navigateFallback` so SPA routes work offline.

## Step 4 — Offline writes (if needed)

Don't try to cache POSTs in the service worker. Pair the SW with **IndexedDB** (e.g. Dexie) + **Workbox Background Sync** to queue mutations and replay them on reconnect.

## Step 5 — Push notifications (if needed)

- Switch to `injectManifest` (custom SW) for push handlers.
- Subscribe via `PushManager`, store the subscription server-side, send via **VAPID**.
- iOS: web push works **only for installed PWAs** (16.4+) — set expectations.

## Step 6 — Avoid the #1 PWA bug

A stale or over-aggressive service worker is the most common PWA support ticket. Always:
- Ship a **skipWaiting / update** strategy.
- Surface an in-app **"New version available"** prompt using the plugin's `useRegisterSW` — don't silently reload mid-session.
- Provide a custom offline fallback page; test via the Lighthouse PWA audit + DevTools "Offline" before shipping.

## Output

Deliver: the `vite-plugin-pwa` config, the manifest, the caching-strategy choices, the update prompt, and (if requested) the IndexedDB+Background-Sync or push setup.

## Reference

vite-pwa/vite-plugin-pwa (~4k⭐), GoogleChrome/workbox (~13k⭐), web.dev Learn PWA, expo/skills (for native).
