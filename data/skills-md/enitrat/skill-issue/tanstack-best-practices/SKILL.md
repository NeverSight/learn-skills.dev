---
name: tanstack-best-practices
description: "Best practices for building hook libraries with TanStack Query. Use when: (1) Writing useQuery/useMutation hooks that wrap async data-fetching functions, (2) Designing query key schemas and cache identity systems, (3) Building framework-agnostic query options factories, (4) Implementing cache invalidation patterns (invalidate vs remove vs setQueryData), (5) Wrapping TanStack Query in a multi-layered library (core actions to query options to framework hooks), (6) Handling non-serializable values (bigint, class instances) in query keys, (7) Bridging external stores (zustand, signals) with TanStack Query reactivity. Derived from wagmi's production architecture (React/Vue/Solid Ethereum hooks)."
---

# TanStack Query Best Practices for Hook Libraries

## TanStack Query Core Concepts

### Cache Model

TanStack Query is a **key-value cache** for async data. Two components using the same query key share one cache entry and one network request (deduplication). If Component B mounts while Component A's fetch is in-flight, B subscribes to A's request — no duplicate.

### staleTime vs gcTime

These control the cache lifecycle:

- **`staleTime`** (default: 0) — how long data is "fresh" after fetching. While fresh, TQ serves from cache without refetching. Once stale, TQ refetches in the background on mount/focus (stale-while-revalidate: user sees old data instantly, then re-renders with fresh data).
- **`gcTime`** (default: 5 min) — how long unused cache entries survive after all observing components unmount. After gcTime, the entry is garbage-collected.

Timeline: `fetch -> fresh (staleTime) -> stale -> component unmounts -> gcTime expires -> entry deleted`

If a component remounts within gcTime with stale data: instant cached data + background refetch.
If a component remounts after gcTime: full loading state + fresh fetch.

Tune per-query: `gcTime: 0` for block numbers (change every ~12s, no point caching). `staleTime: Infinity` for immutable data (manual refetch only).

### Queries vs Mutations

- **Queries** (`useQuery`): declarative reads. Run on mount, cached by key, auto-refetch when stale. For GET/read operations.
- **Mutations** (`useMutation`): imperative writes. Run only when `mutate()`/`mutateAsync()` is called. Not cached. For POST/write operations.

`mutate()` is fire-and-forget (errors go to the `error` state). `mutateAsync()` returns a Promise you can await/catch.

## Three-Layer Architecture

### Why Three Layers

The key insight: **Layer 2 (query options factory) is framework-agnostic**. It lives in the core package and produces TanStack Query config objects that React, Vue, and Solid all consume identically. Adding a new framework adapter is ~4 lines of hook code. Each layer is independently testable and usable (Layer 1 works from Node.js/CLI, Layer 2 works with any TanStack Query adapter).

```
Layer 1: Core Action     — pure async function, no caching awareness
Layer 2: Query Options   — framework-agnostic TanStack Query config factory
Layer 3: Framework Hook  — thin wrapper (React/Vue/Solid), ~4 lines of real logic
```

### Layer 1: Core Action

```ts
// actions/getBalance.ts
export async function getBalance(config: Config, params: GetBalanceParams): Promise<Balance> {
  const client = config.getClient({ chainId: params.chainId })
  return client.fetchBalance(params.address)
}
```

Pure `(config, params) => Promise<Result>`. No TanStack Query imports. No framework imports.

### Layer 2: Query Options Factory

```ts
// query/getBalance.ts
export function getBalanceQueryOptions(config, options) {
  return {
    ...options.query,                    // (A) user overrides spread FIRST
    enabled: Boolean(                    // (B) then factory sets these — overrides user's
      options.address && (options.query?.enabled ?? true)
    ),
    queryKey: getBalanceQueryKey(options),  // (B) can't be overridden
    queryFn: async (context) => {
      const [, { scopeKey: _, ...params }] = context.queryKey  // extract from KEY
      return getBalance(config, params)
    },
  }
}
```

**Spread order matters:** `...options.query` is spread first (A), then `enabled`/`queryKey`/`queryFn` are set after (B). JS object spread means later properties overwrite earlier ones, so the factory's critical properties always win even if the user passes `query: { queryFn: ... }`.

**Params from queryKey, not closure:** The `queryFn` extracts parameters from `context.queryKey`, not from the surrounding scope. This guarantees cache consistency — the function fetches for exactly the parameters that determined which cache entry to use. Without this, a stale closure could fetch address `0xdef` while the cache entry is keyed by `0xabc`.

**Auto-gating via `enabled`:** Required params are AND-ed together. If `address` is undefined (e.g., wallet not connected), the query sits idle — no network request, no error. The moment `address` becomes defined, TanStack Query fires the fetch. Users never need to write conditional guards like `useBalance(address ? { address } : { enabled: false })`.

For multiple required params: `Boolean(address && abi && functionName && (query?.enabled ?? true))`.

### Layer 3: Framework Hook

```ts
// hooks/useBalance.ts
export function useBalance(parameters = {}) {
  const config = useConfig(parameters)
  const chainId = useChainId({ config })
  const options = getBalanceQueryOptions(config, {
    ...parameters,
    chainId: parameters.chainId ?? chainId,  // default to current chain from context
  })
  return useQuery({ ...options, queryKeyHashFn: hashFn })
}
```

Four steps: get config from context, get reactive state (chainId), build query options, call useQuery. Pass custom `queryKeyHashFn` if keys contain non-serializable values (bigint).

## Query Key Design

### Shape: `[label, filteredParams]`

Always a 2-element tuple. The label identifies the query type, the params object determines cache identity:
```ts
['balance', { address: '0xabc', chainId: 1 }]
['readContract', { address: '0xabc', functionName: 'balanceOf', args: ['0xdef'] }]
```

### filterQueryOptions — Cache Identity Filter

**Principle:** Only params that change *what data* is fetched belong in the key. Params that change *how the cache behaves* do not.

```ts
export function filterQueryOptions(options) {
  const {
    // TanStack Query behavioral options — NOT data identity
    gcTime, staleTime, enabled, select, refetchInterval, queryFn, queryKey,
    // Library internals — NOT data identity
    config, abi, connector, query, watch,
    ...rest  // only this survives into the key
  } = options
  if (connector) return { connectorUid: connector.uid, ...rest }
  return rest
}
```

Without this, two components with `useBalance({ address, query: { refetchInterval: 10_000 } })` and `useBalance({ address })` would have **different cache entries** despite wanting the same data.

**Why strip ABI:** ABIs can be hundreds of entries — expensive to hash, and redundant for cache identity since `address + functionName + args` already uniquely identify the call. The ABI is still used inside `queryFn` via `options.abi` (from closure), not from the key.

**Why replace connector with connectorUid:** Connector objects (class instances) aren't serializable. Replace with a stable string ID so two queries for the same connector share a cache entry.

### hashFn — BigInt and Key Ordering

Standard `JSON.stringify` fails on bigints (`TypeError`) and produces different strings for `{ a: 1, b: 2 }` vs `{ b: 2, a: 1 }` (cache miss for identical data).

```ts
export function hashFn(queryKey: QueryKey): string {
  return JSON.stringify(queryKey, (_, value) => {
    if (isPlainObject(value))
      return Object.keys(value).sort()
        .reduce((result, key) => { result[key] = value[key]; return result }, {})
    if (typeof value === 'bigint') return value.toString()
    return value
  })
}
```

Pass as `queryKeyHashFn` to `useQuery`. Guarantees deterministic hashing regardless of property insertion order and bigint values.

### scopeKey — Manual Cache Isolation

Users add a `scopeKey` string for separate cache entries with identical params (e.g., same balance displayed in header vs dashboard with different refresh rates). Included in key for identity, stripped in queryFn (not a data-fetching param):

```ts
const [, { scopeKey: _, ...params }] = context.queryKey
```

## Controlled Override Surface

### QueryParameter Type

```ts
type QueryParameter<...> = {
  query?: Omit<QueryOptions, 'queryKey' | 'queryFn'> | undefined
}
```

Users pass `{ query: { staleTime: 60_000, gcTime: 0, select: (d) => d.value } }`. They can tune cache behavior but can't override `queryKey` or `queryFn` — those are owned by the factory to ensure cache consistency.

### MutationParameter Type

```ts
type MutationParameter<...> = {
  mutation?: Omit<MutationOptions, 'mutationFn' | 'mutationKey' | 'throwOnError'> | undefined
}
```

Users get `onSuccess`, `onError`, `onSettled`, `onMutate`, `retry`, etc. Can't override `mutationFn` (would bypass the core action layer) or `mutationKey`.

## Mutation Patterns

```ts
// Layer 2: mutation options factory
export function sendTransactionMutationOptions(config, options) {
  return {
    ...(options.mutation as any),
    mutationFn: (variables) => sendTransaction(config, variables),
    mutationKey: ['sendTransaction'],  // static label, not for caching
  }
}

// Layer 3: React hook
export function useSendTransaction(parameters = {}) {
  const config = useConfig(parameters)
  return useMutation(sendTransactionMutationOptions(config, parameters))
}
```

Key differences from queries:
- `mutationKey` is a static label (exists for devtools/global callbacks, not cache identity)
- `mutationFn` receives `variables` directly from the `mutate()` call (not from a key)
- No `enabled` gating — mutations are imperative, triggered by user action

## The Watch Pattern — Push-to-Pull Bridge

Some data streams continuously (block numbers via WebSocket). Combine a TanStack Query (for cache/dedup) with a subscription that pushes into the cache:

```ts
function useBlockNumber(parameters) {
  const options = getBlockNumberQueryOptions(config, { ... })
  const queryClient = useQueryClient()

  useWatchBlockNumber({
    enabled: Boolean(watch),
    onBlockNumber(blockNumber) {
      queryClient.setQueryData(options.queryKey, blockNumber)  // push into cache
    },
  })

  return useQuery(options)  // reads from cache
}
```

**Why:** The subscription already has the data — refetching via TanStack Query would be a redundant RPC call. `setQueryData` writes directly into the cache, TanStack Query handles re-rendering all subscribers. Users get real-time updates + cache deduplication + stale-while-revalidate, all in one hook.

## Cache Invalidation Patterns

See [references/invalidation-patterns.md](references/invalidation-patterns.md) for detailed patterns with code examples.

## Bridging External Stores with TanStack Query

### Why Two Systems

Use an external store (zustand, signals) for **app state** and TanStack Query for **server/async data**. They serve fundamentally different data patterns:

| Dimension | External Store (zustand) | TanStack Query |
|-----------|--------------------------|----------------|
| Data source | Events (wallet connect/disconnect) | Async requests (RPC calls) |
| Persistence | localStorage, survives refresh | In-memory with GC |
| Staleness | Never stale — it's the truth | Frequently stale, needs refetching |
| Deduplication | Not needed (single source) | Critical (many components, one fetch) |

Trying to use TanStack Query for connection state would be awkward — connections aren't "fetched" data. Trying to use zustand for blockchain data would mean reimplementing caching, dedup, GC, and stale-while-revalidate.

### Bridge via useSyncExternalStore

Use zustand in **vanilla mode** (`zustand/vanilla`) so the store is framework-agnostic (no React dependency in the core package). Bridge to React with `useSyncExternalStore`:

```ts
const chainId = useSyncExternalStore(
  (onChange) => watchChainId(config, { onChange }),  // subscribe to zustand slice
  () => getChainId(config),                          // read current value
)
```

When the store updates, React re-renders, hook params change, query keys change, TanStack Query refetches. Neither system knows about the other — React hooks are the glue.

### Property Access Tracking Optimization

For hooks returning objects (like `useConnection` returning `{ address, connector, chainId }`), wrap the result with getter-based proxies that track which properties each component accesses. On the next state change, only compare tracked properties — if a component only uses `address` and only `chainId` changed, skip the re-render.

### Complete Event Flow

External event (e.g., user switches chain in MetaMask):

```
Wallet extension emits chainChanged
  -> Connector catches it, emits 'change' event with new chainId
  -> Event handler updates zustand store (connection.chainId = 10)
  -> syncConnectedChain subscriber: global store.chainId = 10
  -> useSyncExternalStore fires, useChainId returns 10
  -> useBalance re-renders, query key becomes ['balance', { address, chainId: 10 }]
  -> TanStack Query: new key, cache miss, calls queryFn
  -> getBalance(config, { address, chainId: 10 }) via new viem client
  -> UI updates with new chain's balance
```

No invalidation code needed — the key change naturally triggers the fetch.

## Testing TanStack Query Hook Libraries

Test in four layers, each catching different bugs:

```
Layer 4:  Type Tests         (*.test-d.ts)   — compile-time type assertions (instant)
Layer 3:  Hook Integration   (*.test.tsx)    — full render + fetch + assert lifecycle (~5-10s)
Layer 2:  Query Options      (query/*.test.ts) — factory output: key shape, enabled logic (ms)
Layer 1:  Core Actions       (actions/*.test.ts) — raw async functions against real backend (~1s)
```

**Key philosophy:** Test against real backends (not mocked RPC responses) for integration confidence. Mock only the wallet/auth connection layer — the data-fetching layer hits real services.

See [references/testing-patterns.md](references/testing-patterns.md) for detailed patterns covering:
- Test infrastructure setup (backend instances, mock connectors, worker isolation)
- Query hook test pattern (render, wait, snapshot)
- Mutation hook test pattern (connect, render, mutate, assert)
- Watch/subscription test pattern (render, trigger event, verify reactive update)
- Query options factory tests (synchronous output verification)
- Type-level tests with `expectTypeOf` (generic inference, select transforms, callback types)

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Do This Instead |
|---|---|---|
| Close over params in `queryFn` | Cache entry keyed by X but fetching Y (stale closure) | Extract params from `context.queryKey` |
| Include `staleTime`/`select` in query key | Two components wanting same data get separate cache entries | Use `filterQueryOptions` to strip behavioral options |
| Serialize large objects (ABIs) into keys | Expensive to hash, redundant for identity | Strip from key, pass via closure to queryFn |
| `invalidateQueries` on disconnect | Triggers a refetch that fails (no data source) | `removeQueries` when data source is gone |
| Framework-specific query options | Kills reusability across React/Vue/Solid | Keep Layer 2 framework-agnostic |
| Manual `enabled` guards in components | Verbose, error-prone, duplicated across call sites | Auto-gate in the query options factory |
| `useQuery` for write operations | Fires on mount, caches results, auto-refetches | `useMutation` for imperative writes |
