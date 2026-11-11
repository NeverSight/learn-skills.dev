---
name: electrobun-best-practices
description: Use when building or maintaining Electrobun desktop apps in TypeScript, including electrobun.config.ts, electrobun/bun or electrobun/view imports, BrowserWindow/BrowserView usage, updater flows, and distribution artifacts.
---

# Electrobun Best Practices

Electrobun builds cross-platform desktop apps with TypeScript and Bun. This skill gives safe defaults, typed RPC patterns, and operational guidance for build/update/distribution.

Docs: https://blackboard.sh/electrobun/docs/

## Pair with TypeScript Best Practices

Always load `typescript-best-practices` alongside this skill.

## Version and Freshness

Electrobun APIs evolve quickly. Before relying on advanced options or platform-specific behavior, verify against current docs and CLI output.

## Architecture

Electrobun apps run as Bun apps:
- Bun process (main): imports from `electrobun/bun`
- Browser context (views): imports from `electrobun/view`
- Shared types: RPC schemas shared between both contexts

IPC between bun and browser contexts uses postMessage, FFI, and (in some paths) encrypted WebSockets.

## Quick Start

```bash
bunx electrobun init
bun install
bun start
```

Recommended scripts:

```json
{
  "scripts": {
    "start": "electrobun run",
    "dev": "electrobun dev",
    "dev:watch": "electrobun dev --watch",
    "build:dev": "bun install && electrobun build",
    "build:canary": "electrobun build --env=canary",
    "build:stable": "electrobun build --env=stable"
  }
}
```

## Secure Defaults

Use this baseline for untrusted or third-party content:

```typescript
import { BrowserWindow } from "electrobun/bun";

const win = new BrowserWindow({
  title: "External Content",
  url: "https://example.com",
  sandbox: true,                  // disables RPC, events still work
  partition: "persist:external",
});

win.webview.setNavigationRules([
  "^*",                          // block everything by default
  "*://example.com/*",           // allow only trusted domain(s)
  "^http://*",                   // enforce HTTPS
]);

win.webview.on("will-navigate", (e) => {
  console.log("nav", e.data.url, "allowed", e.data.allowed);
});
```

Security checklist:
- Use `sandbox: true` for untrusted content.
- Apply strict navigation allowlists.
- Use separate `partition` values for isolation.
- Validate all `host-message` payloads from `<electrobun-webview>` preload scripts.
- Do not write to `PATHS.RESOURCES_FOLDER` at runtime; use `Utils.paths.userData`.

## Typed RPC (Minimal Pattern)

```typescript
// src/shared/types.ts
import type { RPCSchema } from "electrobun/bun";

export type MyRPC = {
  bun: RPCSchema<{
    requests: {
      getUser: { params: { id: string }; response: { name: string } };
    };
    messages: {
      logToBun: { msg: string };
    };
  }>;
  webview: RPCSchema<{
    requests: {
      updateUI: { params: { html: string }; response: boolean };
    };
    messages: {
      notify: { text: string };
    };
  }>;
};
```

```typescript
// bun side
import { BrowserView, BrowserWindow } from "electrobun/bun";
import type { MyRPC } from "../shared/types";

const rpc = BrowserView.defineRPC<MyRPC>({
  handlers: {
    requests: {
      getUser: ({ id }) => ({ name: `user-${id}` }),
    },
    messages: {
      logToBun: ({ msg }) => console.log(msg),
    },
  },
});

const win = new BrowserWindow({
  title: "App",
  url: "views://mainview/index.html",
  rpc,
});

await win.webview.rpc.updateUI({ html: "<p>Hello</p>" });
```

```typescript
// browser side
import { Electroview } from "electrobun/view";
import type { MyRPC } from "../shared/types";

const rpc = Electroview.defineRPC<MyRPC>({
  handlers: {
    requests: {
      updateUI: ({ html }) => {
        document.body.innerHTML = html;
        return true;
      },
    },
    messages: {
      notify: ({ text }) => console.log(text),
    },
  },
});

const electroview = new Electroview({ rpc });
await electroview.rpc.request.getUser({ id: "1" });
electroview.rpc.send.logToBun({ msg: "hello" });
```

## Events and Shutdown

Use `before-quit` for shutdown cleanup instead of relying on `process.on("exit")` for async work.

```typescript
import Electrobun from "electrobun/bun";

Electrobun.events.on("before-quit", async (e) => {
  await saveState();
  // e.response = { allow: false }; // optional: cancel quit
});
```

Important caveat:
- Linux currently has a caveat where some system-initiated quit paths (for example Ctrl+C/window-manager/taskbar quit) may not fire `before-quit`. Programmatic quit via `Utils.quit()`/`process.exit()` is reliable.

## Common Patterns

- Keyboard shortcuts (copy/paste/undo): define an Edit `ApplicationMenu` with role-based items.
- Tray-only app: set `runtime.exitOnLastWindowClosed: false`, then drive UX from `Tray`.
- Multi-account isolation: use separate `partition` values per account.
- Chromium consistency: set `bundleCEF: true` and `defaultRenderer: "cef"` in platform config.

## Troubleshooting

- RPC calls fail unexpectedly:
  - Check whether the target webview is sandboxed (`sandbox: true` disables RPC).
  - Confirm shared RPC types match both bun and browser handlers.
- Navigation blocks legitimate URLs:
  - Review `setNavigationRules` ordering; last match wins.
  - Keep `^*` first only when you intentionally run strict allowlist mode.
- Updater says no update:
  - Verify `release.baseUrl` and uploaded `artifacts/` naming (`{channel}-{os}-{arch}-...`).
  - Confirm channel/build env alignment (`canary` vs `stable`).
- User sessions leak across accounts:
  - Use explicit per-account partitions and manage cookies via `Session.fromPartition(...)`.
- Build hooks not running:
  - Ensure hook paths are correct and executable via Bun.
  - Inspect hook env vars (for example `ELECTROBUN_BUILD_ENV`, `ELECTROBUN_OS`, `ELECTROBUN_ARCH`).

## Reference Files

- Build config, artifacts, and hooks: [reference/build-config.md](reference/build-config.md)
- BrowserWindow, BrowserView, and webview tag APIs: [reference/window-and-webview.md](reference/window-and-webview.md)
- Menus, tray, events, updater, utils/session APIs: [reference/platform-apis.md](reference/platform-apis.md)
