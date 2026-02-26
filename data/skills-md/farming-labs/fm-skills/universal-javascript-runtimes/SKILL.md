---
name: universal-javascript-runtimes
description: Explains universal JavaScript deployment, the UnJS ecosystem (Nitro, H3, unenv), WinterCG web standards, and cross-platform runtimes. Use when building apps that deploy anywhere, understanding server adapters, or working with edge functions and serverless platforms.
---

# Universal JavaScript Runtimes

## Overview

Modern JavaScript can run in many environments: Node.js, Deno, Bun, Cloudflare Workers, browsers, and more. Universal JavaScript means writing code once that runs everywhere.

## The Runtime Fragmentation Problem

```
JAVASCRIPT RUNTIMES (2024):

┌─────────────────────────────────────────────────────────────────┐
│                    Traditional Servers                           │
├─────────────────────────────────────────────────────────────────┤
│  Node.js         │ The original server runtime (2009)           │
│  Deno            │ Secure runtime by Node creator (2020)        │
│  Bun             │ Fast all-in-one runtime (2022)               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    Edge/Serverless                               │
├─────────────────────────────────────────────────────────────────┤
│  Cloudflare Workers  │ V8 isolates at the edge                  │
│  Vercel Edge         │ V8 isolates, Next.js optimized           │
│  Deno Deploy         │ Deno at the edge                         │
│  Netlify Edge        │ Deno-based edge functions                │
│  AWS Lambda          │ Node.js/custom runtimes                  │
│  Fastly Compute      │ WebAssembly-based                        │
└─────────────────────────────────────────────────────────────────┘

PROBLEM: Each has different APIs!

// Node.js
const fs = require('fs');
const http = require('http');

// Deno
await Deno.readFile('file.txt');
Deno.serve(handler);

// Cloudflare Workers
export default { fetch(request, env, ctx) {} }

// Bun
Bun.serve({ fetch(req) {} });
```

## Web Standards: The Universal Foundation

The solution is web standard APIs that all runtimes implement:

```javascript
// WEB STANDARD APIs (work everywhere):

// Fetch API
const response = await fetch('https://api.example.com/data');
const data = await response.json();

// Request/Response
const request = new Request('https://example.com', {
  method: 'POST',
  body: JSON.stringify({ key: 'value' }),
});
const response = new Response('Hello', { status: 200 });

// URL
const url = new URL('https://example.com/path?query=value');
console.log(url.pathname);  // '/path'

// Headers
const headers = new Headers();
headers.set('Content-Type', 'application/json');

// TextEncoder/TextDecoder
const encoder = new TextEncoder();
const bytes = encoder.encode('Hello');

// Crypto
const hash = await crypto.subtle.digest('SHA-256', data);

// Streams
const stream = new ReadableStream({ /* ... */ });

// AbortController
const controller = new AbortController();
fetch(url, { signal: controller.signal });
```

### WinterCG (Web-interoperable Runtimes Community Group)

WinterCG standardizes APIs across server runtimes:

```
WINTERCG MEMBERS:
- Cloudflare
- Deno
- Node.js
- Vercel
- Shopify
- Bloomberg
- ... and more

STANDARDIZED APIs:
├── fetch(), Request, Response, Headers
├── URL, URLSearchParams, URLPattern
├── TextEncoder, TextDecoder
├── crypto.subtle (Web Crypto API)
├── Streams (ReadableStream, WritableStream)
├── AbortController, AbortSignal
├── setTimeout, setInterval
├── console
├── structuredClone
├── atob, btoa
└── Performance API

RESULT: Code using these APIs works on ANY compliant runtime
```

## The UnJS Ecosystem

UnJS (Universal JavaScript) is a collection of packages for building universal JavaScript:

```
UNJS ECOSYSTEM:

┌─────────────────────────────────────────────────────────────────┐
│                        FRAMEWORKS                                │
├─────────────────────────────────────────────────────────────────┤
│  Nitro       │ Universal server builder (powers Nuxt)           │
│  H3          │ Minimal HTTP framework                           │
│  Nuxt        │ Full-stack Vue framework (uses Nitro)           │
│  Analog      │ Angular meta-framework (uses Nitro)              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      CORE UTILITIES                              │
├─────────────────────────────────────────────────────────────────┤
│  ofetch      │ Better fetch with auto-retry, interceptors       │
│  unenv       │ Runtime environment polyfills                    │
│  unbuild     │ Unified build system for libraries               │
│  unimport    │ Auto-import utilities                            │
│  unstorage   │ Universal storage layer                          │
│  uncrypto    │ Universal crypto utilities                       │
│  unhead      │ Universal document head manager                  │
│  unctx       │ Composable async context                         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     INFRASTRUCTURE                               │
├─────────────────────────────────────────────────────────────────┤
│  listhen     │ Universal HTTP server listener                   │
│  ufo         │ URL utilities                                    │
│  pathe       │ Cross-platform path utilities                    │
│  consola     │ Universal logger                                 │
│  defu        │ Deep defaults merging                            │
│  hookable    │ Async hooks system                               │
│  c12         │ Config loading utility                           │
└─────────────────────────────────────────────────────────────────┘
```

## H3: The Universal HTTP Framework

H3 is a minimal, high-performance HTTP framework that runs everywhere:

```javascript
// H3 BASICS:

import { createApp, createRouter, defineEventHandler } from 'h3';

const app = createApp();
const router = createRouter();

// Define routes
router.get('/hello', defineEventHandler((event) => {
  return { message: 'Hello World' };
}));

router.post('/users', defineEventHandler(async (event) => {
  const body = await readBody(event);
  return { created: body };
}));

app.use(router);

// H3 is runtime-agnostic - it works with:
// - Node.js http server
// - Bun.serve
// - Deno.serve  
// - Cloudflare Workers
// - Any web standard runtime
```

### H3 Event Handler Model

```javascript
// H3 uses an "event" abstraction over Request/Response:

import {
  defineEventHandler,
  getQuery,
  getRouterParams,
  readBody,
  setCookie,
  setHeader,
  createError,
  sendRedirect,
} from 'h3';

// Request utilities
const handler = defineEventHandler(async (event) => {
  // URL query parameters
  const query = getQuery(event);  // ?page=1 → { page: '1' }
  
  // Route parameters
  const params = getRouterParams(event);  // /users/:id → { id: '123' }
  
  // Request body (auto-parsed)
  const body = await readBody(event);  // JSON, FormData, etc.
  
  // Request headers
  const auth = getHeader(event, 'authorization');
  
  // Response utilities
  setHeader(event, 'X-Custom', 'value');
  setCookie(event, 'session', 'abc123');
  
  // Return response (auto-serialized)
  return { success: true };  // Becomes JSON response
});

// Error handling
const protectedHandler = defineEventHandler((event) => {
  const user = getUser(event);
  if (!user) {
    throw createError({
      statusCode: 401,
      message: 'Unauthorized',
    });
  }
  return { user };
});

// Redirects
const redirectHandler = defineEventHandler((event) => {
  return sendRedirect(event, '/new-location', 302);
});
```

### Why H3 Over Express/Fastify?

```
EXPRESS (Traditional Node.js):
┌─────────────────────────────────────────────────────────────────┐
│  - Built on Node.js http module                                 │
│  - req/res are Node-specific objects                           │
│  - Middleware modifies req/res                                  │
│  - Large ecosystem but Node-only                                │
│  - Callback-based (older pattern)                               │
│                                                                  │
│  LIMITATION: Only works on Node.js                              │
└─────────────────────────────────────────────────────────────────┘

H3 (Universal):
┌─────────────────────────────────────────────────────────────────┐
│  - Built on web standards (Request/Response)                   │
│  - Event abstraction over different runtimes                   │
│  - Composable with defineEventHandler                          │
│  - Tree-shakeable (small bundle)                               │
│  - TypeScript-first                                             │
│                                                                  │
│  ADVANTAGE: Works everywhere via adapters                       │
└─────────────────────────────────────────────────────────────────┘

// Express (Node.js only):
app.get('/api', (req, res) => {
  res.json({ message: 'Hello' });
});

// H3 (Universal):
router.get('/api', defineEventHandler(() => {
  return { message: 'Hello' };  // Works on Node, Deno, Workers, etc.
}));
```

## Nitro: Universal Server Builder

Nitro is the server framework that powers Nuxt. It builds universal server applications:

```
NITRO OVERVIEW:

┌─────────────────────────────────────────────────────────────────┐
│                      YOUR CODE                                   │
│                                                                  │
│   server/                                                        │
│   ├── api/           API routes (auto-registered)               │
│   │   ├── hello.ts   → /api/hello                               │
│   │   └── users/                                                │
│   │       └── [id].ts → /api/users/:id                          │
│   ├── routes/        Custom routes                              │
│   ├── middleware/    Server middleware                          │
│   ├── plugins/       Server plugins                             │
│   └── utils/         Server utilities                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     NITRO BUILD                                  │
│                                                                  │
│   1. Scan routes and handlers                                   │
│   2. Bundle server code                                         │
│   3. Apply runtime-specific transforms                          │
│   4. Generate optimized output                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌───────────────┴───────────────┐
              │         PRESETS               │
              ├───────────────────────────────┤
              │  node-server    │ Node.js     │
              │  cloudflare     │ Workers     │
              │  vercel         │ Vercel      │
              │  netlify        │ Netlify     │
              │  deno           │ Deno Deploy │
              │  bun            │ Bun         │
              │  aws-lambda     │ Lambda      │
              │  ... 20+ more   │             │
              └───────────────────────────────┘
```

### Nitro File-Based Routing

```
server/
├── api/
│   ├── hello.ts              → GET  /api/hello
│   ├── hello.post.ts         → POST /api/hello
│   ├── users/
│   │   ├── index.ts          → GET  /api/users
│   │   ├── index.post.ts     → POST /api/users
│   │   └── [id].ts           → GET  /api/users/:id
│   └── [...slug].ts          → /api/* (catch-all)
├── routes/
│   └── feed.xml.ts           → GET  /feed.xml
└── middleware/
    └── auth.ts               → Runs on all requests
```

```typescript
// server/api/users/[id].ts
export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id');
  const user = await db.users.findById(id);
  
  if (!user) {
    throw createError({
      statusCode: 404,
      message: 'User not found',
    });
  }
  
  return user;
});

// server/middleware/auth.ts
export default defineEventHandler((event) => {
  const token = getHeader(event, 'authorization');
  if (token) {
    event.context.user = verifyToken(token);
  }
});
```

### Nitro Deployment Presets

```javascript
// nitro.config.ts
export default defineNitroConfig({
  // Target platform
  preset: 'cloudflare-pages',  // or 'vercel', 'netlify', 'node', etc.
  
  // Preset-specific options
  cloudflare: {
    pages: {
      routes: {
        exclude: ['/static/*'],
      },
    },
  },
});

// BUILD COMMAND:
// npx nitro build

// OUTPUT varies by preset:

// preset: 'node-server'
// → .output/
//   ├── server/
//   │   └── index.mjs     (Node.js server)
//   └── public/           (Static files)

// preset: 'cloudflare-pages'  
// → .output/
//   ├── _worker.js        (Workers script)
//   └── public/           (Static files)

// preset: 'vercel'
// → .vercel/
//   └── output/
//       ├── functions/    (Serverless functions)
//       └── static/       (Static files)
```

### How Nitro Achieves Universality

```
NITRO'S UNIVERSAL ARCHITECTURE:

┌─────────────────────────────────────────────────────────────────┐
│                     YOUR H3 HANDLERS                             │
│                                                                  │
│   // Same code for all platforms                                │
│   defineEventHandler((event) => {                               │
│     return { message: 'Hello' };                                │
│   });                                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        H3 LAYER                                  │
│                                                                  │
│   Abstracts Request/Response handling                           │
│   Provides consistent event interface                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       UNENV LAYER                                │
│                                                                  │
│   Polyfills Node.js APIs for non-Node runtimes                 │
│   - process.env → runtime env vars                              │
│   - Buffer → Uint8Array                                         │
│   - fs → unstorage                                              │
│   - crypto → Web Crypto                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RUNTIME ADAPTER                               │
│                                                                  │
│   Node.js:     http.createServer(toNodeHandler(app))            │
│   Deno:        Deno.serve(toWebHandler(app))                    │
│   Workers:     export default { fetch: toWebHandler(app) }      │
│   Bun:         Bun.serve({ fetch: toWebHandler(app) })          │
└─────────────────────────────────────────────────────────────────┘
```

## unenv: The Environment Polyfill Layer

unenv provides Node.js API compatibility for non-Node runtimes:

```javascript
// THE PROBLEM:

// Your code uses Node.js APIs:
import { readFileSync } from 'fs';
import { createHash } from 'crypto';

// But Cloudflare Workers doesn't have fs or crypto modules!
// ❌ Error: Cannot find module 'fs'


// UNENV SOLUTION:

// unenv provides mock/polyfill implementations:

// fs → Mock (errors or uses storage abstraction)
// crypto → Web Crypto API wrapper
// process → Minimal process-like object
// Buffer → Uint8Array wrapper

// In nitro.config.ts:
export default defineNitroConfig({
  preset: 'cloudflare',
  // unenv automatically applies polyfills
});

// Now your Node.js code "just works" on Workers
// (with some limitations for truly Node-specific APIs)
```

### What unenv Polyfills

```
NODE.JS MODULE        → UNENV REPLACEMENT
──────────────────────────────────────────────────────────────────
process              → Minimal process object with env
Buffer               → Uint8Array-based implementation
stream               → Web Streams API
crypto               → Web Crypto API
path                 → Pure JS implementation
url                  → Native URL class
util                 → Pure JS utilities
events               → EventEmitter implementation
assert               → Pure JS assert

NODE.JS MODULE        → UNENV MOCK (no-op or error)
──────────────────────────────────────────────────────────────────
fs                   → Mock (use unstorage instead)
child_process        → Mock (not available in edge)
net                  → Mock (not available in edge)
http                 → Use fetch instead
```

## unstorage: Universal Storage

unstorage provides a unified storage API across different backends:

```javascript
// UNSTORAGE BASICS:

import { createStorage } from 'unstorage';
import fsDriver from 'unstorage/drivers/fs';
import redisDriver from 'unstorage/drivers/redis';
import cloudflareKVDriver from 'unstorage/drivers/cloudflare-kv-binding';

// Development: File system
const devStorage = createStorage({
  driver: fsDriver({ base: './data' }),
});

// Production (Redis):
const prodStorage = createStorage({
  driver: redisDriver({ url: 'redis://localhost:6379' }),
});

// Cloudflare Workers:
const edgeStorage = createStorage({
  driver: cloudflareKVDriver({ binding: 'MY_KV' }),
});

// SAME API everywhere:
await storage.setItem('user:123', { name: 'John' });
const user = await storage.getItem('user:123');
await storage.removeItem('user:123');
const keys = await storage.getKeys('user:');
```

### Storage Drivers

```
DRIVER                 USE CASE
──────────────────────────────────────────────────────────────────
memory                Local development, testing
fs                    Node.js file system
redis                 Production caching
cloudflare-kv-binding Cloudflare Workers KV
vercel-kv             Vercel KV storage
netlify-blobs         Netlify Blob storage
planetscale           PlanetScale database
mongodb               MongoDB collections
s3                    AWS S3 buckets
github                GitHub repository files
http                  Remote HTTP storage
lru-cache             In-memory LRU cache
```

## ofetch: Universal Fetch

ofetch is an enhanced fetch that works everywhere:

```javascript
import { ofetch } from 'ofetch';

// BASIC USAGE (same as fetch):
const data = await ofetch('/api/users');

// AUTO-PARSING:
// JSON responses automatically parsed
const users = await ofetch('/api/users');  // Returns parsed JSON

// BASE URL:
const api = ofetch.create({ baseURL: 'https://api.example.com' });
const user = await api('/users/123');

// RETRY:
const data = await ofetch('/api/data', {
  retry: 3,
  retryDelay: 1000,
});

// INTERCEPTORS:
const api = ofetch.create({
  onRequest({ options }) {
    options.headers.set('Authorization', `Bearer ${token}`);
  },
  onResponse({ response }) {
    console.log('Response:', response.status);
  },
  onResponseError({ response }) {
    if (response.status === 401) {
      logout();
    }
  },
});

// TYPE-SAFE:
interface User {
  id: number;
  name: string;
}
const user = await ofetch<User>('/api/users/123');
// user is typed as User
```

## Comparing Server Approaches

```
┌────────────┬──────────────┬────────────────┬─────────────────┐
│            │   Express    │    Fastify     │       H3        │
├────────────┼──────────────┼────────────────┼─────────────────┤
│ Runtime    │ Node.js only │ Node.js only   │ Universal       │
├────────────┼──────────────┼────────────────┼─────────────────┤
│ Standards  │ Node http    │ Node http      │ Web standards   │
├────────────┼──────────────┼────────────────┼─────────────────┤
│ Bundle     │ ~200KB       │ ~100KB         │ ~20KB           │
├────────────┼──────────────┼────────────────┼─────────────────┤
│ Edge ready │ ❌           │ ❌             │ ✅              │
├────────────┼──────────────┼────────────────┼─────────────────┤
│ TypeScript │ Manual types │ Built-in       │ Built-in        │
├────────────┼──────────────┼────────────────┼─────────────────┤
│ Ecosystem  │ Huge         │ Growing        │ UnJS + adapters │
└────────────┴──────────────┴────────────────┴─────────────────┘
```

---

## Deep Dive: Understanding Universal JavaScript

### Why Runtime Diversity Exists

```
THE JAVASCRIPT RUNTIME HISTORY:

2009: Node.js
      └─► JavaScript on servers (V8 engine)
      └─► npm ecosystem explodes
      └─► Everyone uses Node-specific APIs (fs, http, etc.)

2018: Cloudflare Workers
      └─► JavaScript at the edge (V8 isolates)
      └─► No file system, limited APIs
      └─► Web standard APIs only
      └─► Startup in milliseconds (vs seconds for Node)

2020: Deno
      └─► "Fixed" Node.js design mistakes
      └─► Web standards first
      └─► Built-in TypeScript
      └─► Secure by default (permissions)

2022: Bun
      └─► Speed-focused runtime (JavaScriptCore engine)
      └─► Node.js compatible
      └─► Built-in bundler, test runner
      └─► Faster npm, native APIs

2023+: More edge runtimes
      └─► Vercel Edge Runtime
      └─► Netlify Edge Functions
      └─► AWS Lambda@Edge
      └─► Fastly Compute


THE CHALLENGE:
- Code written for Node.js doesn't work on Workers
- Code written for Workers might not use Node.js ecosystem
- Each runtime has unique features/limitations
- Deployment target affects how you write code

THE SOLUTION: Write to web standards + abstract the differences
```

### How V8 Isolates Enable Edge Computing

```
TRADITIONAL NODE.JS DEPLOYMENT:

┌─────────────────────────────────────────────────────────────────┐
│                      EC2 Instance                                │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   Node.js Process                        │    │
│  │                                                          │    │
│  │  - Full V8 engine                                       │    │
│  │  - Complete Node.js runtime                             │    │
│  │  - File system access                                   │    │
│  │  - Network access                                       │    │
│  │  - All npm packages available                          │    │
│  │                                                          │    │
│  │  Startup: 500ms - 2s (cold start)                       │    │
│  │  Memory: 128MB - 1GB                                    │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘


CLOUDFLARE WORKERS (V8 Isolates):

┌─────────────────────────────────────────────────────────────────┐
│                   Cloudflare Edge Server                         │
│                                                                  │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐       │
│  │ Isolate 1 │ │ Isolate 2 │ │ Isolate 3 │ │ Isolate N │       │
│  │  (App A)  │ │  (App B)  │ │  (App A)  │ │  (App X)  │       │
│  │           │ │           │ │           │ │           │       │
│  │  ~128KB   │ │  ~256KB   │ │  ~128KB   │ │  ~512KB   │       │
│  │  5ms cold │ │  5ms cold │ │  0ms warm │ │  5ms cold │       │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘       │
│                                                                  │
│  Single V8 engine, many isolated contexts                       │
│  No file system (security)                                      │
│  Limited memory per isolate                                     │
│  Millisecond cold starts                                        │
└─────────────────────────────────────────────────────────────────┘


WHY ISOLATES ARE FAST:
1. V8 engine already warm (shared)
2. No process startup overhead
3. Minimal memory per request
4. Snapshot-based initialization
5. Thousands of isolates per machine
```

### The Web Standard Request/Response Model

```javascript
// THE WEB STANDARD MODEL:

// Everything is Request → Response

// INPUT: Request object
const request = new Request('https://example.com/api/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer token',
  },
  body: JSON.stringify({ name: 'John' }),
});

// Properties available:
request.method       // 'POST'
request.url          // 'https://example.com/api/users'
request.headers      // Headers object
request.body         // ReadableStream
await request.json() // Parse body as JSON
await request.text() // Parse body as text

// OUTPUT: Response object
const response = new Response(
  JSON.stringify({ id: 1, name: 'John' }),
  {
    status: 201,
    headers: {
      'Content-Type': 'application/json',
    },
  }
);

// A UNIVERSAL HANDLER:
async function handler(request: Request): Promise<Response> {
  const url = new URL(request.url);
  
  if (url.pathname === '/api/hello') {
    return new Response('Hello World');
  }
  
  return new Response('Not Found', { status: 404 });
}

// This handler works on:
// - Cloudflare Workers: export default { fetch: handler }
// - Deno: Deno.serve(handler)
// - Bun: Bun.serve({ fetch: handler })
// - Node.js (with adapter): http.createServer(toNodeHandler(handler))
```

### How H3 Abstracts Runtime Differences

```javascript
// H3's event abstraction layer:

// H3 Event wraps different runtime request types:
interface H3Event {
  node?: {              // Node.js
    req: IncomingMessage;
    res: ServerResponse;
  };
  web?: {               // Web standard
    request: Request;
    url: URL;
  };
  context: Record<string, any>;  // Request context
}

// H3 utilities work regardless of underlying runtime:

export function getHeader(event: H3Event, name: string): string | undefined {
  // Node.js path:
  if (event.node) {
    return event.node.req.headers[name.toLowerCase()];
  }
  // Web standard path:
  if (event.web) {
    return event.web.request.headers.get(name);
  }
}

export function setHeader(event: H3Event, name: string, value: string): void {
  // Node.js path:
  if (event.node) {
    event.node.res.setHeader(name, value);
  }
  // Web standard path:
  if (event._responseHeaders) {
    event._responseHeaders.set(name, value);
  }
}

// YOUR CODE just uses the abstraction:
defineEventHandler((event) => {
  const auth = getHeader(event, 'authorization');
  setHeader(event, 'X-Custom', 'value');
  return { message: 'Hello' };
});
// Works on Node, Deno, Workers, Bun without changes
```

### Nitro's Build Process Deep Dive

```
NITRO BUILD PIPELINE:

INPUT:
server/
├── api/
│   └── users.ts     // H3 handlers
├── routes/
│   └── index.ts
├── middleware/
│   └── auth.ts
└── plugins/
    └── database.ts

STEP 1: SCAN
─────────────────────────────────────────────────────────────────
- Find all route files
- Parse route patterns from file names
- Discover middleware and plugins
- Build route table

Route Table:
[
  { path: '/api/users', handler: './api/users.ts', method: 'get' },
  { path: '/', handler: './routes/index.ts', method: 'get' },
]


STEP 2: BUNDLE WITH ROLLUP
─────────────────────────────────────────────────────────────────
- Bundle all handlers into single file
- Tree-shake unused code
- Apply preset-specific transforms

rollup.config:
  input: virtual:nitro-entry
  output: format based on preset (esm, cjs, iife)


STEP 3: APPLY UNENV TRANSFORMS
─────────────────────────────────────────────────────────────────
- Replace Node.js imports with polyfills
- Inject runtime-specific code
- Remove unavailable APIs

Example transforms:
  import fs from 'fs'           → import fs from 'unenv/runtime/node/fs'
  import crypto from 'crypto'   → import crypto from 'unenv/runtime/node/crypto'


STEP 4: GENERATE RUNTIME ENTRY
─────────────────────────────────────────────────────────────────

// Node.js preset:
import { createServer } from 'http';
import { toNodeHandler } from 'h3';
import { app } from './app.mjs';
createServer(toNodeHandler(app)).listen(3000);

// Cloudflare Workers preset:
import { toWebHandler } from 'h3';
import { app } from './app.mjs';
export default { fetch: toWebHandler(app) };

// Deno preset:
import { toWebHandler } from 'h3';
import { app } from './app.mjs';
Deno.serve(toWebHandler(app));


STEP 5: OUTPUT
─────────────────────────────────────────────────────────────────
.output/
├── server/
│   ├── index.mjs        // Entry point
│   └── chunks/          // Code-split chunks
└── public/              // Static assets
```

### Edge vs Serverless vs Traditional

```
┌─────────────────────────────────────────────────────────────────┐
│                    TRADITIONAL SERVER                            │
├─────────────────────────────────────────────────────────────────┤
│  Location:    Single region (us-east-1)                         │
│  Runtime:     Node.js process (long-running)                    │
│  Cold start:  0ms (always warm)                                 │
│  Scaling:     Manual or auto-scaling groups                     │
│  Cost:        Pay for uptime                                    │
│  APIs:        Full Node.js (fs, net, child_process)            │
│                                                                  │
│  Best for:    WebSocket, long computations, file processing    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      SERVERLESS                                  │
├─────────────────────────────────────────────────────────────────┤
│  Location:    Single or few regions                             │
│  Runtime:     Node.js container (ephemeral)                     │
│  Cold start:  100ms - 3s                                        │
│  Scaling:     Automatic, per-request                            │
│  Cost:        Pay per invocation                                │
│  APIs:        Full Node.js (fs, net, etc.)                     │
│                                                                  │
│  Best for:    Infrequent traffic, variable load, APIs          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        EDGE                                      │
├─────────────────────────────────────────────────────────────────┤
│  Location:    Global (200+ locations)                           │
│  Runtime:     V8 isolate (lightweight)                          │
│  Cold start:  < 10ms                                            │
│  Scaling:     Automatic, instant                                │
│  Cost:        Pay per request (very cheap)                      │
│  APIs:        Web standards only (limited)                      │
│                                                                  │
│  Best for:    Low latency, personalization, A/B tests, auth    │
└─────────────────────────────────────────────────────────────────┘

HYBRID APPROACH (Modern best practice):
┌─────────────────────────────────────────────────────────────────┐
│  Edge Layer:           Auth, routing, personalization           │
│       ↓                                                         │
│  Serverless Layer:     API routes, database queries             │
│       ↓                                                         │
│  Traditional Layer:    WebSocket, heavy computation             │
└─────────────────────────────────────────────────────────────────┘
```

### Universal Storage Patterns

```javascript
// THE STORAGE ABSTRACTION PATTERN:

// Different platforms have different storage:
// - Node.js: File system, Redis, PostgreSQL
// - Workers: KV, D1, R2
// - Vercel: Vercel KV, Postgres
// - AWS: S3, DynamoDB

// UNSTORAGE provides one API:

import { createStorage } from 'unstorage';

// Configuration varies by environment:
function createAppStorage() {
  if (process.env.CLOUDFLARE) {
    return createStorage({
      driver: cloudflareKVBindingDriver({ binding: 'CACHE' }),
    });
  }
  
  if (process.env.VERCEL) {
    return createStorage({
      driver: vercelKVDriver({ /* ... */ }),
    });
  }
  
  // Development / Node.js
  return createStorage({
    driver: fsDriver({ base: './.data' }),
  });
}

// YOUR CODE uses the same API everywhere:
const storage = createAppStorage();

export async function getUser(id: string) {
  // Check cache first
  const cached = await storage.getItem(`user:${id}`);
  if (cached) return cached;
  
  // Fetch from database
  const user = await db.users.findById(id);
  
  // Cache for 5 minutes
  await storage.setItem(`user:${id}`, user, { ttl: 300 });
  
  return user;
}
```

### Practical: Building a Universal API

```typescript
// A complete universal API example:

// server/api/posts/[id].ts
export default defineEventHandler(async (event) => {
  // Works on any runtime
  const id = getRouterParam(event, 'id');
  const method = event.method;
  
  // Universal storage
  const storage = useStorage('cache');
  
  if (method === 'GET') {
    // Check cache
    const cached = await storage.getItem(`post:${id}`);
    if (cached) {
      setHeader(event, 'X-Cache', 'HIT');
      return cached;
    }
    
    // Fetch from database (works on edge via fetch)
    const post = await ofetch(`https://api.example.com/posts/${id}`);
    
    // Cache for 1 hour
    await storage.setItem(`post:${id}`, post, { ttl: 3600 });
    
    return post;
  }
  
  if (method === 'PUT') {
    const body = await readBody(event);
    
    // Update via API
    const updated = await ofetch(`https://api.example.com/posts/${id}`, {
      method: 'PUT',
      body,
    });
    
    // Invalidate cache
    await storage.removeItem(`post:${id}`);
    
    return updated;
  }
  
  throw createError({ statusCode: 405, message: 'Method not allowed' });
});

// This single file works on:
// - Node.js server
// - Cloudflare Workers/Pages
// - Vercel Serverless/Edge
// - Netlify Functions/Edge
// - Deno Deploy
// - AWS Lambda
// - And more...

// Just change the Nitro preset in config!
```

### When to Use What Runtime

```
DECISION MATRIX:

Use EDGE when:
├─► Request latency is critical (< 50ms)
├─► Doing auth, redirects, header manipulation
├─► A/B testing, personalization
├─► Simple data transformations
└─► Global user base

Use SERVERLESS when:
├─► Database connections needed
├─► Moderate computation
├─► Node.js ecosystem required
├─► Moderate traffic with spikes
└─► Cost optimization for variable load

Use TRADITIONAL when:
├─► WebSocket connections
├─► Long-running processes
├─► Heavy computation (ML, video)
├─► Predictable high traffic
└─► Full Node.js APIs needed

Use HYBRID when:
├─► Different parts have different needs
├─► Global reach with complex backend
├─► Optimizing for both latency and capability
└─► Most production applications!
```

---

## For Framework Authors: Building Universal Runtime Systems

> **Implementation Note**: The patterns and code examples below represent one proven approach to building universal runtime systems. The adapter pattern shown here is inspired by Nitro/H3 but other approaches exist—SvelteKit uses a similar adapter system, while Remix uses a different deployment abstraction. The direction shown here provides portable patterns based on web standards. Adapt based on which runtimes you need to support and your polyfill strategy.

### Creating Runtime Adapters

```javascript
// NITRO-STYLE ADAPTER PATTERN

class RuntimeAdapter {
  constructor(name, options = {}) {
    this.name = name;
    this.options = options;
  }
  
  // Transform the universal handler for target runtime
  async adapt(handler, buildOutput) {
    throw new Error('Must implement adapt()');
  }
  
  // Generate entry point for runtime
  generateEntry() {
    throw new Error('Must implement generateEntry()');
  }
  
  // Get runtime-specific build config
  getBuildConfig() {
    return {};
  }
}

// Node.js Adapter
class NodeAdapter extends RuntimeAdapter {
  constructor(options = {}) {
    super('node', options);
    this.port = options.port || 3000;
  }
  
  generateEntry() {
    return `
import { createServer } from 'node:http';
import { toNodeHandler } from 'h3';
import { app } from '#internal/app';

const handler = toNodeHandler(app);
const server = createServer(handler);

server.listen(${this.port}, () => {
  console.log(\`Server running on http://localhost:${this.port}\`);
});
    `.trim();
  }
  
  getBuildConfig() {
    return {
      target: 'node',
      external: ['node:*'],
      minify: false,
    };
  }
}

// Cloudflare Workers Adapter
class CloudflareAdapter extends RuntimeAdapter {
  constructor(options = {}) {
    super('cloudflare', options);
  }
  
  generateEntry() {
    return `
import { toWebHandler } from 'h3';
import { app } from '#internal/app';

const handler = toWebHandler(app);

export default {
  async fetch(request, env, ctx) {
    // Inject environment bindings
    globalThis.__env__ = env;
    
    return handler(request, {
      waitUntil: (p) => ctx.waitUntil(p),
      passThroughOnException: () => ctx.passThroughOnException(),
    });
  },
};
    `.trim();
  }
  
  getBuildConfig() {
    return {
      target: 'webworker',
      format: 'esm',
      external: [],
      minify: true,
      define: {
        'process.env.NODE_ENV': '"production"',
      },
    };
  }
}

// Vercel Edge Adapter
class VercelEdgeAdapter extends RuntimeAdapter {
  constructor(options = {}) {
    super('vercel-edge', options);
  }
  
  generateEntry() {
    return `
import { toWebHandler } from 'h3';
import { app } from '#internal/app';

const handler = toWebHandler(app);

export const config = { runtime: 'edge' };

export default function (request) {
  return handler(request);
}
    `.trim();
  }
  
  // Generate vercel.json config
  generateConfig(routes) {
    return {
      version: 3,
      routes: routes.map(r => ({
        src: r.pattern,
        dest: r.handler,
      })),
    };
  }
}

// AWS Lambda Adapter
class LambdaAdapter extends RuntimeAdapter {
  constructor(options = {}) {
    super('lambda', options);
  }
  
  generateEntry() {
    return `
import { toWebHandler } from 'h3';
import { app } from '#internal/app';

const handler = toWebHandler(app);

export async function handler(event, context) {
  // Convert Lambda event to Web Request
  const request = lambdaToRequest(event);
  
  // Handle request
  const response = await handler(request);
  
  // Convert Web Response to Lambda response
  return responseToLambda(response);
}

function lambdaToRequest(event) {
  const url = \`https://\${event.headers.host}\${event.rawPath}\`;
  return new Request(url, {
    method: event.requestContext.http.method,
    headers: event.headers,
    body: event.body,
  });
}

async function responseToLambda(response) {
  return {
    statusCode: response.status,
    headers: Object.fromEntries(response.headers),
    body: await response.text(),
    isBase64Encoded: false,
  };
}
    `.trim();
  }
}
```

### Implementing Polyfill Presets

```javascript
// UNENV-STYLE POLYFILL SYSTEM

class EnvironmentPreset {
  constructor(name) {
    this.name = name;
    this.polyfills = new Map();
    this.aliases = new Map();
    this.globals = new Map();
    this.external = new Set();
  }
  
  // Register a polyfill for a module
  polyfill(module, implementation) {
    this.polyfills.set(module, implementation);
    return this;
  }
  
  // Alias one module to another
  alias(from, to) {
    this.aliases.set(from, to);
    return this;
  }
  
  // Define global injection
  global(name, value) {
    this.globals.set(name, value);
    return this;
  }
  
  // Mark module as external
  external(module) {
    this.external.add(module);
    return this;
  }
  
  // Generate bundler config
  toBundlerConfig() {
    return {
      alias: Object.fromEntries(this.aliases),
      define: Object.fromEntries(
        [...this.globals].map(([k, v]) => [`globalThis.${k}`, v])
      ),
      external: [...this.external],
    };
  }
}

// Node preset for edge runtimes
const nodePresetForEdge = new EnvironmentPreset('node-edge')
  // Polyfill Node.js built-ins with web-compatible versions
  .polyfill('node:buffer', 'unenv/runtime/node/buffer')
  .polyfill('node:crypto', 'unenv/runtime/node/crypto')
  .polyfill('node:stream', 'unenv/runtime/node/stream')
  .polyfill('node:events', 'unenv/runtime/node/events')
  .polyfill('node:util', 'unenv/runtime/node/util')
  .polyfill('node:path', 'unenv/runtime/node/path')
  .polyfill('node:url', 'unenv/runtime/node/url')
  
  // Stub Node.js modules not available on edge
  .polyfill('node:fs', 'unenv/runtime/mock/empty')
  .polyfill('node:child_process', 'unenv/runtime/mock/empty')
  .polyfill('node:net', 'unenv/runtime/mock/empty')
  .polyfill('node:tls', 'unenv/runtime/mock/empty')
  
  // Global injections
  .global('process', 'unenv/runtime/node/process')
  .global('Buffer', 'unenv/runtime/node/buffer')
  
  // Aliases
  .alias('buffer', 'node:buffer')
  .alias('stream', 'node:stream')
  .alias('events', 'node:events');

// Create polyfill bundle
function createPolyfillBundle(preset) {
  const imports = [];
  const exports = [];
  
  for (const [module, impl] of preset.polyfills) {
    const safeName = module.replace(/[^a-z0-9]/gi, '_');
    imports.push(`import * as ${safeName} from '${impl}';`);
    exports.push(`'${module}': ${safeName},`);
  }
  
  return `
${imports.join('\n')}

export const polyfills = {
  ${exports.join('\n  ')}
};

// Auto-inject polyfills
for (const [name, impl] of Object.entries(polyfills)) {
  globalThis.__modules__ = globalThis.__modules__ || {};
  globalThis.__modules__[name] = impl;
}
  `.trim();
}
```

### Building a Universal Storage Adapter

```javascript
// UNSTORAGE-STYLE DRIVER SYSTEM

class StorageDriver {
  constructor(options = {}) {
    this.options = options;
  }
  
  // Required methods
  async hasItem(key) { throw new Error('Not implemented'); }
  async getItem(key) { throw new Error('Not implemented'); }
  async setItem(key, value) { throw new Error('Not implemented'); }
  async removeItem(key) { throw new Error('Not implemented'); }
  async getKeys(base) { throw new Error('Not implemented'); }
  async clear() { throw new Error('Not implemented'); }
  
  // Optional methods
  async getMeta(key) { return {}; }
  async setMeta(key, meta) {}
}

// Memory driver (works everywhere)
class MemoryDriver extends StorageDriver {
  constructor(options = {}) {
    super(options);
    this.data = new Map();
    this.meta = new Map();
  }
  
  async hasItem(key) {
    return this.data.has(key);
  }
  
  async getItem(key) {
    return this.data.get(key) ?? null;
  }
  
  async setItem(key, value) {
    this.data.set(key, value);
    this.meta.set(key, { mtime: Date.now() });
  }
  
  async removeItem(key) {
    this.data.delete(key);
    this.meta.delete(key);
  }
  
  async getKeys(base = '') {
    return [...this.data.keys()].filter(k => k.startsWith(base));
  }
  
  async clear() {
    this.data.clear();
    this.meta.clear();
  }
}

// Cloudflare KV driver
class CloudflareKVDriver extends StorageDriver {
  constructor(options) {
    super(options);
    this.binding = options.binding; // KV namespace binding name
  }
  
  getKV() {
    // Access from Cloudflare env
    return globalThis.__env__?.[this.binding];
  }
  
  async hasItem(key) {
    return (await this.getKV().get(key)) !== null;
  }
  
  async getItem(key) {
    const value = await this.getKV().get(key, 'text');
    return value ? JSON.parse(value) : null;
  }
  
  async setItem(key, value) {
    await this.getKV().put(key, JSON.stringify(value), {
      expirationTtl: this.options.ttl,
    });
  }
  
  async removeItem(key) {
    await this.getKV().delete(key);
  }
  
  async getKeys(base = '') {
    const list = await this.getKV().list({ prefix: base });
    return list.keys.map(k => k.name);
  }
}

// Universal storage factory
function createStorage(options = {}) {
  const drivers = new Map();
  
  return {
    // Mount driver at prefix
    mount(prefix, driver) {
      drivers.set(prefix, driver);
    },
    
    // Get driver for key
    getDriver(key) {
      for (const [prefix, driver] of drivers) {
        if (key.startsWith(prefix)) {
          return { driver, key: key.slice(prefix.length) };
        }
      }
      return { driver: drivers.get('') || new MemoryDriver(), key };
    },
    
    // Unified interface
    async getItem(key) {
      const { driver, key: k } = this.getDriver(key);
      return driver.getItem(k);
    },
    
    async setItem(key, value, opts) {
      const { driver, key: k } = this.getDriver(key);
      return driver.setItem(k, value, opts);
    },
    
    async removeItem(key) {
      const { driver, key: k } = this.getDriver(key);
      return driver.removeItem(k);
    },
  };
}
```

### Implementing Cross-Runtime Crypto

```javascript
// WEB CRYPTO ABSTRACTION (UNCRYPTO-STYLE)

// Universal crypto that works on Node, Deno, Bun, Edge
const crypto = globalThis.crypto || (await import('node:crypto')).webcrypto;

class UniversalCrypto {
  // Random bytes
  static getRandomBytes(length) {
    const bytes = new Uint8Array(length);
    crypto.getRandomValues(bytes);
    return bytes;
  }
  
  // Generate UUID
  static randomUUID() {
    return crypto.randomUUID();
  }
  
  // Hash with SHA-256
  static async sha256(data) {
    const encoder = new TextEncoder();
    const buffer = typeof data === 'string' ? encoder.encode(data) : data;
    const hash = await crypto.subtle.digest('SHA-256', buffer);
    return new Uint8Array(hash);
  }
  
  // Hash to hex string
  static async sha256Hex(data) {
    const hash = await this.sha256(data);
    return Array.from(hash)
      .map(b => b.toString(16).padStart(2, '0'))
      .join('');
  }
  
  // HMAC signing
  static async hmacSign(key, data) {
    const encoder = new TextEncoder();
    const keyMaterial = await crypto.subtle.importKey(
      'raw',
      encoder.encode(key),
      { name: 'HMAC', hash: 'SHA-256' },
      false,
      ['sign']
    );
    
    const signature = await crypto.subtle.sign(
      'HMAC',
      keyMaterial,
      encoder.encode(data)
    );
    
    return new Uint8Array(signature);
  }
  
  // AES-GCM encryption
  static async encrypt(key, data) {
    const encoder = new TextEncoder();
    const iv = this.getRandomBytes(12);
    
    const keyMaterial = await crypto.subtle.importKey(
      'raw',
      await this.sha256(key),
      'AES-GCM',
      false,
      ['encrypt']
    );
    
    const encrypted = await crypto.subtle.encrypt(
      { name: 'AES-GCM', iv },
      keyMaterial,
      encoder.encode(data)
    );
    
    // Combine IV + encrypted data
    const result = new Uint8Array(iv.length + encrypted.byteLength);
    result.set(iv);
    result.set(new Uint8Array(encrypted), iv.length);
    
    return result;
  }
  
  // AES-GCM decryption
  static async decrypt(key, encryptedData) {
    const iv = encryptedData.slice(0, 12);
    const data = encryptedData.slice(12);
    
    const keyMaterial = await crypto.subtle.importKey(
      'raw',
      await this.sha256(key),
      'AES-GCM',
      false,
      ['decrypt']
    );
    
    const decrypted = await crypto.subtle.decrypt(
      { name: 'AES-GCM', iv },
      keyMaterial,
      data
    );
    
    return new TextDecoder().decode(decrypted);
  }
}

// Base64 URL encoding (works everywhere)
function base64UrlEncode(data) {
  const bytes = typeof data === 'string' 
    ? new TextEncoder().encode(data) 
    : data;
  
  const base64 = btoa(String.fromCharCode(...bytes));
  return base64
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');
}

function base64UrlDecode(str) {
  const base64 = str
    .replace(/-/g, '+')
    .replace(/_/g, '/');
  
  const binary = atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  
  return bytes;
}
```

### Building Universal Fetch Wrapper

```javascript
// OFETCH-STYLE UNIVERSAL FETCH

function createFetch(defaults = {}) {
  return async function $fetch(url, options = {}) {
    const config = {
      ...defaults,
      ...options,
      headers: {
        ...defaults.headers,
        ...options.headers,
      },
    };
    
    // Resolve URL
    const resolvedUrl = config.baseURL 
      ? new URL(url, config.baseURL).toString() 
      : url;
    
    // Prepare request
    const fetchOptions = {
      method: config.method || 'GET',
      headers: config.headers,
      signal: config.signal,
    };
    
    // Handle body
    if (config.body !== undefined) {
      if (typeof config.body === 'object' && 
          !(config.body instanceof FormData) &&
          !(config.body instanceof ReadableStream)) {
        fetchOptions.body = JSON.stringify(config.body);
        fetchOptions.headers['Content-Type'] = 'application/json';
      } else {
        fetchOptions.body = config.body;
      }
    }
    
    // Add query params
    if (config.query) {
      const separator = resolvedUrl.includes('?') ? '&' : '?';
      const params = new URLSearchParams(config.query).toString();
      url = resolvedUrl + separator + params;
    }
    
    // Retry logic
    const maxRetries = config.retry ?? 1;
    let lastError;
    
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        // Interceptors - request
        if (config.onRequest) {
          await config.onRequest({ request: fetchOptions, options: config });
        }
        
        const response = await fetch(resolvedUrl, fetchOptions);
        
        // Interceptors - response
        if (config.onResponse) {
          await config.onResponse({ response, options: config });
        }
        
        // Handle errors
        if (!response.ok) {
          const error = new FetchError(response.statusText);
          error.response = response;
          error.status = response.status;
          
          if (config.onResponseError) {
            await config.onResponseError({ error, response, options: config });
          }
          
          throw error;
        }
        
        // Parse response
        const contentType = response.headers.get('content-type') || '';
        
        if (config.responseType === 'stream') {
          return response.body;
        }
        
        if (config.responseType === 'blob') {
          return response.blob();
        }
        
        if (config.responseType === 'arrayBuffer') {
          return response.arrayBuffer();
        }
        
        if (contentType.includes('application/json')) {
          return response.json();
        }
        
        return response.text();
        
      } catch (error) {
        lastError = error;
        
        // Don't retry on certain errors
        if (error.status && error.status < 500) {
          throw error;
        }
        
        // Wait before retry
        if (attempt < maxRetries) {
          await new Promise(r => setTimeout(r, 1000 * (attempt + 1)));
        }
      }
    }
    
    throw lastError;
  };
}

class FetchError extends Error {
  constructor(message) {
    super(message);
    this.name = 'FetchError';
  }
}

// Create default instance
const $fetch = createFetch();

// Create with defaults
const api = createFetch({
  baseURL: 'https://api.example.com',
  headers: {
    'Authorization': 'Bearer token',
  },
  retry: 2,
});
```

## Related Skills

- See [meta-frameworks-overview](../meta-frameworks-overview/SKILL.md) for framework deployment options
- See [rendering-patterns](../rendering-patterns/SKILL.md) for SSR on edge
- See [build-pipelines-bundling](../build-pipelines-bundling/SKILL.md) for build output formats
