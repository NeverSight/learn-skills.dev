---
name: middleware-patterns
description: Explains middleware concepts, patterns, and implementations. Covers server middleware, edge middleware, request/response pipelines, and common use cases like auth, logging, and CORS. Use when implementing middleware or understanding request processing pipelines.
---

# Middleware Patterns

## Overview

Middleware is code that runs between receiving a request and sending a response. It's the backbone of request processing in web applications.

## What is Middleware?

```
THE MIDDLEWARE CONCEPT:

REQUEST → [Middleware 1] → [Middleware 2] → [Middleware N] → HANDLER → RESPONSE
              ↓                 ↓                 ↓              ↓
          (logging)         (auth)           (parse)       (business logic)


MIDDLEWARE CAN:
├── Modify the request before it reaches the handler
├── Modify the response before it's sent
├── Short-circuit the chain (e.g., return 401 early)
├── Pass data to subsequent middleware/handlers
├── Perform side effects (logging, analytics)
└── Handle errors from downstream middleware
```

## The Middleware Pipeline

```
REQUEST LIFECYCLE:

┌─────────────────────────────────────────────────────────────────┐
│                      INCOMING REQUEST                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  MIDDLEWARE 1: Logging                                           │
│  ─────────────────────────────────────────────────────────────  │
│  console.log(`${method} ${url}`);                               │
│  const start = Date.now();                                      │
│  await next();  ────────────────────────┐                       │
│  console.log(`Completed in ${Date.now() - start}ms`);  ◄────────┘
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  MIDDLEWARE 2: Authentication                                    │
│  ─────────────────────────────────────────────────────────────  │
│  const token = getHeader('Authorization');                      │
│  if (!token) return error(401);  // Short-circuit!              │
│  request.user = verifyToken(token);                             │
│  await next();  ────────────────────────┐                       │
│  // (response flows back through)        │                       │
└──────────────────────────────────────────┼──────────────────────┘
                              │            │
                              ▼            │
┌─────────────────────────────────────────────────────────────────┐
│  MIDDLEWARE 3: Rate Limiting                                     │
│  ─────────────────────────────────────────────────────────────  │
│  if (isRateLimited(request.ip)) return error(429);              │
│  await next();  ────────────────────────┐                       │
│                                          │                       │
└──────────────────────────────────────────┼──────────────────────┘
                              │            │
                              ▼            │
┌─────────────────────────────────────────────────────────────────┐
│                       ROUTE HANDLER                              │
│  ─────────────────────────────────────────────────────────────  │
│  return { data: 'Hello World' };                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     OUTGOING RESPONSE                            │
│  (flows back through middleware in reverse order)               │
└─────────────────────────────────────────────────────────────────┘
```

## Types of Middleware

```
MIDDLEWARE CLASSIFICATION:

BY SCOPE:
┌─────────────────────────────────────────────────────────────────┐
│  Global Middleware     │ Runs on every request                  │
│  Route Middleware      │ Runs on specific routes                │
│  Group Middleware      │ Runs on route groups                   │
│  Handler Middleware    │ Wraps specific handlers                │
└─────────────────────────────────────────────────────────────────┘

BY LOCATION:
┌─────────────────────────────────────────────────────────────────┐
│  Edge Middleware       │ Runs at CDN edge (before origin)       │
│  Server Middleware     │ Runs on origin server                  │
│  Client Middleware     │ Runs in browser (route guards)         │
└─────────────────────────────────────────────────────────────────┘

BY FUNCTION:
┌─────────────────────────────────────────────────────────────────┐
│  Request Middleware    │ Modifies incoming request              │
│  Response Middleware   │ Modifies outgoing response             │
│  Error Middleware      │ Handles errors                         │
│  Passthrough           │ Side effects only (logging)            │
└─────────────────────────────────────────────────────────────────┘
```

## Common Middleware Patterns

### Express-Style Middleware (Node.js)

```javascript
// EXPRESS MIDDLEWARE PATTERN:
// (req, res, next) => void

// Logging middleware
const logger = (req, res, next) => {
  console.log(`${req.method} ${req.url}`);
  next();  // Pass to next middleware
};

// Auth middleware
const auth = (req, res, next) => {
  const token = req.headers.authorization;
  if (!token) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  req.user = verifyToken(token);
  next();
};

// Error handling middleware (4 params)
const errorHandler = (err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal Server Error' });
};

// Usage
const app = express();
app.use(logger);           // Global
app.use('/api', auth);     // Path-specific
app.use(errorHandler);     // Error handler (must be last)

// Route-specific middleware
app.get('/admin', adminOnly, (req, res) => {
  res.json({ admin: true });
});
```

### H3/Nitro Middleware (Universal)

```javascript
// H3 MIDDLEWARE PATTERN:
// defineEventHandler((event) => { ... })

// server/middleware/logger.ts
export default defineEventHandler((event) => {
  console.log(`${event.method} ${event.path}`);
  // No return = pass through to next handler
});

// server/middleware/auth.ts
export default defineEventHandler((event) => {
  const token = getHeader(event, 'authorization');
  
  // Only protect /api routes
  if (!event.path.startsWith('/api')) return;
  
  if (!token) {
    throw createError({
      statusCode: 401,
      message: 'Unauthorized',
    });
  }
  
  event.context.user = verifyToken(token);
  // No return = continue to route handler
});

// server/middleware/timing.ts
export default defineEventHandler(async (event) => {
  const start = Date.now();
  
  // Run after response
  event.waitUntil(
    Promise.resolve().then(() => {
      console.log(`Request took ${Date.now() - start}ms`);
    })
  );
});
```

### Edge Middleware (Vercel/Next.js)

```typescript
// middleware.ts (at project root)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Redirect logic
  if (request.nextUrl.pathname === '/old-page') {
    return NextResponse.redirect(new URL('/new-page', request.url));
  }
  
  // Auth check
  const token = request.cookies.get('token');
  if (request.nextUrl.pathname.startsWith('/dashboard') && !token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  
  // Add headers
  const response = NextResponse.next();
  response.headers.set('x-custom-header', 'my-value');
  
  // Geolocation (available at edge)
  const country = request.geo?.country || 'US';
  response.cookies.set('country', country);
  
  return response;
}

// Configure which paths run middleware
export const config = {
  matcher: [
    // Match all paths except static files
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
};
```

### Cloudflare Workers Middleware

```javascript
// Cloudflare Workers middleware pattern
export default {
  async fetch(request, env, ctx) {
    // Create middleware chain
    const middlewares = [
      corsMiddleware,
      authMiddleware,
      rateLimitMiddleware,
    ];
    
    // Execute chain
    let response;
    for (const middleware of middlewares) {
      response = await middleware(request, env, ctx);
      if (response) return response;  // Short-circuit
    }
    
    // Main handler
    return handleRequest(request, env);
  },
};

// CORS middleware
async function corsMiddleware(request) {
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      },
    });
  }
  return null;  // Continue to next middleware
}

// Auth middleware
async function authMiddleware(request, env) {
  const url = new URL(request.url);
  
  if (url.pathname.startsWith('/api/protected')) {
    const token = request.headers.get('Authorization');
    if (!token) {
      return new Response('Unauthorized', { status: 401 });
    }
  }
  return null;  // Continue
}
```

## Common Middleware Use Cases

### 1. Authentication & Authorization

```javascript
// JWT Authentication
export default defineEventHandler(async (event) => {
  // Skip auth for public routes
  const publicRoutes = ['/api/login', '/api/register', '/api/health'];
  if (publicRoutes.includes(event.path)) return;
  
  const token = getHeader(event, 'authorization')?.replace('Bearer ', '');
  
  if (!token) {
    throw createError({ statusCode: 401, message: 'No token provided' });
  }
  
  try {
    const decoded = await verifyJWT(token);
    event.context.user = decoded;
  } catch (error) {
    throw createError({ statusCode: 401, message: 'Invalid token' });
  }
});

// Role-based Authorization
export default defineEventHandler((event) => {
  if (!event.path.startsWith('/api/admin')) return;
  
  const user = event.context.user;
  if (!user || user.role !== 'admin') {
    throw createError({ statusCode: 403, message: 'Admin access required' });
  }
});
```

### 2. CORS (Cross-Origin Resource Sharing)

```javascript
// CORS Middleware
export default defineEventHandler((event) => {
  const origin = getHeader(event, 'origin');
  const allowedOrigins = ['https://example.com', 'https://app.example.com'];
  
  if (origin && allowedOrigins.includes(origin)) {
    setHeader(event, 'Access-Control-Allow-Origin', origin);
    setHeader(event, 'Access-Control-Allow-Credentials', 'true');
  }
  
  setHeader(event, 'Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  setHeader(event, 'Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  // Handle preflight
  if (event.method === 'OPTIONS') {
    setHeader(event, 'Access-Control-Max-Age', '86400');  // 24 hours
    return null;  // Return empty 200 response
  }
});
```

### 3. Rate Limiting

```javascript
// Simple in-memory rate limiter
const requestCounts = new Map();

export default defineEventHandler((event) => {
  const ip = getHeader(event, 'x-forwarded-for') || 'unknown';
  const now = Date.now();
  const windowMs = 60 * 1000;  // 1 minute window
  const maxRequests = 100;
  
  // Get or create request record
  let record = requestCounts.get(ip);
  if (!record || now - record.start > windowMs) {
    record = { start: now, count: 0 };
    requestCounts.set(ip, record);
  }
  
  record.count++;
  
  // Set rate limit headers
  setHeader(event, 'X-RateLimit-Limit', maxRequests.toString());
  setHeader(event, 'X-RateLimit-Remaining', Math.max(0, maxRequests - record.count).toString());
  setHeader(event, 'X-RateLimit-Reset', (record.start + windowMs).toString());
  
  if (record.count > maxRequests) {
    throw createError({
      statusCode: 429,
      message: 'Too many requests',
    });
  }
});
```

### 4. Request Logging

```javascript
// Structured logging middleware
export default defineEventHandler(async (event) => {
  const start = Date.now();
  const requestId = crypto.randomUUID();
  
  // Attach request ID
  event.context.requestId = requestId;
  setHeader(event, 'X-Request-ID', requestId);
  
  // Log request
  console.log(JSON.stringify({
    type: 'request',
    requestId,
    method: event.method,
    path: event.path,
    query: getQuery(event),
    userAgent: getHeader(event, 'user-agent'),
    ip: getHeader(event, 'x-forwarded-for'),
    timestamp: new Date().toISOString(),
  }));
  
  // Log response after completion
  event.waitUntil(
    Promise.resolve().then(() => {
      console.log(JSON.stringify({
        type: 'response',
        requestId,
        duration: Date.now() - start,
        status: event.node?.res?.statusCode || 200,
      }));
    })
  );
});
```

### 5. Response Compression

```javascript
// Compression middleware (Node.js)
import { createGzip, createBrotliCompress } from 'zlib';

export default defineEventHandler((event) => {
  const acceptEncoding = getHeader(event, 'accept-encoding') || '';
  
  if (acceptEncoding.includes('br')) {
    event.context.compress = 'br';
    setHeader(event, 'Content-Encoding', 'br');
  } else if (acceptEncoding.includes('gzip')) {
    event.context.compress = 'gzip';
    setHeader(event, 'Content-Encoding', 'gzip');
  }
});
```

### 6. Security Headers

```javascript
// Security headers middleware
export default defineEventHandler((event) => {
  // Prevent clickjacking
  setHeader(event, 'X-Frame-Options', 'DENY');
  
  // Prevent MIME type sniffing
  setHeader(event, 'X-Content-Type-Options', 'nosniff');
  
  // XSS protection
  setHeader(event, 'X-XSS-Protection', '1; mode=block');
  
  // Referrer policy
  setHeader(event, 'Referrer-Policy', 'strict-origin-when-cross-origin');
  
  // Content Security Policy
  setHeader(event, 'Content-Security-Policy', [
    "default-src 'self'",
    "script-src 'self' 'unsafe-inline'",
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' data: https:",
  ].join('; '));
  
  // HSTS (HTTPS only)
  setHeader(event, 'Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
});
```

### 7. Request Validation

```javascript
// Validation middleware using Zod
import { z } from 'zod';

// Factory function for validation middleware
function validateBody(schema) {
  return defineEventHandler(async (event) => {
    if (event.method === 'GET') return;
    
    const body = await readBody(event);
    const result = schema.safeParse(body);
    
    if (!result.success) {
      throw createError({
        statusCode: 400,
        message: 'Validation failed',
        data: result.error.flatten(),
      });
    }
    
    event.context.validatedBody = result.data;
  });
}

// Usage in route
const userSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
});

// server/api/users.post.ts
export default defineEventHandler({
  onRequest: [validateBody(userSchema)],
  handler: (event) => {
    const { name, email } = event.context.validatedBody;
    return createUser({ name, email });
  },
});
```

### 8. Caching

```javascript
// Response caching middleware
export default defineEventHandler(async (event) => {
  // Only cache GET requests
  if (event.method !== 'GET') return;
  
  // Skip caching for authenticated requests
  if (getHeader(event, 'authorization')) return;
  
  const cacheKey = `cache:${event.path}:${JSON.stringify(getQuery(event))}`;
  const cached = await useStorage('cache').getItem(cacheKey);
  
  if (cached) {
    setHeader(event, 'X-Cache', 'HIT');
    return cached;
  }
  
  // Mark for caching after response
  event.context.cacheKey = cacheKey;
});

// In route handler
export default defineEventHandler(async (event) => {
  const data = await fetchExpensiveData();
  
  // Cache if middleware marked it
  if (event.context.cacheKey) {
    await useStorage('cache').setItem(event.context.cacheKey, data, {
      ttl: 3600,  // 1 hour
    });
  }
  
  return data;
});
```

## Framework-Specific Middleware

### Next.js Middleware

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Geo-based routing
  const country = request.geo?.country || 'US';
  if (country === 'EU') {
    return NextResponse.rewrite(new URL('/eu' + request.nextUrl.pathname, request.url));
  }
  
  // A/B testing
  const bucket = request.cookies.get('ab-bucket')?.value || 
    (Math.random() < 0.5 ? 'a' : 'b');
  
  const response = NextResponse.next();
  response.cookies.set('ab-bucket', bucket);
  
  // Bot detection
  const userAgent = request.headers.get('user-agent') || '';
  if (isBot(userAgent)) {
    // Serve pre-rendered version for bots
    return NextResponse.rewrite(new URL('/static' + request.nextUrl.pathname, request.url));
  }
  
  return response;
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

### Nuxt Middleware

```typescript
// server/middleware/auth.ts (Server middleware - runs on server)
export default defineEventHandler((event) => {
  const token = getCookie(event, 'auth_token');
  if (token) {
    event.context.user = verifyToken(token);
  }
});

// middleware/auth.ts (Route middleware - runs on client navigation)
export default defineNuxtRouteMiddleware((to, from) => {
  const user = useAuth();
  
  if (!user.value && to.path.startsWith('/dashboard')) {
    return navigateTo('/login');
  }
});

// Using route middleware in pages
// pages/dashboard.vue
definePageMeta({
  middleware: 'auth',  // or middleware: ['auth', 'admin']
});
```

### SvelteKit Hooks

```typescript
// src/hooks.server.ts
import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
  // Before route handler
  const token = event.cookies.get('token');
  if (token) {
    event.locals.user = await verifyToken(token);
  }
  
  // Call route handler
  const response = await resolve(event);
  
  // After route handler
  response.headers.set('X-Custom-Header', 'value');
  
  return response;
};

// Sequence multiple handlers
import { sequence } from '@sveltejs/kit/hooks';

export const handle = sequence(
  handleAuth,
  handleLogging,
  handleCompression
);
```

### Remix Middleware Pattern

```typescript
// Remix doesn't have traditional middleware
// Use loader/action patterns instead

// app/utils/auth.server.ts
export async function requireUser(request: Request) {
  const session = await getSession(request.headers.get('Cookie'));
  const userId = session.get('userId');
  
  if (!userId) {
    throw redirect('/login');
  }
  
  return await getUser(userId);
}

// app/routes/dashboard.tsx
export async function loader({ request }: LoaderFunctionArgs) {
  const user = await requireUser(request);  // "Middleware" pattern
  return json({ user });
}

// For cross-cutting concerns, use root loader
// app/root.tsx
export async function loader({ request }: LoaderFunctionArgs) {
  const env = {
    API_URL: process.env.API_URL,
  };
  const user = await getOptionalUser(request);
  
  return json({ env, user });
}
```

## Edge Middleware vs Server Middleware

```
EDGE MIDDLEWARE:
┌─────────────────────────────────────────────────────────────────┐
│  Location:    CDN edge (globally distributed)                  │
│  Latency:     < 50ms (runs near user)                          │
│  Cold start:  < 5ms                                            │
│  Runtime:     V8 isolates (limited APIs)                       │
│  Use cases:   Auth, redirects, A/B tests, geolocation          │
│                                                                  │
│  RUNS BEFORE: Static files, serverless functions, origin       │
│                                                                  │
│  LIMITATIONS:                                                   │
│  - No Node.js APIs                                              │
│  - No database connections                                      │
│  - Limited execution time (usually < 30s)                       │
│  - Limited memory                                               │
└─────────────────────────────────────────────────────────────────┘

SERVER MIDDLEWARE:
┌─────────────────────────────────────────────────────────────────┐
│  Location:    Origin server (single region)                    │
│  Latency:     50-200ms (depends on user distance)              │
│  Cold start:  100ms-3s (serverless) or 0 (traditional)         │
│  Runtime:     Node.js (full APIs)                              │
│  Use cases:   DB access, complex auth, heavy computation       │
│                                                                  │
│  RUNS AFTER:  CDN cache, edge middleware                       │
│                                                                  │
│  CAPABILITIES:                                                  │
│  - Full Node.js ecosystem                                       │
│  - Database connections                                         │
│  - File system access                                           │
│  - Long execution times                                         │
└─────────────────────────────────────────────────────────────────┘

WHEN TO USE EDGE:
├─► Authentication checks (JWT validation)
├─► Redirects (marketing, localization)
├─► A/B testing (cookie-based routing)
├─► Geolocation-based personalization
├─► Bot detection and blocking
├─► Header manipulation
└─► Feature flags

WHEN TO USE SERVER:
├─► Database queries
├─► Complex business logic
├─► Third-party API calls requiring secrets
├─► File processing
├─► Session management with storage
└─► Heavy computation
```

## Middleware Composition Patterns

### Chain Pattern

```javascript
// Composing middleware into a chain
function createMiddlewareChain(...middlewares) {
  return async (request, context) => {
    let index = 0;
    
    async function next() {
      if (index < middlewares.length) {
        const middleware = middlewares[index++];
        return await middleware(request, context, next);
      }
    }
    
    return await next();
  };
}

// Usage
const chain = createMiddlewareChain(
  loggingMiddleware,
  authMiddleware,
  rateLimitMiddleware
);

export default {
  fetch: (request) => chain(request, {}),
};
```

### Pipeline Pattern

```javascript
// Functional pipeline approach
const pipe = (...fns) => (value) =>
  fns.reduce((acc, fn) => acc.then(fn), Promise.resolve(value));

const pipeline = pipe(
  addRequestId,
  validateAuth,
  checkRateLimit,
  handleRequest
);

async function addRequestId(event) {
  event.context.requestId = crypto.randomUUID();
  return event;
}

async function validateAuth(event) {
  // Throws if invalid
  event.context.user = await authenticate(event);
  return event;
}
```

### Decorator Pattern

```typescript
// Middleware as decorators (TypeScript)
function withAuth(handler: EventHandler): EventHandler {
  return defineEventHandler(async (event) => {
    const user = await authenticate(event);
    if (!user) {
      throw createError({ statusCode: 401 });
    }
    event.context.user = user;
    return handler(event);
  });
}

function withCache(ttl: number) {
  return (handler: EventHandler): EventHandler => {
    return defineEventHandler(async (event) => {
      const cached = await getCache(event);
      if (cached) return cached;
      
      const result = await handler(event);
      await setCache(event, result, ttl);
      return result;
    });
  };
}

// Usage
export default withAuth(
  withCache(3600)(
    defineEventHandler((event) => {
      return { data: 'protected and cached' };
    })
  )
);
```

---

## Deep Dive: Understanding Middleware Internals

### The Onion Model

```
MIDDLEWARE EXECUTION ORDER (Onion Model):

                    REQUEST
                       ↓
        ┌──────────────────────────────────┐
        │  ┌────────────────────────────┐  │
        │  │  ┌──────────────────────┐  │  │
        │  │  │  ┌────────────────┐  │  │  │
        │  │  │  │                │  │  │  │
        │  │  │  │    HANDLER     │  │  │  │
        │  │  │  │                │  │  │  │
        │  │  │  └────────────────┘  │  │  │
        │  │  │    Middleware 3      │  │  │
        │  │  └──────────────────────┘  │  │
        │  │      Middleware 2          │  │
        │  └────────────────────────────┘  │
        │        Middleware 1              │
        └──────────────────────────────────┘
                       ↓
                   RESPONSE


EXECUTION FLOW:

1. Middleware 1: ENTER (request phase)
2. Middleware 2: ENTER (request phase)
3. Middleware 3: ENTER (request phase)
4. Handler: EXECUTE
5. Middleware 3: EXIT (response phase)
6. Middleware 2: EXIT (response phase)
7. Middleware 1: EXIT (response phase)

CODE EXAMPLE:

async function middleware1(request, next) {
  console.log('1: entering');      // Step 1
  const response = await next();
  console.log('1: exiting');       // Step 7
  return response;
}

async function middleware2(request, next) {
  console.log('2: entering');      // Step 2
  const response = await next();
  console.log('2: exiting');       // Step 6
  return response;
}

async function middleware3(request, next) {
  console.log('3: entering');      // Step 3
  const response = await next();
  console.log('3: exiting');       // Step 5
  return response;
}

async function handler(request) {
  console.log('handler');          // Step 4
  return new Response('OK');
}
```

### How `next()` Works

```javascript
// SIMPLIFIED IMPLEMENTATION OF next():

function createMiddlewareRunner(middlewares, handler) {
  return async function runner(request) {
    let index = 0;
    
    async function dispatch(i) {
      // Prevent calling next() multiple times
      if (i <= index) {
        throw new Error('next() called multiple times');
      }
      index = i;
      
      // Get current middleware or handler
      let fn;
      if (i < middlewares.length) {
        fn = middlewares[i];
      } else if (i === middlewares.length) {
        fn = handler;
      } else {
        return;  // No more middleware
      }
      
      // Create next function for this middleware
      const next = () => dispatch(i + 1);
      
      // Execute middleware
      return await fn(request, next);
    }
    
    return dispatch(0);
  };
}

// USAGE:
const run = createMiddlewareRunner(
  [logger, auth, rateLimit],
  handler
);

const response = await run(request);


// WHAT HAPPENS:

// dispatch(0) - logger middleware
//   └─► calls next()
//       └─► dispatch(1) - auth middleware
//           └─► calls next()
//               └─► dispatch(2) - rateLimit middleware
//                   └─► calls next()
//                       └─► dispatch(3) - handler
//                           └─► returns response
//                       └─► returns response
//                   └─► returns response
//               └─► returns response
//           └─► returns response
//       └─► returns response
//   └─► returns response
```

### Error Handling in Middleware

```javascript
// ERRORS PROPAGATE BACK THROUGH THE CHAIN:

async function errorHandlingMiddleware(request, next) {
  try {
    return await next();
  } catch (error) {
    // Handle error
    console.error('Error:', error);
    
    // Transform to response
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: error.statusCode || 500 }
    );
  }
}

// ERROR PROPAGATION:

// 1. Middleware 1: enter
// 2. Middleware 2: enter
// 3. Handler: throws Error!
// 4. Middleware 2: catch (if try/catch) OR propagate up
// 5. Middleware 1: catch (if try/catch) OR propagate up
// 6. Framework error handler

// EXPRESS ERROR MIDDLEWARE:
// Special 4-parameter signature
app.use((err, req, res, next) => {
  // Only called if error occurred
  console.error(err);
  res.status(500).json({ error: 'Something went wrong' });
});

// H3 ERROR HANDLING:
// Uses createError and error handlers
export default defineEventHandler((event) => {
  throw createError({
    statusCode: 400,
    message: 'Bad Request',
    data: { field: 'email' },  // Additional data
  });
});

// Global error handler in Nitro
// nitro.config.ts
export default defineNitroConfig({
  errorHandler: '~/error-handler.ts',
});

// error-handler.ts
export default defineNitroErrorHandler((error, event) => {
  setResponseStatus(event, error.statusCode || 500);
  return { error: error.message };
});
```

### Context Passing

```javascript
// HOW DATA FLOWS THROUGH MIDDLEWARE:

// 1. REQUEST CONTEXT PATTERN (Recommended)
// Attach data to request/event context

async function authMiddleware(request, next) {
  const user = await authenticate(request);
  request.context.user = user;  // Attach to context
  return next();
}

async function handler(request) {
  const user = request.context.user;  // Access later
  return Response.json({ user });
}


// 2. HEADERS PATTERN
// Pass data via headers (good for edge → origin)

async function edgeMiddleware(request) {
  const country = request.geo.country;
  request.headers.set('X-User-Country', country);
  return fetch(request);  // Forward to origin
}


// 3. ASYNC LOCAL STORAGE (Node.js)
// Thread-local storage for request scope

import { AsyncLocalStorage } from 'async_hooks';

const requestContext = new AsyncLocalStorage();

function middleware(req, res, next) {
  const context = { user: null, requestId: crypto.randomUUID() };
  requestContext.run(context, () => next());
}

// Anywhere in the request lifecycle:
function getRequestContext() {
  return requestContext.getStore();
}


// 4. UNCTX (UnJS Context)
// Similar to AsyncLocalStorage but universal

import { createContext } from 'unctx';

const eventContext = createContext();

export const useEvent = eventContext.use;

// In middleware
eventContext.call(event, () => handler());

// In any function
const event = useEvent();  // Get current event
```

### Performance Considerations

```
MIDDLEWARE PERFORMANCE IMPACT:

1. CHAIN LENGTH
   - Each middleware adds latency
   - More middleware = more function calls
   - 10 middleware × 1ms each = 10ms overhead

2. ASYNC OPERATIONS
   - await in middleware blocks the chain
   - Database calls in middleware slow EVERY request
   - Use caching, lazy loading

3. MEMORY ALLOCATIONS
   - Creating objects per request
   - Closures capture variables
   - GC pressure from high traffic


OPTIMIZATION STRATEGIES:

// 1. SHORT-CIRCUIT EARLY
async function rateLimitMiddleware(request, next) {
  if (isRateLimited(request.ip)) {
    return new Response('Too Many Requests', { status: 429 });
  }
  return next();  // Only call next if not limited
}

// 2. LAZY MIDDLEWARE EXECUTION
async function conditionalAuth(request, next) {
  // Only run auth logic for protected routes
  if (!request.url.includes('/api/protected')) {
    return next();  // Skip auth entirely
  }
  // ... auth logic
}

// 3. PARALLEL OPERATIONS
async function aggregatingMiddleware(request, next) {
  // Don't await sequentially if not dependent
  const [user, config] = await Promise.all([
    getUser(request),
    getConfig(),
  ]);
  request.context.user = user;
  request.context.config = config;
  return next();
}

// 4. CACHE MIDDLEWARE RESULTS
const middlewareCache = new Map();

async function cachedMiddleware(request, next) {
  const cacheKey = getCacheKey(request);
  
  if (middlewareCache.has(cacheKey)) {
    request.context.data = middlewareCache.get(cacheKey);
    return next();
  }
  
  const data = await expensiveOperation();
  middlewareCache.set(cacheKey, data);
  request.context.data = data;
  return next();
}
```

### Middleware Order Matters

```
COMMON MIDDLEWARE ORDER:

1. Error Handler (wrap everything)
2. Request ID / Tracing
3. Logging (log all requests)
4. Security Headers
5. CORS
6. Compression
7. Rate Limiting
8. Authentication
9. Authorization
10. Validation
11. Caching
12. → Route Handler


WHY ORDER MATTERS:

WRONG ORDER:
[Auth] → [RateLimit] → [Logging]
└─► Rate limit bypassed by failed auth
└─► Failed requests not logged

CORRECT ORDER:
[Logging] → [RateLimit] → [Auth]
└─► All requests logged
└─► Rate limit applied before auth (protect from brute force)
└─► Auth checked after rate limit


EXAMPLE CONFIGURATION:

// Nitro/H3 - file naming controls order
server/middleware/
├── 01.logging.ts       // First (prefix controls order)
├── 02.security.ts
├── 03.cors.ts
├── 04.rate-limit.ts
├── 05.auth.ts
└── 06.validation.ts

// Express - use() order matters
app.use(logging);
app.use(security);
app.use(cors);
app.use(rateLimit);
app.use(auth);
app.use(validation);
```

## Testing Middleware

```javascript
// UNIT TESTING MIDDLEWARE:

import { describe, it, expect, vi } from 'vitest';

// Mock event for H3
function createMockEvent(options = {}) {
  return {
    method: options.method || 'GET',
    path: options.path || '/',
    headers: new Headers(options.headers || {}),
    context: {},
  };
}

describe('authMiddleware', () => {
  it('should set user in context when token is valid', async () => {
    const event = createMockEvent({
      headers: { authorization: 'Bearer valid-token' },
    });
    
    await authMiddleware(event);
    
    expect(event.context.user).toBeDefined();
    expect(event.context.user.id).toBe('123');
  });
  
  it('should throw 401 when no token', async () => {
    const event = createMockEvent();
    
    await expect(authMiddleware(event)).rejects.toMatchObject({
      statusCode: 401,
    });
  });
});

// INTEGRATION TESTING MIDDLEWARE CHAIN:

import { createApp, createRouter, toNodeHandler } from 'h3';
import supertest from 'supertest';

describe('middleware chain', () => {
  const app = createApp();
  app.use(loggingMiddleware);
  app.use(authMiddleware);
  app.use(router);
  
  const request = supertest(toNodeHandler(app));
  
  it('should allow authenticated requests', async () => {
    const response = await request
      .get('/api/protected')
      .set('Authorization', 'Bearer valid-token');
    
    expect(response.status).toBe(200);
  });
  
  it('should reject unauthenticated requests', async () => {
    const response = await request.get('/api/protected');
    
    expect(response.status).toBe(401);
  });
});
```

---

## For Framework Authors: Building Middleware Systems

> **Implementation Note**: The patterns and code examples below represent one proven approach to building middleware systems. Middleware patterns vary—Express uses a callback-based approach, Koa uses async/await with context, and H3 uses a minimal event-based system. The direction shown here follows the modern async/await pattern with composability. Adapt based on your framework's async model, error handling strategy, and whether you need framework-specific integrations.

### Implementing a Middleware Pipeline

```javascript
// CORE MIDDLEWARE EXECUTION ENGINE

class MiddlewarePipeline {
  constructor() {
    this.middlewares = [];
    this.errorHandlers = [];
  }
  
  // Register middleware
  use(path, ...handlers) {
    // If first arg is a function, it's a global middleware
    if (typeof path === 'function') {
      handlers = [path, ...handlers];
      path = '/';
    }
    
    for (const handler of handlers) {
      this.middlewares.push({
        path: this.normalizePath(path),
        handler,
        isError: handler.length === 4, // (error, ctx, next)
      });
    }
    
    return this;
  }
  
  // Register error handler
  onError(handler) {
    this.errorHandlers.push(handler);
    return this;
  }
  
  normalizePath(path) {
    if (path === '/') return '';
    return path.replace(/\/$/, '');
  }
  
  // Create request handler
  handler() {
    return async (request, context = {}) => {
      const ctx = this.createContext(request, context);
      
      try {
        await this.execute(ctx);
        
        // If no response set, return 404
        if (!ctx.response) {
          ctx.response = new Response('Not Found', { status: 404 });
        }
        
        return ctx.response;
      } catch (error) {
        return this.handleError(error, ctx);
      }
    };
  }
  
  createContext(request, extra = {}) {
    const url = new URL(request.url);
    
    return {
      request,
      url,
      path: url.pathname,
      method: request.method,
      headers: request.headers,
      query: Object.fromEntries(url.searchParams),
      params: {},
      state: {},
      response: null,
      ...extra,
      
      // Helper methods
      json(data, status = 200) {
        this.response = Response.json(data, { status });
      },
      
      text(body, status = 200) {
        this.response = new Response(body, { status });
      },
      
      redirect(url, status = 302) {
        this.response = Response.redirect(url, status);
      },
      
      set(key, value) {
        this.state[key] = value;
      },
      
      get(key) {
        return this.state[key];
      },
    };
  }
  
  async execute(ctx) {
    const applicableMiddlewares = this.middlewares.filter(m => 
      !m.isError && ctx.path.startsWith(m.path)
    );
    
    let index = 0;
    
    const next = async () => {
      if (index >= applicableMiddlewares.length) return;
      
      const middleware = applicableMiddlewares[index++];
      await middleware.handler(ctx, next);
    };
    
    await next();
  }
  
  async handleError(error, ctx) {
    // Try error handlers
    for (const handler of this.errorHandlers) {
      try {
        await handler(error, ctx);
        if (ctx.response) return ctx.response;
      } catch (e) {
        error = e;
      }
    }
    
    // Try error middlewares
    const errorMiddlewares = this.middlewares.filter(m => m.isError);
    for (const { handler } of errorMiddlewares) {
      try {
        await handler(error, ctx, () => {});
        if (ctx.response) return ctx.response;
      } catch (e) {
        error = e;
      }
    }
    
    // Default error response
    console.error('Unhandled error:', error);
    return new Response(
      JSON.stringify({ error: 'Internal Server Error' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
}

// Usage
const app = new MiddlewarePipeline();

app.use(async (ctx, next) => {
  console.log(`${ctx.method} ${ctx.path}`);
  await next();
});

app.use('/api', async (ctx, next) => {
  ctx.set('apiVersion', 'v1');
  await next();
});

export default app.handler();
```

### Composable Middleware Factories

```javascript
// MIDDLEWARE COMPOSITION PATTERNS

// Higher-order middleware (factory pattern)
function withAuth(options = {}) {
  const { 
    header = 'Authorization',
    scheme = 'Bearer',
    verify = async (token) => { throw new Error('Must implement verify'); },
    onError = (ctx) => ctx.json({ error: 'Unauthorized' }, 401),
  } = options;
  
  return async (ctx, next) => {
    const authHeader = ctx.headers.get(header);
    
    if (!authHeader?.startsWith(`${scheme} `)) {
      return onError(ctx);
    }
    
    const token = authHeader.slice(scheme.length + 1);
    
    try {
      const user = await verify(token);
      ctx.set('user', user);
      await next();
    } catch (error) {
      return onError(ctx);
    }
  };
}

// Compose multiple middlewares
function compose(...middlewares) {
  return async (ctx, next) => {
    let index = -1;
    
    async function dispatch(i) {
      if (i <= index) {
        throw new Error('next() called multiple times');
      }
      index = i;
      
      let fn = middlewares[i];
      if (i === middlewares.length) fn = next;
      if (!fn) return;
      
      await fn(ctx, dispatch.bind(null, i + 1));
    }
    
    return dispatch(0);
  };
}

// Conditional middleware
function when(condition, middleware) {
  return async (ctx, next) => {
    const shouldRun = typeof condition === 'function' 
      ? await condition(ctx) 
      : condition;
    
    if (shouldRun) {
      await middleware(ctx, next);
    } else {
      await next();
    }
  };
}

// Path-scoped middleware
function scope(path, ...middlewares) {
  const composed = compose(...middlewares);
  
  return async (ctx, next) => {
    if (ctx.path.startsWith(path)) {
      await composed(ctx, next);
    } else {
      await next();
    }
  };
}

// Usage
const apiMiddleware = compose(
  withAuth({ verify: verifyJWT }),
  when(ctx => ctx.method === 'POST', validateBody),
  rateLimiter({ max: 100, window: 60000 }),
);

app.use('/api', apiMiddleware);
```

### Route-Specific Middleware Integration

```javascript
// INTEGRATING MIDDLEWARE WITH ROUTER

class Router {
  constructor() {
    this.routes = [];
    this.middlewares = [];
  }
  
  use(...middlewares) {
    this.middlewares.push(...middlewares);
    return this;
  }
  
  route(method, path, ...handlers) {
    const middleware = handlers.slice(0, -1);
    const handler = handlers[handlers.length - 1];
    
    this.routes.push({
      method: method.toUpperCase(),
      pattern: this.compile(path),
      middleware,
      handler,
    });
    
    return this;
  }
  
  get(path, ...handlers) { return this.route('GET', path, ...handlers); }
  post(path, ...handlers) { return this.route('POST', path, ...handlers); }
  put(path, ...handlers) { return this.route('PUT', path, ...handlers); }
  delete(path, ...handlers) { return this.route('DELETE', path, ...handlers); }
  
  compile(path) {
    const params = [];
    const regex = path.replace(/:(\w+)/g, (_, name) => {
      params.push(name);
      return '([^/]+)';
    });
    
    return {
      regex: new RegExp(`^${regex}$`),
      params,
    };
  }
  
  match(method, path) {
    for (const route of this.routes) {
      if (route.method !== method && route.method !== 'ALL') continue;
      
      const match = path.match(route.pattern.regex);
      if (match) {
        const params = {};
        route.pattern.params.forEach((name, i) => {
          params[name] = match[i + 1];
        });
        
        return { route, params };
      }
    }
    
    return null;
  }
  
  // Convert to middleware
  routes() {
    return async (ctx, next) => {
      const matched = this.match(ctx.method, ctx.path);
      
      if (!matched) {
        return next();
      }
      
      ctx.params = matched.params;
      
      // Combine all middlewares
      const allMiddleware = [
        ...this.middlewares,
        ...matched.route.middleware,
        matched.route.handler,
      ];
      
      await compose(...allMiddleware)(ctx, next);
    };
  }
}

// Usage
const userRouter = new Router();

userRouter.use(withAuth());

userRouter.get('/users', async (ctx) => {
  ctx.json({ users: await getUsers() });
});

userRouter.get('/users/:id', 
  validateParams({ id: 'number' }),
  async (ctx) => {
    const user = await getUser(ctx.params.id);
    ctx.json(user);
  }
);

app.use('/api', userRouter.routes());
```

### Async Context Propagation

```javascript
// ASYNC LOCAL STORAGE FOR MIDDLEWARE CONTEXT

import { AsyncLocalStorage } from 'node:async_hooks';

// Create storage for request context
const requestContext = new AsyncLocalStorage();

// Middleware to initialize context
function contextMiddleware() {
  return async (ctx, next) => {
    const store = {
      requestId: crypto.randomUUID(),
      startTime: Date.now(),
      user: null,
      tracing: {},
    };
    
    // Run rest of middleware chain within context
    await requestContext.run(store, async () => {
      await next();
    });
  };
}

// Get current request context (works anywhere in call stack)
function getContext() {
  return requestContext.getStore();
}

// Helper to get specific values
function getRequestId() {
  return getContext()?.requestId;
}

function getCurrentUser() {
  return getContext()?.user;
}

function setCurrentUser(user) {
  const ctx = getContext();
  if (ctx) ctx.user = user;
}

// Usage in middleware
const authMiddleware = async (ctx, next) => {
  const user = await verifyToken(ctx.headers.get('authorization'));
  setCurrentUser(user); // Available anywhere in request
  await next();
};

// Usage in any function (no need to pass context)
async function createOrder(data) {
  const user = getCurrentUser(); // Works!
  const requestId = getRequestId();
  
  console.log(`[${requestId}] Creating order for user ${user.id}`);
  
  return await db.orders.create({
    ...data,
    userId: user.id,
    createdAt: new Date(),
  });
}

// For edge runtimes without AsyncLocalStorage
class EdgeContext {
  static storage = new Map();
  
  static run(ctx, id, fn) {
    this.storage.set(id, ctx);
    try {
      return fn();
    } finally {
      this.storage.delete(id);
    }
  }
  
  static get(id) {
    return this.storage.get(id);
  }
}
```

### Plugin-Based Middleware System

```javascript
// EXTENSIBLE MIDDLEWARE PLUGIN ARCHITECTURE

class MiddlewarePlugin {
  constructor(name) {
    this.name = name;
    this.hooks = {};
  }
  
  // Lifecycle hooks
  onInit(fn) { this.hooks.init = fn; return this; }
  onRequest(fn) { this.hooks.request = fn; return this; }
  onResponse(fn) { this.hooks.response = fn; return this; }
  onError(fn) { this.hooks.error = fn; return this; }
  onDestroy(fn) { this.hooks.destroy = fn; return this; }
  
  // Convert to middleware
  toMiddleware() {
    return async (ctx, next) => {
      // Request phase
      if (this.hooks.request) {
        await this.hooks.request(ctx);
      }
      
      try {
        await next();
        
        // Response phase
        if (this.hooks.response) {
          await this.hooks.response(ctx);
        }
      } catch (error) {
        // Error phase
        if (this.hooks.error) {
          await this.hooks.error(error, ctx);
        } else {
          throw error;
        }
      }
    };
  }
}

// Plugin registry
class PluginRegistry {
  constructor() {
    this.plugins = new Map();
  }
  
  register(plugin) {
    this.plugins.set(plugin.name, plugin);
    return this;
  }
  
  async init(config) {
    for (const plugin of this.plugins.values()) {
      if (plugin.hooks.init) {
        await plugin.hooks.init(config);
      }
    }
  }
  
  getMiddlewares() {
    return [...this.plugins.values()].map(p => p.toMiddleware());
  }
  
  async destroy() {
    for (const plugin of this.plugins.values()) {
      if (plugin.hooks.destroy) {
        await plugin.hooks.destroy();
      }
    }
  }
}

// Example: Logging plugin
const loggingPlugin = new MiddlewarePlugin('logging')
  .onInit((config) => {
    console.log('Logging plugin initialized');
  })
  .onRequest((ctx) => {
    ctx.set('startTime', Date.now());
    console.log(`→ ${ctx.method} ${ctx.path}`);
  })
  .onResponse((ctx) => {
    const duration = Date.now() - ctx.get('startTime');
    console.log(`← ${ctx.response?.status} (${duration}ms)`);
  })
  .onError((error, ctx) => {
    console.error(`✕ Error: ${error.message}`);
    throw error; // Re-throw to let error handlers deal with it
  });

// Example: Metrics plugin
const metricsPlugin = new MiddlewarePlugin('metrics')
  .onInit(async (config) => {
    // Initialize metrics client
  })
  .onResponse((ctx) => {
    const duration = Date.now() - ctx.get('startTime');
    // Record metrics
    metrics.histogram('http_request_duration', duration, {
      method: ctx.method,
      path: ctx.path,
      status: ctx.response?.status,
    });
  });

// Usage
const registry = new PluginRegistry();
registry.register(loggingPlugin);
registry.register(metricsPlugin);

await registry.init(config);

const app = new MiddlewarePipeline();
app.use(...registry.getMiddlewares());
```

### Testing Middleware

```javascript
// MIDDLEWARE TESTING UTILITIES

class MockContext {
  constructor(options = {}) {
    this.method = options.method || 'GET';
    this.path = options.path || '/';
    this.headers = new Headers(options.headers);
    this.query = options.query || {};
    this.params = options.params || {};
    this.body = options.body;
    this.state = {};
    this.response = null;
  }
  
  json(data, status = 200) {
    this.response = { type: 'json', data, status };
  }
  
  text(body, status = 200) {
    this.response = { type: 'text', body, status };
  }
  
  set(key, value) {
    this.state[key] = value;
  }
  
  get(key) {
    return this.state[key];
  }
}

// Test helper
async function testMiddleware(middleware, options = {}) {
  const ctx = new MockContext(options);
  let nextCalled = false;
  let nextError = null;
  
  const next = async () => {
    nextCalled = true;
    if (options.nextThrows) {
      throw options.nextThrows;
    }
  };
  
  try {
    await middleware(ctx, next);
  } catch (error) {
    nextError = error;
  }
  
  return {
    ctx,
    nextCalled,
    error: nextError,
  };
}

// Tests
describe('authMiddleware', () => {
  it('passes authenticated requests', async () => {
    const { ctx, nextCalled, error } = await testMiddleware(
      withAuth({ verify: async () => ({ id: 1, name: 'Test' }) }),
      {
        headers: { authorization: 'Bearer valid-token' },
      }
    );
    
    expect(nextCalled).toBe(true);
    expect(error).toBeNull();
    expect(ctx.state.user).toEqual({ id: 1, name: 'Test' });
  });
  
  it('blocks unauthenticated requests', async () => {
    const { ctx, nextCalled } = await testMiddleware(
      withAuth({ verify: async () => ({ id: 1 }) }),
      { headers: {} }
    );
    
    expect(nextCalled).toBe(false);
    expect(ctx.response.status).toBe(401);
  });
  
  it('handles verification errors', async () => {
    const { ctx, nextCalled } = await testMiddleware(
      withAuth({ verify: async () => { throw new Error('Invalid'); } }),
      { headers: { authorization: 'Bearer bad-token' } }
    );
    
    expect(nextCalled).toBe(false);
    expect(ctx.response.status).toBe(401);
  });
});
```

## Related Skills

- See [universal-javascript-runtimes](../universal-javascript-runtimes/SKILL.md) for H3 and Nitro middleware
- See [routing-patterns](../routing-patterns/SKILL.md) for route-specific middleware
- See [meta-frameworks-overview](../meta-frameworks-overview/SKILL.md) for framework-specific middleware
