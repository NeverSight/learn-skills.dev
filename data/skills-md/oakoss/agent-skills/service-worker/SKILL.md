---
name: service-worker
description: |
  Service worker lifecycle, caching strategies, background sync, push notifications, and static routing for progressive web apps. Covers Workbox v7.4 strategies (CacheFirst, NetworkFirst, StaleWhileRevalidate), workbox-precaching for app shells, Background Sync API with cross-browser fallbacks, Push API with VAPID keys, and the Service Worker Static Routing API (Chrome 123+).

  Use when registering service workers, implementing offline caching, configuring background sync, adding push notifications, optimizing fetch handling with static routes, or integrating service workers with local-first sync engines.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
user-invocable: false
---

# Service Worker

## Overview

Service workers are event-driven scripts that run in a separate thread from the main page, intercepting network requests, managing caches, and enabling offline functionality. Workbox v7.4 (maintained by the Chrome Aurora team) provides a production-ready abstraction over the low-level Cache API and fetch event handling.

**When to use:** Progressive web apps needing offline support, apps requiring push notifications, background data synchronization, app shell caching, network request optimization with static routing.

**When NOT to use:** Simple static sites served from a CDN, server-rendered apps with no offline requirements, apps where stale data is unacceptable (use network-only), prototypes where caching complexity is premature.

## Quick Reference

| Pattern                | API / Tool                           | Key Points                                          |
| ---------------------- | ------------------------------------ | --------------------------------------------------- |
| Registration           | `navigator.serviceWorker.register()` | Register in window context, scope defaults to path  |
| Precaching             | `workbox-precaching`                 | Revision-hashed app shell, injected at build time   |
| Cache-first            | `CacheFirst` strategy                | Static assets, fonts, images                        |
| Network-first          | `NetworkFirst` strategy              | API responses needing freshness                     |
| Stale-while-revalidate | `StaleWhileRevalidate` strategy      | Balance between speed and freshness                 |
| Background sync        | `workbox-background-sync`            | Replay failed requests when back online             |
| Push notifications     | Push API + Notifications API         | VAPID keys, server-sent push, offline-first display |
| Static routing         | `event.addRoutes()` in install       | Bypass fetch handler for known routes               |
| Skip waiting           | `self.skipWaiting()`                 | Activate new SW immediately, use with caution       |
| Clients claim          | `self.clients.claim()`               | Control existing tabs without reload                |
| Navigation preload     | `navigationPreload.enable()`         | Parallel network request during SW startup          |
| Update prompt          | `workbox-window` Workbox class       | Detect updates, prompt user, postMessage to SW      |
| Offline fallback       | `workbox-recipes` offlineFallback    | Serve fallback page when cache and network fail     |
| Cache expiration       | `workbox-expiration`                 | maxEntries and maxAgeSeconds per cache              |

## Browser Support Quick Reference

| Feature             | Chrome | Firefox | Safari | Edge |
| ------------------- | ------ | ------- | ------ | ---- |
| Service Workers     | 40+    | 44+     | 11.1+  | 17+  |
| Background Sync     | 49+    | No      | No     | 79+  |
| Periodic Sync       | 80+    | No      | No     | 80+  |
| Push API            | 50+    | 44+     | 16.4+  | 17+  |
| Navigation Preload  | 59+    | 99+     | 15.4+  | 18+  |
| Static Routing API  | 123+   | No      | No     | 123+ |
| Background Fetch    | 74+    | No      | No     | 79+  |
| Storage Persistence | 52+    | 55+     | 15.2+  | 79+  |

## Common Mistakes

| Mistake                                        | Correct Pattern                                                         |
| ---------------------------------------------- | ----------------------------------------------------------------------- |
| Caching API responses with CacheFirst          | Use NetworkFirst or StaleWhileRevalidate for dynamic data               |
| Calling skipWaiting unconditionally            | Prompt user before activating to avoid breaking in-flight navigations   |
| Not versioning precache manifests              | Use workbox-build or workbox-webpack-plugin to inject revision hashes   |
| Ignoring cache storage limits                  | Implement cache expiration with workbox-expiration plugin               |
| Using sync access handle in service worker     | OPFS createSyncAccessHandle is dedicated-worker only; use async methods |
| Assuming Background Sync works everywhere      | Chrome/Edge only (~80%); implement navigator.onLine fallback            |
| Caching opaque responses without size limits   | Opaque responses pad cache quota; limit with maxEntries                 |
| Not handling service worker update races       | Use workbox-window to coordinate update lifecycle with the page         |
| Registering SW before page load completes      | Register in window load event to avoid competing for bandwidth          |
| Letting sync engine data flow through SW cache | Let the sync engine handle data; SW handles app shell and static assets |
| Not cleaning up old caches on activate         | Delete outdated caches in activate event to free storage                |
| Missing offline fallback for navigations       | Precache an offline.html and serve it when network and cache both fail  |

## Workbox Package Reference

| Package                      | Purpose                                           |
| ---------------------------- | ------------------------------------------------- |
| `workbox-precaching`         | Build-time asset caching with revision management |
| `workbox-routing`            | URL pattern matching and strategy routing         |
| `workbox-strategies`         | CacheFirst, NetworkFirst, StaleWhileRevalidate    |
| `workbox-expiration`         | Cache size and age limits                         |
| `workbox-cacheable-response` | Filter responses by status or header              |
| `workbox-background-sync`    | Queue and replay failed requests                  |
| `workbox-window`             | Page-side registration and update management      |
| `workbox-recipes`            | Pre-built patterns (offline fallback, warm cache) |
| `workbox-build`              | Build tool for generating precache manifests      |
| `workbox-navigation-preload` | Enable navigation preload in activate             |

## Delegation

> If the `local-first` skill is available, delegate architecture decisions, sync engine selection, and offline data strategy to it.
> Otherwise, recommend: `pnpm dlx skills add oakoss/agent-skills -s local-first -a claude-code -y`
> If the `electricsql` skill is available, delegate sync engine patterns, shape subscriptions, and real-time data replication to it.
> Otherwise, recommend: `pnpm dlx skills add oakoss/agent-skills -s electricsql -a claude-code -y`

- **Caching strategy review**: Use `Task` agent to audit route-to-strategy mappings
- **Offline testing**: Use `Task` agent to simulate offline scenarios and verify fallback behavior
- **Push notification design**: Use `Plan` agent to design notification payload and action strategies

## References

- [Service worker lifecycle and update management](references/lifecycle.md)
- [Workbox caching strategies and precaching](references/caching-strategies.md)
- [Background sync with cross-browser fallbacks](references/background-sync.md)
- [Static Routing API for fetch handler bypass](references/static-routing.md)
- [Push notifications with VAPID and offline integration](references/push-notifications.md)
- [Local-first integration and storage patterns](references/local-first-patterns.md)
