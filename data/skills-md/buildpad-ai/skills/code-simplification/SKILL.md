---
name: code-simplification
description: Simplifies code while preserving behavior. Use when code works but is harder to read or maintain than it should be. Use when complexity has accumulated and needs reduction.
---

# Code Simplification

## Overview

Reduce complexity while preserving exact behavior. Simplification is not refactoring for its own sake — it's removing accidental complexity that makes code harder to understand, test, and maintain. The goal is clarity, not cleverness.

## When to Use

- Code works but is harder to read or maintain than it should be
- A function or module has grown too complex
- After a feature is complete and tests pass, before moving to the next phase
- During Phase 5 (Polish) of DaaS development

**When NOT to use:** Don't simplify code you don't understand yet. Don't simplify during active feature development (finish the feature first).

## Core Principles

### Chesterton's Fence

Before changing anything that seems unnecessary, understand why it exists:

```
See code that looks wrong or unnecessary
├── Understand why it was written this way
│   ├── Has a good reason → Document the reason, leave it
│   └── Has no good reason → Safe to simplify
└── Don't understand → Research before changing
```

### Rule of 500

If a function exceeds ~500 lines, it's almost certainly doing too much. But extract only when the extracted piece has a clear, independent purpose.

### Complexity Budget

Every abstraction has a cost. Before adding one, ask:
- Does this abstraction serve at least 3 use cases?
- Is the complexity it adds less than the complexity it removes?
- Could this be done with a simple function instead?

## Simplification Patterns

### Remove Dead Code

```typescript
// Before: Accumulated unused code
function processTask(task: Task) {
  // const legacyFormat = convertToLegacy(task); // Removed in v2
  const result = validate(task);
  // if (USE_OLD_PIPELINE) { ... } // Feature flag removed
  return result;
}

// After: Only live code
function processTask(task: Task) {
  return validate(task);
}
```

### Flatten Nested Logic

```typescript
// Before: Deeply nested
function getStatus(task: Task) {
  if (task) {
    if (task.completed) {
      if (task.archived) {
        return 'archived';
      } else {
        return 'completed';
      }
    } else {
      return 'pending';
    }
  }
  return 'unknown';
}

// After: Early returns
function getStatus(task: Task) {
  if (!task) return 'unknown';
  if (task.archived) return 'archived';
  if (task.completed) return 'completed';
  return 'pending';
}
```

### Replace Clever Code

```typescript
// Before: Clever but unclear
const x = ~~(Math.random() * 100);
const y = arr.reduce((a, b) => (a[b] = (a[b] || 0) + 1, a), {});

// After: Clear intent
const x = Math.floor(Math.random() * 100);
const counts: Record<string, number> = {};
for (const item of arr) {
  counts[item] = (counts[item] ?? 0) + 1;
}
```

### Inline Over-Abstractions

```typescript
// Before: Abstraction for one use
class TaskStatusManager {
  getStatus(task: Task) { return task.status; }
  setStatus(task: Task, s: string) { task.status = s; }
}

// After: Direct and clear
task.status = 'completed';
```

## DaaS-Specific Simplifications

- Replace custom filter UI with `FilterPanel` component
- Replace custom table + pagination with `CollectionList`
- Replace manual permission checks with `CollectionForm`/`CollectionList` built-in RBAC
- Replace custom form validation with DaaS extension hooks
- Replace custom audit trail with DaaS built-in activity logging

## Process

1. **Ensure tests pass** before making any changes
2. **Identify complexity** — what's hard to understand or maintain?
3. **Understand why** — Chesterton's Fence check
4. **Make one change** at a time
5. **Run tests** after each change
6. **Commit** each simplification separately
7. **Never mix** simplification with behavior changes

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "It might be needed later" | YAGNI. Remove it. If needed later, git has it. |
| "It's working, don't touch it" | Working but unreadable code costs every time someone reads it. |
| "The abstraction makes it flexible" | Unused flexibility is complexity. Simplify to what's actually used. |
| "I'll just quickly refactor this too" | Simplification is its own commit. Don't mix with feature work. |

## Red Flags

- Abstractions with only one implementation
- Functions longer than 50 lines that do multiple things
- Deep nesting (more than 3 levels)
- Comments explaining what the code does (instead of the code being self-explanatory)
- Unused imports, variables, or functions
- Feature flags for features that shipped months ago

## Verification

After simplification:

- [ ] All existing tests still pass (behavior unchanged)
- [ ] Build succeeds
- [ ] No dead code remains
- [ ] Each simplification is a separate commit
- [ ] The "why" is documented for anything that looks unnecessary but was kept
