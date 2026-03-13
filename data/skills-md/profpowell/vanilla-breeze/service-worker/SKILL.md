---
name: service-worker
description: Service worker patterns for offline support, caching strategies, and PWA functionality. Use when implementing offline-first features, caching, or background sync.
allowed-tools: Read, Write, Edit
---

# Service Worker Skill

This skill covers service worker implementation patterns for offline support, intelligent caching, and Progressive Web App (PWA) functionality—without relying on Workbox or other abstractions.

## Philosophy

Service workers should be:

1. **Progressive** - Enhance, don't break; site works without SW
2. **Predictable** - Clear caching strategies with versioned caches
3. **Debuggable** - Logging and clear update paths
4. **Lightweight** - Vanilla JS, no frameworks required

---

## File Structure

```
src/
├── sw.js                    # Main service worker
├── sw-assets.js             # Asset list for precaching (optional)
└── js/
    └── sw-register.js       # Registration script
```

---

## Service Worker Registration

### Basic Registration

```javascript
// js/sw-register.js

/**
 * Register service worker with update handling
 */
export async function registerServiceWorker() {
  if (!('serviceWorker' in navigator)) {
    console.log('Service workers not supported');
    return null;
  }

  try {
    const registration = await navigator.serviceWorker.register('/sw.js', {
      scope: '/',
    });

    console.log('SW registered:', registration.scope);

    // Check for updates on page load
    registration.update();

    // Handle updates
    registration.addEventListener('updatefound', () => {
      const newWorker = registration.installing;

      newWorker.addEventListener('statechange', () => {
        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
          // New version available
          dispatchEvent(new CustomEvent('sw-update-available', {
            detail: { registration },
          }));
        }
      });
    });

    return registration;
  } catch (error) {
    console.error('SW registration failed:', error);
    return null;
  }
}

/**
 * Skip waiting and reload when update is accepted
 * @param {ServiceWorkerRegistration} registration
 */
export function acceptUpdate(registration) {
  if (registration.waiting) {
    registration.waiting.postMessage({ type: 'SKIP_WAITING' });
  }

  // Reload once the new SW takes control
  navigator.serviceWorker.addEventListener('controllerchange', () => {
    window.location.reload();
  });
}
```

### Registration in HTML

```html
<script type="module">
  import { registerServiceWorker } from '/js/sw-register.js';

  registerServiceWorker();

  // Optional: Show update prompt
  window.addEventListener('sw-update-available', (event) => {
    if (confirm('New version available. Reload?')) {
      acceptUpdate(event.detail.registration);
    }
  });
</script>
```

---

## Service Worker Template

### Complete SW Structure

```javascript
// sw.js

const CACHE_VERSION = 'v1.0.0';
const CACHE_NAME = `app-cache-${CACHE_VERSION}`;

// Assets to precache on install
const PRECACHE_ASSETS = [
  '/',
  '/index.html',
  '/styles/main.css',
  '/js/app.js',
  '/offline.html',
];

// ==================== INSTALL ====================

self.addEventListener('install', (event) => {
  console.log('[SW] Installing version:', CACHE_VERSION);

  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(PRECACHE_ASSETS))
      .then(() => {
        console.log('[SW] Precache complete');
        // Don't skip waiting by default - let user decide
      })
  );
});

// ==================== ACTIVATE ====================

self.addEventListener('activate', (event) => {
  console.log('[SW] Activating version:', CACHE_VERSION);

  event.waitUntil(
    // Clean up old caches
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((name) => name.startsWith('app-cache-') && name !== CACHE_NAME)
            .map((name) => {
              console.log('[SW] Deleting old cache:', name);
              return caches.delete(name);
            })
        );
      })
      .then(() => {
        // Take control of all pages immediately
        return self.clients.claim();
      })
  );
});

// ==================== FETCH ====================

self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // Skip cross-origin requests
  if (url.origin !== self.location.origin) {
    return;
  }

  // Choose caching strategy based on request type
  if (isNavigationRequest(request)) {
    event.respondWith(networkFirstWithOffline(request));
  } else if (isStaticAsset(url)) {
    event.respondWith(cacheFirst(request));
  } else if (isApiRequest(url)) {
    event.respondWith(networkFirst(request));
  } else {
    event.respondWith(staleWhileRevalidate(request));
  }
});

// ==================== MESSAGE ====================

self.addEventListener('message', (event) => {
  if (event.data?.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

// ==================== HELPERS ====================

function isNavigationRequest(request) {
  return request.mode === 'navigate';
}

function isStaticAsset(url) {
  return /\.(css|js|woff2?|ttf|eot|ico|png|jpe?g|gif|svg|webp|avif)$/.test(url.pathname);
}

function isApiRequest(url) {
  return url.pathname.startsWith('/api/');
}

// ==================== STRATEGIES ====================

// ... (strategies defined below)
```

---

## Caching Strategies

### Cache First (Static Assets)

Best for: CSS, JS, fonts, images—things that rarely change.

```javascript
/**
 * Cache first, falling back to network
 * @param {Request} request
 * @returns {Promise<Response>}
 */
async function cacheFirst(request) {
  const cached = await caches.match(request);

  if (cached) {
    return cached;
  }

  try {
    const response = await fetch(request);

    // Cache successful responses
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }

    return response;
  } catch (error) {
    console.error('[SW] Cache first failed:', error);
    throw error;
  }
}
```

### Network First (API, Dynamic Content)

Best for: API responses, user data, frequently updated content.

```javascript
/**
 * Network first, falling back to cache
 * @param {Request} request
 * @returns {Promise<Response>}
 */
async function networkFirst(request) {
  try {
    const response = await fetch(request);

    // Cache successful responses
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }

    return response;
  } catch (error) {
    const cached = await caches.match(request);

    if (cached) {
      console.log('[SW] Serving from cache:', request.url);
      return cached;
    }

    throw error;
  }
}
```

### Network First with Offline Fallback (Navigation)

Best for: HTML pages—show offline page when network fails.

```javascript
/**
 * Network first with offline fallback for navigation
 * @param {Request} request
 * @returns {Promise<Response>}
 */
async function networkFirstWithOffline(request) {
  try {
    const response = await fetch(request);

    // Cache the page
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }

    return response;
  } catch (error) {
    // Try cached version of this page
    const cached = await caches.match(request);
    if (cached) {
      return cached;
    }

    // Fall back to offline page
    const offlinePage = await caches.match('/offline.html');
    if (offlinePage) {
      return offlinePage;
    }

    // Last resort: simple offline response
    return new Response('Offline', {
      status: 503,
      statusText: 'Service Unavailable',
      headers: { 'Content-Type': 'text/plain' },
    });
  }
}
```

### Stale While Revalidate (General Content)

Best for: Content that changes but stale is acceptable—blog posts, product pages.

```javascript
/**
 * Return cached immediately, update cache in background
 * @param {Request} request
 * @returns {Promise<Response>}
 */
async function staleWhileRevalidate(request) {
  const cache = await caches.open(CACHE_NAME);
  const cached = await cache.match(request);

  // Fetch in background regardless
  const fetchPromise = fetch(request)
    .then((response) => {
      if (response.ok) {
        cache.put(request, response.clone());
      }
      return response;
    })
    .catch(() => null);

  // Return cached immediately, or wait for network
  return cached || fetchPromise;
}
```

---

## Strategy Selection Guide

| Content Type | Strategy | Reason |
|-------------|----------|--------|
| CSS, JS, fonts | Cache First | Versioned, rarely changes |
| Images | Cache First | Large files, cache aggressively |
| HTML pages | Network First + Offline | Fresh content, offline fallback |
| API responses | Network First | Dynamic data, cache as backup |
| Blog/articles | Stale While Revalidate | Fast response, background update |
| User avatars | Stale While Revalidate | Changes occasionally |

---

## Offline Page

Create a simple offline fallback:

```html
<!-- offline.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Offline</title>
  <style>
    body {
      font-family: system-ui, sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      margin: 0;
      background: #f3f4f6;
      color: #374151;
    }
    .offline-message {
      text-align: center;
      padding: 2rem;
    }
    h1 { margin: 0 0 1rem; }
    button {
      margin-top: 1rem;
      padding: 0.75rem 1.5rem;
      font-size: 1rem;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <div class="offline-message">
    <h1>You're offline</h1>
    <p>Please check your internet connection and try again.</p>
    <button onclick="location.reload()">Retry</button>
  </div>
</body>
</html>
```

---

## Cache Versioning

### Version Bump Strategy

```javascript
// sw.js

// Increment when precached assets change
const CACHE_VERSION = 'v1.2.0';

// Or use build hash
const CACHE_VERSION = 'v1-abc123';

// Cache name includes version
const CACHE_NAME = `app-cache-${CACHE_VERSION}`;
```

### Automatic Version from Build

```javascript
// Generated by build process
// sw-version.js
export const SW_VERSION = '2024-01-15T10:30:00Z';
```

```javascript
// sw.js
import { SW_VERSION } from './sw-version.js';

const CACHE_NAME = `app-cache-${SW_VERSION}`;
```

---

## Common Pitfalls

### 1. Not Handling Updates

**Problem:** Users stuck on old version.

```javascript
// BAD: Skip waiting immediately
self.addEventListener('install', () => {
  self.skipWaiting(); // Dangerous!
});

// GOOD: Let user trigger update
self.addEventListener('message', (event) => {
  if (event.data?.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
```

### 2. Caching Error Responses

**Problem:** Caching 404 or 500 responses.

```javascript
// BAD: Cache any response
cache.put(request, response.clone());

// GOOD: Only cache successful responses
if (response.ok) {
  cache.put(request, response.clone());
}
```

### 3. Cache Size Growth

**Problem:** Cache grows indefinitely.

```javascript
// Add cache size limits
const MAX_CACHE_SIZE = 50;

async function trimCache(cacheName, maxSize) {
  const cache = await caches.open(cacheName);
  const keys = await cache.keys();

  if (keys.length > maxSize) {
    // Delete oldest entries
    const toDelete = keys.slice(0, keys.length - maxSize);
    await Promise.all(toDelete.map((key) => cache.delete(key)));
  }
}
```

### 4. Forgetting to Handle POST/PUT

**Problem:** SW intercepts non-GET requests.

```javascript
// GOOD: Skip non-GET requests
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') {
    return; // Let browser handle it
  }
  // ... caching logic
});
```

### 5. Not Cleaning Old Caches

**Problem:** Old caches accumulate.

```javascript
// GOOD: Clean up in activate
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((names) => {
      return Promise.all(
        names
          .filter((name) => name !== CACHE_NAME)
          .map((name) => caches.delete(name))
      );
    })
  );
});
```

---

## Debugging

### Console Logging Pattern

```javascript
const DEBUG = true;

function log(...args) {
  if (DEBUG) {
    console.log('[SW]', ...args);
  }
}

// Usage
log('Fetch:', request.url);
log('Strategy: cache-first');
log('Cache hit:', !!cached);
```

### DevTools Checklist

1. **Application > Service Workers**
   - Check registration status
   - "Update on reload" for development
   - "Bypass for network" to test without SW

2. **Application > Cache Storage**
   - Verify cached assets
   - Check cache versions
   - Delete caches to test fresh install

3. **Network tab**
   - "(from ServiceWorker)" indicates cached response
   - Check which requests are intercepted

### Force Update During Development

```javascript
// In DevTools console
navigator.serviceWorker.getRegistration().then((reg) => {
  reg.unregister().then(() => {
    console.log('SW unregistered');
    location.reload();
  });
});
```

---

## Manifest Integration

Service workers work with `manifest.webmanifest` for full PWA support:

```html
<head>
  <link rel="manifest" href="/manifest.webmanifest"/>
</head>
```

```json
{
  "name": "My App",
  "short_name": "App",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#2563eb",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

---

## Background Sync (Optional)

Queue failed requests for retry when online:

```javascript
// In main app
async function sendData(data) {
  try {
    await fetch('/api/data', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  } catch (error) {
    // Queue for background sync
    const registration = await navigator.serviceWorker.ready;
    await registration.sync.register('sync-data');
    // Store data in IndexedDB for later
  }
}
```

```javascript
// In sw.js
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-data') {
    event.waitUntil(syncStoredData());
  }
});

async function syncStoredData() {
  // Retrieve from IndexedDB and POST
}
```

---

## Checklist

When implementing a service worker:

- [ ] Registration handles errors gracefully
- [ ] Update mechanism notifies users
- [ ] CACHE_VERSION incremented with asset changes
- [ ] Old caches cleaned in activate event
- [ ] Only GET requests are intercepted
- [ ] Only successful responses are cached
- [ ] Offline fallback page exists and is precached
- [ ] Appropriate strategy per content type
- [ ] No `skipWaiting()` without user consent
- [ ] Cache size limits prevent unbounded growth
- [ ] Cross-origin requests are not cached
- [ ] Debug logging available for development

## Related Skills

- **data-storage** - Implement client-side data storage with localStorage, Ind...
- **performance** - Write performance-friendly HTML pages
- **api-client** - Fetch API patterns with error handling, retry logic, and ...
- **progressive-enhancement** - HTML-first development with CSS-only interactivity patterns
