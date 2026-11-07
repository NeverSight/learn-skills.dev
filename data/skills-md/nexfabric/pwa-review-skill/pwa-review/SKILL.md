---
name: pwa-review
description: "Evidence-based 209-point PWA audit beyond Lighthouse — manifest, service worker, offline, install, security headers, performance, iOS/Safari, real-time resilience. Audits a live URL, a local source tree, or both."
argument-hint: "<url> [local-source-dir]"
allowed-tools: Bash(python3:*), Bash(curl:*), Read, Grep, Glob, WebFetch
---

<pwa-review>

# PWA Review Skill (v6.2.1)

Audits a Progressive Web App across 11 categories (209 nominal points) and grades it on the
**points that actually apply** to that app. Lighthouse removed its PWA category in v12 (2024);
this skill covers that gap and goes further (iOS/Safari behaviour, update UX, real-time
resilience, Chromium-only manifest features).

Every pass/fail must cite evidence: a file from the evidence folder with a line or snippet,
a response header, or a manifest field. No evidence, no pass.

## Scoring Overview

| # | Category | Points | Focus |
|---|----------|-------:|-------|
| 1 | Manifest Compliance | 22 | Required manifest fields, manifest and icons reachable |
| 2 | Advanced Manifest | 15 | Install-UI richness, identity, iOS splash |
| 3 | Service Worker & Caching | 35 | Lifecycle, caching strategies, cache hygiene |
| 4 | Offline Capability | 24 | Fallbacks, update UX, storage, sync, real-time resilience |
| 5 | Installability | 15 | Install criteria, install UX on Chromium and iOS |
| 6 | Security | 16 | HTTPS redirect, CSP, response headers, SRI |
| 7 | Performance Signals | 19 | Loading, Core Web Vitals signals, compression, bfcache |
| 8 | UX & Accessibility | 35 | Viewport, safe areas, a11y, mobile layout, theming, state |
| 9 | SEO & Discoverability | 8 | Meta, social, indexability |
| 10 | PWA Advanced | 19 | Chromium manifest capabilities, push, badging, share |
| 11 | iOS Compatibility | 1 | Bonus for the complete iOS meta set |
| | **Total** | **209** | |

### Applicability (N/A) and verifiability

Some checks only make sense for some apps. Mark them **N/A** and remove their points from
the maximum, with the reason in the report:

| N/A group | Points | N/A when |
|-----------|-------:|----------|
| Real-time resilience (Cat 4) | 5 | No WebSocket / socket.io / SSE / realtime SDK (`realtime` signal = 0 and nothing in source) |
| Dark-mode theme pairs (Cat 8) | 7 | App ships no dark mode (`dark_mode` signal = 0) |
| Mobile dropdowns (Cat 8) | 3 | No dropdown/popover menus in the UI |
| Touch double-fire guard (Cat 8) | 1 | No element binds both click and touchend |
| SRI (Cat 6) | 2 | No third-party `<script>` (`html.scripts.third_party` empty) |
| `note_taking` (Cat 2) | 1 | App is not a note-taking app |
| SPA view-state persistence (Cat 8) | 2 | Multi-page site without client-side routing |

A check is **Unverifiable** when the evidence needed is not reachable (e.g. source-only patterns
in URL mode when bundles could not be fetched, or a site behind login). Unverifiable points are
also removed from the maximum but listed separately. If unverifiable points exceed 10% of the
applicable maximum, label the grade **provisional**.

**Score % = earned / (209 − N/A − unverifiable).**
Grade: **A+** ≥ 90% · **A** 80–89% · **B** 70–79% · **C** 60–69% · **D** 40–59% · **F** < 40%.
With every check applicable: A+ 189+, A 168–188, B 147–167, C 126–146, D 84–125, F < 84.

Partial credit only where a row says so. Category status: ✅ ≥ 80%, ⚠️ 50–79%, ❌ < 50%.

---

## Execution Workflow

Arguments (`$ARGUMENTS` in agents that substitute it): a URL, a local project directory, or both
(`/pwa-review https://app.example.com ./my-app`). URL without scheme → assume `https://`.

### Step 1: Collect evidence (one command)

Run the bundled collector from this skill's base directory (shown when the skill loads;
e.g. `~/.agents/skills/pwa-review`). Write evidence to a scratch/temp directory, never into
the audited project:

```bash
python3 <skill-dir>/scripts/collect.py <url> --out <scratch>/pwa-<host> [--source <dir>]
python3 <skill-dir>/scripts/collect.py --source <dir> --out <scratch>/pwa-src   # source only
```

It fetches the raw HTML and response headers, probes HTTP→HTTPS redirect and `br`/`gzip`
compression, downloads the manifest, the 192/512/maskable icons, the service worker (from the
registration call, else common paths) and its `importScripts`, up to 25 same-origin JS bundles
(two levels deep) and 10 stylesheets, and `robots.txt`. It then scans everything for ~65 code
signals. Outputs in the evidence folder:

- `summary.json` — facts: status, headers, compression, redirect, parsed `<head>` (meta, links,
  scripts, images, landmarks), manifest (+ `data`, `icons_checked`), service worker (+
  `cache_control`, imports), bundles, robots, `signals` (counts), `fetch_log`
- `signals.json` — every signal hit with `file`, `line`, `count`, `snippet`
- raw files: `index.html`, `headers.json`, `manifest.json`, `sw.js`, `sw-import-*`, `bundles/*`

**Fallback** (no Python, or the collector cannot reach the site): use `curl -sSL -D -` for HTML
and headers, then `curl` the manifest and SW. Use WebFetch only as a last resort: it summarizes
pages through a model and drops `<head>` tags and headers, so mark anything it could not show
as Unverifiable rather than failed.

### Step 2: Read the facts

Read `summary.json` first (skip `manifest.data` duplication by reading `manifest.json` if long).
Signals are leads, not verdicts: a hit in a third-party library or a comment is not a pass.
Open the cited `file:line` with Read/Grep to confirm before awarding points, especially for
weighted rows (≥ 2 points) and for anything you will report as a finding.

**SW vs client:** SW-side rows (Cat 3, offline fallback, navigation fallback) must be evidenced in
`sw.js` / `sw-import-*` (or the SW source file in source mode). Client-side rows (update prompt,
sync registration, storage, install UI) must be evidenced in `bundles/*`, inline scripts or source.

**Source mode:** with `--source`, `summary.source_audit` pre-computes Tailwind theme pairs
(`theme_pairs.*`: total / unpaired / `file:line` samples), dropdown positioning (`dropdowns`) and
CSS-variable theming (`css_var_theme_tokens`). These are line-based heuristics: treat counts as
leads, open 2–3 samples before scoring, and judge intent (always-dark hero, brand-coloured button).
Also Grep the project for view-state persistence and reconnection on `connect`. Minified bundles
rarely show these reliably; prefer source evidence when both exist. Without `--source`, the theme
and dropdown rows are Unverifiable unless the app ships no dark mode / no menus (then N/A).

### Step 3: Score

Walk every row of the checklist below. For each row record: result (pass / partial / fail /
N/A / unverifiable), points, and one line of evidence. Apply the N/A rules above.

### Step 4: Report

Use the report template at the end. Write it in the language the user is writing in (translate
headings; keep code, header names and manifest keys verbatim). For long platform caveats or fix
code, read `references/platform-notes.md` and `references/fix-recipes.md` in this skill folder.
Print the report; save it to a file only if the user asks.

---

## Detailed Scoring Checklist

Signal names (`sig:`) refer to `summary.json → signals` / `signals.json`.

### Category 1: Manifest Compliance (22 points)

| Check | Pts | How to verify |
|-------|----:|---------------|
| `name` present, non-empty | 2 | `manifest.data.name` |
| `short_name` present (≤ 12 chars recommended) | 2 | `manifest.data.short_name`; > 12 chars → warning, still pass |
| 192×192 icon | 4 | `icons[]` with `sizes` containing `192x192` |
| 512×512 icon | 4 | `icons[]` with `sizes` containing `512x512` |
| `start_url` defined | 2 | `manifest.data.start_url` |
| `display` is standalone / fullscreen / minimal-ui | 2 | or `display_override` with `window-controls-overlay` and a valid `display` fallback |
| `background_color` | 2 | valid CSS colour |
| `theme_color` | 2 | valid CSS colour; mismatch with `<meta name=theme-color>` → warning |
| Manifest reachable and valid | 1 | `manifest.status` 200, `valid_json` true, content type `application/manifest+json` or `application/json` (other type → partial 0, warning) |
| Declared icons reachable | 1 | every `icons_checked[]` is 200 with `image/*` content type |

**Critical blocker:** no manifest linked → 0/22 and 0/15 for Category 2.

### Category 2: Advanced Manifest Features (15 points)

| Check | Pts | How to verify |
|-------|----:|---------------|
| `description` | 1 | present, non-empty |
| `screenshots` | 2 | 2 = at least one `form_factor: "wide"` and one narrow/unspecified (Chrome's richer install UI); 1 = screenshots without `form_factor` |
| `shortcuts` | 2 | ≥ 1 item with `name` + `url`; 1 if any shortcut lacks icons (warning only). Source mode: each `url` must map to a real route or a param the app reads — a shortcut to a 404 or an ignored `?param` → 0 |
| `categories` | 1 | array present |
| `orientation` | 1 | present |
| `lang` / `dir` | 1 | either present |
| `id` | 1 | present (stable app identity across `start_url` changes) |
| `scope` | 1 | present |
| Maskable icon | 1 | an icon with `purpose` containing `maskable`. Combined `"any maskable"` → pass with warning (padding looks wrong as `any`) |
| `start_url` inside `scope`, same origin | 1 | resolve both against the manifest URL |
| `note_taking` | 1 | N/A unless it is a note-taking app; `new_note_url` must open a new note/task (check its param in source) |
| iOS splash screens | 2 | 2 = `apple-touch-startup-image` links with `media` for ≥ 3 device sizes; 1 = one generic image |

### Category 3: Service Worker & Caching (35 points)

| Check | Pts | How to verify |
|-------|----:|---------------|
| SW registered by the page | 2 | `service_worker.registration_seen` true (registration code in inline/bundle/source; minified workbox-window passes the path in a variable, so `found_via` may say `(path literal)`). `found_via: probe` with `registration_seen` false = 1, note "registration not seen in fetched code" (2 if source mode confirms it) |
| `install` handler | 3 | `sig:sw_install` in SW files |
| `activate` handler | 3 | `sig:sw_activate` in SW files |
| `fetch` handler that responds | 4 | `sig:sw_fetch` **and** `sig:sw_respond_with` (or Workbox `registerRoute`). A fetch listener that never calls `respondWith` is a no-op: 0 points + warning (it slows every navigation) |
| Cache API usage | 3 | `sig:cache_api` or Workbox strategies |
| Cache naming / versioning | 2 | `sig:cache_version_name`, Workbox `cacheName`, or precache revisions |
| Old cache cleanup in activate | 2 | `sig:cache_cleanup` inside the activate flow |
| Background Sync handler | 2 | `sig:sw_sync` (`sync` / `periodicsync` / `BackgroundSyncPlugin`) |
| Precache revisioning | 1 | `sig:precache_revision` — hashed filenames or `{url, revision}` entries, so updates are atomic |
| `skipWaiting()` | 1 | `sig:skip_waiting`. Best practice: call it on a `SKIP_WAITING` message after user consent; unconditional call in `install` → pass with note |
| `clients.claim()` | 1 | `sig:clients_claim` |
| Navigation preload | 1 | `sig:nav_preload` |
| Stale-while-revalidate | 1 | `sig:strategy_swr` or equivalent manual pattern |
| `push` handler | 1 | `sig:sw_push` |
| `notificationclick` handler | 1 | `sig:sw_notificationclick` |
| Notification actions | 1 | `sig:notif_actions` (actions array or `event.action` branch) |
| Multiple strategies by resource type | 2 | ≥ 2 of `strategy_cache_first` / `strategy_network_first` / `strategy_swr`, routed by destination/path; 1 = one strategy with explicit routing |
| Cache expiration | 1 | `sig:expiration` or manual trimming logic |
| SW `message` handler | 1 | `sig:sw_message` |
| Response guard before caching | 1 | `sig:response_guard` — caches only `ok`/200 (or `CacheableResponsePlugin`), skips non-GET. Caching opaque/error responses wastes quota and can pin a 500 offline |
| SW script not long-cached | 1 | `service_worker.cache_control` is `no-cache`/`max-age=0`/short (≤ 300 s), or absent. Browsers cap SW HTTP caching at 24 h, but long `max-age` still delays updates |

**Critical blocker:** no service worker → 0/35 and 0/24 for Category 4.

### Category 4: Offline Capability (24 points)

| Check | Pts | How to verify |
|-------|----:|---------------|
| Offline fallback page | 3 | `sig:offline_page` in SW, and the page is precached |
| App shell precached | 3 | install/precache includes `/` or the HTML shell plus core JS/CSS |
| SPA navigation fallback | 1 | `sig:navigate_fallback` — navigation requests are answered from cache when offline |
| Offline indicator in UI | 2 | `sig:online_offline` in client code |
| Clear fetch strategy | 2 | network-first / cache-first logic is evident in the fetch handler |
| Update prompt shown to user | 1 | `sig:update_prompt` in client code with user-facing UI |
| Graceful update flow | 1 | user chooses when to reload (no forced reload on `controllerchange` without warning) |
| Update state persistence | 1 | `sig:update_flag` or equivalent suppression so the prompt does not reappear after updating |
| Persistent storage request | 1 | `sig:persist` |
| IndexedDB for structured data | 1 | `sig:indexeddb` in client code (a library name only in the precache list is not enough) |
| Storage quota monitoring | 1 | `sig:quota` |
| Background Sync client trigger | 1 | `sig:sync_register` (Chromium only; pass also if Workbox `BackgroundSyncPlugin` queues requests) |
| Periodic sync registration | 1 | `sig:periodic_register`, ideally behind a `periodic-background-sync` permission check |
| Reconnect on `visibilitychange` | 2 | N/A group. `sig:visibility` near socket/connection code |
| Reconnection strategy | 2 | N/A group. `sig:reconnect_cfg` with attempts > 5 or `Infinity`, `reconnectionDelayMax` ≥ 5000, manual retry UI |
| Re-subscribe after reconnect | 1 | N/A group. Room/channel join runs in a persistent `connect` listener, not only on first mount |

### Category 5: Installability (15 points)

Current Chromium criteria: HTTPS, a manifest with `name`/`short_name`, 192 and 512 icons,
`start_url`, a standalone-type `display`, and `prefer_related_applications` not `true`. Since
Chrome 108 (Android) / 112 (desktop) a fetch handler is **not** required for menu install, but
the automatic install prompt still looks for one.

| Check | Pts | How to verify |
|-------|----:|---------------|
| Served over HTTPS | 3 | `summary.https` (localhost counts for dev only) |
| Manifest linked | 2 | `html.links.manifest`; behind auth needs `crossorigin="use-credentials"` |
| Fetch handler (prompt eligibility) | 2 | cross-check Cat 3 fetch row |
| 192×192 icon | 1 | cross-check |
| 512×512 icon | 1 | cross-check |
| `apple-touch-icon` | 1 | `html.links.apple-touch-icon` (iOS ignores manifest icons for the home screen) |
| `beforeinstallprompt` handled | 2 | `sig:bip` in client code (see the next row: it must also be offered) |
| Custom install UI | 1 | `sig:bip_prompt` — the deferred event's `.prompt()` is called from a visible button/banner; `sig:appinstalled` hides it. A `beforeinstallprompt` listener that calls `preventDefault()` but never `.prompt()` suppresses the browser's own install UI → 0 and **warning** |
| iOS install guidance | 1 | `sig:ios_install_hint` — instructions for Share → Add to Home Screen (iOS has no prompt API) |
| Standalone-mode detection | 1 | `sig:display_mode` — `matchMedia('(display-mode: standalone)')` or `navigator.standalone` to hide install UI once installed |

`prefer_related_applications: true` blocks the browser install prompt → CRITICAL.

### Category 6: Security (16 points)

Headers come from `summary.headers` / `headers.json` (the collector fetches them), so these are
verifiable. Use the `<meta http-equiv>` equivalents where they exist.

| Check | Pts | How to verify |
|-------|----:|---------------|
| HTTP redirects to HTTPS | 2 | `http_redirect.to_https` true with 301/308 (302/307 → 1) |
| Content-Security-Policy | 3 | 2 = CSP header or meta present; +1 = `script-src` (or `default-src`) without `'unsafe-inline'`/`'unsafe-eval'` (nonces/hashes OK). `Content-Security-Policy-Report-Only` alone = 1 |
| Subresource Integrity | 2 | N/A group. `third_party_with_sri` = number of third-party scripts → 2; some → 1 |
| No mixed content | 2 | `html.mixed_content` empty |
| Manifest scope not broader than needed | 1 | `scope` is the app path, not a whole multi-app origin |
| `Strict-Transport-Security` | 1 | `max-age` ≥ 15552000 (180 days) |
| `X-Content-Type-Options: nosniff` | 1 | header |
| `Referrer-Policy` | 1 | header or meta; `unsafe-url` → fail |
| `Permissions-Policy` | 1 | header present |
| `Cross-Origin-Opener-Policy` | 1 | `same-origin` or `same-origin-allow-popups`. COEP is only required for `SharedArrayBuffer`; report it as info, never as a failure |
| Clickjacking protection | 1 | CSP `frame-ancestors` or `X-Frame-Options` |

### Category 7: Performance Signals (19 points)

| Check | Pts | How to verify |
|-------|----:|---------------|
| No render-blocking scripts in head | 2 | `html.scripts.render_blocking_in_head` empty (module scripts are deferred by default) |
| Image lazy loading | 2 | below-fold images use `loading="lazy"` (`images.lazy`) or IntersectionObserver; the LCP image must **not** be lazy |
| Resource hints | 2 | `preload` / `preconnect` / `dns-prefetch` / `modulepreload` in `html.links` |
| Code splitting | 2 | `sig:dynamic_import` or multiple chunks in `bundles` |
| Font optimization | 2 | `sig:font_display` or preloaded self-hosted fonts |
| LCP signals | 1 | hero image preloaded or `fetchpriority="high"` (`images.fetchpriority_high`), server-rendered above-fold content |
| INP signals | 1 | qualitative: no huge synchronous inline scripts, heavy work deferred/chunked |
| CLS prevention | 1 | images have width/height (`images.with_dimensions`) or `aspect-ratio` |
| Critical CSS | 1 | inline `<style>` in head (`inline_style_bytes` > 0) or small preloaded CSS |
| Compression | 1 | `summary.compression` is `br`, `gzip` or `zstd` |
| Vendor/bundle chunking | 1 | `sig:manual_chunks`, framework chunk naming (`_next/static/chunks`, `vendor-*.js`) |
| Network Information API | 1 | `sig:net_info` (Chromium only; progressive enhancement) |
| bfcache friendly | 1 | `sig:unload_listener` = 0 **and** document `cache-control` not `no-store` |
| Modern image formats | 1 | `images.modern_format_sources` or `modern_format_imgs` > 0, or an image CDN negotiating AVIF/WebP. N/A not allowed: no images at all → pass |

### Category 8: UX & Accessibility (35 points)

| Check | Pts | How to verify |
|-------|----:|---------------|
| Responsive viewport | 2 | `width=device-width, initial-scale=1` |
| `viewport-fit=cover` | 2 | in viewport meta |
| Safe-area CSS | 2 | `sig:safe_area` for fixed/sticky header and bottom bar |
| Zoom not disabled | 2 | `sig:unsafe_zoom` = 0 — `user-scalable=no` / `maximum-scale=1` fail WCAG 1.4.4. iOS ignores them in Safari but Android honours them |
| Semantic landmarks | 2 | `html.landmarks` has `main` + at least one of nav/header/footer (SPA shells: check source) |
| ARIA / roles | 1 | `aria_or_role_elements` > 0 or in source; wrong roles (e.g. `role=button` on a `<div>` without keyboard handling) → 0 |
| `<html lang>` | 2 | `html.lang` |
| Touch-friendly targets | 2 | qualitative; ≥ 24×24 CSS px (WCAG 2.5.8), 44×44 recommended |
| Tap reliability on iOS | 1 | interactive elements are `<button>`/`<a>` or have `cursor: pointer` (`sig:cursor_pointer`); `touch-action: manipulation` (`sig:touch_manipulation`) on controls |
| Touch double-fire guard | 1 | N/A group. If both `onClick` and `onTouchEnd` exist, `preventDefault()` or a guard flag stops a second run |
| Visible focus | 1 | `:focus-visible` styles; no bare `outline: none` |
| Skip link | 1 | first anchor `#main`/`#content` (`first_anchor_hrefs`) |
| Dynamic viewport units | 1 | `sig:dvh`; if `sig:vh100` is used for full-height layouts without `dvh`/`svh` → fail (iOS toolbar hides content) |
| Reduced motion respected | 1 | `sig:reduced_motion` |
| Overscroll control | 1 | `sig:overscroll` on scroll containers / body in standalone mode |
| Colour-scheme signals | 1 | `sig:color_scheme` (`<meta name="color-scheme">` / CSS `color-scheme`), or theme-color `<meta>` with `media` variants |
| Mobile dropdown positioning | 2 | N/A group. `source_audit.dropdowns`: `mobile_safe` (viewport-positioned on phones, or width capped with `max-w-[calc(100vw-…)]`) = `candidates` → 2; some → 1; none → 0. Open 2 `samples` to confirm they are menus that can overflow a phone screen (URL-only mode: Unverifiable) |
| Dropdown safe-area handling | 1 | N/A group. dropdowns apply `safe-area-inset-left/right` |
| Theme consistency | 2 | N/A group. `source_audit.theme_pairs.surface` unpaired = 0, or the app themes through CSS variables (`css_var_theme_tokens` high) and the unpaired samples are intentional (always-dark splash/hero). Verified light-mode breakage → 0 |
| Overlay pairs | 1 | N/A group. `theme_pairs.overlay.unpaired` = 0 (scrims — `fixed`/`absolute inset-0` over modals, images or avatars, and `backdrop` — are exempt; they stay dark in both themes) |
| Border pairs | 1 | N/A group. `theme_pairs.border.unpaired` = 0, or samples sit on always-dark sections |
| Hover pairs | 1 | N/A group. `theme_pairs.hover.unpaired` = 0, or samples sit on always-dark/coloured sections |
| Gradient pairs | 1 | N/A group. `theme_pairs.gradient.unpaired` = 0, or samples are image scrims |
| Contextual `text-white` | 1 | N/A group. `theme_pairs.text_white` unpaired lines are on solid coloured backgrounds (check 3 samples; the heuristic looks back 3 lines for the background) |
| SPA view-state persistence | 2 | N/A group. Active view / tab / conversation id persisted (`sig:localstorage_set`, URL state or history state) and stale ids handled |

### Category 9: SEO & Discoverability (8 points)

| Check | Pts | How to verify |
|-------|----:|---------------|
| `<title>` | 1 | `html.title` non-empty |
| Meta description | 2 | `html.meta.description` |
| Open Graph | 2 | `og:title`, `og:description`, `og:image` (1 if partial) |
| Canonical URL | 1 | `html.links.canonical` |
| Structured data | 1 | `html.json_ld` > 0 |
| Indexable | 1 | no `noindex` robots meta on the start page and `robots.disallow_all` false (private/internal apps: N/A) |

### Category 10: PWA Advanced Capabilities (19 points)

Mostly Chromium features. Note browser support in the report; never fail an app for a
platform it does not target.

| Check | Pts | How to verify |
|-------|----:|---------------|
| `launch_handler` | 2 | object with `client_mode` |
| `file_handlers` | 2 | array with `action` + `accept` (requires `launchQueue` consumer: `sig:launch_queue`, else 1) |
| `protocol_handlers` | 2 | array with `protocol` + `url`, and the target route handles `%s` in source. Declared but unhandled → 0 + warning |
| `share_target` | 2 | object with `action` (+ `method`/`enctype` for files) **and** the app reads the shared params (`sig:launch_params` or a POST handler). Declared but unhandled → 0 + warning |
| `handle_links` | 2 | `preferred` / `auto` / `not-preferred` present (experimental, Chromium) |
| `display_override` | 1 | array present |
| `edge_side_panel` | 1 | object present (Edge) |
| `scope_extensions` | 1 | array present (origin trial; informational) |
| `related_applications` | 1 | present (informational) |
| `prefer_related_applications` false/absent | 1 | `true` = CRITICAL |
| Web Push configured | 1 | `sig:push_subscribe` — `applicationServerKey` (VAPID) or Firebase `getToken({ vapidKey })` client-side, or Declarative Web Push. `gcm_sender_id` is obsolete and does not count |
| Notification permission UX | 1 | `sig:notif_permission` called from a user gesture handler, not on load |
| Badging API | 1 | `sig:badging` |
| Web Share API | 1 | `sig:web_share` |

### Category 11: iOS Compatibility Bonus (1 point)

| Check | Pts | How to verify |
|-------|----:|---------------|
| Complete iOS meta set | 1 | `apple-mobile-web-app-capable` (or manifest `display` + iOS 16.4+), `apple-mobile-web-app-status-bar-style`, `apple-mobile-web-app-title` **and** standard `mobile-web-app-capable` |

---

## Issue Classification

### Critical (blocks install or offline)
- No manifest linked, manifest 404 or invalid JSON
- No service worker / SW fetch handler never responds (no offline at all)
- `prefer_related_applications: true`
- Not served over HTTPS (except localhost dev)
- Missing 192×192 or 512×512 icon, or icons 404

### Warnings (should fix)
- Manifest features declared but not handled by the app (share target, shortcuts to missing routes, file/protocol handlers, widgets)
- `beforeinstallprompt` suppressed but never offered (no install UI at all)
- Missing theme_color/background_color, `theme_color` ≠ meta theme-color
- No offline fallback, no navigation fallback for SPA routes
- No CSP, CSP with `'unsafe-inline'` scripts, no HTTPS redirect, weak/absent HSTS
- Zoom disabled (`user-scalable=no` / `maximum-scale=1`)
- `100vh` full-height layouts without `dvh`/`svh`
- Missing `apple-touch-icon`, iOS splash screens, iOS install guidance
- No cache versioning/cleanup, caching unchecked responses, SW script long-cached
- No update prompt, forced reload on update, prompt reappears after update
- Missing `viewport-fit=cover` or safe-area CSS for fixed elements
- Dark-mode gaps (only when the app ships a dark mode)
- Real-time: no `visibilitychange` reconnect, ≤ 5 attempts, no re-join on reconnect (only when real-time is used)
- No SPA view-state persistence
- `unload` listeners or `no-store` document (blocks bfcache)

### Informational
- Missing advanced manifest / Chromium-only capabilities
- No structured data, shortcuts, navigation preload, stale-while-revalidate
- No persistent-storage request, IndexedDB, quota monitoring
- No Background Sync / Periodic Sync client registration
- No Network Information API, Badging, Web Share
- Single caching strategy, no cache expiration
- COEP absent (only needed for cross-origin isolation)

---

## Report Template

```markdown
# PWA Audit Report

**Target:** [URL and/or source path] · **Mode:** [url | source | url+source]
**Date:** [YYYY-MM-DD] · **Evidence:** [evidence folder path]
**Score:** [earned]/[applicable] applicable points ([%]) — **Grade: [letter]**[ (provisional)]
**Nominal:** [earned]/209 · N/A: [n] pts · Unverifiable: [n] pts

---

## Score Breakdown

| Category | Score | Applicable | % | Status |
|----------|------:|-----------:|--:|:------:|
| Manifest Compliance | X | /22 | % | ✅/⚠️/❌ |
| Advanced Manifest | X | /15 | % | |
| Service Worker & Caching | X | /35 | % | |
| Offline Capability | X | /[24 − N/A] | % | |
| Installability | X | /15 | % | |
| Security | X | /[16 − N/A] | % | |
| Performance Signals | X | /19 | % | |
| UX & Accessibility | X | /[35 − N/A] | % | |
| SEO & Discoverability | X | /8 | % | |
| PWA Advanced | X | /19 | % | |
| iOS Compatibility | X | /1 | % | |

**N/A:** [group — reason] · **Unverifiable:** [check — what was missing]

---

## Critical Issues
- **[Category] Issue** — evidence (`file:line` / header / manifest key). **Fix:** one-line fix.

## Warnings
- **[Category] Issue** — evidence. **Fix:** …

## Passed Highlights
- [Grouped one-liners of what is done well, with evidence]

---

## Recommendations

### High Priority (biggest score and user impact)
1. [Fix] — +[n] pts — [effort: S/M/L]

### Medium Priority
1. …

### Quick Wins (< 15 min each)
- …

## Platform Notes
[Only the iOS/Safari/Chromium caveats relevant to this app, from references/platform-notes.md]

---

<details><summary>Machine-readable summary</summary>

```json
{"version":"6.2.1","target":"…","date":"…","earned":0,"applicable":0,"nominal":209,
 "percent":0,"grade":"…","provisional":false,
 "categories":{"manifest":[0,22],"advanced_manifest":[0,15],"service_worker":[0,35],
 "offline":[0,24],"installability":[0,15],"security":[0,16],"performance":[0,19],
 "ux":[0,35],"seo":[0,8],"advanced":[0,19],"ios":[0,1]},
 "na":[],"unverifiable":[],"critical":[],"warnings":[]}
```
</details>

*Generated by PWA Review Skill v6.2.1*
```

Category arrays are `[earned, applicable]`. Keep the JSON block so audits can be diffed over time.

---

## Error Handling

| Situation | Action |
|-----------|--------|
| Page fetch fails (DNS, TLS, timeout, 4xx/5xx) | Report the `fetch_log` error; if `--source` given, continue in source mode; else stop with a short explanation |
| Login wall / bot challenge (HTML is a sign-in or challenge page) | Score only what is public (manifest, SW, headers); mark app-code rows Unverifiable; suggest re-running with `--source` |
| No manifest linked | Cat 1 = 0/22, Cat 2 = 0/15, CRITICAL |
| Manifest 404 / invalid JSON | Same as above; quote `json_error` |
| No service worker | Cat 3 = 0/35, Cat 4 = 0/24, Cat 5 fetch row = 0, CRITICAL |
| SW found only by path probe | Score it; if `registration_seen` is false, flag "registration not seen" (it may be stale or unused) |
| Bundles not fetchable (CDN on another origin) | Client-code rows → Unverifiable unless `--source` evidence exists |
| SSR shell with little HTML | Rely on bundles/source; do not fail landmarks/ARIA from an empty shell alone |

---

## Example Usage

```
/pwa-review https://looknex.com
/pwa-review https://app.example.com ~/code/my-app     # live site + source evidence
/pwa-review ./my-app                                  # source only, before deploy
```

The agent will: run the collector → read `summary.json` and confirm signals at `file:line` →
score 11 categories with N/A rules → print the report with evidence and fixes.

</pwa-review>
