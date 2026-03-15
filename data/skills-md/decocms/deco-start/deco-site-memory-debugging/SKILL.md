---
name: deco-site-memory-debugging
description: Debug memory issues on Deno/Fresh sites running on Kubernetes/Knative. Connects to pods via Chrome DevTools Protocol (CDP) to analyze heap, ArrayBuffers, Response leaks, and native memory. Guides GC analysis and V8 heap tuning.
---

# Deco Site Memory Debugging

Debug memory issues on Deno sites running in Kubernetes pods using Chrome DevTools Protocol (CDP) over WebSocket.

## When to Use This Skill

- Pod memory usage is high or growing over time
- Kubernetes OOMKill events on site pods
- Need to identify what's consuming memory inside a Deno process
- Investigating Response/Request body leaks
- Need to determine if memory is a real leak vs lazy GC

## Quick Start

```
1. IDENTIFY POD        → kubectl get pods -n sites-<sitename>
2. PORT-FORWARD        → kubectl port-forward <pod> 9229:9229
3. GET WS URL          → curl http://127.0.0.1:9229/json/list
4. CONNECT CDP         → WebSocket to the debuggerUrl
5. FORCE GC            → HeapProfiler.collectGarbage
6. ANALYZE MEMORY      → Deno.memoryUsage() + queryObjects + heap snapshot
7. DIAGNOSE            → Is it a leak or lazy GC?
8. RECOMMEND           → Tune --v8-flags=--max-old-space-size or fix leak
```

## Files in This Skill

| File | Purpose |
|------|---------|
| `SKILL.md` | This overview and quick reference |
| `cdp-connection.md` | How to connect to pods and common pitfalls |
| `memory-analysis.md` | Step-by-step memory analysis procedures |

## Key Concept: GC is Lazy

**V8's garbage collector is lazy by design.** It won't collect garbage until memory pressure forces it to. A pod showing 1.8 GB RSS might drop to 700 MB after a forced GC — meaning there was no leak, just uncollected garbage.

**Always force GC before concluding there's a leak:**

```
HeapProfiler.collectGarbage  (via CDP)
```

Then check `Deno.memoryUsage()` again. The difference between before-GC and after-GC tells you how much was reclaimable garbage vs actual retained memory.

### Recommendation: Reduce Max Heap Size

If post-GC memory is reasonable but pre-GC memory is causing OOMKills or high pod memory:

**Decrease the V8 max old space size** so GC runs more frequently:

```
--v8-flags=--max-old-space-size=512
```

This forces V8 to GC more aggressively instead of letting garbage accumulate. For most Deco sites this doesn't affect performance because the actual live heap is much smaller than the default limit. The GC runs are fast (milliseconds) and the trade-off is worth it to keep RSS predictable.

Example Deno flags:
```bash
deno run --v8-flags=--max-old-space-size=512 -A main.ts
```

## Memory Breakdown Model

RSS is composed of multiple layers. You must understand what each layer represents:

```
RSS = V8 Heap + V8 External + Native (untracked)

V8 Heap     → JavaScript objects, closures, strings, compiled code
V8 External → ArrayBuffers (including a ~304MB static V8/ICU data buffer)
Native      → Deno Rust runtime, module graph, JIT code cache, mmap'd files, thread stacks
```

Use `Deno.memoryUsage()` to get the breakdown:
- `rss`: Total resident set size
- `heapUsed`: V8 JavaScript heap
- `heapTotal`: V8 heap capacity
- `external`: V8 external allocations (ArrayBuffers)
- `rss - heapUsed - external` = native/untracked memory

**The native gap is normal.** For a large Deno/Fresh app with thousands of modules, 500MB-1GB of native memory is expected (JIT compiled code, Rust allocator, module cache). This is NOT a leak.

## Common Memory Consumers

| What | Typical Size | Is It a Problem? |
|------|-------------|-----------------|
| Static V8/ICU ArrayBuffer | ~304 MB | No — built into V8, constant |
| Deno module cache on disk | ~100-200 MB | No — normal for large apps |
| V8 JIT compiled code | ~200-500 MB | No — proportional to loaded modules |
| Response bodies not consumed | Variable, grows | **YES — leak if bodyUsed=false** |
| OpenTelemetry export buffers | ~10-50 MB | Minor — accumulates slowly |
| Rendered HTML strings (SSR cache) | ~20-100 MB | Monitor — should be bounded |
| LRU cache metadata | Small (booleans) | No — only stores `true` with size tracking |

## Diagnostic Decision Tree

```
Pod memory high?
├── Force GC → Memory drops significantly?
│   ├── YES → Not a leak. Recommend reducing --max-old-space-size
│   └── NO → Real retained memory. Continue investigation:
│       ├── Check Response objects (queryObjects Response.prototype)
│       │   └── bodyUsed=false count high? → Response body leak
│       ├── Check ArrayBuffers
│       │   └── Many large OTEL/JSON buffers? → Export/cache leak
│       ├── Check heap snapshot top consumers
│       │   └── Large HTML strings? → SSR cache unbounded
│       └── Large native gap (RSS - heap - external)?
│           └── Normal for large Deno apps (JIT + Rust runtime)
```

## Related Skills

- `deco-incident-debugging` — For general incident response and triage
- `deco-performance-audit` — For deep performance analysis
