---
name: studio-sdk
description: Use when user asks to "connect to Studio", "set up Studio SDK", "add Studio analytics", "send events to Studio", "configure studio bridge", "studio storage sync", or needs help with @flowsterix/studio package, createStudioBridge, event serialization, batched transport, or Studio ingest integration.
version: 0.1.0
metadata:
  tags: flowsterix, studio, sdk, analytics, bridge, ingest, telemetry
---

# Flowsterix Studio SDK

`@flowsterix/studio` bridges the open-source Flowsterix library to the proprietary Studio backend. It intercepts analytics events and storage operations, serializes them to JSON-safe payloads, and ships them in batches to a Studio ingest endpoint.

## Architecture

```
TourProvider
  analytics={bridge.analytics}     --> serializer --> transport --> POST /v1/ingest
  storageAdapter={bridge.storage({ inner: localStorage })}
                                       |
                                       +--> inner adapter (read/write)
                                       +--> transport (fire-and-forget sync)
```

- **No React dependency** - pure JS, works with any framework
- **Dep**: `@flowsterix/core` only (uses `FlowAnalyticsHandlers`, `StorageAdapter` types)
- **Package**: `packages/studio/` in the monorepo

## Quick Start

```ts
import { createStudioBridge } from '@flowsterix/studio'
import { createLocalStorageAdapter } from '@flowsterix/core'

const bridge = createStudioBridge({
  projectId: 'proj_abc',
  apiKey: 'sk_live_xxx',
  // endpoint: 'https://ingest.flowsterix.studio', // default
  // batchSize: 20,        // default
  // flushIntervalMs: 5000, // default
  // debug: false,          // include stack traces in error events
  user: { id: 'user-123', traits: { plan: 'pro' } },
})

// In React:
<TourProvider
  flows={flows}
  analytics={bridge.analytics}
  storageAdapter={bridge.storage({ inner: createLocalStorageAdapter() })}
>
```

## Public API

### `createStudioBridge(params: StudioBridgeOptions): StudioBridge`

```ts
interface StudioBridgeOptions {
  projectId: string
  apiKey: string
  endpoint?: string          // default: https://ingest.flowsterix.studio
  user?: UserContext
  debug?: boolean            // include stack traces in error events
  batchSize?: number         // default: 20
  flushIntervalMs?: number   // default: 5000
}

interface UserContext {
  id: string
  traits?: Record<string, unknown>
}

interface StudioBridge {
  analytics: FlowAnalyticsHandlers<unknown>   // pass to TourProvider
  storage: (params: { inner: StorageAdapter }) => StorageAdapter  // wraps an inner adapter
  identify: (params: { user: UserContext }) => void  // update user mid-session
  flush: () => Promise<void>    // force-flush buffered events
  shutdown: () => void          // flush + cleanup listeners
}
```

### Lifecycle

- `identify()` — update user context after login; enqueues an `identify` event
- `flush()` — force-send buffered events (useful before navigation)
- `shutdown()` — flush remaining via `sendBeacon`, remove `visibilitychange` listener, clear interval

## Module Overview

| File | Responsibility |
|---|---|
| `src/bridge.ts` | `createStudioBridge` — factory, wires serializer + transport + storage |
| `src/serializer.ts` | Strips functions, ReactNodes, RegExp from payloads; produces `StudioEvent` |
| `src/transport.ts` | Batched HTTP POST to `/v1/ingest`, retry on failure, 500-event buffer cap, `sendBeacon` fallback |
| `src/storage.ts` | `StorageAdapter` wrapper — delegates to inner, fire-and-forget enqueues `storage.set`/`storage.remove` |
| `src/types.ts` | All type definitions |

## Serialization Rules

The serializer strips non-JSON-safe values from `FlowDefinition` and `Step`:

**Flow**: keeps `id`, `version`, `metadata`, `autoStart`, `resumeStrategy`, `stepCount`. Drops `steps` array, `hud`, `migrate`, `dialogs`.

**Step**: keeps `id`, `target` (selector string or `'screen'`), `placement`, `mask`, `controls`, `dialogId`, `route` (RegExp `.source`), `advance` (drops `check` fn). Drops `content`, `onEnter`, `onExit`, `onResume`, `waitFor`, `targetBehavior`.

**Error events**: keeps `code`, `meta`, `message`, `name`. Stack only if `debug: true`.

**Version mismatch**: serializes `oldVersion`/`newVersion` as `"major.minor"` strings.

## Transport Details

- Buffer flushes when `batchSize` reached OR every `flushIntervalMs`
- On fetch error: events re-added to front of buffer (retry next flush)
- Buffer capped at 500 events to prevent memory leaks
- On `visibilitychange` → `hidden`: calls `shutdown()` which uses `sendBeacon`
- Shutdown fallback: `fetch` with `keepalive: true`
- Auth header: `Authorization: Bearer ${apiKey}`

## Flow Registration

Flows are not registered upfront. The first analytics event for each flow implicitly registers it — every `StudioEvent` contains a serialized `flow` field. The backend deduplicates by `(projectId, flowId, version)`.

## Key Patterns

### Wrapping storage with Studio sync

```ts
// The storage wrapper delegates all reads/writes to the inner adapter
// and fire-and-forget enqueues sync events to the transport
const storageAdapter = bridge.storage({
  inner: createLocalStorageAdapter()
})
```

### Identifying users after auth

```ts
// Call after login — updates user on all subsequent events
bridge.identify({ user: { id: userId, traits: { plan, role } } })
```

### Cleanup on unmount

```ts
useEffect(() => {
  return () => bridge.shutdown()
}, [])
```
