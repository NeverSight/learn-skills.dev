---
name: performance-optimizer
description: Performance optimization expert. Use when profiling, benchmarking, or optimizing application performance across languages.
disable-model-invocation: true
argument-hint: [file-or-area]
allowed-tools: Read, Grep, Glob, Bash
---

# Performance Optimizer

Analyze and optimize $ARGUMENTS for performance:

## Analysis Process

1. **Identify the bottleneck** — don't optimize without measuring
2. **Profile first** — use language-appropriate tools
3. **Propose changes** with expected impact
4. **Verify improvement** with benchmarks

## Common Optimization Patterns

### Algorithmic
- Replace O(n²) with O(n log n) or O(n) where possible
- Use appropriate data structures (HashMap for lookups, not array scan)
- Avoid unnecessary sorting — use partial sorts or heaps
- Cache computed results (memoization)

### I/O & Network
- Batch database queries (avoid N+1)
- Use connection pooling
- Implement caching layers (in-memory, Redis)
- Use streaming for large data instead of loading all into memory
- Compress responses (gzip, brotli)
- Parallelize independent I/O operations

### Memory
- Avoid unnecessary copies — use references/borrows/views
- Use generators/iterators for large sequences
- Release large objects early (set to null, use weak refs)
- Use appropriate collection types with size hints
- Pool expensive-to-create objects

### Frontend
- Lazy load images and non-critical resources
- Code split routes and heavy components
- Debounce/throttle frequent events
- Use virtual scrolling for long lists
- Minimize re-renders (memoization, stable references)

### Database
- Use `EXPLAIN ANALYZE` to understand query plans
- Add missing indexes for common query patterns
- Denormalize for read-heavy access patterns
- Use materialized views for expensive aggregations
- Optimize pagination (keyset > offset)

## Profiling Tools by Language
- **JavaScript/Node.js**: Chrome DevTools, `node --prof`, `clinic.js`
- **Python**: `cProfile`, `py-spy`, `memory_profiler`
- **Go**: `pprof`, `trace`
- **Rust**: `flamegraph`, `criterion`
- **Java**: `JProfiler`, `async-profiler`, `JMH`
- **C#/.NET**: `dotnet-trace`, `BenchmarkDotNet`
