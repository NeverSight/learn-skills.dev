---
name: php-laravel
description: >-
  Modern PHP 8.4 and Laravel patterns: architecture, Eloquent, queues, testing.
  Use when working with Laravel, Eloquent, Blade, artisan, PHPUnit, PHPStan,
  or building/testing PHP applications with frameworks. Not for PHP internals (php-src)
  or general PHP language discussion.
---

# PHP & Laravel Development

## Code Style

- `declare(strict_types=1)` in every file
- Happy path last — handle errors/guards first, success at the end. Use early returns; avoid `else`.
- Comments only explain *why*, never *what*. Never comment tests. If code needs a "what" comment, rename or restructure instead.
- No single-letter variables — `$exception` not `$e`, `$request` not `$r`
- `?string` not `string|null`. Always specify `void`. Import classnames everywhere, never inline FQN.
- Validation uses array notation `['required', 'email']` for easier custom rule classes
- Static analysis: run PHPStan at level 8+ (`phpstan analyse --level=8`). Aim for level 9 on new projects. Use `@phpstan-type` and `@phpstan-param` for generic collection types.

## Modern PHP (8.4)

Use these when applicable — do not explain them in comments (Claude and developers know them):
- Readonly classes and properties for immutable data
- Enums with methods and interfaces for domain constants
- Match expressions over switch
- Constructor promotion with readonly
- First-class callable syntax `$fn = $obj->method(...)`
- Fibers for cooperative async when Swoole/ReactPHP not available
- DNF types `(Stringable&Countable)|null` for complex constraints
- Property hooks: `public string $name { get => strtoupper($this->name); set => trim($value); }`
- Asymmetric visibility: `public private(set) string $name` — public read, private write
- `new` without parentheses in chains: `new MyService()->handle()`
- `array_find()`, `array_any()`, `array_all()` — native array search/check without closures wrapping Collection

## Laravel Architecture

- **Fat models, thin controllers** — controllers only: validate, call service/action, return response
- **Service classes** for business logic with readonly DI: `__construct(private readonly PaymentService $payments)`
- **Action classes** (single-purpose invokable) for operations that cross service boundaries
- **Form Requests** for all validation — never validate inline in controllers. Add `toDto()` method to convert validated data to typed service parameters.
- Conditional validation: `Rule::requiredIf()`, `sometimes`, `exclude_if` for complex form logic
- **Events + Listeners** for side effects (notifications, logging, cache invalidation). Do not put side effects in services.
- Feature folder organization over type-based when project exceeds ~20 models

## Eloquent

- `Model::preventLazyLoading(!app()->isProduction())` — catch N+1 during development
- Select only needed columns: `Post::with(['user:id,name'])->select(['id', 'title', 'user_id'])`
- Bulk operations at database level: `Post::where('status', 'draft')->update([...])` — do not load into memory to update
- `increment()`/`decrement()` for counters in a single query
- Composite indexes for common query combinations
- Chunking for large datasets (`chunk(1000)`), lazy collections for memory-constrained processing
- Query scopes (`scopeActive`, `scopeRecent`) for reusable constraints
- `withCount('comments')` / `withExists('approvals')` for aggregate subqueries — never load relations just to count
- `->when($filter, fn($q) => $q->where(...))` for conditional query building
- `DB::transaction(fn() => ...)` — automatic rollback on exception
- `Model::upsert($rows, ['unique_key'], ['update_cols'])` for bulk insert-or-update
- `Prunable` / `MassPrunable` trait with `prunable()` query for automatic stale record cleanup
- `$guarded = []` is a mass assignment vulnerability — always use explicit `$fillable`

## API Resources

- `whenLoaded()` for relationships — prevents N+1 in responses
- `when()` / `mergeWhen()` for permission-based field inclusion
- `whenPivotLoaded()` for pivot data
- `withResponse()` for custom headers, `with()` for metadata (version, pagination)

## Queues & Jobs

- Job batching with `Bus::batch([...])->then()->catch()->finally()->dispatch()`
- Job chaining for sequential ops: `Bus::chain([new Step1, new Step2])->dispatch()`
- Rate limiting: `Redis::throttle('api')->allow(10)->every(60)->then(fn() => ...)`
- `ShouldBeUnique` interface to prevent duplicate processing
- Always handle failures — implement `failed()` method on jobs

## Testing (PHPUnit)

- **Feature tests** (`tests/Feature/`): HTTP through the full stack. Use `$this->getJson()`, `$this->postJson()`, etc.
- **Unit tests** (`tests/Unit/`): Isolated logic -- services, actions, value objects. No HTTP, minimal database.
- Default to feature tests for anything touching routes, controllers, or models
- `use RefreshDatabase` trait in every test class that touches the database
- Model factories for all test data -- never raw `DB::table()` inserts
- One behavior per test. Name with `test_` prefix: `test_user_can_update_own_profile`
- Assert both response status AND side effects (DB state, dispatched jobs, sent notifications)
- `actingAs($user)` for auth, `Sanctum::actingAs($user, ['ability'])` for API auth
- Fake facades BEFORE the action: `Queue::fake()` then act then `Queue::assertPushed(...)`
- `assertDatabaseHas` / `assertDatabaseMissing` to verify persistence
General testing discipline (anti-patterns, rationalization resistance): `writing-tests` skill.
See [testing patterns and examples](./references/testing.md) for PHPUnit essentials, data providers, and running tests.
See [feature testing](./references/feature-testing.md) for auth, validation, API, console, and DB assertions.
See [mocking and faking](./references/mocking-and-faking.md) for facade fakes and action mocking.
See [factories](./references/factories.md) for states, relationships, sequences, and afterCreating hooks.

## Discipline

- For non-trivial changes, pause and ask: "is there a more elegant way?" Skip for obvious fixes.
- Simplicity first — every change as simple as possible, impact minimal code
- Only touch what's necessary — avoid introducing unrelated changes
- No hacky workarounds — if a fix feels wrong, step back and implement the clean solution

## Production Performance

- **OPcache**: enable in production (`opcache.enable=1`), set `opcache.memory_consumption=256`, `opcache.max_accelerated_files=20000`. Validate with `opcache_get_status()`.
- **JIT**: enable with `opcache.jit_buffer_size=100M`, `opcache.jit=1255` (tracing). Biggest gains on CPU-bound code (math, loops), minimal impact on I/O-bound Laravel requests.
- **Preloading**: `opcache.preload=preload.php` — preload framework classes and hot app classes. Use `composer dumpautoload --classmap-authoritative` in production.
- **Laravel-specific**: `php artisan config:cache && php artisan route:cache && php artisan view:cache && php artisan event:cache` — run on every deploy. `composer install --optimize-autoloader --no-dev` for production.

## Anti-Patterns

- Querying in loops — use eager loading or `whereIn()` instead
- Empty catch blocks — log or rethrow, never swallow
- Business logic in controllers — extract to service/action instead
- `protected $guarded = []` — use `$fillable` instead
- Inline validation in controllers — use Form Requests instead

## References

- [laravel-ecosystem.md](./references/laravel-ecosystem.md) -- Notifications, Task Scheduling, Custom Casts
- [testing.md](./references/testing.md) -- PHPUnit essentials, data providers, running tests
- [feature-testing.md](./references/feature-testing.md) -- Auth, validation, API, console, DB assertions
- [mocking-and-faking.md](./references/mocking-and-faking.md) -- Facade fakes, action mocking, Mockery
- [factories.md](./references/factories.md) -- States, relationships, sequences, afterCreating hooks
