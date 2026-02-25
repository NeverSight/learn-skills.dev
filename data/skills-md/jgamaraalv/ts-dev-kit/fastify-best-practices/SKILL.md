---
name: fastify-best-practices
description: "Fastify 5 best practices, API reference, and patterns for routes, plugins, hooks, validation, error handling, and TypeScript. Use when: (1) writing new Fastify routes, plugins, or hooks, (2) looking up Fastify API signatures or options, (3) debugging Fastify issues (lifecycle, encapsulation, validation, plugin timeout), (4) reviewing Fastify code for anti-patterns. Triggers: 'add a route', 'create plugin', 'Fastify hook', 'validation schema', 'Fastify error', 'setErrorHandler', 'fastify-plugin'."
---

# Fastify 5 Best Practices

## Table of Contents

- [Request lifecycle](#request-lifecycle-exact-order)
- [Top anti-patterns](#top-anti-patterns)
- [Quick patterns](#quick-patterns)
  - [Plugin with fastify-plugin (FastifyPluginCallback)](#plugin-with-fastify-plugin-fastifyplugincallback)
  - [Route with validation](#route-with-validation)
  - [Hook (application-level)](#hook-application-level)
  - [Error handler](#error-handler)
- [Reference files](#reference-files)

## Request lifecycle (exact order)

```
Incoming Request
  └─ Routing
      └─ onRequest hooks
          └─ preParsing hooks
              └─ Content-Type Parsing
                  └─ preValidation hooks
                      └─ Schema Validation (→ 400 on failure)
                          └─ preHandler hooks
                              └─ Route Handler
                                  └─ preSerialization hooks
                                      └─ onSend hooks
                                          └─ Response Sent
                                              └─ onResponse hooks
```

Error at any stage → `onError` hooks → error handler → `onSend` → response → `onResponse`.

## Top anti-patterns

1. **Mixing async/callback in handlers** — Use `async` OR callbacks, never both. With async, `return` the value; don't call `reply.send()` AND return.

2. **Returning `undefined` from async handler** — Fastify treats this as "no response yet". Return the data or call `reply.send()`.

3. **Using arrow functions when you need `this`** — Arrow functions don't bind `this` to the Fastify instance. Use `function` declarations for handlers that need `this`.

4. **Forgetting `fastify-plugin` wrapper** — Without it, decorators/hooks stay scoped to the child context. Parent and sibling plugins won't see them.

5. **Decorating with reference types directly** — `decorateRequest('data', {})` shares the SAME object across all requests. Use `null` initial + `onRequest` hook to assign per-request.

6. **Sending response in `onError` hook** — `onError` is read-only for logging. Use `setErrorHandler()` to modify error responses.

7. **Not handling `reply.send()` in async hooks** — Call `return reply` after `reply.send()` in async hooks to prevent "Reply already sent" errors.

8. **Ignoring encapsulation** — Decorators/hooks registered in child plugins are invisible to parents. Design your plugin tree carefully.

9. **String concatenation in SQL from route params** — Always use parameterized queries. Fastify validates input shape, not content safety.

10. **Missing response schema** — Without `response` schema, Fastify serializes with `JSON.stringify()` (slow) and may leak sensitive fields. Use `fast-json-stringify` via response schemas.

## Quick patterns

### Plugin with fastify-plugin (FastifyPluginCallback)

Project convention: use `FastifyPluginCallback` + `done()` (avoids `require-await` lint errors).

```ts
import fp from "fastify-plugin";
import type { FastifyPluginCallback } from "fastify";

const myPlugin: FastifyPluginCallback = (fastify, opts, done) => {
  fastify.decorate("myService", new MyService());
  done();
};

export default fp(myPlugin, { name: "my-plugin" });
```

### Route with validation

```ts
fastify.post<{ Body: CreateUserBody }>("/users", {
  schema: {
    body: {
      type: "object",
      required: ["email", "name"],
      properties: {
        email: { type: "string", format: "email" },
        name: { type: "string", minLength: 1 },
      },
    },
    response: {
      201: {
        type: "object",
        properties: {
          id: { type: "string" },
          email: { type: "string" },
        },
      },
    },
  },
  handler: async (request, reply) => {
    const user = await createUser(request.body);
    return reply.code(201).send(user);
  },
});
```

### Hook (application-level)

```ts
fastify.addHook("onRequest", async (request, reply) => {
  request.startTime = Date.now();
});

fastify.addHook("onResponse", async (request, reply) => {
  request.log.info({ elapsed: Date.now() - request.startTime }, "request completed");
});
```

### Error handler

```ts
fastify.setErrorHandler((error, request, reply) => {
  request.log.error(error);
  const statusCode = error.statusCode ?? 500;
  reply.code(statusCode).send({
    error: statusCode >= 500 ? "Internal Server Error" : error.message,
  });
});
```

## Reference files

Load the relevant file when you need detailed API information:

- **Server factory & options** — constructor options, server methods, properties: [references/server-and-options.md](references/server-and-options.md)
- **Routes & handlers** — declaration, URL params, async patterns, constraints: [references/routes-and-handlers.md](references/routes-and-handlers.md)
- **Hooks & lifecycle** — all 16 hook types, signatures, scope, early response: [references/hooks-and-lifecycle.md](references/hooks-and-lifecycle.md)
- **Plugins & encapsulation** — creating plugins, fastify-plugin, context inheritance: [references/plugins-and-encapsulation.md](references/plugins-and-encapsulation.md)
- **Validation & serialization** — JSON Schema, Ajv, response schemas, custom validators: [references/validation-and-serialization.md](references/validation-and-serialization.md)
- **Request, Reply & errors** — request/reply API, error handling, FST_ERR codes: [references/request-reply-errors.md](references/request-reply-errors.md)
- **TypeScript & logging** — route generics, type providers, Pino config, decorators: [references/typescript-and-logging.md](references/typescript-and-logging.md)
