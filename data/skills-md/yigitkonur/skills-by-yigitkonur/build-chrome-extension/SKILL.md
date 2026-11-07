---
name: build-chrome-extension
description: "Use if building or debugging a Chrome MV3 extension — manifest v3, service_worker, content_scripts."
disable-model-invocation: true
---

# Build Chrome Extension

Build, debug, package, and ship Chrome Manifest V3 extensions. Optimize for restart-safe service workers, isolated content scripts, least-privilege permissions, and Web Store review readiness.

## When To Use

Trigger when the request matches any of:

- *creating a new Chrome MV3 extension or scaffolding from a framework (WXT, Plasmo, CRXJS, Vite)*
- *editing or generating `manifest.json` with `manifest_version: 3`, `service_worker`, `content_scripts`, `host_permissions`, `action`, or `side_panel` fields*
- *implementing or debugging `chrome.runtime`, `chrome.storage`, `chrome.alarms`, `chrome.scripting`, `chrome.tabs`, `chrome.declarativeNetRequest`, `chrome.sidePanel`, or `chrome.offscreen` APIs*
- *connecting a Chrome extension to desktop apps or local daemons (Raycast Companion, local WebSocket servers, Native Messaging hosts)*
- *fixing MV3 service-worker lifecycle issues: idle termination, top-level listener registration, async `onMessage` returns, `chrome.alarms` vs `setInterval`*
- *bridging content scripts between ISOLATED and MAIN worlds, or routing fetches through the service worker for cross-origin host permissions*
- *migrating an MV2 extension to MV3 (background page → service worker, blocking `webRequest` → `declarativeNetRequest`, browser_action → action)*
- *validating a built `dist/` or `.output/chrome-mv3/` folder, packaging the Web Store zip, writing privacy/permission justifications, or preparing review notes*
- *choosing or comparing Chrome MV3 frameworks for a new project*

Do NOT use this skill when:

- *the target is Firefox, Safari, or a cross-browser polyfill (`browser.*` namespace, `web-ext` tooling, Safari App Extensions)*
- *the request is generic browser automation outside an extension context — out of scope*
- *publishing a regular npm package or library — route to `publish-npm-package`*
- *building a different platform's extension surface (Raycast script command, VS Code extension, Edge enterprise-policy package) — route to that platform's skill*

## Pinned Defaults — Apply Before Generating Code

| Key | Default |
|---|---|
| Manifest target | `manifest_version: 3` only; never generate MV2 |
| Greenfield framework | WXT unless the repo already chose another MV3 tool |
| Persistent state | `chrome.storage.local`; `chrome.storage.session` for ephemeral restart-safe state |
| Background model | Event-driven service worker, listeners registered synchronously at top level |
| Periodic work | `chrome.alarms` — never `setTimeout`/`setInterval` for background scheduling |
| Network modification | `chrome.declarativeNetRequest` — never blocking `webRequest` |
| Permissions | Least privilege; prefer `optional_permissions` and `optional_host_permissions` granted via `chrome.permissions.request` |
| Loaded folder | Built output only: WXT `.output/chrome-mv3-dev/` or `.output/chrome-mv3/`; Plasmo `build/chrome-mv3-*`; CRXJS/Vite `dist/` |
| Desktop IPC transport | Local WebSocket for unprivileged daemons; Native Messaging for installer-backed system tools |
| Package preflight | Run `scripts/check-mv3-manifest.sh` and `scripts/preflight-extension.sh` against the production build before zipping |

## MV3 Footguns — Keep In Working Memory

These are the failures that recur across every MV3 build. Internalize before writing code:

- Service workers idle out (~30s default). Global module-scope state disappears between events. Persist before each await and rehydrate at event entry.
- Register `chrome.runtime.onMessage`, `onInstalled`, `onStartup`, alarm, and tab listeners **synchronously at top level**. Late-registered listeners miss wake-up events.
- `setTimeout`/`setInterval` cannot keep a service worker alive and will not fire reliably across idle cycles. Use `chrome.alarms.create` with `periodInMinutes >= 0.5`.
- In Chrome 148+, `chrome.runtime.onMessage` listeners natively support returning a `Promise` or using `async`. For backward compatibility (<148 and cross-browser), async handlers must synchronously `return true` and invoke `sendResponse` when complete; otherwise the message channel closes immediately and the sender receives `undefined` (or rejects with "The message port closed before a response was received").
- Local WebSocket connections in service workers terminate after ~30 seconds of inactivity. You must maintain an active heartbeat ping (<30s interval, e.g. 24s) to reset Chrome 116+ idle timers. Idle open sockets do not keep the worker alive.
- Local WebSockets listening on 127.0.0.1 are vulnerable to Cross-Site WebSocket Hijacking (CSWSH) from malicious web pages. Daemons MUST validate the `Origin` header against `chrome-extension://<id>` and require an authentication token during HTTP Upgrade.
- Native Messaging hosts must NEVER write debug logs or unformatted output to standard output (`stdout`). Any non-framed stdout output corrupts the 32-bit length prefix and crashes the connection. Send logs to `stderr`.
- Messages sent from a Native Messaging host to Chrome are strictly capped at 1 MB. Exceeding 1 MB terminates the process immediately.
- Content scripts run in an isolated world by default. The page's JS, frameworks, and `window.*` globals are invisible. Use `world: "MAIN"` only for page-JS access, then bridge with `postMessage` plus a same-origin token.
- Extension-origin `fetch` requires matching `host_permissions`. Content-script `fetch` is bound by the page's origin and CORS rules — route privileged requests through the service worker via `chrome.runtime.sendMessage`.
- MV3 CSP forbids inline `<script>`, `eval()`, `new Function()`, and remote executable code in extension pages. Bundle everything; no CDN-loaded scripts. (Sandboxed pages in `manifest.sandbox` are the sole exception where `unsafe-eval` is permitted).
- Hand-written `manifest.json` paths must point at built artifacts (e.g. `background.js`, `content.js`, `popup.html`), never `src/*.ts` or unbuilt source.
- Requesting `<all_urls>` or broad host permissions at install time triggers Web Store review friction. Prefer `activeTab` plus optional host grants.

## Decision Rules

| Decision | Default | Escalate when |
|---|---|---|
| Background state | `chrome.storage.session`/`local` | Transactions, large indexes, binary blobs → IndexedDB |
| Periodic work | `chrome.alarms` | Real-time stream → design reconnect + queue |
| Network modification | `declarativeNetRequest` | Read-only observation → non-blocking `webRequest` |
| Page data fetch | Service worker `fetch` with host permissions | Page origin is sufficient → content-script `fetch` |
| Page JS access | `world: "MAIN"` bridge with payload validation | DOM-only access → stay in ISOLATED world |
| UI state persistence | `chrome.storage.session` | Must survive browser restart → `local` or `sync` |
| Host access | `activeTab` or optional host grants | Extension is non-functional without install-time host access |
| Side panel vs popup | Side panel for persistent companion UI | Quick action or short form → popup |
| Offscreen document | DOM/canvas/clipboard/audio/Worker from service worker | Popup/options/content script can own it → skip |
| Desktop communication | Local WebSocket (`ws://127.0.0.1:<port>`) with CSWSH protection | Deep OS integration / enterprise distribution / zero local port exposure → `chrome.runtime.connectNative` |

## Routing Boundary

| Request shape | Action |
|---|---|
| "Build a Chrome extension" | Use this skill; target MV3 |
| "Build for Chrome and Firefox" | Keep Chrome MV3 here; cross-browser layer is out of scope |
| "Automate a website in a browser" | Out of scope (general browser automation) |
| "Write Playwright tests for an extension" | Extension launch/load notes here; broader Playwright authoring is out of scope for this pack |
| "Publish to npm" | Route to `publish-npm-package` |
| "Submit to Chrome Web Store" | Use this skill; read `references/publishing/web-store.md` |
| "Deploy via enterprise policy" | Out of scope unless a dedicated enterprise skill exists |

## Workflow

### 1. Scope The Extension

Ask: *"Which extension surfaces exist, which Chrome APIs are required, which permissions can be deferred to runtime?"*

1. List required surfaces: popup, options, side panel, content script, service worker, offscreen document, devtools.
2. List required Chrome APIs and resulting permissions.
3. Split install-time vs `optional_permissions`/`optional_host_permissions`.
4. Choose the framework — see `references/frameworks/comparison.md`.
5. Record the built-output folder Chrome will load.

### 2. Scaffold Or Adapt

Ask: *"Greenfield, existing framework build, or hand-written manifest?"*

- Greenfield default: WXT.
- Existing Vite app becoming an extension: CRXJS.
- Custom build pipeline / explicit control: vanilla + Vite.
- Existing repo: follow its framework and output conventions.

Chrome must load the built output folder, never `src/` or unbundled TypeScript.

### 3. Implement Extension Contexts

Ask: *"Which context owns the state, which owns the DOM, which messages cross the boundary?"*

Read the matching reference before writing code:

- Service worker lifecycle, persistence, alarms, offscreen → `references/patterns/service-worker.md`
- Content scripts, world isolation, idempotency, cross-origin routing → `references/patterns/content-scripts.md`
- Popup, options, side panel, devtools, new-tab surfaces → `references/patterns/ui-surfaces.md`
- One-time messages, ports, external/native messaging, page bridges → `references/apis/messaging.md`
- Desktop communication, Raycast Companion, Native Messaging → `references/patterns/desktop-ipc.md`
- `chrome.storage` areas, quotas, typed wrappers, migrations → `references/apis/storage.md`
- Tabs, scripting, alarms, DNR, side panel, offscreen, runtime → `references/apis/core-apis.md`
- Manifest, permission, and MV2 migration decisions are covered by the pinned defaults and guardrails in this `SKILL.md`.

Validate every cross-boundary payload: messages, storage reads, external API responses, MAIN-world bridge data.

### 4. Validate Built Output

Ask: *"Can Chrome load this exact folder, and do all manifest paths exist there?"*

Run from the skill directory against your build folder:

```bash
scripts/check-mv3-manifest.sh dist
scripts/preflight-extension.sh dist
```

Adjust the path per framework:

| Framework | Dev output | Production output |
|---|---|---|
| WXT | `.output/chrome-mv3-dev/` | `.output/chrome-mv3/` |
| Plasmo | `build/chrome-mv3-dev/` | `build/chrome-mv3-prod/` |
| CRXJS | `dist/` | `dist/` |
| Vanilla Vite | `dist/` | `dist/` |

Read `scripts/check-mv3-manifest.md` and `scripts/preflight-extension.md` before modifying either script.

### 5. Test Extension Behavior

Ask: *"What failure only appears once Chrome loads the extension?"*

- Unit-test pure logic and message/storage helpers; mock `chrome.*` only at boundaries.
- Manually load the built output via `chrome://extensions` → "Load unpacked".
- Inspect the service worker from the extensions page; trigger an idle/wake cycle.
- Test content-script injection on allowed and disallowed URLs.
- Verify the runtime permission request UX (`chrome.permissions.request`) before the host call.

Read `references/testing/testing-guide.md` for extension-specific tests and `references/testing/debugging.md` for service-worker, popup, content-script, permission, and storage debugging.

### 6. Package For Web Store Review

Ask: *"Could a reviewer state the single purpose, each permission's need, the data use, and the remote-code posture in one sentence each?"*

1. Build production output.
2. Run both bundled scripts against that production build.
3. Strip junk before zipping: source maps (unless intentionally shipped), tests, `.DS_Store`, `__MACOSX`, framework caches.
4. Create the zip from inside the built-output folder (so `manifest.json` sits at the zip root).
5. Prepare: privacy practices, per-permission justification, remote-code disclosure, data-use certification, reviewer test instructions.
6. Read `references/publishing/web-store.md` before submission.

## Minimal Build Evidence

Match evidence to the task before stopping:

| Task | Evidence |
|---|---|
| New scaffold | Built-output path + `check-mv3-manifest.sh` result |
| Feature change | Relevant unit/integration test + manual-load note when Chrome behavior changed |
| Manifest/permission change | `check-mv3-manifest.sh` result + permission justification |
| Content-script change | Allowed-URL injection result + disallowed-URL injection result |
| Service-worker change | Restart-resilience note OR explicit "not exercised" caveat |
| Package/Web Store work | `preflight-extension.sh` result + zip path + reviewer notes |

## Output Contract

Final reports include:

- loaded build directory
- zip path (when packaged)
- Chrome version used for manual load (when manually tested)
- summary of permissions and host-permissions justification
- Web Store policy posture: single purpose, data use, remote code, MV3 compliance
- scripts/tests run, including failures
- reviewer notes for remaining manual checks

## Guardrails

- Never generate or preserve Manifest V2 for new work.
- Never load `src/` in Chrome unless the framework explicitly emits loadable code there.
- Never hold durable state in module-scope globals inside the service worker.
- Never rely on `setTimeout`/`setInterval` to keep the service worker alive.
- Never use blocking `webRequest` for normal MV3 network modification.
- Never request `<all_urls>` without a feature-level justification and a documented narrower alternative.
- Never expose arbitrary background `fetch` through unauthenticated content-script messages.
- Never ship remote executable code or undeclared remote-code behavior.
- Always validate built-output paths against `manifest.json` before claiming done.
- Always make each permission explainable in one sentence.

## Bottom Line

MV3 punishes the same mistakes repeatedly: lost service-worker state, late-registered listeners, timer-based scheduling, isolated-world surprises, over-broad permissions, and shipping `src/` instead of built output. Apply the pinned defaults, route to references for depth, run the bundled scripts against the built folder, and produce review-ready evidence.
