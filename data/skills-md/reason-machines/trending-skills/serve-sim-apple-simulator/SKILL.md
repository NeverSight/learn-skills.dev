---
name: serve-sim-apple-simulator
description: Host Apple iOS Simulators in the browser with MJPEG streaming, touch/gesture control, and AI agent integration via npx serve-sim.
triggers:
  - serve iOS simulator in browser
  - stream apple simulator
  - host simulator for AI agent
  - npx serve-sim setup
  - simulator preview server
  - connect simulator to Claude or Cursor
  - embed simulator in dev server
  - simulator MJPEG stream
---

# serve-sim — Apple Simulator Hosting Tool

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

`serve-sim` is the `npx serve` of Apple Simulators. It spawns a Swift helper that captures a booted iOS Simulator's framebuffer via `simctl io`, exposes it as an MJPEG stream + WebSocket control channel, and serves a React preview UI in your browser. Works with any booted iOS Simulator — no Xcode plugin, no app instrumentation required.

## Requirements

- macOS with Xcode command line tools installed (`xcrun simctl` must be available)
- At least one booted iOS Simulator
- Node.js / npm (for `npx`)

## Quick Start

```sh
# Start preview server (auto-detects booted simulator)
npx serve-sim
# → Preview at http://localhost:3200
```

## CLI Reference

```sh
serve-sim [device...]                 # Start preview server (default: localhost:3200)
serve-sim --no-preview [device...]    # Stream only, no web UI
serve-sim gesture '<json>' [-d udid]  # Send a touch gesture
serve-sim button [name] [-d udid]     # Send a button press (default: home)
serve-sim rotate <orientation> [-d udid]
serve-sim ca-debug <option> <on|off> [-d udid]
serve-sim memory-warning [-d udid]    # Simulate a memory warning

# Options
-p, --port <port>   Starting port (preview default: 3200, stream default: 3100)
-d, --detach        Spawn helper and exit (daemon mode)
-q, --quiet         JSON-only output
    --no-preview    Skip the web UI; stream in foreground only
    --list [device] List running streams
    --kill [device] Kill running stream(s)
```

### Common CLI Examples

```sh
# Target a specific device by name
serve-sim "iPhone 16 Pro"

# Start on a custom port
serve-sim -p 4000

# Start as background daemon, returns JSON with stream info
serve-sim --detach

# List all running streams
serve-sim --list

# Kill all running helpers
serve-sim --kill

# Send home button press
serve-sim button home -d <udid>

# Rotate simulator
serve-sim rotate landscape_left -d <udid>
# orientations: portrait | portrait_upside_down | landscape_left | landscape_right

# Toggle CoreAnimation debug flags
serve-sim ca-debug slow-animations on -d <udid>
# options: blended | copies | misaligned | offscreen | slow-animations

# Simulate memory warning
serve-sim memory-warning -d <udid>

# Multiple simulators at once
serve-sim "iPhone 16 Pro" "iPad Pro"

# Send a touch gesture (JSON format)
serve-sim gesture '{"type":"tap","x":200,"y":400}' -d <udid>
```

## Features

- 60 FPS MJPEG video stream in browser
- Touch, swipe, pinch (hold Option key) gestures
- Keyboard input and hotkeys forwarded to simulator (CMD+SHIFT+H = home)
- Simulator logs forwarded to browser
- Drag and drop images/videos onto simulator
- Apple Watch, iPad, and iOS support
- Connect-style middleware for embedding in existing dev servers

## Architecture

```
┌──────────────┐   simctl io   ┌─────────────────┐  MJPEG / WS  ┌─────────┐
│ iOS Simulator│ ────────────► │ serve-sim-bin   │ ───────────► │ Browser │
└──────────────┘   (Swift)     │ (per-device)    │              └─────────┘
                               └─────────────────┘
                                       ▲
                                  state file in
                                $TMPDIR/serve-sim/
                                       ▲
                               ┌──────────────────┐
                               │ serve-sim CLI /  │
                               │ middleware       │
                               └──────────────────┘
```

State files are written to `$TMPDIR/serve-sim/`. The Swift binary is bundled in the npm package — no separate Xcode build needed at runtime.

## Integration Patterns

### Claude Code Desktop

Create `.claude/launch.json` in your project root:

```json
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "ios",
      "runtimeExecutable": "npx",
      "runtimeArgs": ["serve-sim"],
      "port": 3200
    }
  ]
}
```

Claude will automatically start the simulator preview when you open the project.

### Expo / Metro Dev Server

Customize `metro.config.js` to embed serve-sim at `http://localhost:8081/.sim`:

```js
// metro.config.js
const { getDefaultConfig } = require("expo/metro-config");
const connect = require("connect");
const { simMiddleware } = require("serve-sim/middleware");

/** @type {import('expo/metro-config').MetroConfig} */
const config = getDefaultConfig(__dirname);

config.server = config.server || {};
const originalEnhanceMiddleware = config.server.enhanceMiddleware;

config.server.enhanceMiddleware = (metroMiddleware, server) => {
  const middleware = originalEnhanceMiddleware
    ? originalEnhanceMiddleware(metroMiddleware, server)
    : metroMiddleware;

  const app = connect();
  app.use(simMiddleware({ basePath: "/.sim" }));
  app.use(middleware);
  return app;
};

module.exports = config;
```

Then run `npx expo start` — simulator preview available at `http://localhost:8081/.sim`.

### Express / Connect Dev Server

```ts
import express from "express";
import { simMiddleware } from "serve-sim/middleware";

const app = express();

// First start the helper in daemon mode
// $ npx serve-sim --detach

app.use(simMiddleware({ basePath: "/.sim" }));

app.listen(3000, () => {
  console.log("Dev server at http://localhost:3000");
  console.log("Simulator preview at http://localhost:3000/.sim");
});
```

### Vite Dev Server

```ts
// vite.config.ts
import { defineConfig } from "vite";
import { simMiddleware } from "serve-sim/middleware";

export default defineConfig({
  server: {
    middlewareMode: false,
  },
  plugins: [
    {
      name: "serve-sim",
      configureServer(server) {
        // Start helper first: npx serve-sim --detach
        server.middlewares.use("/.sim", simMiddleware({ basePath: "/.sim" }));
      },
    },
  ],
});
```

### Next.js Custom Server

```ts
// server.ts
import { createServer } from "http";
import { parse } from "url";
import next from "next";
import { simMiddleware } from "serve-sim/middleware";

const dev = process.env.NODE_ENV !== "production";
const app = next({ dev });
const handle = app.getRequestHandler();
const simHandler = simMiddleware({ basePath: "/.sim" });

app.prepare().then(() => {
  createServer((req, res) => {
    const parsedUrl = parse(req.url!, true);
    if (parsedUrl.pathname?.startsWith("/.sim")) {
      return simHandler(req, res, () => handle(req, res, parsedUrl));
    }
    handle(req, res, parsedUrl);
  }).listen(3000);
});
```

## Middleware API

```ts
import { simMiddleware } from "serve-sim/middleware";

// Mount options
simMiddleware({
  basePath: "/.sim",  // URL prefix for all serve-sim routes
});

// Middleware exposes:
// GET  /.sim        → Preview HTML UI
// GET  /.sim/api    → State JSON (connected devices, stream URLs)
// GET  /.sim/logs   → SSE log stream from simulator
```

The middleware reads state from `$TMPDIR/serve-sim/` and proxies the browser to the live MJPEG + WebSocket endpoints. CORS is open on the helper, so no additional proxy config is needed.

## Daemon / Detach Mode

Use `--detach` to start the helper as a background process and get JSON output for scripting:

```sh
# Start daemon and capture JSON output
STREAM_INFO=$(npx serve-sim --detach --quiet)
echo $STREAM_INFO
# {"udid":"...","mjpeg":"http://localhost:3100/stream","ws":"ws://localhost:3100/control"}

# List running streams as JSON
npx serve-sim --list --quiet

# Kill specific device stream
npx serve-sim --kill "iPhone 16 Pro"

# Kill all streams
npx serve-sim --kill
```

## Programmatic Usage (TypeScript)

```ts
import { simMiddleware } from "serve-sim/middleware";
import connect from "connect";

const app = connect();

// Attach middleware — requires serve-sim helper already running (--detach)
app.use(
  simMiddleware({
    basePath: "/.sim",
  })
);

export default app;
```

## Gesture JSON Format

When using `serve-sim gesture '<json>'`:

```sh
# Tap at coordinates
serve-sim gesture '{"type":"tap","x":200,"y":400}' -d <udid>

# Swipe gesture
serve-sim gesture '{"type":"swipe","startX":200,"startY":800,"endX":200,"endY":200,"duration":0.3}' -d <udid>
```

## Development Setup

```sh
git clone https://github.com/EvanBacon/serve-sim
cd serve-sim
bun install

# Build JS bundles
bun run --filter serve-sim build

# Rebuild Swift helper binary
bun run --filter serve-sim build:swift

# Watch mode for development
bun run --filter serve-sim dev
```

## Troubleshooting

**No simulator detected**
```sh
# Check booted simulators
xcrun simctl list devices booted

# Boot a simulator if none running
xcrun simctl boot "iPhone 16 Pro"
```

**Port already in use**
```sh
# Use a different port
serve-sim -p 4200

# Kill existing helpers first
serve-sim --kill
```

**Stream not appearing in middleware**
```sh
# Ensure helper is running first
serve-sim --detach

# Verify state files exist
ls $TMPDIR/serve-sim/

# Check running streams
serve-sim --list
```

**Swift binary not found / won't execute**
```sh
# Ensure Xcode CLT are installed
xcode-select --install

# Verify simctl works
xcrun simctl list
```

**Multiple simulators — wrong device targeted**
```sh
# List all booted simulators with UDIDs
xcrun simctl list devices booted

# Target by UDID explicitly
serve-sim -d <udid>
```

**Rebuild Swift helper if binary is stale**
```sh
bun run --filter serve-sim build:swift
```
