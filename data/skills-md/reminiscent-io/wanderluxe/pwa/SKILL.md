---
name: pwa
description: "Expert guidance on Progressive Web App (PWA) development - installability, service workers, offline functionality, and native-feeling UX. Use this skill whenever the user mentions PWA, service worker, web app manifest, manifest.json, offline-first, installable web app, add to home screen, beforeinstallprompt, app shell, workbox, cache strategies, or push notifications for web apps. Also trigger when the user wants to make their website work offline, feel like a native app, or be installable - even if they don't use the term 'PWA' explicitly. Trigger on phrases like 'make it work without internet', 'can users install this', 'offline mode', 'home screen icon', or 'why does my app feel like a website'."
---

# PWA Engineering Skill

You are an expert Progressive Web App engineer. Your job is to help developers build web apps that are installable, work offline, and feel indistinguishable from native apps. You prioritize working code over theory, platform-specific workarounds over idealized specs, and user experience over technical compliance checkboxes.

## How to Use This Skill

This skill has three layers. The SKILL.md you're reading now covers the core decision framework and the most important patterns. For deeper implementation details, read the relevant reference file:

| When you need...                                    | Read                                                   |
|-----------------------------------------------------|--------------------------------------------------------|
| Manifest fields, icons, screenshots, advanced APIs  | [references/manifest-and-apis.md](references/manifest-and-apis.md) |
| Service worker strategies, Workbox, offline patterns| [references/service-workers.md](references/service-workers.md)     |
| iOS/Safari workarounds, platform quirks             | [references/platform-quirks.md](references/platform-quirks.md)     |

Read the relevant reference file before giving detailed implementation advice on that topic. For quick questions or architecture-level guidance, this file alone is sufficient.

## The Mental Model

A PWA is not a technology checklist. It's a commitment to three user promises:

1. **"I can always reach you."** The app loads instantly — even offline, even on a train in rural Japan, even on flaky airport Wi-Fi. This means a service worker with an intelligent caching strategy, not just a fetch handler that passes everything through to the network.

2. **"You feel like you belong here."** The app sits on the home screen, launches in its own window, doesn't show browser chrome, handles the notch correctly, doesn't bounce when you overscroll, and doesn't select text when you tap buttons. This means a correct manifest, platform-specific meta tags, and CSS that eliminates "web-ness."

3. **"I'll keep you in the loop."** Push notifications, background sync, badge counts. The app stays alive and relevant even when it's not open. This means service worker event handlers, proper permission flows, and platform-aware notification strategies.

Every implementation decision should map back to one of these promises. If a feature doesn't serve one of them, question whether it belongs in the PWA layer at all.

## The Installability Checklist

For Chrome/Edge to fire `beforeinstallprompt`, you need exactly:

1. HTTPS (or localhost for dev)
2. A web app manifest linked in `<head>` with at least `name` and one icon
3. A service worker registered with a `fetch` event handler
4. ~30 seconds of user engagement with the domain

That's it. But "installable" and "good" are different things. The checklist gets you the install prompt; the rest of this skill gets you an app worth installing.

## Manifest: The Critical Decisions

A minimal manifest works, but a complete one dramatically improves the install experience. Here are the fields that actually matter and why:

```json
{
  "id": "/",
  "name": "Your App Name",
  "short_name": "App",
  "description": "What your app does in one sentence",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#000000",
  "orientation": "portrait-primary",
  "icons": [],
  "screenshots": [],
  "shortcuts": []
}
```

**Fields that developers get wrong:**

- **`id`**: This is the stable identity of your app across manifest URL changes. Set it explicitly or browsers will derive it from `start_url`, which can break things if you reorganize your URLs.

- **`scope`**: Defines which URLs are "inside" the app. Navigation outside scope opens the system browser. If you don't set it, it defaults to the directory of the manifest file — which is almost never what you want.

- **`icons` with `purpose`**: This is the single most common mistake in the wild. Do NOT use `"purpose": "any maskable"` on one icon entry. Maskable icons have a safe zone (~80% of the icon area) and get cropped on Android. If you use the same icon for both, it either looks tiny in non-maskable contexts or gets clipped in maskable contexts. Always provide separate entries:

```json
"icons": [
  { "src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any" },
  { "src": "/icons/icon-192-maskable.png", "sizes": "192x192", "type": "image/png", "purpose": "maskable" },
  { "src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any" },
  { "src": "/icons/icon-512-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
]
```

- **`screenshots`**: On Android, providing screenshots transforms the install dialog from a boring banner into an app-store-like sheet with previews. This meaningfully improves install conversion. Use `"form_factor": "narrow"` for mobile and `"wide"` for desktop.

- **`display`**: Use `standalone` for most apps. `fullscreen` hides the system status bar — only appropriate for games or immersive experiences. For desktop apps that want a custom title bar, use `display_override: ["window-controls-overlay", "standalone"]`.

For the complete field reference, icon sizing guide, and advanced manifest features (shortcuts, share_target, file_handlers, protocol_handlers, launch_handler), see [references/manifest-and-apis.md](references/manifest-and-apis.md).

## Service Worker Strategy Selection

Don't write service workers from scratch. Use **Workbox** — it's maintained by the Chrome team, used by the majority of production PWAs, and handles edge cases that hand-written code inevitably misses.

Choose your caching strategy by resource type:

| Resource Type            | Strategy                  | Why                                                    |
|--------------------------|---------------------------|--------------------------------------------------------|
| App shell (HTML/CSS/JS)  | **Precache** (Cache First)| These are your app's skeleton. Must load instantly.     |
| Fonts, logos             | **Cache First**           | Rarely change. Cache aggressively.                     |
| API data (lists, feeds)  | **Stale-While-Revalidate**| Show cached data instantly, update in background.      |
| User-specific data       | **Network First**         | Freshness matters more than speed.                     |
| Transactional data       | **Network Only**          | Checkout prices, stock levels — stale data is dangerous.|
| Images                   | **Cache First** + limits  | Big payloads. Cache with size/age eviction.            |

**The offline fallback is non-negotiable.** If a navigation request fails and there's no cached response, return a custom offline page — never the browser's default error. This is the bare minimum for the "I can always reach you" promise.

**Service worker updates are tricky.** The default lifecycle (install -> wait -> activate) exists to prevent version skew. Using `skipWaiting()` + `clientsClaim()` forces immediate activation, which is simpler but can break apps that lazy-load versioned assets. The safest pattern is to notify the user that an update is available and let them choose when to reload.

For complete Workbox configuration, caching recipes, background sync patterns, navigation preload, and update strategies, see [references/service-workers.md](references/service-workers.md).

## Native Feel: The CSS That Matters

These CSS rules eliminate the most common "this feels like a website" complaints:

```css
/* Prevent pull-to-refresh in standalone mode */
body {
  overscroll-behavior-y: contain;
}

/* Prevent text selection on interactive elements */
button, nav, [role="button"], .toolbar {
  user-select: none;
  -webkit-user-select: none;
}

/* Prevent tap highlight on mobile */
* {
  -webkit-tap-highlight-color: transparent;
}

/* Safe area handling for notched devices */
body {
  padding-top: env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-bottom);
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}
```

**Input handling**: Set `inputmode` on inputs to trigger the correct mobile keyboard. `inputmode="numeric"` for PINs, `inputmode="email"` for email fields, `inputmode="tel"` for phone numbers. This detail is small but users notice when the wrong keyboard appears.

**Viewport meta tag**: Verify this exists — without it, mobile browsers add a 300ms tap delay:
```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

## iOS: The Platform That Needs Extra Work

iOS/Safari has meaningful gaps compared to Chromium browsers. The key things to know:

1. **No `beforeinstallprompt`**: You cannot programmatically prompt installation on iOS. Build a manual "Add to Home Screen" instructional UI instead.

2. **Meta tags required**: iOS doesn't reliably read the manifest for icons or splash screens. You need:
   ```html
   <meta name="apple-mobile-web-app-capable" content="yes">
   <meta name="apple-mobile-web-app-status-bar-style" content="default">
   <meta name="apple-mobile-web-app-title" content="Your App">
   <link rel="apple-touch-icon" href="/icon-180x180.png">
   ```

3. **Push notifications work** (iOS 16.4+) but only for installed PWAs, not in Safari browser. Users must manually add to home screen first.

4. **Storage gets evicted**: Safari aggressively removes cached data after periods of non-use. Monitor `navigator.storage.estimate()` and re-cache proactively. Request persistent storage where possible: `navigator.storage.persist()`.

5. **No background sync, no periodic sync, no file handlers, no protocol handlers**: Design your offline strategy around what iOS actually supports, not what the specs promise.

For the complete iOS workaround guide, splash screen generation, and cross-platform feature matrix, see [references/platform-quirks.md](references/platform-quirks.md).

## Custom Install Flow

Never rely on the browser's default install banner. Intercept `beforeinstallprompt` and show your own UI at the right moment — after the user has experienced value, not on first page load:

```javascript
let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  // Don't show immediately — wait for the right moment
});

// Show after a meaningful action (e.g., saving their first item)
function showInstallPrompt() {
  if (!deferredPrompt) return;
  showInstallBanner(); // Your custom install UI
}

async function handleInstallClick() {
  if (!deferredPrompt) return;
  deferredPrompt.prompt();
  const { outcome } = await deferredPrompt.userChoice;
  // Track: outcome === 'accepted' or 'dismissed'
  deferredPrompt = null;
}
```

**Detect if already installed** to avoid showing install prompts to existing users:
```javascript
// Chromium browsers
const isStandalone = window.matchMedia('(display-mode: standalone)').matches;
// iOS
const isIOSStandalone = window.navigator.standalone === true;
// Track installation
window.addEventListener('appinstalled', () => { /* hide install UI */ });
```

## Testing & Validation

Run Lighthouse PWA audits during development, not just before launch:

```bash
npx lighthouse https://your-app.com --only-categories=pwa --output=html --view
```

Chrome DevTools Application panel is your primary debugging tool:
- **Manifest tab**: Validates your manifest and shows parsed values
- **Service Workers tab**: View status, trigger updates, simulate offline
- **Cache Storage tab**: Inspect what's cached and how much space it uses
- **Storage tab**: Monitor quota usage across all storage APIs

Test these scenarios before shipping:
1. Fresh install — is the install prompt working?
2. Airplane mode — does the app load? Can the user do anything useful?
3. Kill the app and reopen — does it resume correctly?
4. Update the service worker — does the user get the new version without confusion?
5. iOS Safari — add to home screen — does it launch standalone with correct icon and splash?

## Architecture Decision: When NOT to PWA

Not every web app benefits from the full PWA treatment. Skip it when:
- The app is purely server-rendered with no client-side interactivity
- Offline access provides zero value (e.g., a real-time stock trading dashboard)
- The app requires capabilities that only native apps provide (NFC, Bluetooth LE in some cases)
- The target audience is exclusively desktop users who won't install

In these cases, a service worker for asset caching still helps performance, but the full manifest + install flow isn't worth the maintenance overhead.
