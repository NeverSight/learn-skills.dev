---
name: visual-feedback-loop
description: "AI agent visual feedback loop for any web app. Use when iterating on visual code (UI, canvas, 3D, SVG, charts, animations) and you need to SEE the rendered result to evaluate quality. Covers: dev-screenshot API pattern (GET trigger → SSE → client capture → POST back → file saved), parameterized rendering, metadata sidecars, visual regression with pixel diff, WebMCP tool registration, and console fallbacks. Activate on: 'take a screenshot', 'show me the render', 'visual QA', 'compare before/after', 'pixel diff', or any iterative visual work where the agent needs to inspect rendered output."
---

# Visual Feedback Loop

Capture, inspect, and compare visual output from a running web app during iterative development.

## How It Works

```
Agent (CLI)                     Server                            Browser
     |--- GET /api/dev-screenshot -->|--- SSE "capture" ----------->|
     |    ?param=value               |                              |-- capture canvas
     |                               |<-- POST { dataUrl } ---------|
     |                               | writes:
     |                               |   .screenshots/{UTC}.webp
     |                               |   .screenshots/{UTC}.json  (metadata)
     |                               |   .screenshots/latest.webp (convenience copy)
     |<-- { ok, path, latest } ------|
```

Agent can't access the browser directly. Server relays: GET triggers → SSE notifies browser → browser captures and POSTs back → GET resolves.

## Usage

Capture current view:
```bash
curl http://localhost:3000/api/dev-screenshot
```

Capture with params (app-specific — browser client interprets them):
```bash
curl 'http://localhost:3000/api/dev-screenshot?component=header&theme=dark'
curl 'http://localhost:3000/api/dev-screenshot?letter=б&depth=0.8'
```

Then read the result. Response includes `path` (timestamped file) and `latest` (convenience copy):
```
Read .screenshots/latest.webp
```

### Visual Regression (pixel diff)

Compare against a ground truth screenshot using ImageMagick:
```bash
magick compare -metric RMSE .screenshots/ground-truth.webp .screenshots/latest.webp .screenshots/diff.webp
```

RMSE output: `0.01` = ~1% difference (rendering noise), `0.03+` = visible change. Save diff image for inspection.

### Metadata Sidecars

Each screenshot gets a JSON sidecar with the same UTC timestamp:
```json
{
  "timestamp": "2026-02-25T08:22:12.655Z",
  "git": { "commit": "0a5726f", "dirty": true },
  "params": { "letter": "о", "chamferModel": "membrane", "cameraView": "front" },
  "format": "webp",
  "file": "2026-02-25T08-22-12-655Z.webp"
}
```

Use this to trace which code state + params produced a screenshot — critical when iterating across multiple code changes.

### A/B Comparison Workflow

1. Capture ground truth: `curl '...?letter=о'` → note the `{UTC}.webp` filename
2. Make code changes, refresh browser
3. Capture again: `curl '...?letter=о'`
4. Diff: `magick compare -metric RMSE .screenshots/{ground-truth}.webp .screenshots/latest.webp .screenshots/diff.webp`
5. Read diff image + check RMSE value

Console fallback: `await window.__takeDevScreenshot()`

## Rules

1. **Always `Read .screenshots/latest.webp` after capture.** Never assume the render is correct.
2. **Browser tab must be open** at the app URL. Timeout = no SSE connection = ask user to refresh.
3. **One request at a time.** Second GET returns 409. Wait for first to resolve (success/error/10s timeout).
4. **Errors return instantly**, not as timeouts. Client POSTs errors back: `{ ok: false, error: "..." }`.
5. **HMR resilience.** Store server-side SSE state on `globalThis` so it survives module reloads. EventSource auto-reconnects on the client. If screenshots still fail after code changes, ask user to refresh.
6. **HMR does NOT update offscreen render paths.** Closures in `useEffect` capture stale module references. After code changes to rendering logic, always ask user to **hard refresh** (Cmd+Shift+R on macOS, Ctrl+Shift+R on Windows/Linux).

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Timeout: browser did not respond | Open/refresh app in browser |
| 409: already in progress | Wait for timeout (10s) |
| Black/empty image | Refresh browser tab |
| Works once, then times out | HMR broke SSE — refresh tab (rare if using globalThis pattern) |
| Code changes not reflected in screenshots | HMR doesn't update offscreen renderers — hard refresh (Cmd+Shift+R on macOS, Ctrl+Shift+R on Windows/Linux) |
| Comparing screenshots from different code states | Check JSON sidecar for git commit + dirty flag |

See [references/errors.md](references/errors.md) for full error reference.

## Setup

The pattern is framework-agnostic — it only requires an HTTP server with GET/POST routes and SSE. The reference implementation uses Next.js, but the same approach works with Express, Fastify, Hono, Vite dev server plugins, or any Node.js HTTP server.

See [references/setup-nextjs.md](references/setup-nextjs.md) for a complete Next.js implementation (API route, SSE listener, WebMCP registration). Adapt the route handler to your framework — the client-side SSE listener and capture logic are identical regardless of server framework.
