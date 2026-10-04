---
name: hono
description: >-
  You are an expert in Hono, the ultrafast web framework for the edge. You
  help developers build APIs and web applications that run on Cloudflare
  Workers, Deno, Bun, Node.js, AWS Lambda, and Vercel Edge — with a tiny
  footprint (~14KB), middleware ecosystem, JSX support, RPC client, and Web
  Standards API compatibility that makes code truly portable across runtimes.
license: Apache-2.0
compatibility: ''
metadata:
  author: terminal-skills
  version: 1.0.0
  category: Backend Development
  tags:
    - web-framework
    - edge
    - cloudflare
    - bun
    - deno
    - fast
    - typescript
---

# Hono — Ultrafast Web Framework

You are an expert in Hono, the ultrafast web framework for the edge. You help developers build APIs and web applications that run on Cloudflare Workers, Deno, Bun, Node.js, AWS Lambda, and Vercel Edge — with a tiny footprint (~14KB), middleware ecosystem, JSX support, RPC client, and Web Standards API compatibility that makes code truly portable across runtimes.

## Core Capabilities

### API Routes

```typescript
import { Hono } from "hono";
import { cors } from "hono/cors";
import { logger } from "hono/logger";
import { jwt } from "hono/jwt";
import { zValidator } from "@hono/zod-validator";
import { z } from "zod";

const app = new Hono();

// Middleware
app.use("*", logger());
app.use("/api/*", cors({ origin: ["https://myapp.com"], credentials: true }));
app.use("/api/protected/*", jwt({ secret: process.env.JWT_SECRET! }));

// Typed routes with Zod validation
const createUserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  role: z.enum(["user", "admin"]).default("user"),
});

app.get("/api/users", async (c) => {
  const { page, limit } = c.req.query();
  const users = await db.users.findMany({
    skip: ((+page || 1) - 1) * (+limit || 20),
    take: +limit || 20,
  });
  return c.json({ data: users });
});

app.post("/api/users", zValidator("json", createUserSchema), async (c) => {
  const body = c.req.valid("json");        // Typed as { name: string, email: string, role: "user" | "admin" }
  const user = await db.users.create({ data: body });
  return c.json(user, 201);
});

app.get("/api/users/:id", async (c) => {
  const id = c.req.param("id");
  const user = await db.users.findUnique({ where: { id } });
  if (!user) return c.json({ error: "Not found" }, 404);
  return c.json(user);
});

// Protected route
app.get("/api/protected/me", (c) => {
  const payload = c.get("jwtPayload");
  return c.json({ userId: payload.sub });
});

export default app;
```

### RPC Client (Type-Safe)

```typescript
// server.ts — Export typed routes
const routes = app
  .get("/api/users", ...)
  .post("/api/users", ...);

export type AppType = typeof routes;

// client.ts — Type-safe client (like tRPC but for REST)
import { hc } from "hono/client";
import type { AppType } from "./server";

const client = hc<AppType>("https://api.myapp.com");

const users = await client.api.users.$get();
const json = await users.json();           // Typed as User[]

const newUser = await client.api.users.$post({
  json: { name: "Alice", email: "alice@example.com" },  // Type-checked!
});
```

### JSX and HTML

```tsx
import { Hono } from "hono";
import { html } from "hono/html";

const app = new Hono();

app.get("/", (c) => {
  return c.html(
    <html>
      <body>
        <h1>Hello from Hono!</h1>
        <p>Running on {c.runtime}</p>
      </body>
    </html>
  );
});

// Streaming
app.get("/stream", (c) => {
  return c.streamText(async (stream) => {
    for (const word of "Hello World from Hono!".split(" ")) {
      await stream.write(word + " ");
      await stream.sleep(100);
    }
  });
});
```

## Installation

```bash
npm create hono@latest my-app
# Choose: cloudflare-workers | nodejs | bun | deno | vercel | aws-lambda
cd my-app && npm install
npm run dev
```

## Best Practices

1. **Web Standards** — Uses `Request`/`Response` API; code runs on any runtime without changes
2. **Zod validation** — Use `@hono/zod-validator` for type-safe request validation; compile + runtime safety
3. **RPC client** — Use `hc<AppType>()` for type-safe client; catches API contract mismatches at compile time
4. **Middleware** — Rich ecosystem: cors, jwt, logger, compress, cache, rate-limit, OpenAPI
5. **Edge-first** — 14KB bundle; runs on Cloudflare Workers with <1ms cold start
6. **Multi-runtime** — Same code deploys to Workers, Bun, Deno, Node, Lambda; switch with one config change
7. **JSX support** — Built-in JSX for server-rendered HTML; no React needed for simple pages
8. **Streaming** — `c.streamText()` and `c.stream()` for SSE, chunked responses, AI streaming
