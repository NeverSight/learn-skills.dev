---
name: clean-code
description: Clean Code practices for TypeScript/JavaScript. Identify code smells, apply refactoring patterns, and write maintainable code. Use when reviewing code quality, refactoring messy code, or ensuring code follows best practices. Triggers on requests like "clean up this code", "refactor for readability", "identify code smells", or "make this more maintainable".
---

# Clean Code for TypeScript/JavaScript

Practical patterns for writing and refactoring clean, maintainable TypeScript/JavaScript code.

## Code Smell Detection

### Naming Smells

| Smell | Example | Fix |
|-------|---------|-----|
| Single-letter names | `const d = new Date()` | `const createdAt = new Date()` |
| Abbreviations | `const usrMgr = ...` | `const userManager = ...` |
| Generic names | `data`, `info`, `temp`, `result` | Name by what it represents |
| Misleading names | `userList` (but it's a Set) | `users` or `userSet` |
| Encoding types | `strName`, `arrItems` | `name`, `items` |

### Function Smells

| Smell | Indicator | Refactoring |
|-------|-----------|-------------|
| Too many parameters | >3 params | Extract to options object |
| Flag arguments | `process(data, true)` | Split into separate functions |
| Side effects hidden | Function does more than name suggests | Rename or split |
| God function | >20 lines or multiple responsibilities | Extract smaller functions |
| Deep nesting | >3 levels of indentation | Early returns, extract functions |

### Structure Smells

| Smell | Indicator | Refactoring |
|-------|-----------|-------------|
| Long file | >300 lines | Split by responsibility |
| Feature envy | Function uses another object's data extensively | Move to that object |
| Data clumps | Same group of params passed together | Extract to type/class |
| Primitive obsession | Using primitives for domain concepts | Create value objects |
| Switch on type | `if (type === 'A') ... else if (type === 'B')` | Polymorphism or lookup |

## Refactoring Patterns

For detailed before/after code examples, see [references/refactoring-patterns.md](references/refactoring-patterns.md).

**Quick reference:**

1. **Guard clauses** — Replace nested if/else with early returns
2. **Object lookup** — Replace switch/if-else chains with Record mapping
3. **Options object** — Replace >3 parameters with a single options object
4. **Named constants** — Replace magic numbers/strings with descriptive constants
5. **Extract function** — Break god functions into single-responsibility pieces
6. **Flatten ternaries** — Replace nested ternaries with lookup or function
7. **Consolidate duplicates** — Extract repeated logic into shared functions
8. **Simplify booleans** — Return condition directly instead of if/else true/false
9. **Array methods** — Replace manual loops with filter/map/reduce
10. **Destructure** — Use destructuring for cleaner property access

## Naming Conventions

### Functions
- **Actions**: verb + noun → `createUser`, `validateInput`, `fetchOrders`
- **Booleans**: is/has/can/should prefix → `isValid`, `hasPermission`, `canEdit`
- **Event handlers**: handle + event → `handleClick`, `handleSubmit`
- **Transformers**: to/from/parse/format → `toJSON`, `fromDTO`, `parseDate`

### Variables
- **Booleans**: positive names → `isEnabled` not `isNotDisabled`
- **Arrays/collections**: plural → `users`, `orderItems`
- **Counts**: noun + Count → `retryCount`, `errorCount`

### Constants
- **Module-level**: SCREAMING_SNAKE_CASE → `MAX_RETRIES`, `API_BASE_URL`
- **Enum-like objects**: PascalCase key, values match usage → `Status.Active`

## Quick Refactoring Checklist

When reviewing code for cleanliness:

1. **Names** — Can you understand intent without reading implementation?
2. **Functions** — Does each do exactly one thing? <20 lines?
3. **Parameters** — More than 3? Extract to object
4. **Nesting** — More than 2 levels? Use early returns
5. **Duplication** — Same logic in 2+ places? Extract
6. **Magic values** — Any unexplained numbers/strings? Name them
7. **Comments** — Explaining "what"? Rewrite code to be self-explanatory
8. **Dead code** — Commented-out code or unused vars? Delete

## Anti-Patterns to Avoid

### Over-Engineering
- Don't create abstractions for single-use cases
- Don't add configurability "for the future"
- Don't wrap simple operations in utility functions

### Under-Engineering
- Don't ignore repeated patterns (3+ occurrences = extract)
- Don't leave deeply nested code unrefactored
- Don't use `any` to avoid typing properly

### Wrong Abstraction
- Don't force inheritance when composition works
- Don't create god classes that do everything
- Don't split tightly coupled logic across files
