---
name: desktop-security-electron
description: Electron fuses, ASAR integrity, sandbox hardening, CSP, permission handling, navigation restrictions
---

# Electron Security & Fuses

> **Quick Guide:** Electron fuses are compile-time security flags flipped via `@electron/fuses` before code signing. Disable `RunAsNode`, `EnableNodeOptionsEnvironmentVariable`, `EnableNodeCliInspectArguments`, and `GrantFileProtocolExtraPrivileges`. Enable `EnableCookieEncryption`, `EnableEmbeddedAsarIntegrityValidation`, and `OnlyLoadAppFromAsar`. Rely on secure defaults: `contextIsolation: true` (Electron 12+), `sandbox: true` (Electron 20+), `nodeIntegration: false` (Electron 5+). Set a restrictive Content Security Policy. Use `setPermissionRequestHandler` to deny all permissions except an explicit allowlist. Block navigation and new-window creation.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST flip fuses BEFORE code signing -- the OS enforces fuse state after signing, so flipping after signing invalidates the signature)**

**(You MUST disable `RunAsNode`, `EnableNodeOptionsEnvironmentVariable`, `EnableNodeCliInspectArguments`, and `GrantFileProtocolExtraPrivileges` fuses in production builds -- these are the most commonly exploited attack vectors)**

**(You MUST enable both `EnableEmbeddedAsarIntegrityValidation` AND `OnlyLoadAppFromAsar` together -- enabling integrity validation alone still allows bypassing via the app code search path)**

**(You MUST NOT override security defaults (`contextIsolation: true`, `sandbox: true`, `nodeIntegration: false`) -- each one unlocks a critical attack surface)**

**(You MUST restrict permissions via `session.setPermissionRequestHandler()` -- Electron grants most permissions by default, including camera, microphone, and geolocation)**

</critical_requirements>

---

**Auto-detection:** Electron fuses, @electron/fuses, FuseV1Options, FuseVersion, flipFuses, RunAsNode, EnableCookieEncryption, EnableEmbeddedAsarIntegrityValidation, OnlyLoadAppFromAsar, GrantFileProtocolExtraPrivileges, ASAR integrity, Electron security, contextIsolation, sandbox, nodeIntegration, webPreferences security, Content-Security-Policy, setPermissionRequestHandler, setPermissionCheckHandler, will-navigate, setWindowOpenHandler, shell.openExternal validation, deep link validation, registerSchemesAsPrivileged, ELECTRON_RUN_AS_NODE, NODE_OPTIONS

**When to use:**

- Configuring Electron fuses for production builds
- Setting up ASAR integrity validation
- Hardening webPreferences and sandbox settings
- Defining Content Security Policy for renderer HTML
- Restricting permissions, navigation, and new-window creation
- Validating deep link / custom protocol URLs
- Securing `shell.openExternal()` calls
- Auditing an Electron app's security posture

**When NOT to use:**

- General Electron architecture (main/renderer process model, IPC patterns, app lifecycle)
- Packaging and distribution (Electron Forge, Electron Builder setup)
- Native OS API integration (dialogs, menus, tray, notifications)
- Choosing a UI framework for the renderer window

**Key patterns covered:**

- Fuse configuration with `@electron/fuses` (all 9 fuses explained)
- ASAR integrity validation (macOS + Windows, required fuses, tooling support)
- Secure webPreferences defaults and audit pattern
- Content Security Policy (meta tag and session headers)
- Permission request/check handlers with allowlists
- Navigation and new-window restriction
- `shell.openExternal()` URL validation
- Custom protocol security and deep link validation
- `file://` protocol replacement with custom schemes

---

<philosophy>

## Philosophy

Electron security follows a **defense-in-depth** strategy: multiple independent layers each reduce attack surface, so a breach in one layer does not compromise the entire app.

The layers from outermost to innermost:

1. **Fuses** -- compile-time flags that remove features from the binary entirely (cannot be re-enabled at runtime)
2. **ASAR integrity** -- ensures packaged app code has not been tampered with
3. **Process sandbox** -- OS-level isolation restricting what renderer processes can access
4. **Context isolation** -- separates preload script scope from renderer globals
5. **Content Security Policy** -- restricts what the renderer can load and execute
6. **Permission handlers** -- explicit allowlist for web API permissions
7. **Navigation restrictions** -- prevent renderers from leaving the app's origin
8. **Input validation** -- treat all IPC messages and URLs as untrusted

**Key principle:** Never rely on a single security mechanism. Each layer handles a different class of attack. Fuses stop living-off-the-land attacks. Sandboxing stops renderer-to-OS escalation. CSP stops code injection. Permission handlers stop unauthorized API access.

**When to use this skill:**

- Preparing an Electron app for production distribution
- Responding to a security audit or penetration test
- Configuring build tooling to flip fuses and enable ASAR integrity
- Reviewing webPreferences, CSP, and permission handling

**When NOT to use:**

- Initial app scaffolding (set up the app first, then harden)
- Debugging IPC or window management (not a security concern)
- Styling or UI framework decisions

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Fuse Configuration

Fuses are compile-time feature toggles embedded in the Electron binary. Once flipped and code-signed, the OS prevents reversal. Use the `@electron/fuses` package to flip them during your build step.

```javascript
// build-scripts/flip-fuses.js
const { flipFuses, FuseVersion, FuseV1Options } = require("@electron/fuses");

await flipFuses(
  // Path to your packaged Electron binary
  require("electron"),
  {
    version: FuseVersion.V1,
    [FuseV1Options.RunAsNode]: false,
    [FuseV1Options.EnableCookieEncryption]: true,
    [FuseV1Options.EnableNodeOptionsEnvironmentVariable]: false,
    [FuseV1Options.EnableNodeCliInspectArguments]: false,
    [FuseV1Options.EnableEmbeddedAsarIntegrityValidation]: true,
    [FuseV1Options.OnlyLoadAppFromAsar]: true,
    [FuseV1Options.LoadBrowserProcessSpecificV8Snapshot]: false,
    [FuseV1Options.GrantFileProtocolExtraPrivileges]: false,
  },
);
```

**Why these settings:** Disabling `RunAsNode` prevents `ELECTRON_RUN_AS_NODE` living-off-the-land attacks. Disabling `GrantFileProtocolExtraPrivileges` removes `file://` fetch/frame escalation. Enabling cookie encryption and ASAR integrity adds tamper protection. See [examples/core.md](examples/core.md) for the full fuse reference table and integration with Electron Forge and electron-builder.

---

### Pattern 2: ASAR Integrity Validation

ASAR integrity ensures the packaged `app.asar` has not been tampered with. Requires **two** fuses enabled together.

| Fuse                                    | Purpose                                                 |
| --------------------------------------- | ------------------------------------------------------- |
| `EnableEmbeddedAsarIntegrityValidation` | Validates the ASAR header hash at runtime               |
| `OnlyLoadAppFromAsar`                   | Prevents loading app code from outside the ASAR archive |

**Platform support:** macOS (Electron 16+), Windows (Electron 30+).

**Key point:** Electron Forge (7.4.0+) and `@electron/packager` (18.3.1+) automatically generate the integrity metadata when ASAR is enabled. Electron Builder supports it via the `electronFuses` config or `afterPack` hook. If only `EnableEmbeddedAsarIntegrityValidation` is enabled without `OnlyLoadAppFromAsar`, an attacker can place a plain `app` folder alongside the ASAR and bypass validation entirely.

See [examples/core.md](examples/core.md) for platform-specific configuration details.

---

### Pattern 3: Secure webPreferences Defaults

Modern Electron (v20+) defaults to the secure configuration. Never override these defaults.

```javascript
const mainWindow = new BrowserWindow({
  webPreferences: {
    preload: path.join(__dirname, "preload.js"),
    // All of these are DEFAULTS -- do NOT set them explicitly unless
    // you need to verify them in a security audit
    // contextIsolation: true   -- Electron 12+
    // sandbox: true            -- Electron 20+
    // nodeIntegration: false   -- Electron 5+
    // webSecurity: true        -- always
  },
});
```

**Why good:** Relying on defaults means future Electron upgrades automatically apply new secure defaults. Explicitly setting values can mask future changes.

```javascript
// BAD -- overriding secure defaults
const mainWindow = new BrowserWindow({
  webPreferences: {
    contextIsolation: false, // exposes preload scope to renderer
    nodeIntegration: true, // gives renderer full Node.js access
    sandbox: false, // disables OS-level process isolation
  },
});
```

**Why bad:** Each override removes a security layer. `contextIsolation: false` lets renderer code access preload globals. `nodeIntegration: true` gives the renderer `fs`, `child_process`, and every Node.js API. `sandbox: false` removes OS-level process isolation.

See [examples/core.md](examples/core.md) for the development-only audit pattern that catches accidental overrides.

---

### Pattern 4: Content Security Policy

Set CSP to restrict what the renderer can load and execute. Use the `<meta>` tag for static apps or session headers for dynamic CSP.

```html
<!-- index.html -- static CSP -->
<meta
  http-equiv="Content-Security-Policy"
  content="
    default-src 'self';
    script-src 'self';
    style-src 'self' 'unsafe-inline';
    img-src 'self' data:;
    connect-src 'self';
    font-src 'self';
  "
/>
```

**Key point:** `'self'` restricts loading to the app's own origin. Never add `'unsafe-eval'` in production -- it enables `eval()` and template injection attacks. See [examples/csp-permissions.md](examples/csp-permissions.md) for session header CSP and development-specific overrides.

---

### Pattern 5: Permission Handling

By default, Electron grants most web API permissions (camera, microphone, geolocation, notifications). Use an explicit allowlist to deny everything else.

```javascript
const ALLOWED_PERMISSIONS = new Set([
  "clipboard-read",
  "clipboard-sanitized-write",
]);

session.defaultSession.setPermissionRequestHandler(
  (_webContents, permission, callback) => {
    callback(ALLOWED_PERMISSIONS.has(permission));
  },
);

session.defaultSession.setPermissionCheckHandler((_webContents, permission) => {
  return ALLOWED_PERMISSIONS.has(permission);
});
```

**Why both handlers:** `setPermissionRequestHandler` handles async permission requests (prompted). `setPermissionCheckHandler` handles synchronous permission queries (silent checks). Without both, some permissions can slip through. See [examples/csp-permissions.md](examples/csp-permissions.md) for extended examples.

---

### Pattern 6: Navigation and New-Window Restrictions

Prevent the renderer from navigating to unexpected URLs or opening new windows.

```javascript
// Block navigation away from the app
mainWindow.webContents.on("will-navigate", (event, url) => {
  const appUrl = mainWindow.webContents.getURL();
  if (url !== appUrl) {
    event.preventDefault();
  }
});

// Block new window creation -- open external links in default browser
mainWindow.webContents.setWindowOpenHandler(({ url }) => {
  const parsed = new URL(url);
  if (parsed.protocol === "https:") {
    shell.openExternal(url);
  }
  return { action: "deny" };
});
```

**Why critical:** Without these guards, a compromised renderer could navigate to a phishing page styled to look like your app, or spawn pop-up windows. `setWindowOpenHandler` replaces the deprecated `new-window` event. See [examples/navigation-protocols.md](examples/navigation-protocols.md) for complete patterns.

---

### Pattern 7: Deep Link and Custom Protocol Security

Custom protocols (`myapp://`) replace `file://` for serving local content and handling deep links. Always validate incoming URLs.

```javascript
protocol.registerSchemesAsPrivileged([
  {
    scheme: "myapp",
    privileges: { standard: true, secure: true, supportFetchAPI: true },
  },
]);
```

**Key point:** `secure: true` makes the scheme behave like `https:` for CSP and mixed-content checks. Deep link URLs must be parsed and validated before acting on them -- an attacker can craft arbitrary `myapp://` URLs to trigger unintended actions. Disable `GrantFileProtocolExtraPrivileges` fuse and serve content via your custom protocol instead of `file://`.

See [examples/navigation-protocols.md](examples/navigation-protocols.md) for deep link validation, safe `shell.openExternal()`, and custom protocol handler patterns.

</patterns>

---

<decision_framework>

## Decision Framework

### Fuse Selection

```
For each fuse, decide based on your app's needs:

RunAsNode
+-- Does your app need ELECTRON_RUN_AS_NODE?
|   +-- YES (rare -- testing tools only) --> Leave enabled
|   +-- NO (most apps) --> Disable (prevents living-off-the-land attacks)

EnableCookieEncryption
+-- Does your app store cookies?
|   +-- YES --> Enable (one-way transition -- cannot decrypt after enabling)
|   +-- NO --> Enable anyway (no downside, protects future use)

EnableNodeOptionsEnvironmentVariable
+-- Does your production app need NODE_OPTIONS?
|   +-- YES (extremely rare) --> Leave enabled
|   +-- NO --> Disable (prevents env-var code injection)

EnableNodeCliInspectArguments
+-- Does your production app need --inspect?
|   +-- YES (never in production) --> Leave enabled only for dev builds
|   +-- NO --> Disable (prevents debugger attachment)

EnableEmbeddedAsarIntegrityValidation
+-- Is your app packaged as ASAR?
|   +-- YES --> Enable (ALWAYS pair with OnlyLoadAppFromAsar)
|   +-- NO --> Not applicable

OnlyLoadAppFromAsar
+-- Is ASAR integrity validation enabled?
|   +-- YES --> Enable (prevents bypass via unpacked app folder)
|   +-- NO --> Enable anyway (prevents loading tampered code)

GrantFileProtocolExtraPrivileges
+-- Does your app serve content via file:// protocol?
|   +-- YES --> Migrate to custom protocol, then disable
|   +-- NO --> Disable (removes file:// fetch and frame escalation)
```

### CSP Strategy

```
What content does your renderer load?
+-- Only local files (bundled with app)?
|   +-- Use: default-src 'self'; script-src 'self'
+-- Local files + CDN assets?
|   +-- Use: default-src 'self'; script-src 'self' https://cdn.example.com
+-- Remote content (web app in a window)?
|   +-- Use: restrictive CSP + sandbox: true + disable nodeIntegration
+-- Dev server with HMR?
    +-- Use: relaxed CSP in dev only, strict in production
```

</decision_framework>

---

**Detailed resources:**

- [examples/core.md](examples/core.md) -- Fuse reference table, ASAR integrity, webPreferences audit, fuse integration with build tools
- [examples/csp-permissions.md](examples/csp-permissions.md) -- Content Security Policy, permission handlers, session-level security
- [examples/navigation-protocols.md](examples/navigation-protocols.md) -- Navigation restrictions, deep link validation, custom protocols, shell.openExternal
- [reference.md](reference.md) -- Security checklist, fuse defaults table, version history

---

<red_flags>

## RED FLAGS

**Critical Security Issues:**

- Disabling `contextIsolation` (`contextIsolation: false`) -- exposes preload globals to renderer, enabling full preload scope access from untrusted code
- Enabling `nodeIntegration: true` -- gives renderer full Node.js access (`fs`, `child_process`, `net`), equivalent to giving a web page OS-level control
- Not flipping fuses before code signing -- fuses must be flipped before signing or the signature is invalidated; flipping after signing breaks the app on macOS
- Enabling `EnableEmbeddedAsarIntegrityValidation` WITHOUT `OnlyLoadAppFromAsar` -- attacker can bypass validation by placing an `app` folder next to the ASAR
- Leaving `RunAsNode` enabled in production -- allows `ELECTRON_RUN_AS_NODE=1 /path/to/your/app malicious-script.js` to execute arbitrary code
- Leaving `GrantFileProtocolExtraPrivileges` enabled when not using `file://` -- grants `file://` pages fetch access and universal frame access unnecessarily
- Passing unvalidated URLs to `shell.openExternal()` -- can execute arbitrary commands via `file://` or custom protocol URLs

**Medium Priority Issues:**

- Missing `Content-Security-Policy` in renderer HTML -- XSS attacks can inject and execute arbitrary scripts
- No `setPermissionRequestHandler` -- Electron grants camera, microphone, geolocation by default
- Not blocking navigation (`will-navigate` unhandled) -- renderer can navigate to phishing pages
- Using `'unsafe-eval'` in CSP -- enables `eval()`, `new Function()`, and template injection
- Disabling `webSecurity` in production (`webSecurity: false`) -- disables same-origin policy entirely
- Setting `allowRunningInsecureContent: true` -- allows HTTP content on HTTPS pages

**Gotchas & Edge Cases:**

- Cookie encryption is a one-way transition -- once enabled, existing unencrypted cookies become unreadable; plan migration carefully
- ASAR integrity is not encryption -- it prevents tampering but a determined attacker can extract, modify, and repackage; keep sensitive logic server-side
- `setPermissionCheckHandler` and `setPermissionRequestHandler` serve different purposes -- you need both for complete coverage (sync checks vs async requests)
- `setWindowOpenHandler` replaces the deprecated `new-window` event -- using the old event does nothing in recent Electron versions
- Development CSP may need `'unsafe-inline'` for bundler-injected scripts -- scope this to dev builds only, never ship it
- `strictlyRequireAllFuses: true` in `@electron/fuses` will fail if a new fuse is added in a future Electron version and you haven't configured it -- useful for staying current but breaks builds on Electron upgrades until you update config
- `resetAdHocDarwinSignature` must be `true` for arm64 macOS builds when not immediately code-signing afterward -- without it, the app fails to launch on Apple Silicon
- ASAR integrity validation on Windows requires Electron 30+ -- earlier versions only support macOS

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST flip fuses BEFORE code signing -- the OS enforces fuse state after signing, so flipping after signing invalidates the signature)**

**(You MUST disable `RunAsNode`, `EnableNodeOptionsEnvironmentVariable`, `EnableNodeCliInspectArguments`, and `GrantFileProtocolExtraPrivileges` fuses in production builds -- these are the most commonly exploited attack vectors)**

**(You MUST enable both `EnableEmbeddedAsarIntegrityValidation` AND `OnlyLoadAppFromAsar` together -- enabling integrity validation alone still allows bypassing via the app code search path)**

**(You MUST NOT override security defaults (`contextIsolation: true`, `sandbox: true`, `nodeIntegration: false`) -- each one unlocks a critical attack surface)**

**(You MUST restrict permissions via `session.setPermissionRequestHandler()` -- Electron grants most permissions by default, including camera, microphone, and geolocation)**

**Failure to follow these rules will create exploitable security vulnerabilities in your Electron application.**

</critical_reminders>
