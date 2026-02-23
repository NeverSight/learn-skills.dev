---
name: parallel-execution
description: Execute multiple independent tasks simultaneously using parallel agent coordination to maximize throughput. Use when tasks have no dependencies, results can be aggregated, and agents are available for concurrent work.
---

# Parallel Execution

Execute multiple independent tasks simultaneously to maximize throughput and minimize total execution time.

## When to Use

- Multiple independent tasks (no dependencies)
- Tasks benefit from concurrent execution
- Maximizing throughput is priority
- Available agents for parallel work
- Results can be aggregated after completion

## Core Concepts

### Independence

**Tasks are independent when**:
- ✓ No data dependencies
- ✓ No resource conflicts
- ✓ No ordering requirements
- ✓ Failures are isolated

### Concurrency

**Critical**: Use **single message** with **multiple Task tool calls**:

```markdown
[Task tool] → Agent A
[Task tool] → Agent B
[Task tool] → Agent C

All start simultaneously.
```

## Execution Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| Homogeneous | Same agent, different inputs | Test 3 modules |
| Heterogeneous | Different agents, related task | Review + Test + Profile |
| Parallel + Convergence | Parallel → Synthesize | Profile + Analyze → Root cause |

## Synchronization Strategies

- **Wait for All**: Proceed when ALL complete
- **Wait for Any**: Early termination on first success
- **Threshold**: Proceed when N of M complete

## Performance

```
Sequential: T1 + T2 + T3
Parallel: max(T1, T2, T3)
Speedup = Sequential / Parallel
```

**Example**: 3 tasks (10+15+8 min) → Parallel (15 min) = 2.2x faster

## Best Practices

✓ Verify independence before parallelizing
✓ Use single message with multiple Task calls
✓ Balance workload across agents
✓ Handle failures gracefully

✗ Don't parallelize dependent tasks
✗ Don't send sequential messages
