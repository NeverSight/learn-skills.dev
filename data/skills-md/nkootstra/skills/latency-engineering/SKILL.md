---
name: latency-engineering
description: "Diagnose and reduce latency in software systems. Use when dealing with slow APIs, tail latency, p99 spikes, caching, replication, partitioning, concurrency, async I/O, or any question about making systems faster."
---

# Latency Engineering

Comprehensive guidance for diagnosing and reducing latency across the full software/hardware stack.

## Mental Model

Latency = time delay between a cause and its observed effect. It is a **distribution**, not a single number. Always think in percentiles (p50, p95, p99, p99.9). Tail latency dominates real-world user experience far more than averages suggest.

**Two fundamental laws:**
- **Little's Law**: `Concurrency = Throughput × Latency`. Use it to size systems and understand queue dynamics.
- **Amdahl's Law**: `Speedup = 1 / ((1-P) + P/N)`. Use it to set realistic expectations on parallelization gains.

## Decision Framework: Where to Optimize First

```
1. Measure → identify where time is actually spent
2. Data locality?     → see references/data-latency.md
3. Computation cost?  → see references/compute-latency.md
4. Can't reduce it?   → see references/hiding-latency.md
```

## Key Latency Constants (back-of-envelope)

| Operation              | Latency      |
|------------------------|--------------|
| CPU cycle (3 GHz)      | ~0.3 ns      |
| L1 cache access        | ~1 ns        |
| LLC / 40 Gbps NIC      | ~10–40 ns    |
| DRAM access            | ~100 ns      |
| NVMe disk              | ~10 µs       |
| SSD disk               | ~100 µs      |
| Same datacenter (LAN)  | < 1 ms       |
| NYC → London (WAN)     | ~60–150 ms   |

## Common Sources of Latency (checklist)

- [ ] **Geographic distance** — physical speed-of-light limit; only solution is colocation
- [ ] **Last-mile network** — Wi-Fi adds 5–50 ms on top of backbone latency
- [ ] **Algorithmic complexity** — O(n²) workloads hidden inside hot paths
- [ ] **Serialization/deserialization** — often surprisingly expensive
- [ ] **Memory management / GC** — stop-the-world pauses introduce tail latency spikes
- [ ] **OS overhead** — virtual memory, interrupts, context switching
- [ ] **Lock contention** — mutex waits serialize concurrent requests
- [ ] **NUMA effects** — remote memory access costs 2–3× local on multi-socket systems
- [ ] **TCP Nagle algorithm / delayed ACKs** — batches small packets, adds ~40ms delay on interactive traffic; disable with `TCP_NODELAY`
- [ ] **Tail-at-scale** — with fanout N, even rare slow calls affect most users

## Measuring Latency Correctly

- Always capture full **distributions**, not just averages. Use histograms or eCDF plots.
- Report **p95, p99, p99.9** for SLAs and debugging.
- Understand **coordinated omission** — naive benchmarks under-measure tail latency.
- Validate measurements: compare minimum to theoretical lower bound from latency constants table.

## Reference Files

Load the relevant reference file based on the category of the problem:

| Problem category                              | Reference file                           |
|-----------------------------------------------|------------------------------------------|
| Data placement, caching, replication, sharding | `references/data-latency.md`            |
| CPU, algorithms, concurrency, memory           | `references/compute-latency.md`         |
| Async I/O, prefetching, hiding unavoidable lag | `references/hiding-latency.md`          |
| Networking, kernel bypass, intranode           | `references/network-latency.md`         |

When the user's question spans multiple areas, load all relevant files.
