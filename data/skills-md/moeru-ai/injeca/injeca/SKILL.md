---
name: injeca
description: >-
  Guide for using injeca — a pure functional dependency injection library with application
  lifecycle management, inspired by go.uber.org/dig and go.uber.org/fig. Use this skill
  whenever the user imports from 'injeca', mentions injeca, needs dependency injection in
  TypeScript/JavaScript without classes, wants to wire up services with lifecycle hooks
  (start/stop), needs to manage application startup/shutdown order, or discusses functional
  DI patterns. Also use when the user asks about alternatives to tsyringe, inversify, or
  awilix that avoid class-based decorators.
license: MIT
metadata:
  author: moeru-ai
  version: "0.1.0"
---

# injeca

Pure functional dependency injection with application lifecycle management.

## Core Concepts

1. **No classes, no decorators** — everything is plain functions and objects
2. **Singleton by default** — `build` runs once, the result is cached
3. **Lifecycle hooks** — `onStart` / `onStop` for ordered startup and graceful shutdown
4. **Topological resolution** — dependencies are resolved in correct order, circular deps are detected

## API Quick Reference

### Global Container (Singleton)

The simplest way — `injeca` is a pre-created global container:

```ts
import { injeca, lifecycle } from 'injeca'

// Register a provider (returns a typed key for dependency declaration)
const config = injeca.provide('config', () => ({ port: 3000 }))

// Provider with dependencies and lifecycle
const server = injeca.provide({
  dependsOn: { config, lifecycle },
  async build({ dependsOn }) {
    const { config, lifecycle } = dependsOn
    const app = createServer()

    lifecycle.appHooks.onStart(() => app.listen(config.port))
    lifecycle.appHooks.onStop(() => app.close())

    return app
  },
})

// Invoke — runs after all providers are resolved
injeca.invoke({
  dependsOn: { server },
  async callback({ server }) {
    console.log('Server ready:', server.address())
  },
})

// Start the application (resolves deps → runs onStart hooks → runs invocations)
await injeca.start()

// Graceful shutdown (runs onStop hooks in reverse topological order)
process.once('SIGINT', () => injeca.stop())
```

### Scoped Container (for tests, per-request, or multiple instances)

```ts
import { createContainer, invoke, lifecycle, provide, start, stop } from 'injeca'

const container = createContainer()

const token = provide(container, 'token', () => crypto.randomUUID())

invoke(container, {
  dependsOn: { token },
  callback: ({ token }) => console.log('token', token),
})

await start(container)
await stop(container)
```

### Provider Patterns

#### Simple value provider

```ts
const config = injeca.provide('config', () => ({ port: 3000 }))
// or with scoped container:
const config = provide(container, 'config', () => ({ port: 3000 }))
```

#### Provider with dependencies

```ts
const db = injeca.provide({
  dependsOn: { config },
  build: ({ dependsOn }) => createDatabase(dependsOn.config.connectionString),
})
```

#### Provider with lifecycle hooks

```ts
const server = injeca.provide({
  dependsOn: { config, lifecycle },
  async build({ dependsOn }) {
    const { config, lifecycle } = dependsOn
    const app = createServer()

    lifecycle.appHooks.onStart(() => app.listen(config.port))
    lifecycle.appHooks.onStop(() => app.close())

    return app
  },
})
```

#### Lazy / reusable provider

If `build` returns a function, that function itself is cached (not its return value). Useful for factory patterns:

```ts
const createWindow = injeca.provide('createWindow', {
  dependsOn: { config },
  build: ({ dependsOn }) => {
    const getWindow = setupReusableWindow(dependsOn.config)
    return async () => await getWindow() // callable many times, same window
  },
})
```

### Lifecycle

Import `lifecycle` from `injeca` to declare start/stop hooks inside providers:

```ts
import { lifecycle } from 'injeca'

const service = injeca.provide({
  dependsOn: { lifecycle },
  build({ dependsOn }) {
    dependsOn.lifecycle.appHooks.onStart(() => { /* runs on start */ })
    dependsOn.lifecycle.appHooks.onStop(() => { /* runs on stop */ })
    return myService
  },
})
```

- `onStart` hooks run in topological order (dependencies first)
- `onStop` hooks run in reverse topological order (dependents first)
- Both are async-safe

### Manual Resolution

```ts
import { resolve } from 'injeca'

const resolved = await resolve(container, { config, db })
// resolved.config and resolved.db are ready to use
```

### Logger Configuration

```ts
import { createContainer } from 'injeca'

// Disable logging
const container = createContainer({ enabled: false })

// Custom logger
import { createLoggLogger } from 'injeca'
const container = createContainer({ logger: createLoggLogger() })
```

## Key Rules

1. **Singletons**: `build` only runs once — the return value is cached. If you return a function, the function is cached, not its result.
2. **Dependency declaration**: Use `dependsOn` with typed keys from `provide()` for full type safety.
3. **Lifecycle**: Always import `lifecycle` from `injeca` and declare it in `dependsOn` to get `onStart`/`onStop` hooks.
4. **Start order**: Call `start(container)` or `injeca.start()` after all providers and invocations are registered.
5. **Circular deps**: Injeca detects circular dependencies at resolution time and throws an error.
6. **No `any`**: Provider types are fully inferred from `build` return type and `dependsOn` declarations.

## Documentation

For the latest API reference, use context7 to query `injeca` documentation.
