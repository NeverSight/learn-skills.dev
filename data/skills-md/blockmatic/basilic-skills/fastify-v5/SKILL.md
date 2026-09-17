---
name: fastify-v5
description: TypeBox schemas with Fastify routes for type-safe API development — native JSON Schema, automatic OpenAPI generation. Use when building Fastify REST APIs with schema validation and OpenAPI generation.
---

# Skill: fastify

## Scope

- Applies to: Fastify v5+ with TypeBox schemas, type-safe route definitions, automatic OpenAPI generation, plugins, hooks, testing
- Does NOT cover: Database integration (see [drizzle-orm](../drizzle-orm-v0/SKILL.md))

## Assumptions

- Fastify v5+
- `@fastify/type-provider-typebox` for TypeBox type provider
- `@sinclair/typebox` for schema definitions
- TypeScript v5+ with strict mode

## Principles

- Use TypeBox schemas for route validation (params, query, body, response)
- Use `TypeBoxTypeProvider` for automatic type inference from schemas
- Define response schemas for all status codes
- Use OpenAPI generation from schemas (via `@fastify/swagger`)
- Request types (`request.params`, `request.query`, `request.body`) are inferred from schemas
- Response validation happens automatically based on schema

## Constraints

### MUST

- Use `TypeBoxTypeProvider` for type safety: `fastify.withTypeProvider<TypeBoxTypeProvider>()`
- Define response schemas for all status codes
- Use TypeBox `Type.*` constructors for schema definitions

### SHOULD

- Use `operationId` in route schemas for OpenAPI generation
- Use `tags` for route organization in OpenAPI docs
- Define error response schemas for error cases

### AVOID

- Manual type assertions (types inferred from schemas)
- Skipping response schema definitions
- Mixing TypeBox with other schema libraries in same route

## Interactions

- Complements [drizzle-orm](../drizzle-orm-v0/SKILL.md) for database integration
- Generates OpenAPI specs compatible with [openapi-ts](../openapi-ts-v0/SKILL.md) codegen

## Patterns

### Route Schema Pattern

```typescript
import { Type } from '@sinclair/typebox'
import type { FastifyPluginAsync } from 'fastify'

const UserSchema = Type.Object({
  id: Type.String(),
  email: Type.String({ format: 'email' }),
  name: Type.String(),
})

const userRoutes: FastifyPluginAsync = async fastify => {
  fastify.get('/users/:id', {
    schema: {
      operationId: 'getUser',
      params: Type.Object({ id: Type.String() }),
      response: {
        200: UserSchema,
        404: Type.Object({ code: Type.String(), message: Type.String() }),
      },
    },
  }, async (request, reply) => {
    // request.params.id is typed
    const { id } = request.params
    return reply.send(user)
  })
}
```

### Schema Types

```typescript
Type.String()
Type.Number()
Type.Boolean()
Type.Object({ id: Type.String() })
Type.Array(Type.String())
Type.Optional(Type.String())
Type.Union([Type.String(), Type.Number()])
```

See [Route Schema Template](templates/route-schema.ts) for complete example.

### Instance Configuration

Configure Fastify instance with TypeBox type provider, logger, and request settings:

```typescript
import type { TypeBoxTypeProvider } from '@fastify/type-provider-typebox'
import Fastify, { LogController } from 'fastify'

const fastify = Fastify({
  logger: {
    level: 'info',
    transport: process.env.NODE_ENV === 'development' ? {
      target: 'pino-pretty',
    } : undefined,
  },
  trustProxy: true,
  bodyLimit: 1048576, // 1MB
  requestTimeout: 30000,
  requestIdHeader: 'x-request-id',
  logController: new LogController({ requestIdLogLabel: 'reqId', disableRequestLogging: false }),
}).withTypeProvider<TypeBoxTypeProvider>()
```

See [Instance Configuration](references/instance-config.md) for complete setup.

### Plugin Development

Create reusable plugins with `fastify-plugin` for non-encapsulated behavior:

```typescript
import type { FastifyPluginAsync } from 'fastify'
import fp from 'fastify-plugin'

const myPlugin: FastifyPluginAsync = async fastify => {
  // Plugin logic
}

export default fp(myPlugin, {
  name: 'my-plugin',
})
```

See [Plugin Patterns](references/plugins.md) and [Plugin Template](templates/plugin.ts) for examples.

### Hooks (Request Lifecycle)

Use hooks to intercept requests, modify responses, or handle errors:

```typescript
fastify.addHook('onRequest', async (request, reply) => {
  // Add security headers, logging, etc.
})

fastify.addHook('onResponse', async (request, reply) => {
  // Modify response, add headers, etc.
})

fastify.addHook('onError', async (request, reply, error) => {
  // Handle errors
})
```

See [Hooks Guide](references/hooks.md) and [Hook Plugin Template](templates/hook-plugin.ts) for patterns.

### Testing with inject()

Test routes using Fastify's `inject()` method for blackbox testing:

```typescript
const response = await fastify.inject({
  method: 'GET',
  url: '/users/123',
})

expect(response.statusCode).toBe(200)
const data = JSON.parse(response.body)
```

See [Testing Patterns](references/testing.md) and [Test Utils Template](templates/test-utils.ts) for setup.

### Streaming Responses

Handle streaming responses (e.g., Server-Sent Events, text streams):

```typescript
fastify.post('/stream', {
  schema: {
    response: {
      200: Type.String({ description: 'Streaming response' }),
    },
  },
}, async (request, reply) => {
  reply.header('Content-Type', 'text/event-stream')
  reply.header('Cache-Control', 'no-cache')
  return reply.send(stream)
})
```

### Common Plugins

#### Rate Limiting

```typescript
import rateLimit from '@fastify/rate-limit'

await fastify.register(rateLimit, {
  max: 100,
  timeWindow: 60000,
  keyGenerator: request => request.ip,
})
```

#### CORS

```typescript
import cors from '@fastify/cors'

await fastify.register(cors, {
  origin: (origin, callback) => {
    // Validate origin
    callback(null, true)
  },
  credentials: false,
})
```

#### Error Handler

```typescript
fastify.setErrorHandler((error, request, reply) => {
  // Global error handling
  reply.status(error.statusCode ?? 500).send({
    code: 'ERROR',
    message: error.message,
  })
})
```

### Graceful Shutdown

Handle process signals for graceful shutdown:

```typescript
const shutdown = async (signal: string) => {
  fastify.log.info({ signal }, 'Shutting down')
  await fastify.close()
  process.exit(0)
}

process.on('SIGTERM', () => shutdown('SIGTERM'))
process.on('SIGINT', () => shutdown('SIGINT'))
```

### AutoLoad Pattern

Use `@fastify/autoload` for automatic plugin/route discovery:

```typescript
import AutoLoad from '@fastify/autoload'

await fastify.register(AutoLoad, {
  dir: path.join(__dirname, 'plugins'),
  forceESM: true,
})
```

## References

- [OpenAPI Integration](references/openapi-integration.md) - OpenAPI generation patterns
- [Plugin Patterns](references/plugins.md) - Plugin development with fastify-plugin
- [Hooks Guide](references/hooks.md) - Request lifecycle hooks
- [Testing Patterns](references/testing.md) - Testing with inject()
- [Instance Configuration](references/instance-config.md) - Fastify instance setup