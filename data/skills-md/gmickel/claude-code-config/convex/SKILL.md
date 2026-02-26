---
name: convex
description: Convex backend development patterns, validators, indexes, actions, queries, mutations, file storage, scheduling, React hooks, and components. Use when writing Convex code, debugging Convex issues, or planning Convex architecture.
---

<objective>
Provide comprehensive Convex development guidance to avoid common mistakes and ensure code compiles on first try.
</objective>

<quick_reference>
Key rules (full details in references/guide.md):

**Functions**: Import from `./_generated/server`, use `query({ args, handler })` syntax
**Indexes**: Never use `.filter()` - use `.withIndex()`. Never define `by_creation_time` index
**Actions**: Add `"use node";` at top, never use `ctx.db` - use `ctx.runQuery`/`ctx.runMutation`
**Scheduler**: Auth does NOT propagate - use internal functions
**React**: Never call hooks conditionally - use `"skip"` pattern
</quick_reference>

<process>
1. Read `references/guide.md` for comprehensive Convex patterns
2. Apply patterns to the specific task
3. Verify against the checklist in section 18 of the guide
</process>

<required_reading>
Always load: references/guide.md
</required_reading>
