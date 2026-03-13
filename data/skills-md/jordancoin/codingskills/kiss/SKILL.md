---
name: kiss
description: When writing or reviewing code to reduce complexity and improve readability. Use when the user says "simplify this," "too complex," "hard to read," "clean up," "what does this do," or "can't follow this code." For over-engineering concerns, see yagni. For structural clarity, see separation-of-concerns.
metadata:
  version: 1.0.0
---

# KISS — Keep It Simple

## Before Applying

If `.agents/stack-context.md` exists, read it first. Apply this principle using idiomatic patterns for the detected stack. For framework-specific details, use context7 MCP or web search — don't guess.

## Principle

Given two solutions that produce the same result, prefer the one that is easier to read, understand, and change.

## Why This Matters in Production

Simple code survives contact with production. Complex code breaks in ways that are hard to diagnose, hard to fix, and hard to verify the fix didn't break something else. Every incident response starts with someone reading code under pressure — if they can't understand it quickly, the outage gets longer.

Complexity compounds. A "slightly clever" solution today becomes an "incomprehensible" solution after six months of patches by three different developers.

The most dangerous bugs hide in code that's too complex for any single person to hold in their head.

## Rules

1. **Optimize for reading, not writing.** Code is read 10x more often than it's written. A few extra lines of clear code beats a one-liner that requires a comment to explain.
2. **Use boring technology.** Prefer well-understood tools, patterns, and libraries over novel ones. Novel solutions carry hidden costs in debugging, hiring, and documentation.
3. **Limit nesting depth.** If a function has more than 3 levels of nesting, flatten it with early returns, guard clauses, or extraction into helper functions.
4. **One function, one job.** If you need the word "and" to describe what a function does, split it.
5. **Name things for what they do, not how they do it.** `get_active_users()` not `query_db_filter_status_map_results()`.
6. **Avoid clever tricks.** Bitwise hacks, regex one-liners for complex parsing, operator overloading for non-obvious operations — these optimize for the writer's ego, not the reader's comprehension.
7. **Prefer explicit over implicit.** Magic values, hidden state, implicit type conversions, and action-at-a-distance make code unpredictable.

## Anti-Patterns

- **Premature optimization:** Sacrificing readability for performance without profiling data showing it matters
- **Abstraction astronautics:** Factory factory patterns, deeply nested generics, frameworks for simple tasks
- **Clever one-liners:** Dense expressions that compress logic to the point of obscurity
- **God functions:** 200+ line functions that handle multiple concerns
- **Stringly typed systems:** Using raw strings where enums, types, or constants would add clarity
- **Hidden control flow:** Decorators, middleware chains, or event systems that make it impossible to trace what happens when a request arrives

## Examples

```
-- Overly clever
users = {u.id: u for u in db.query(User) if u.active and u.role in roles and not u.banned}

-- Simple and scannable
active_users = db.query(User).where(active=true, banned=false)
users = filter_by_role(active_users, roles)
users_by_id = index_by(users, key="id")
```

```
-- Deeply nested
def process(data):
    if data:
        if data.valid:
            if data.type == "order":
                if data.items:
                    # actual logic buried 4 levels deep

-- Flattened with guard clauses
def process(data):
    if not data:
        return
    if not data.valid:
        return
    if data.type != "order":
        return
    if not data.items:
        return
    # actual logic at top level
```

## Boundaries

- **Simple does not mean naive.** Error handling, input validation, and proper data structures are not "complexity" — they're correctness. Don't strip away safety in the name of simplicity.
- **Simple does not mean primitive.** Using a well-chosen library or pattern (like a state machine for complex state transitions) can be simpler than hand-rolling the equivalent logic.
- **Some domains are inherently complex.** Cryptography, distributed consensus, and financial calculations have irreducible complexity. KISS means don't add unnecessary complexity on top.
- **Tension with DRY:** Sometimes duplicating a few lines is simpler than introducing an abstraction. Prefer the version a new team member could understand in 30 seconds.

## Code Review Checklist

- [ ] Can a new team member understand this code without asking the author?
- [ ] Are there any "clever" shortcuts that save lines but cost clarity?
- [ ] Is nesting depth 3 or less throughout?
- [ ] Does every function have a single, clear responsibility?
- [ ] Could any complex logic be replaced with a well-named helper function?
- [ ] Are there any comments explaining "what" instead of "why"? (If so, the code itself isn't clear enough.)

## Related Skills

- **yagni**: When the complexity comes from building things you don't need yet
- **separation-of-concerns**: When complexity comes from mixed responsibilities
- **solid**: When complexity comes from poor module design
