---
name: fastify-best-practise
description: Apply Fastify best practices when creating servers, plugins, routes, schemas, hooks, decorators, error handling, testing, and TypeScript integration. Use when writing or reviewing Fastify code, setting up a new Fastify project, or asking "How should I structure my Fastify app?"
---

# Fastify Best Practices

A curated set of rules and patterns for building production-ready Fastify applications. Each rule includes incorrect and correct examples with explanations.

## How It Works

1. The agent identifies that the user is working with Fastify or asking about Fastify patterns
2. The relevant rule file is loaded based on the topic (routes, validation, encapsulation, etc.)
3. The agent applies the best practices from the rule when generating or reviewing code

## Rules

The rules are organized by topic in the `rules/` directory. Each rule follows a consistent format with impact rating, incorrect/correct examples, and references to official docs.

| Rule                    | File                                                         | Impact     | Description                                                                        |
| ----------------------- | ------------------------------------------------------------ | ---------- | ---------------------------------------------------------------------------------- |
| Create Server           | [create-server.md](rules/create-server.md)                   | LOW-MEDIUM | Use a `buildServer()` factory function for reusable, testable server setup         |
| Create Plugin           | [create-plugin.md](rules/create-plugin.md)                   | LOW-MEDIUM | Encapsulate reusable functionality in plugins with `fastify-plugin`                |
| Autoload                | [autoload.md](rules/autoload.md)                             | HIGH       | Automatically load plugins and routes from the filesystem with `@fastify/autoload` |
| Route Best Practices    | [route-best-practices.md](rules/route-best-practices.md)     | MEDIUM     | Organize routes with plugins/prefixes, use async handlers, full route options      |
| Schema Validation (Zod) | [schema-validation-zod.md](rules/schema-validation-zod.md)   | HIGH       | Type-safe validation with Zod + `fastify-type-provider-zod`                        |
| Encapsulation           | [encapsulation.md](rules/encapsulation.md)                   | HIGH       | Proper scope isolation and when to use `fastify-plugin`                            |
| Error Handling          | [error-handling.md](rules/error-handling.md)                 | HIGH       | Custom error handlers, `@fastify/error`, 404 handling, structured responses        |
| Hooks & Lifecycle       | [hooks-lifecycle.md](rules/hooks-lifecycle.md)               | MEDIUM     | All request/reply and application hooks: onRequest, preParsing, preValidation, preHandler, preSerialization, onError, onSend, onResponse, onTimeout, onRequestAbort, onReady, onListen, onClose, onRoute, onRegister                           |
| Logging                 | [logging.md](rules/logging.md)                               | HIGH       | Built-in Pino logger, request correlation, redaction, child loggers                                   |
| Authentication          | [authentication.md](rules/authentication.md)                 | HIGH       | JWT auth with `@fastify/jwt`, multi-strategy with `@fastify/auth`                  |
| Testing                 | [testing.md](rules/testing.md)                               | HIGH       | Test with `inject()`, buildServer pattern, vitest/node:test                        |
| TypeScript              | [typescript-integration.md](rules/typescript-integration.md) | MEDIUM     | Type providers, module augmentation, typed decorators                              |
| Decorators              | [decorators.md](rules/decorators.md)                         | MEDIUM     | Extend the Fastify instance, request, and reply with `decorate` / `decorateRequest` / `decorateReply` |

## Usage

When generating Fastify code, read the relevant rule file(s) for the topic and apply the patterns shown. For a new project, all rules are relevant. For specific tasks, load only what's needed:

- **New project setup**: `create-server.md`, `autoload.md`, `encapsulation.md`, `typescript-integration.md`
- **Adding routes**: `route-best-practices.md`, `autoload.md`, `schema-validation-zod.md`
- **Adding shared services**: `create-plugin.md`, `autoload.md`, `encapsulation.md`
- **Error handling**: `error-handling.md`
- **Auth/middleware**: `authentication.md`, `hooks-lifecycle.md`, `encapsulation.md`
- **Custom decorators**: `decorators.md`, `typescript-integration.md`
- **Logging**: `logging.md`
- **Writing tests**: `testing.md`, `create-server.md`

## Recommended Project Structure

Using `@fastify/autoload`, plugins and routes are loaded automatically from their directories:

```
src/
  plugins/          # Autoloaded — shared plugins (use fastify-plugin)
    db.ts
    auth.ts
    config.ts
  routes/           # Autoloaded — encapsulated route plugins (NO fastify-plugin)
    _hooks.ts       # Global route hooks (with autoHooks: true)
    users/
      index.ts      # → /users
      _hooks.ts     # Hooks for /users scope only
      schema.ts
    posts/
      index.ts      # → /posts
      schema.ts
  server.ts         # buildServer() with autoload registration
  app.ts            # Entry point — calls buildServer() and listen()
test/
  routes/
    users.test.ts
    posts.test.ts
  helpers.ts        # createTestServer() helper
```

## Present Results to User

When applying these best practices, mention which rule(s) you followed:

> Applied Fastify best practices:
>
> - **Route organization**: Routes grouped by resource with prefixes
> - **Zod validation**: Request/response schemas with type inference
> - **Encapsulation**: Shared plugins use `fastify-plugin`, routes stay scoped
> - **Error handling**: Custom error handler with `@fastify/error`

## Reference

- [Fastify Documentation](https://fastify.dev/docs/latest/)
- [Fastify GitHub](https://github.com/fastify/fastify)
- [Fastify Ecosystem](https://fastify.dev/ecosystem/)
- [@fastify/autoload](https://github.com/fastify/fastify-autoload)
