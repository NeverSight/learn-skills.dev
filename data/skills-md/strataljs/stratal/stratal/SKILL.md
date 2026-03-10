---
name: stratal
description: >-
  Use when working with the Stratal core framework for Cloudflare Workers — modules,
  dependency injection, controllers, routing, OpenAPI, queues, cron, email, storage,
  caching, i18n, logging, guards, middleware, config, events, and error handling.
  Trigger on: stratal, Stratal, StratalWorker, @Module, @Controller, @Route, IController,
  RouterContext, @inject, Scope, @Listener, @On, queues, cron, email, storage, cache,
  i18n, logging, guards, middleware, config, OpenAPIModule, ConfigModule, CacheModule,
  EmailModule, StorageModule, QueueModule, I18nModule, ApplicationError, StratalEnv,
  registerAs, StratalDurableObject, StratalWorkerEntrypoint, StratalWorkflow, runInScope,
  stratal/workers, DurableObject, Workflow, WorkerEntrypoint, Service Binding, RPC.
user-invocable: false
license: MIT
metadata:
  author: Temitayo Fadojutimi
  version: "2.0"
---

# Stratal Core Framework

Stratal is a modular Cloudflare Workers framework with dependency injection (tsyringe), Hono-based routing with OpenAPI generation, queue consumers, cron jobs, i18n, caching, storage, and email. Full documentation at [stratal.dev](https://stratal.dev).

## Key Constraints

- ESM-only (`"type": "module"`)
- Build with `tsc` only — **never** esbuild/tsup (tsyringe requires `emitDecoratorMetadata`)
- `experimentalDecorators` and `emitDecoratorMetadata` must be enabled in tsconfig
- Always import Zod from `stratal/validation`, never from `zod` directly
- Service classes can be used directly as DI tokens (`@inject(MyService)`). Only create Symbol tokens when the service needs to be replaceable or is part of a reusable library
- Use constructor injection with `@inject()` decorators

## Project Setup

Docs: [Installation](https://stratal.dev/getting-started/installation) · [Your First Worker](https://stratal.dev/getting-started/your-first-worker)

```ts
// src/index.ts — Worker entry point
import { Stratal } from 'stratal';
import { AppModule } from './app.module';

const app = new Stratal({ module: AppModule });

export default app;
```

## Modules

Docs: [Modules](https://stratal.dev/core-concepts/modules) · [Lifecycle Hooks](https://stratal.dev/core-concepts/lifecycle-hooks)

```ts
@Module({
  imports: [OtherModule],
  providers: [MyService],
  controllers: [MyController],
  consumers: [MyConsumer],
  jobs: [MyCronJob],
})
export class AppModule implements OnInitialize {
  onInitialize(ctx: ModuleContext) { /* setup logic */ }
}
```

Dynamic modules use `forRoot()` (sync) or `forRootAsync()` (async factory). Lifecycle hooks: `OnInitialize`, `OnShutdown`.

## Controllers and Routing

Docs: [Controllers & Routing](https://stratal.dev/core-concepts/controllers-and-routing) · [OpenAPI](https://stratal.dev/openapi/overview)

```ts
@Controller('/api/v1/users', { tags: ['Users'] })
export class UsersController implements IController {
  constructor(@inject(UsersService) private usersService: UsersService) {}

  @Route({ body: CreateUserSchema, response: UserSchema })
  async create(ctx: RouterContext) {
    const data = await ctx.body<CreateUserInput>();
    return ctx.json(await this.usersService.create(data));
  }
}
```

**Method → HTTP mapping:** `index` → GET, `show` → GET /:id, `create` → POST (201), `update` → PUT /:id, `patch` → PATCH /:id, `destroy` → DELETE /:id.

Use `await ctx.body<T>()` to get validated body — **not** `ctx.req.valid('json')`.

## Dependency Injection

Docs: [DI](https://stratal.dev/core-concepts/dependency-injection) · [Providers](https://stratal.dev/core-concepts/providers)

```ts
// Simple: use class directly as token
@Transient()
export class UsersService { /* ... */ }
// inject with: @inject(UsersService)

// Symbol tokens — only for replaceable abstractions
const USER_REPO = Symbol.for('UserRepository');
@Module({
  providers: [
    { provide: USER_REPO, useClass: PgUserRepository, scope: Scope.Request },
  ],
})
```

| Scope | Behavior |
|---|---|
| `Scope.Transient` | New instance per resolution (default) |
| `Scope.Singleton` | Single instance globally |
| `Scope.Request` | New instance per HTTP request |

**Provider types:** `useClass`, `useValue`, `useFactory` (with `inject` array), `useExisting`.

## StratalEnv Augmentation

Docs: [Environment Typing](https://stratal.dev/guides/environment-typing)

```ts
// 1. Generate wrangler types: npx wrangler types
// 2. Extend StratalEnv with Cloudflare.Env:
export {};

declare module 'stratal' {
  interface StratalEnv extends Cloudflare.Env {}
}
```

Run `npx wrangler types` to generate `Cloudflare.Env` from your `wrangler.jsonc` bindings.

## Guards and Middleware

Docs: [Guards](https://stratal.dev/guides/guards) · [Middleware](https://stratal.dev/guides/middleware)

```ts
// Guard — implements CanActivate
@Transient()
export class ApiKeyGuard implements CanActivate {
  constructor(@inject(DI_TOKENS.CloudflareEnv) private env: StratalEnv) {}
  canActivate(ctx: RouterContext): boolean {
    return ctx.header('x-api-key') === this.env.API_KEY;
  }
}
// Apply with @UseGuards(ApiKeyGuard) on controller or method
```

```ts
// Middleware class — implements Middleware
@Transient()
export class LoggingMiddleware implements Middleware {
  async handle(ctx: RouterContext, next: () => Promise<void>) {
    console.log(`--> ${ctx.c.req.method} ${ctx.c.req.path}`);
    await next();
  }
}
```

```ts
// Middleware registration — module implements MiddlewareConfigurable
export class AppModule implements MiddlewareConfigurable {
  configure(consumer: MiddlewareConsumer) {
    consumer.apply(LoggingMiddleware).forRoutes('*');
    consumer.apply(CorsMiddleware).exclude('/health').forRoutes(ApiController);
  }
}
```

## Configuration

Docs: [Configuration](https://stratal.dev/core-concepts/configuration)

```ts
const databaseConfig = registerAs('database', (env: StratalEnv) => ({
  url: env.DATABASE_URL,
  poolSize: 10,
}));

@Module({ providers: [databaseConfig.asProvider()] })
export class AppModule {}
// Inject with: @inject(databaseConfig.KEY) config: { url: string; poolSize: number }
```

## Events

Docs: [Events](https://stratal.dev/core-concepts/events)

```ts
@Listener()
export class UserCreatedListener {
  @On('after.User.create')
  async sendWelcomeEmail(context: EventContext<'after.User.create'>) {
    // handle event
  }
}
```

Augment `CustomEventRegistry` for type-safe custom events. Options: `priority` (number), `blocking` (boolean).

## Error Handling

Docs: [Error Handling](https://stratal.dev/guides/error-handling)

```ts
import { ApplicationError, ERROR_CODES } from 'stratal/errors';

export class UserNotFoundError extends ApplicationError {
  constructor(userId: string) {
    super('errors.userNotFound', ERROR_CODES.RESOURCE.NOT_FOUND, { userId });
  }
}
```

`ApplicationError` provides structured JSON responses with i18n message keys, numeric error codes (from `ERROR_CODES`), and metadata.

## Queue Consumers

Docs: [Queues](https://stratal.dev/integrations/queues)

```ts
@Transient()
export class EmailConsumer implements IQueueConsumer<EmailPayload> {
  readonly messageTypes = ['email.send'];

  async handle(message: QueueMessage<EmailPayload>) {
    // process message.payload
  }
}
```

Register in module `consumers` array. Messages have `id`, `type`, `payload`, and optional `metadata`.

## Cron Jobs

Docs: [Cron Jobs](https://stratal.dev/integrations/cron-jobs)

```ts
@Transient()
export class CleanupJob implements CronJob {
  readonly schedule = '0 2 * * *';

  async execute(controller: ScheduledController) {
    // runs daily at 2 AM UTC
  }
}
```

Register in module `jobs` array. Schedule must match a trigger in `wrangler.jsonc`.

## Workers

Docs: [Durable Objects](https://stratal.dev/integrations/durable-objects) · [Service Bindings](https://stratal.dev/integrations/service-bindings) · [Workflows](https://stratal.dev/integrations/workflows)

Stratal provides base classes for Cloudflare Workers primitives (Durable Objects, Service Bindings/RPC, Workflows) with built-in DI support. Each class exposes a `runInScope()` method that creates a request-scoped DI container from the static Stratal singleton.

```ts
// src/index.ts — MUST export Stratal as default + worker classes as named exports
export { Counter } from './counter';
export { AuthRpc } from './auth-rpc';
export { MyWorkflow } from './my-workflow';
export default new Stratal({ module: AppModule });
```

### StratalDurableObject

Extends `DurableObject`. `runInScope` auto-registers `DI_TOKENS.DurableObjectState` and `DI_TOKENS.DurableObjectId`.

```ts
export class Counter extends StratalDurableObject {
  async increment() {
    return this.runInScope(async (container) => {
      const counterService = container.resolve<CounterService>(CounterService)

      counterService.increment();
    });
  }
}
```

### StratalWorkerEntrypoint

Extends `WorkerEntrypoint` for RPC / Service Bindings.

```ts
export class AuthRpc extends StratalWorkerEntrypoint {
  async verifyToken(token: string) {
    return this.runInScope(async (container) => {
      const auth = container.resolve(AuthService);
      return auth.verify(token);
    });
  }
}
```

### StratalWorkflow

Extends `WorkflowEntrypoint` with generic `Env` and `Params` types.

```ts
export class MyWorkflow extends StratalWorkflow<Env, { orderId: string }> {
  async run(event: WorkflowEvent<{ orderId: string }>, step: WorkflowStep) {
    await step.do('process', () =>
      this.runInScope(async (container) => {
        const svc = container.resolve(OrderService);
        return svc.validate(event.payload.orderId);
      })
    );
  }
}
```

## Built-in Modules Quick Reference

| Module | Import | Docs |
|---|---|---|
| `CacheModule` | `stratal/cache` | [Caching](https://stratal.dev/integrations/caching) |
| `EmailModule` | `stratal/email` | [Email](https://stratal.dev/integrations/email) |
| `StorageModule` | `stratal/storage` | [Storage](https://stratal.dev/integrations/storage) |
| `I18nModule` | `stratal/i18n` | [i18n](https://stratal.dev/integrations/i18n) |
| `OpenAPIModule` | `stratal/openapi` | [OpenAPI](https://stratal.dev/openapi/overview) |
| `LoggerService` | `stratal/logger` | [Logging](https://stratal.dev/integrations/logging) |
| `ConfigModule` | `stratal/config` | [Configuration](https://stratal.dev/core-concepts/configuration) |
| `QueueModule` | `stratal/queue` | [Queues](https://stratal.dev/integrations/queues) |

## Sub-path Imports

| Path | Key Exports |
|---|---|
| `stratal` | `Stratal`, `Application`, `@Module`, `StratalEnv` |
| `stratal/di` | `Container`, `DI_TOKENS`, `Scope`, `inject`, `Transient` |
| `stratal/router` | `@Controller`, `@Route`, `RouterContext`, `UseGuards`, `IController` |
| `stratal/validation` | `z` (Zod), `ZodType`, validation utilities |
| `stratal/errors` | `ApplicationError`, `ERROR_CODES`, built-in error classes |
| `stratal/events` | `@Listener`, `@On`, `EventRegistry` |
| `stratal/i18n` | `I18nModule`, `I18nService` |
| `stratal/cache` | `CacheModule`, `CacheService` |
| `stratal/email` | `EmailModule`, `EmailService` |
| `stratal/storage` | `StorageModule`, `StorageService` |
| `stratal/queue` | `QueueModule`, `QueueService`, `IQueueConsumer` |
| `stratal/logger` | `LoggerService`, `LOGGER_TOKENS` |
| `stratal/config` | `ConfigModule`, `registerAs` |
| `stratal/openapi` | `OpenAPIModule` |
| `stratal/workers` | `StratalDurableObject`, `StratalWorkerEntrypoint`, `StratalWorkflow`, `runInScope` |

## Do's and Don'ts

- **Do** use class references as DI tokens for simple services (`@inject(MyService)`)
- **Do** use Symbol tokens only for replaceable abstractions or reusable libraries
- **Do** use `await ctx.body<T>()` for validated request bodies
- **Do** import Zod from `stratal/validation`
- **Do** use constructor injection with `@inject()`
- **Do** add `@Transient()` to consumers, jobs, guards, middleware, and listeners
- **Do** register consumers in `consumers` and jobs in `jobs` arrays
- **Don't** use esbuild or tsup — only `tsc`
- **Don't** use `ctx.req.valid('json')` — use `await ctx.body<T>()`
- **Don't** import Zod from `zod` directly
- **Do** export the `Stratal` instance as the default export (required for the static singleton used by worker classes)
- **Do** use `runInScope` for each method/workflow step that needs DI — each call gets a fresh request-scoped container
- **Don't** cache container references across `runInScope` calls — the container is only valid within the callback
- **Don't** disable `emitDecoratorMetadata` in tsconfig
