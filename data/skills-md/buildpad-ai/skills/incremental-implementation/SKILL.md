---
name: incremental-implementation
description: Delivers changes incrementally. Use when implementing any feature or change that touches more than one file. Use when you're about to write a large amount of code at once, or when a task feels too big to land in one step.
---

# Incremental Implementation

## Overview

Build in thin vertical slices — implement one piece, test it, verify it, then expand. Avoid implementing an entire feature in one pass. Each increment should leave the system in a working, testable state.

## When to Use

- Implementing any multi-file change
- Building a new feature from a task breakdown
- Refactoring existing code
- Any time you're tempted to write more than ~100 lines before testing

**When NOT to use:** Single-file, single-function changes where the scope is already minimal.

> **Parallel slices:** independent slices can be built by parallel subagents (see `subagent-delegation`), but integration and the build/test/verify loop stay on the main thread.

## The Increment Cycle

```
┌──────────────────────────────────────┐
│                                      │
│   Implement ──→ Test ──→ Verify ──┐  │
│       ▲                           │  │
│       └───── Commit ◄─────────────┘  │
│              │                       │
│              ▼                       │
│          Next slice                  │
│                                      │
└──────────────────────────────────────┘
```

## Slicing Strategies

### Vertical Slices (Preferred)

Build one complete path through the stack:

```
Slice 1: Create a task (define the collection with `create-collection` + API route + basic form)
    → Tests pass, user can create a task

Slice 2: List tasks (DaaS query + API route + CollectionList)
    → Tests pass, user can see their tasks

Slice 3: Edit a task (update API + CollectionForm edit mode)
    → Tests pass, user can modify tasks

Slice 4: Delete a task (API + CollectionList enableDelete)
    → Tests pass, full CRUD complete
```

### Risk-First Slicing

Tackle the riskiest piece first:

```
Slice 1: Prove the DaaS workflow integration works (highest risk)
Slice 2: Build the approval UI on the proven workflow
Slice 3: Add notifications and audit trail
```

If Slice 1 fails, you discover it before investing in Slices 2 and 3.

## Implementation Rules

### Rule 0: Simplicity First

Before writing any code, ask: "What is the simplest thing that could work?"

```
SIMPLICITY CHECK:
✗ Generic EventBus with middleware pipeline for one notification
✓ Simple function call

✗ Abstract factory pattern for two similar components
✓ Two straightforward components with shared utilities

✗ Config-driven form builder for three forms
✓ Three CollectionForm instances with field configs
```

### Rule 0.5: Scope Discipline

Touch only what the task requires. Do NOT:
- "Clean up" code adjacent to your change
- Refactor imports in files you're not modifying
- Add features not in the spec because they "seem useful"

```
NOTICED BUT NOT TOUCHING:
- src/utils/format.ts has an unused import (unrelated)
- The auth middleware could use better error messages (separate task)
→ Want me to create tasks for these?
```

### Rule 1: One Thing at a Time

Each increment changes one logical thing. Don't mix concerns.

### Rule 2: Keep It Compilable

After each increment, `pnpm build` and `pnpm test` must pass.

### Rule 3: Feature Flags for Incomplete Features

```typescript
const ENABLE_TASK_SHARING = process.env.FEATURE_TASK_SHARING === 'true';
if (ENABLE_TASK_SHARING) {
  // New sharing UI — hidden until ready
}
```

### Rule 4: Safe Defaults

New code should default to safe, conservative behavior.

### Rule 5: Rollback-Friendly

Each increment should be independently revertable.

## DaaS Layer Alignment

Incremental slicing follows the DaaS dependency layers used in the spec's `tasks.md`:

| Layer | Typical Slices |
|-------|---------------|
| Data | Collection (`create-collection`) → API route → Types → API tests |
| UI | List page → Form page → Navigation |
| Logic | Validation → Permissions → Workflow |
| Relations | M2O → M2M → File fields |
| Hardening | Error handling → Performance → A11y → Docs |

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll test it all at the end" | Bugs compound. A bug in Slice 1 makes Slices 2-5 wrong. Test each slice. |
| "It's faster to do it all at once" | It *feels* faster until something breaks and you can't find which of 500 changed lines caused it. |
| "These changes are too small to commit separately" | Small commits are free. Large commits hide bugs. |
| "This refactor is small enough to include" | Refactors mixed with features make both harder to debug. Separate them. |

## Red Flags

- More than 100 lines of code written without running tests
- Multiple unrelated changes in a single increment
- "Let me just quickly add this too" scope expansion
- Skipping the test/verify step to move faster
- Build or tests broken between increments
- Building abstractions before the third use case
- Touching files outside the task scope "while I'm here"

## Verification

After completing all increments:

- [ ] Each increment was individually tested and committed
- [ ] The full test suite passes
- [ ] The build is clean
- [ ] The feature works end-to-end as specified
- [ ] No uncommitted changes remain
