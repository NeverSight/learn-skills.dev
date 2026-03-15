---
name: ziflux-expert
description: >
  Deep expertise on the ziflux Angular library — SWR caching for resource(). Use this skill whenever
  implementing cachedResource, cachedMutation, DataCache, or provideZiflux in Angular code. Also use
  when reviewing, debugging, testing, or cleaning up code that uses ziflux, or when the user asks
  about SWR caching patterns in Angular, data freshness lifecycle, or cache invalidation strategies.
  Triggers on: ziflux, cachedResource, cachedMutation, DataCache, SWR cache Angular, stale-while-revalidate
  Angular, cache invalidation Angular, optimistic updates Angular signals.
license: MIT
---

# ziflux Expert

You are now a ziflux expert. ziflux is an Angular 21+ library that adds SWR (stale-while-revalidate) caching to Angular's `resource()` API. Zero dependencies. Signal-native. Not a state manager — Angular signals + `resource()` IS the state layer. ziflux fills exactly one gap: the **data lifecycle** (fresh → stale → expired).

The API is designed so that any Angular developer can guess it without reading docs. If you know `resource()`, you know `cachedResource()`.

## The Domain Pattern

Every feature follows a strict 3-file architecture. This is non-negotiable:

**`feature.api.ts`** — `providedIn: 'root'`, owns the `DataCache`, exposes HTTP methods:
```typescript
@Injectable({ providedIn: 'root' })
export class OrderApi {
  readonly #http = inject(HttpClient);
  readonly cache = new DataCache({ name: 'orders' });

  getOrders(filters: OrderFilters) {
    return this.#http.get<Order[]>('/api/orders', { params: filters });
  }

  getOrder(id: string) {
    return this.#http.get<Order>(`/api/orders/${id}`);
  }

  createOrder(order: NewOrder) {
    return this.#http.post<Order>('/api/orders', order);
  }
}
```

**`feature.store.ts`** — route-scoped `@Injectable()`, wires `cachedResource` + `cachedMutation`:
```typescript
@Injectable()
export class OrderListStore {
  readonly #api = inject(OrderApi);

  readonly orders = cachedResource({
    cache: this.#api.cache,
    cacheKey: ['orders', 'list'],
    loader: () => this.#api.getOrders({}),
  });

  readonly createOrder = cachedMutation({
    cache: this.#api.cache,
    mutationFn: (order: NewOrder) => this.#api.createOrder(order),
    invalidateKeys: () => [['orders']],
  });
}
```

**`feature.component.ts`** — injects the store, reads signals in the template:
```typescript
@Component({
  providers: [OrderListStore],
  template: `
    @if (store.orders.isInitialLoading()) {
      <spinner />
    } @else {
      @for (order of store.orders.value(); track order.id) {
        <order-card [order]="order" />
      }
    }
  `,
})
export class OrderListComponent {
  readonly store = inject(OrderListStore);
}
```

**Hard rules:**
- Component NEVER injects the API service directly
- HTTP logic lives exclusively in the API service
- Store NEVER instantiates `DataCache` — it reads `this.#api.cache`
- `DataCache` MUST live in a `providedIn: 'root'` service (survives navigation)

## API Quick Reference

### `provideZiflux(config?, ...features)`
Called once in `app.config.ts`. Sets global defaults.
```typescript
provideZiflux({ staleTime: 60_000, expireTime: 300_000 }, withDevtools())
```

### `DataCache`
In-memory SWR cache. Must be created inside an injection context.
```typescript
readonly cache = new DataCache({ name: 'orders', staleTime: 30_000, expireTime: 300_000 });

cache.get<T>(key: string[], opts?): { data: T; fresh: boolean } | null
cache.set<T>(key: string[], data: T): void
cache.invalidate(prefix: string[]): void      // marks stale, never deletes
cache.deduplicate<T>(key: string[], fn): Promise<T>  // one in-flight per key
cache.prefetch<T>(key: string[], fn): Promise<void>
cache.wrap<T>(key: string[], obs$): Observable<T>     // tap → set
cache.clear(): void
cache.cleanup(): number                        // evict expired entries
cache.inspect(): CacheInspection<unknown>
cache.version: Signal<number>                  // bumps on invalidate/clear
```

### `cachedResource<T, P>(options)`
Angular `resource()` with SWR. Must be called inside an injection context.
```typescript
cachedResource({
  cache: this.#api.cache,
  cacheKey: params => ['orders', 'details', params.id],
  params: () => ({ id: this.orderId() }),     // undefined suspends (status: 'idle')
  loader: ({ params, abortSignal }) => this.#api.getOrder(params.id),
  staleTime: 10_000,                          // optional per-resource override
  retry: { maxRetries: 3, baseDelay: 1000 },  // optional
  refetchInterval: 30_000,                     // optional polling
})
```

Returns `CachedResourceRef<T>`:
- `value: Signal<T | undefined>` — SWR-aware: shows stale data during revalidation
- `status: Signal<ResourceStatus>` — `'idle'|'loading'|'reloading'|'resolved'|'error'|'local'`
- `isLoading: Signal<boolean>` — true during any fetch
- `isStale: Signal<boolean>` — true when showing stale data during background refetch
- `isInitialLoading: Signal<boolean>` — true only on cold cache (use this for spinners)
- `error: Signal<unknown>`
- `hasValue(): boolean`
- `reload(): boolean`
- `set(value: T): void` — optimistic update, writes through to DataCache (status becomes `'local'`)
- `update(updater: (T | undefined) => T): void` — optimistic update, writes through to DataCache
- `destroy(): void`

### `cachedMutation<A, R, C>(options)`
Mutation wrapper. No injection context needed.
```typescript
cachedMutation({
  cache: this.#api.cache,
  mutationFn: (order: NewOrder) => this.#api.createOrder(order),
  invalidateKeys: (args, result) => [['orders']],
  onMutate: (args) => { /* optimistic update; return context */ },
  onSuccess: (result, args) => { /* after invalidation */ },
  onError: (error, args, context) => { /* rollback with context */ },
})
```

Returns `CachedMutationRef<A, R>`:
- `mutate(...args): Promise<R | undefined>` — **never rejects**, errors go to `error` signal
- `status: Signal<CachedMutationStatus>` — `'idle'|'pending'|'success'|'error'`
- `isPending: Signal<boolean>`
- `error: Signal<unknown>`
- `data: Signal<R | undefined>`
- `reset(): void`

Void args: when `A = void`, call `mutation.mutate()` with no argument.

### `anyLoading(...signals: Signal<boolean>[]): Signal<boolean>`
Combines loading signals. `computed(() => signals.some(s => s()))`. No injection context.

### `withDevtools(config?)`
Feature function for `provideZiflux()`. Enables `CacheRegistry` and console logging.
```typescript
provideZiflux(config, withDevtools({ logOperations: true }))
```

### `ZifluxDevtoolsComponent`
Standalone component. Selector: `<ziflux-devtools />`. Auto-hides in production via `isDevMode()`.

## SWR Lifecycle

```
1. Cold cache → loader fires → status: 'loading' → isInitialLoading: true
2. Data arrives → cache.set() → status: 'resolved' → value has data
3. Navigate away → DataCache persists (root-scoped)
4. Navigate back → cache.get() returns fresh → NO loader call → instant render
5. Time passes → entry becomes stale
6. Next read → stale data shown immediately → background refetch starts
   → status: 'reloading' → isStale: true → isInitialLoading: false
7. Fresh data arrives → value updates → isStale: false
```

The key UX insight: `isInitialLoading` controls spinners (cold cache only). `isStale` is informational — stale data is still shown, the user sees content immediately.

## Cache Key Design

Keys are `string[]` serialized via `JSON.stringify()`. Prefix matching on `invalidate()` uses `JSON.stringify(prefix).slice(0, -1)`.

```typescript
// Good: hierarchical keys
['orders', 'list']
['orders', 'details', orderId]
['orders', 'list', JSON.stringify(filters)]

// invalidate(['orders']) → invalidates ALL order-related entries
// invalidate(['orders', 'list']) → invalidates only the list
```

**Gotcha:** `invalidate(['order'])` does NOT match `['orders']` — the JSON prefix `["order"` does not match `["orders"`. This is by design to prevent accidental cross-invalidation.

**Empty prefix `invalidate([])` is a no-op.** Use `cache.clear()` for full wipe.

## Top Anti-Patterns

1. **DataCache outside injection context** → NG0203. Must be in class field, constructor, or `runInInjectionContext`.
2. **DataCache in route-scoped service** → cache dies on navigation, killing SWR. Always `providedIn: 'root'`.
3. **`staleTime > expireTime`** → constructor throws.
4. **Expecting `invalidate()` to delete** → it marks stale. `get()` still returns `{ data, fresh: false }`.
5. **`invalidate([])` for full wipe** → no-op. Use `clear()`.
6. **`ref.value.set()`** → `value` is a read-only `Signal`, not `WritableSignal`. Use `ref.set()` or `ref.update()`.
7. **`await mutate()` then checking success** → `mutate()` never rejects. Check `mutation.error()` signal or capture return value (`undefined` = error).
8. **Component injecting API service directly** → breaks the domain pattern. Component → Store → API.
9. **Using Subjects/Observables for state** → forbidden. Signals only.
10. **Forgetting `params: () => undefined` suspends** → resource stays `'idle'`, loader never fires.

## Optimistic Updates

The `onMutate` → `onError` pattern with context:
```typescript
readonly deleteItem = cachedMutation<string, void, Item[]>({
  mutationFn: (id) => this.#api.deleteItem(id),
  cache: this.#api.cache,
  invalidateKeys: () => [['items']],
  onMutate: (id) => {
    const previous = this.items.value()!;
    this.items.update(items => items!.filter(i => i.id !== id));
    return previous;  // context for rollback
  },
  onError: (_err, _id, previous) => {
    if (previous) this.items.set(previous);  // rollback
  },
});
```

## Concurrent Mutation Semantics

Latest-wins by **call order**, not resolution order. If two `mutate()` calls overlap:
- Both run their `mutationFn`
- Both invalidate the cache on success (server state changed)
- Only the **last-invoked** call updates signals and fires `onSuccess`
- Earlier calls' results are silently dropped from signals

## Configuration Priority

Constructor arg > `provideZiflux()` global config > hardcoded defaults (staleTime: 30s, expireTime: 5min).

## References

For deeper information, read these reference files:

- **`references/api-reference.md`** — Read when you need complete type signatures, all configuration options, DataCacheOptions validation rules, RetryConfig details, CacheInspection shape, or edge-case behaviors.
- **`references/patterns.md`** — Read when implementing a new feature with ziflux, setting up optimistic updates, designing cache key hierarchies, configuring polling/retry, or writing the provideZiflux setup.
- **`references/review-and-debug.md`** — Read when reviewing code that uses ziflux, debugging cache issues (stale data, missing invalidation, NG0203 errors), writing tests for ziflux code, or cleaning up ziflux usage.
