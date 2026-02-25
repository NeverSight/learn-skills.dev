---
name: latency-principles
description: "Comprehensive guide for diagnosing, optimizing, and hiding latency in software systems. Use when: (1) Debugging slow performance, (2) Designing low-latency architectures (High Frequency Trading, Real-time), (3) Optimizing Data/Compute layers, or (4) Learning about latency theory (Little's Law, Coordinated Omission)."
---

# Latency Principles

This skill provides a systematic framework for minimizing delay in software systems, covering the entire stack from Physics and Hardware to Application Architecture and User Experience.

## 1. Core Principles
**Start here for theory and diagnosis.**
- **[references/principles.md](references/principles.md)**: Definitions of Little's Law, Amdahl's Law, Tail Latency, and Coordinated Omission.
- **[references/diagnostic_checklist.md](references/diagnostic_checklist.md)**: A checklist for identifying bottlenecks across Hardware, OS, and Runtime.

## 2. Optimization Strategies
Choose the strategy based on the bottleneck layer:

### Data Layer (Storage & Access)
**Problem:** Database queries are slow, network round-trips are killing performance, or throughput is low.
**Solution:** **[references/data_patterns.md](references/data_patterns.md)**
- **Colocation**: Moving code to data (Edge/Kernel-bypass).
- **Partitioning**: Sharding data to increase parallelism.
- **Caching**: Storing hot data in memory (Strategies & Eviction policies).
- **Replication**: Consistency models (Strong vs Eventual) and topologies.

### Compute Layer (Processing Logic)
**Problem:** High CPU usage, lock contention, Garbage Collection pauses, or slow algorithms.
**Solution:** **[references/compute_optimization.md](references/compute_optimization.md)**
- **Eliminating Work**: Better algorithms, Zero-copy serialization, Object pooling.
- **Wait-Free Sync**: Replacing Mutexes with Atomics, Ring Buffers, and Lock-free structures.
- **Concurrency**: Thread-per-core, Coroutines, and parallel execution models.

### UX Layer (Hiding Latency)
**Problem:** The backend cannot be made faster, but the user experience feels sluggish.
**Solution:** **[references/hiding_latency.md](references/hiding_latency.md)**
- **Asynchronous Processing**: Event loops, Non-blocking I/O, Request Hedging.
- **Predictive Techniques**: Prefetching data, Optimistic UI updates, Speculative execution.

## Decision Guide: Which technique to use?

| Symptom | Probable Cause | Recommended Strategy |
|---------|----------------|----------------------|
| **High Avg Latency** | Sequential processing / Slow I/O | **Concurrency** (Async I/O) or **Partitioning** |
| **High Tail Latency (p99)** | Lock contention / GC / Neighbor noise | **Wait-free Sync** (Atomics) or **Request Hedging** |
| **Network Slowness** | Distance / Protocol overhead | **Colocation** (Edge) or **Binary Serialization** (Protobuf) |
| **Database Load** | Hot keys / Complex queries | **Caching** (Read-through) or **Materialized Views** |
| **Slow Writes** | ACID guarantees / Indexing | **Write-Behind Caching** or **Sharding** |
| **"It feels slow"** | UI blocking on network | **Optimistic Updates** or **Prefetching** |
