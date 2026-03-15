---
name: condition-based-waiting
description: Fixes flaky tests by replacing arbitrary timeouts with condition polling. Use when tests fail intermittently, have setTimeout delays, or involve async operations that need proper wait conditions.
---

# Condition-Based Waiting

**Use with:** `writing-tests` skill for overall test guidance. This skill focuses on timing-based flakiness.

**Related:** If tests pass alone but fail concurrently, the problem may be shared state, not timing. See `fixing-flaky-tests` skill for diagnosis.

## Overview

Flaky tests often guess at timing with arbitrary delays. This creates race conditions where tests pass on fast machines but fail under load or in CI.

**Core principle:** Wait for the actual condition you care about, not a guess about how long it takes.

## When to use

```
Test has arbitrary delay (setTimeout/sleep)?
    │
    ├─ Testing actual timing (debounce, throttle)?
    │   └─ Yes → Keep timeout, document WHY
    │
    └─ No → Replace with condition-based waiting
```

**Use when:**
- Tests have arbitrary delays (`setTimeout`, `sleep`, `time.sleep()`)
- Tests are flaky with timing-related errors
- Waiting for async operations to complete

**Don't use when:**
- Testing actual timing behavior (debounce, throttle, intervals)
- Problem is shared state between tests (use `fixing-flaky-tests`)

## Core pattern

```typescript
// Bad: Guessing at timing
await new Promise((r) => setTimeout(r, 50));
const result = getResult();
expect(result).toBeDefined();

// Good: Waiting for condition (returns the result)
const result = await waitFor(() => getResult(), 'result to be available');
expect(result).toBeDefined();
```

## Implementation

**Prefer framework built-ins** when available:
- Testing Library: `findBy` queries, `waitFor`
- Playwright: auto-waiting, `expect(locator).toBeVisible()`
- pytest: `asyncio.wait_for`, tenacity

**Custom polling fallback** when built-ins aren't enough:

```typescript
async function waitFor<T>(
  condition: () => T | undefined | null | false,
  description: string,
  timeoutMs = 5000
): Promise<T> {
  const startTime = Date.now();

  while (true) {
    const result = condition();
    if (result) return result;

    if (Date.now() - startTime > timeoutMs) {
      throw new Error(`Timeout waiting for ${description} after ${timeoutMs}ms`);
    }

    await new Promise((r) => setTimeout(r, 50));  // Poll interval
  }
}
```

**Common use cases:**
- `waitFor(() => events.find(e => e.type === 'DONE'), 'done event')`
- `waitFor(() => machine.state === 'ready', 'ready state')`
- `waitFor(() => items.length >= 5, '5+ items')`

## Language-specific patterns

| Stack | Reference |
|-------|-----------|
| Python (pytest, asyncio, tenacity) | [references/python.md](references/python.md) |
| TypeScript (Jest, Testing Library, Playwright) | [references/typescript.md](references/typescript.md) |

## Common mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Polling too fast | `setTimeout(check, 1)` wastes CPU | Poll every 50ms |
| No timeout | Loop forever if condition never met | Always include timeout |
| Stale data | Caching state before loop | Call getter inside loop |
| No description | "Timeout" with no context | Include what you waited for |

## When arbitrary timeout IS correct

```typescript
// Tool ticks every 100ms - need 2 ticks to verify partial output
await waitForEvent(manager, "TOOL_STARTED");  // First: wait for condition
await new Promise((r) => setTimeout(r, 200)); // Then: wait for timed behavior
// 200ms = 2 ticks at 100ms intervals - documented and justified
```

**Requirements:**
1. First wait for triggering condition
2. Based on known timing (not guessing)
3. Comment explaining WHY
