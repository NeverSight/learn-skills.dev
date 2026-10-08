---
name: writing-typescript
description: Use when writing or reviewing TypeScript or JavaScript that uses import/export or require, var/let/const, promise chains or async/await, for loops versus array methods, or vitest/jest tests; also when building React components, hooks, or state, Next.js routing or data fetching, or Node.js built-in imports and file operations.
---

# Writing TypeScript

## Overview

Write new TypeScript and JavaScript with current language syntax: ES modules, block-scoped declarations, `async`/`await`, and array methods. React and Next.js work and Node.js work have their own conventions in two references.

**Core principle:** Familiarity with an older style ("it still runs") is not a reason to use it. Use the current syntax unless a concrete tool or platform constraint requires the older one.

These rules apply to new code and to code you were asked to change. Do not migrate existing working code that is outside the request.

## Reference Map

Read every applicable reference before editing, reviewing, or giving implementation guidance. If unsure whether a reference applies, read it:

| Code involved | Read |
| --- | --- |
| React components, hooks, state, Next.js routing, Server Components, data fetching | [references/react-nextjs.md](references/react-nextjs.md) |
| Node.js built-in modules (`node:` imports), file reading or writing | [references/nodejs.md](references/nodejs.md) |

## Quick Reference

| Area | Do | Do not |
| --- | --- | --- |
| Modules | Use ES `import`/`export` | Use `require()` or `module.exports` |
| Declarations | Use `const` by default, `let` when you must reassign | Use `var` |
| Async | Use `async`/`await` | Chain `.then()` by default |
| Collections | Use `.map()`, `.filter()`, `.reduce()`, `.find()` | Write a `for` loop where an array method states the intent better |
| Tests | Use `vitest` or `jest` and add focused tests when behavior changes | Treat a manual check or urgency as a replacement for tests |
| React / Next.js | Function components; server-first App Router with small client boundaries; version-aware caching | Ordinary class-based UI; Pages Router APIs in App Router work; blanket caching defaults |
| Node.js | `node:` import prefix, promise-based `node:fs/promises` | Bare core imports, synchronous file APIs in concurrent paths, callbacks for ordinary sequential async work without a concrete reason |

## Modules

Use ES module `import`/`export` syntax. Avoid CommonJS `require()` and `module.exports`.

Good:

```typescript
import { parseInvoice } from "./parseInvoice";

export { parseInvoice };
```

Bad:

```typescript
const { parseInvoice } = require("./parseInvoice");

module.exports = { parseInvoice };
```

## Variable Declarations

Use `const` by default and `let` when reassignment is needed. Do not use `var`.

Good:

```typescript
const items = await loadItems();
let attempts = 0;
```

Bad:

```typescript
var items = await loadItems();
var attempts = 0;
```

## Async Operations

Use `async`/`await` for asynchronous control flow. Avoid raw `.then()` chains except when they are the clearer primitive for a specific API or composition pattern.

Good:

```typescript
const response = await fetch(url);
const bookmark = Bookmark.parse(await response.json());
```

Bad:

```typescript
fetch(url).then((response) => response.json()).then((value) => value);
```

## Array Transformations

Use modern array methods such as `.map()`, `.filter()`, `.reduce()`, and `.find()` for transformations and lookups. Avoid traditional `for` loops when an array method communicates the intent better.

Good:

```typescript
const unpaidTotals = orders
  .filter((order) => !order.paid)
  .map((order) => order.total);
const firstOverdue = orders.find((order) => order.dueAt < now);
```

Bad:

```typescript
const unpaidTotals = [];
for (let i = 0; i < orders.length; i++) {
  if (!orders[i].paid) {
    unpaidTotals.push(orders[i].total);
  }
}
```

## Tests

Use `vitest` or `jest` for JavaScript and TypeScript tests. When behavior changes, add or update focused tests that prove the new behavior or the regression fix; a manual check or a deadline is not a substitute.

## Related Rules (Short Form)

- Parse external data (API responses, form input, `process.env`) with a schema at the boundary and pass typed values inward instead of passing `unknown` or `any` through the code.
- Keep route handlers, server actions, and UI event handlers thin; business decisions belong in a callable operation, not in the transport or component.

## Red Flags

Stop and use the current syntax if you think or see:

- "Use CommonJS, `var`, or promise chains because the old style is familiar."
- "The legacy syntax still works, so it is fine." Working code is not the same as current convention.
- "Legacy reason" meaning a concrete tool or platform constraint, not personal familiarity or an old example you copied.
- "Use Pages Router APIs for new Next.js App Router work."
- "Import Node built-ins without `node:` because it is shorter."
- "This is a quick behavior change, so manual verification is enough."

## Common Mistakes

- Keeping outdated language or framework style because it still runs, instead of checking the relevant rule.
- Writing `.then()` chains for ordinary sequential async work where `await` is clearer.
- Using a `for` loop with a manual accumulator for a plain transform or lookup.
- Reaching for `var` or `require()` because a snippet found online used them.
- Using synchronous file operations inside request handlers or workers.
- Skipping focused tests for behavior changes because the change looks small or urgent.
- Rewriting unrelated working code to the current style while making a small change; apply the rules to new or requested changes only.
