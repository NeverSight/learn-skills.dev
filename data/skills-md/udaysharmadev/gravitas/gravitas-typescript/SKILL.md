---
name: gravitas-typescript
description: >
  GRAVITAS extension for TypeScript projects. Adds TypeScript-specific recon,
  strict mode patterns, Vitest/Jest integration, and common TS failure modes.
  Load in addition to the base GRAVITAS skill.
triggers:
  - "typescript"
  - "ts"
  - "tsx"
  - "react"
  - "next"
  - "vitest"
  - "jest"
---

# GRAVITAS — TypeScript Extension

Extends the base GRAVITAS skill with TypeScript-specific patterns.
Load `skills/gravitas/SKILL.md` first, then this file.

---

## TypeScript Recon Additions

Add to standard recon checklist:

```
□ tsconfig.json — strict mode? noUncheckedIndexedAccess? exactOptionalPropertyTypes?
□ package.json — TypeScript version, test runner (vitest vs jest)
□ eslint config — @typescript-eslint rules in effect
□ type declarations — are there .d.ts files that affect this module?
□ path aliases — does tsconfig have paths? (affects imports)
```

### Read tsconfig strictly

```bash
cat tsconfig.json | jq '.compilerOptions | {strict, noUncheckedIndexedAccess, exactOptionalPropertyTypes, target, lib}'
```

---

## TypeScript Verification Chain

```bash
# Full chain — always in this order
tsc --noEmit                           # catches type errors first
eslint . --max-warnings 0              # @typescript-eslint rules
vitest run --reporter=verbose          # or: jest --verbose

# With coverage
vitest run --coverage --reporter=verbose

# Type coverage (optional, requires type-coverage)
npx type-coverage --strict
```

---

## TypeScript-Specific Anti-Patterns

### Never use `any`
```typescript
BAD:  function process(data: any) { ... }
GOOD: function process(data: ProcessInput) { ... }
```

### Never use `as` to silence type errors
```typescript
BAD:  const user = data as User;  // silences real type error
GOOD: if (isUser(data)) { const user = data; ... }
```

### Handle `undefined` explicitly
```typescript
BAD:  const name = user.name;          // may be undefined
GOOD: const name = user.name ?? 'Anonymous';
```

### Strict null checks
```typescript
BAD:  return users.find(u => u.id === id).name;  // crash if not found
GOOD: return users.find(u => u.id === id)?.name;
```

---

## Common TypeScript Failure Modes

| Failure | Root Cause | Fix |
|---------|-----------|-----|
| `Object is possibly undefined` | Optional property accessed without guard | Add `?.` or null check |
| `Type 'string' is not assignable to 'number'` | Wrong type passed | Check function signature, fix caller |
| `Property does not exist on type` | Interface mismatch | Update interface or use correct property |
| `Cannot find module` | Path alias not in tsconfig | Add to `paths` in tsconfig |
| `Argument of type X is not assignable to Y` | Generic type mismatch | Check generic constraints |
| Implicit `any` in strict mode | Missing type annotation | Add explicit type |

---

## TypeScript Patterns

### Parameterized types over `any`
```typescript
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}
```

### Discriminated unions for type safety
```typescript
type Result<T> =
  | { ok: true; data: T }
  | { ok: false; error: string };
```

### Type guards instead of casts
```typescript
function isUser(obj: unknown): obj is User {
  return typeof obj === 'object' && obj !== null && 'id' in obj;
}
```

---

## Test Patterns (Vitest)

### Test file location
Follow project convention — check existing tests:
```bash
find src/ -name "*.test.ts" | head -5  # see the pattern
```

### Standard test structure
```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';

describe('[module]', () => {
  beforeEach(() => { vi.clearAllMocks(); });

  it('[behavior] when [condition]', () => {
    // Arrange
    const input = ...;
    // Act
    const result = fn(input);
    // Assert
    expect(result).toEqual(expected);
  });
});
```

### Mocking
```typescript
vi.mock('../db', () => ({
  query: vi.fn().mockResolvedValue({ rows: [] })
}));
```

---

## Quick Reference

```bash
# Find all TypeScript errors
tsc --noEmit 2>&1 | grep "error TS"

# Find implicit any
tsc --noEmit --strict 2>&1

# Count test files
find src/ -name "*.test.ts" | wc -l

# Run single test file
vitest run src/auth/session.test.ts

# Watch mode (dev)
vitest --watch
```
