---
name: frontend-js-best-practices
description: JavaScript performance optimization guidelines. Use when writing, reviewing, or refactoring JavaScript/TypeScript code to ensure optimal performance patterns. Triggers on tasks involving loops, data structures, DOM manipulation, or general JS optimization.
---

# JavaScript Best Practices

Performance optimization and code style patterns for JavaScript and TypeScript code. Contains 17 rules focused on reducing unnecessary computation, optimizing data structures, and maintaining consistent conventions.

## When to Apply

Reference these guidelines when:

- Writing loops or array operations
- Working with data structures (Map, Set, arrays)
- Manipulating the DOM directly
- Caching values or function results
- Optimizing hot code paths
- Declaring variables or functions

## Rules Summary

### const-let-usage (MEDIUM) — @rules/const-let-usage.md

Use `const` at module level, `let` inside functions.

```typescript
// Module level: const with UPPER_SNAKE_CASE for primitives
const MAX_RETRIES = 3;
const userCache = new Map<string, User>();

// Inside functions: always let
function process(items: Item[]) {
  let total = 0;
  let result = [];
  for (let item of items) {
    total += item.price;
  }
  return { total, result };
}
```

### function-declarations (MEDIUM) — @rules/function-declarations.md

Prefer function declarations over arrow functions for named functions.

```typescript
// Good: function declaration
function calculateTotal(items: Item[]): number {
  let total = 0;
  for (let item of items) {
    total += item.price;
  }
  return total;
}

// Good: arrow for inline callbacks
let active = users.filter((u) => u.isActive);

// Good: arrow when type requires it
const handler: ActionFunction = async ({ request }) => {
  // ...
};
```

### no-default-exports (MEDIUM) — @rules/no-default-exports.md

Use named exports. Avoid default exports (except Remix route components).

```typescript
// Bad: default export
export default function formatCurrency(amount: number) { ... }

// Good: named export
export function formatCurrency(amount: number) { ... }

// Exception: Remix routes use default export named "Component"
export default function Component() { ... }
```

### no-as-type-casts (HIGH) — @rules/no-as-type-casts.md

Avoid `as Type` casts. Use type guards or Zod validation instead.

```typescript
// Bad: type assertion
let user = response.data as User;

// Good: Zod validation
let user = UserSchema.parse(response.data);

// Good: type guard
if (isUser(response.data)) {
  let user = response.data;
}
```

### comments-meaningful-only (MEDIUM) — @rules/comments-meaningful-only.md

Only comment when adding info the code cannot express.

```typescript
// Bad: restates the code
// Set the user's name
let userName = user.name;

// Good: explains business rule
// Transactions under $250 don't require written acknowledgment per policy
if (transaction.amount < 250) {
  return { requiresAcknowledgment: false };
}
```

### set-map-lookups (LOW-MEDIUM) — @rules/set-map-lookups.md

Use Set/Map for O(1) lookups instead of Array methods.

```typescript
// Bad: O(n) per check
const allowedIds = ["a", "b", "c"];
items.filter((item) => allowedIds.includes(item.id));

// Good: O(1) per check
const allowedIds = new Set(["a", "b", "c"]);
items.filter((item) => allowedIds.has(item.id));
```

### index-maps (LOW-MEDIUM) — @rules/index-maps.md

Build Map once for repeated lookups.

```typescript
// Bad: O(n) per lookup = O(n*m) total
orders.map((order) => ({
  ...order,
  user: users.find((u) => u.id === order.userId),
}));

// Good: O(1) per lookup = O(n+m) total
const userById = new Map(users.map((u) => [u.id, u]));
orders.map((order) => ({
  ...order,
  user: userById.get(order.userId),
}));
```

### tosorted-immutable (MEDIUM-HIGH) — @rules/tosorted-immutable.md

Use `toSorted()` instead of `sort()` to avoid mutation.

```typescript
// Bad: mutates original array
const sorted = users.sort((a, b) => a.name.localeCompare(b.name));

// Good: creates new sorted array
const sorted = users.toSorted((a, b) => a.name.localeCompare(b.name));
```

### combine-iterations (LOW-MEDIUM) — @rules/combine-iterations.md

Combine multiple filter/map into one loop.

```typescript
// Bad: 3 iterations
const admins = users.filter((u) => u.isAdmin);
const testers = users.filter((u) => u.isTester);
const inactive = users.filter((u) => !u.isActive);

// Good: 1 iteration
const admins: User[] = [],
  testers: User[] = [],
  inactive: User[] = [];
for (const user of users) {
  if (user.isAdmin) admins.push(user);
  if (user.isTester) testers.push(user);
  if (!user.isActive) inactive.push(user);
}
```

### cache-property-access (LOW-MEDIUM) — @rules/cache-property-access.md

Cache object properties in loops.

```typescript
// Bad: repeated lookups
for (let i = 0; i < arr.length; i++) {
  process(obj.config.settings.value);
}

// Good: cached lookup
const value = obj.config.settings.value;
const len = arr.length;
for (let i = 0; i < len; i++) {
  process(value);
}
```

### cache-function-results (MEDIUM) — @rules/cache-function-results.md

Cache expensive function results in module-level Map.

```typescript
const slugifyCache = new Map<string, string>();

function cachedSlugify(text: string): string {
  if (!slugifyCache.has(text)) {
    slugifyCache.set(text, slugify(text));
  }
  return slugifyCache.get(text)!;
}
```

### cache-storage (LOW-MEDIUM) — @rules/cache-storage.md

Cache localStorage/sessionStorage reads in memory.

```typescript
const storageCache = new Map<string, string | null>();

function getLocalStorage(key: string) {
  if (!storageCache.has(key)) {
    storageCache.set(key, localStorage.getItem(key));
  }
  return storageCache.get(key);
}
```

### early-exit (LOW-MEDIUM) — @rules/early-exit.md

Return early when result is determined.

```typescript
// Bad: continues after finding error
function validate(users: User[]) {
  let error = "";
  for (const user of users) {
    if (!user.email) error = "Email required";
  }
  return error ? { error } : { valid: true };
}

// Good: returns immediately
function validate(users: User[]) {
  for (const user of users) {
    if (!user.email) return { error: "Email required" };
  }
  return { valid: true };
}
```

### length-check-first (MEDIUM-HIGH) — @rules/length-check-first.md

Check array length before expensive comparison.

```typescript
// Bad: always sorts even when lengths differ
function hasChanges(a: string[], b: string[]) {
  return a.sort().join() !== b.sort().join();
}

// Good: early return if lengths differ
function hasChanges(a: string[], b: string[]) {
  if (a.length !== b.length) return true;
  let aSorted = a.toSorted();
  let bSorted = b.toSorted();
  return aSorted.some((v, i) => v !== bSorted[i]);
}
```

### min-max-loop (LOW) — @rules/min-max-loop.md

Use loop for min/max instead of sort.

```typescript
// Bad: O(n log n)
const latest = [...projects].sort((a, b) => b.updatedAt - a.updatedAt)[0];

// Good: O(n)
let latest = projects[0];
for (const p of projects) {
  if (p.updatedAt > latest.updatedAt) latest = p;
}
```

### hoist-regexp (LOW-MEDIUM) — @rules/hoist-regexp.md

Hoist RegExp creation outside loops.

```typescript
// Bad: creates regex every iteration
items.forEach(item => {
  if (/pattern/.test(item.text)) { ... }
})

// Good: create once
const PATTERN = /pattern/
items.forEach(item => {
  if (PATTERN.test(item.text)) { ... }
})
```

### batch-dom-css (MEDIUM) — @rules/batch-dom-css.md

Batch DOM reads before writes to avoid layout thrashing.

```typescript
// Bad: interleaved reads/writes force reflows
element.style.width = "100px";
const width = element.offsetWidth; // forces reflow
element.style.height = "200px";

// Good: batch writes, then read
element.style.width = "100px";
element.style.height = "200px";
const { width, height } = element.getBoundingClientRect();
```

### result-type (MEDIUM) — @rules/result-type.md

Use an explicit `Result` type for success/failure.

```typescript
let result = success(data);
if (isFailure(result)) return handleError(result.error);
```
