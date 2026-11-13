---
name: netlify-server
description: Build and deploy a long-lived Node.js backend on Netlify Server (Early Access) from netlify/server/index.ts. Use this skill whenever someone wants to run an Express, Fastify, Hono or Koa app on Netlify as it is, add a backend or REST/GraphQL API that keeps database pools and caches warm, build real-time features such as chat, live dashboards or multiplayer with WebSockets or Server-Sent Events, or stream AI responses and run agent loops. It also covers background work after responding with waitUntil, startup and graceful shutdown hooks, load-aware health checks, edge caching of server responses, region/size/scale settings, local testing with netlify dev, reading server logs with netlify logs or log drains, and debugging a server that gets no requests, fails to start, drops database connections after a minute, or returns 429/500/501/502.
---

# Netlify Server

Early Access, so APIs may change. It is available on credit-based plans and on Enterprise plans with credits enabled. It requires **Node.js 24+** for both build and local dev, and **Netlify CLI 27.17.0+** for both local dev and deploys.

It is free during Early Access and intended for evaluation, experimentation, and low-volume production use. At GA it will bill credits for reserved memory (GB-hours) and active CPU (vCPU-hours). **Every request the server handles already counts toward the web requests meter.**

## Reach for this / avoid this

```ts
// ✅ netlify/server/index.ts — handler (same signature as Netlify Functions)
import type { Context, Config } from "@netlify/server";
export default async (req: Request, context: Context) =>
  new Response(`Hello from ${context.geo.city ?? "somewhere"}`);
export const config: Config = { path: "/api/*" };
```

```js
// ✅ Fetchable app (Hono etc.): export as is
export default app;
// ✅ Node request listener: wrap it, do NOT call listen(). WebSockets work.
export default createServer(handleRequest);
// ✅ Framework that starts itself (Express/Fastify): listen on PORT within 10 s
app.listen(process.env.PORT);
```

```js
// ❌ export default (req, res) => {...}   // two params = treated as a fetch handler, breaks
// ❌ export default expressApp            // works, but WebSocket upgrades get 501
// ❌ server.close(() => process.exit(0))  // cuts off shutdown hooks and background work
// ❌ setInterval / fire-and-forget promise // invisible to Netlify; the instance can stop mid-work
```

You don't configure ports, add health endpoints, or install adapters. Install the package with `npm install @netlify/server`.

## Entry file and detection

- Use **one** server per project: `netlify/server/index.ts`, `.mts`, `.js`, or `.mjs`. **The build fails if more than one exists.**
- Startup runs once per instance:
  1. `PORT` is set.
  2. The entry file is imported, running top-level code (top-level `await` is awaited).
  3. `onStart` hooks run in order.
  4. The default export is inspected.
- No traffic arrives until all steps finish. Any throw fails the start.

Netlify uses the **first matching row** for the default export:

| Default export | Run as | WebSockets |
|---|---|---|
| `http.Server` without `listen()` | Requests sent to it | `upgrade` event (`ws`, Socket.IO) |
| Object with `fetch` (Fetchable, e.g. Hono) | `fetch(request, context)` | `upgradeWebSocket` |
| Express/Connect app, or a function with ≥3 params | Wrapped in its own HTTP server | **501** |
| Any other function | `(request, context) => Response` | `upgradeWebSocket` |
| Anything else / nothing | Waits for your code to listen | `upgrade` event |

> ⚠️ **Self-started servers must listen within 10 s after start hooks finish.**
> - If your code starts several servers, the one on `process.env.PORT` wins. If none listens on it, the start fails.
> - Reserved ports are `53` and `15000–15099`.
> - Only Node.js HTTP servers are supported, not raw TCP.

Create shared resources such as a DB pool at top level so they are reused across requests.

> ⚠️ **Outbound connections are closed after 60 s without data in either direction.** TCP keepalives don't count.
> - Set your pool's idle timeout **below 60 s** (e.g. `idleTimeoutMillis: 30_000`), or it hands out dead connections.
> - Quiet connections such as Postgres `LISTEN` need traffic at least every 60 s (e.g. `SELECT 1`), or must reconnect on close. The symptom is `Connection terminated unexpectedly`.

## Examples

```js
// netlify/server/index.mjs — Express, self-started
import express from "express";
import { getContext } from "@netlify/server";
const app = express();
app.get("/api/hello", (req, res) => {
  const { geo } = getContext();
  res.json({ message: `Hello from ${geo.city ?? "somewhere"}` });
});
app.listen(process.env.PORT || 3000);
```

```js
// Fastify
const app = Fastify();
app.get("/api/hello", async () => ({ message: `Hello from ${getContext().geo.city ?? "somewhere"}` }));
await app.listen({ port: Number(process.env.PORT) || 3000 });
```

### Background work after responding

```ts
export default async (req: Request, context: Context) => {
  const order = await saveOrder(await req.json());
  context.waitUntil(sendConfirmationEmail(order)); // keeps the instance alive until settled
  return Response.json(order, { status: 201 });
};
// In frameworks: const { waitUntil } = getContext();
```

How `waitUntil` behaves:
- It is not bound by the request duration limit.
- Rejections are logged.
- On replacement, background work gets up to 90 s. Persist critical work to Netlify Database or Netlify Blobs.

### WebSockets (handler/Fetchable)

```ts
import { upgradeWebSocket } from "@netlify/server";
export default async (req: Request) => {
  if (req.headers.get("upgrade") === "websocket") {
    const { socket, response } = upgradeWebSocket(req, { idleTimeout: 30 }); // pings off unless set
    socket.onmessage = (e) => socket.send(`Echo: ${e.data}`);
    return response; // return as is
  }
  return new Response("Connect with a WebSocket client");
};
```

### WebSockets (`ws` on a self-started server)

```js
const server = app.listen(process.env.PORT);
const wss = new WebSocketServer({ server });
wss.on("connection", (ws) => ws.on("message", (d) => ws.send(d)));
// On shutdown, close wss.clients yourself. getWebSockets() doesn't include them.
```

### Server-Sent Events / streaming

```ts
export default async () => {
  const enc = new TextEncoder(); let t: ReturnType<typeof setInterval>;
  const stream = new ReadableStream({
    start(c) { t = setInterval(() => c.enqueue(enc.encode(`data: ${new Date().toISOString()}\n\n`)), 1000); },
    cancel() { clearInterval(t); },
  });
  return new Response(stream, { headers: { "content-type": "text/event-stream" } });
};
```

### Client reconnect

Browser `WebSocket` doesn't reconnect on its own; `EventSource` does.

```js
function connect() {
  const s = new WebSocket("wss://example.com/api/chat");
  s.addEventListener("close", (e) => setTimeout(connect, e.code === 1012 ? 0 : 1000));
  return s;
}
```

### Lifecycle hooks

```ts
import { onStart, onShutdown, onHealthCheck, getWebSockets } from "@netlify/server";

onStart(async () => { await db.connect(); }); // in order; rejection = start fails

onShutdown(async ({ drained }) => {           // all hooks run in parallel
  queue.stop();
  for (const s of getWebSockets()) s.close(1012, "Server restarting");
  await drained;                              // never rejects
  await pool.end();                           // close resources only after drained
});

onHealthCheck(() => ({                        // load signal, not health
  utilization: { db_pool: (pool.totalCount - pool.idleCount) / pool.options.max }, // 0–1
  namedMetrics: { db_pool_waiting: pool.waitingCount },  // observability only
}), { interval: 1000 });                      // default and minimum 1000 ms
```

Hook rules:
- `onStart` must be called while the entry file loads. **Calling it later throws.**
- `getContext()` **throws outside a request**, including at top level and inside hooks.
- In health reports, `event_loop` and `memory` are reserved keys. `applicationUtilization` (0–1) overrides the max entry.
- A health hook that throws never stops the instance. Health hooks don't run locally.

### Edge caching

**Responses are never cached unless you set headers.**

```ts
return Response.json(data, { headers: { "Netlify-CDN-Cache-Control": "public, max-age=3600, durable" } });
// Express: res.set(...)  Hono: c.header(...)  Fastify: reply.header(...)
```

Supported features:
- `stale-while-revalidate`
- Cache keys varied by query, header, language, country, or cookie
- Invalidation by site or cache tag

Each deploy invalidates the previous cache.

## Context (`context` arg or `getContext()`)

- `geo`: `city`, `country{code,name}`, `subdivision{code,name}`, `latitude`, `longitude`, `postalCode`, `timezone`.
- `ip` (same as `req.socket.remoteAddress` / `req.ip`), `url` (`URL`), `requestId`.
- `cookies.get(name)` / `.set(options)` / `.delete(name|options)` follow CookieStore semantics.
- `deploy`: `id`, `branch`, `context`, `published`, `skewProtectionToken`.
- `site`: `id`, `name`, `url`. `account.id`. `server.region`.
- `user`: `{ id, email, expiresAt }` on private projects or with team login protection, otherwise `undefined`.
- `waitUntil(promise)`.

Types: `Config`, `Context`, `HealthReport`, `HealthCheckHook`, `HealthCheckOptions`, `LifecycleHook`, `ShutdownHook`, `ShutdownContext`, `ServerRegion`, `ServerSize`, `UpgradeWebSocketOptions`, `WebSocketUpgrade`.

## Configuration

Set config with `export const config: Config` in the entry file (or `config` on a default-exported Fetchable), or in `netlify.toml`. **The entry file wins per setting.** Unknown keys or invalid values **fail the build**.

```toml
[server]
  region = "fra"
  size = "medium"
[server.scale]
  max = 2
```

| Key | Values / default |
|---|---|
| `path` | One or more paths starting with `/`. Same syntax as [function paths](https://docs.netlify.com/build/functions/configuration/#routing). Default `/*` |
| `excludedPath` | Paths handed back to the rest of the project, e.g. `["/legacy/*", "/status"]` |
| `region` | `cmh` (US East Ohio, default) or `fra` (Frankfurt). Also settable in the UI under **Server → Region**, but a `netlify.toml` region overrides it. Changes apply on the next deploy |
| `size` | `small` (1 GB, shared vCPU, 512 MB disk, 32 concurrent requests, default); `medium` (2 GB/1 vCPU/1 GB/64); `large` (4 GB/2 vCPU/2 GB/128). Free/Personal plans can use `small` only |
| `scale` | `{ min, max }`. **`min` must be 0** in Early Access. `max` ≤ 3, or 1 on Free/Personal. Higher values fail the deploy |
| `includedFiles` | Globs for files read at runtime. Entry-file globs are relative to the entry file and **replace** the toml list. Read them via `import.meta.dirname`, never `process.cwd()` |

Other settings:
- **Environment variables:** use `process.env` with variables scoped to **Functions**. Values are fixed at deploy time, so **redeploy after changes**.
- **Filesystem:** read-only except `/tmp`, which is per-instance and wiped on stop.

## Routing

Requests are handled in this order:
1. Edge functions
2. Redirects/rewrites
3. Static files
4. Functions
5. The server, which owns its own 404s

> ⚠️ **Server gets no requests?** Check these causes:
> - An SPA catch-all `/* /index.html 200` swallows everything. Scope it to frontend paths.
> - A static file or function already occupies the same path. **Static files always win.**
> - `path`/`excludedPath` excludes the path.
> - `/.netlify/server/` is reserved.
> - **Full-stack frameworks** (Next.js, Astro, Nuxt, SvelteKit, React Router, TanStack Start) don't run on Netlify Server. Their adapters claim every path, so don't add a server to those projects.

Choosing between options:
- Use a server for a new backend.
- Use [scheduled functions](https://docs.netlify.com/build/functions/scheduled-functions/) for cron jobs and webhooks.
- Use edge functions for logic close to visitors.
- Functions are cheaper for rarely used backends, because instances idle for 5 min before stopping.

## Instances and lifecycle

**Assume multiple instances.** They overlap during deploys and are replaced every 8 h, and memory and `/tmp` are per-instance. Practical consequences:
- In-memory state is a cache. Put shared data in Netlify Database or Netlify Blobs.
- Each instance holds its own WebSocket connections.
- Once-only work can run twice or never. Use a scheduled function and record completion.

Scaling and limits:
- **Concurrency:** depends on size: 32 (`small`), 64 (`medium`), or 128 (`large`) requests per instance. Each open SSE/stream holds one of those slots. WebSockets don't use these slots. They have a separate limit of a couple of hundred per instance, and an instance full of WebSockets still serves ordinary requests.
- **Routing:** new requests go to the least-loaded instance, judged by event loop, memory, and health hooks.
- **Scale to zero:** an instance stops after 5 min idle. Open requests, WS/SSE connections, and `waitUntil` work pause the timer; `setInterval` does not.
- **Cold starts:** the first request waits for the entry file and start hooks. **That time counts toward the 20 s response timeout.** Lazy-init route-specific services and keep dependencies small.

Shutdown sequence:
1. New traffic stops.
2. `SIGTERM` is sent.
3. Your server stops accepting connections.
4. Shutdown hooks start.
5. In-flight work and connections get up to **90 s**.
6. Hooks get up to **115 s** from their start (at least 25 s after work ends).
7. Remaining connections are force-closed.

Close sockets with code `1012` in `onShutdown` so clients move immediately.

**Deploys:**
- A production deploy publishes only after its new server has started. If the server fails to start, the deploy isn't published and the old one keeps serving.
- Rollback rolls back the server too.
- Deploy Previews and branch deploys start their server on first request. That request is a cold start, so slow startup can turn it into a 502.

## Limits

| Limit | Value |
|---|---|
| Response timeout | **20 s to send status + headers, else 502. Cold-start time is included.** Stream the body, or respond and finish with `waitUntil` |
| Request duration (incl. WS/SSE) | 30 min; 2 h on Pro, Business, and Enterprise |
| Outbound connections | Closed after 60 s idle; keepalives don't count |
| Instance lifetime | 8 h |
| Instances | 3 (credit-based Pro/Enterprise); 1 (Free/Personal) |

## Errors

| Status | Meaning / fix |
|---|---|
| 429 | All concurrency slots (32/64/128 by size) are full at max instances. Long SSE streams are often the cause |
| 500 | The instance failed to start (top-level/start hook threw, or no listen on PORT within 10 s), or the handler threw |
| 501 | WebSocket upgrade on a directly exported Express/Connect app. Use `listen()` or `createServer` |
| 502 | No headers within 20 s (including cold start), or the instance crashed/OOM'd |

## Local dev and logs

**Local dev:**
- Run `netlify dev` (CLI 27.17.0+). The **Netlify Vite plugin doesn't run the server.**
- The CLI restarts the server on changes inside `netlify/server/` only. Restart the CLI for changes elsewhere.
- Local differences from production:
  - Single instance.
  - `path`/`excludedPath` ignored.
  - No limits enforced.
  - 5 s shutdown.
  - No `SIGTERM` on Windows.
  - No health hooks.
- For E2E tests, use `@netlify/dev`: `new NetlifyDev({ projectRoot, server: { enabled: true } })`, then `start()` / `stop()`.

**Monitoring and logs:**
- Use the **Server** page under **Cloud compute**. It opens in Live mode (last hour) and shows production by default, and you can switch branches to see branch deploys or Deploy Previews.
  - **Overview:** requests/errors, p95 latency, memory, CPU, and saturation.
  - **Instances table:** state, start reason, and failed-start warnings.
  - **Requests view:** cold start, queue wait, and **Open in Observability**.
  - **Logs view.**
- Per-request views are also in [observability](https://docs.netlify.com/manage/monitoring/observability/overview/).
- Use `console.*` inside a request to attach the `requestId`. Direct `process.stdout` writes aren't linked to requests.

**CLI and log drains:**

```bash
netlify logs                                # server + functions + edge functions, last 10 min
netlify logs --source server --since 30m    # server only; --until ends the window
netlify logs --source server --follow       # stream lines as written
```

- `--level` and `--json` work. **`--deploy-id` and `--url` don't work with server logs**, because they can't be filtered by deploy.
- Long windows show only the most recent lines. Narrow `--since`/`--until` to see older ones.
- For [log drains](https://docs.netlify.com/manage/monitoring/log-drains/#configure-a-log-drain), select **Server logs** as a log type.

<!-- Gaps: instance cap, medium/large size availability, and scale.max default for Business plans are not documented. -->
<!-- Exact per-instance WebSocket limit, netlify.toml spelling of excludedPath/includedFiles, and GA credit rates are unstated. -->

<!-- system: agent-context/server/system.md — human-owned, merged by ctx-gen; edit system.md, not this section -->
# Netlify house rules (server)

These are org conventions, not docs facts — they are merged into the rendered
skill by ctx-gen and are never generated. Owned by the Netlify Server team.

1. Never keep a server alive on purpose: no self-pings, no `setInterval` or
   scheduled function that calls the server, no `waitUntil` chain that
   schedules more work to stay running. Scale to zero is the design. If the
   user asks for an always-on server, explain this and build without it.
2. Run scheduled work with a scheduled function that calls a server route,
   never with timers inside the server.
3. An endpoint that fetches a URL the user supplies must resolve the hostname
   and refuse loopback, private, link-local and unique-local addresses
   (including 169.254.169.254), re-check after every redirect, and return only
   what the feature needs. Never build a generic `/proxy?url=` endpoint or
   forward the caller's method, headers or body — that is an open relay.
4. Process memory is lost on every scale-to-zero, deploy and platform
   maintenance event. In-memory caches are fine; anything that must survive
   belongs in Netlify Blobs or Netlify Database.
5. Don't detach child processes; they are killed on scale-to-zero. Keep work
   in-process with `waitUntil`, or use a background function.
