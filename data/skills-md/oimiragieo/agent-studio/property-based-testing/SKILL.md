---
name: property-based-testing
description: 'fast-check patterns for JS/TS — 6 canonical property categories with worked examples targeting agent-studio utilities (path normalization, safe-json, glob-to-regex, routing logic)'
version: 1.1.0
verified: true
lastVerifiedAt: '2026-03-01'
category: 'Testing'
agents: [qa, developer]
user_invocable: true
invoked_by: both
tools: [Read, Write, Bash]
tags: [testing, property-based, fast-check, javascript, typescript, fuzzing, invariants]
best_practices:
  - State properties as invariants that must hold for ALL inputs
  - Use shrinkage to get minimal counterexamples on failure
  - Combine with unit tests — property tests find edge cases, unit tests document examples
error_handling: graceful
---

# Property-Based Testing

fast-check patterns for JavaScript/TypeScript that find edge cases unit tests miss. Includes 6 canonical property categories with worked examples targeting agent-studio's own utilities.

## When to Use

- New utility functions (path normalization, parsers, transformers)
- Bug fixes where the fix has a general invariant (not just the specific repro case)
- Security-sensitive string handling (avoid escaping bugs, injection vectors)
- Any function where "this property should hold for ALL inputs" can be stated

## The 6 Canonical Property Categories

### 1. Inverse Operations (Round-trip)

```javascript
import fc from 'fast-check';
// If you serialize then deserialize, you get back the original
fc.assert(
  fc.property(fc.anything(), value => {
    expect(deserialize(serialize(value))).toEqual(value);
  })
);
```

### 2. Idempotency

```javascript
// Applying a function twice gives same result as once
fc.assert(
  fc.property(fc.string(), str => {
    expect(normalize(normalize(str))).toEqual(normalize(str));
  })
);
```

### 3. Commutativity / Order Independence

```javascript
// Order of inputs shouldn't matter
fc.assert(
  fc.property(fc.array(fc.integer()), arr => {
    expect(sum(arr)).toEqual(sum([...arr].reverse()));
  })
);
```

### 4. Invariants (Properties that must always hold)

```javascript
// Output always has certain structural properties
fc.assert(
  fc.property(fc.string(), input => {
    const result = parseArgs(input);
    expect(result).toHaveProperty('args');
    expect(Array.isArray(result.args)).toBe(true);
  })
);
```

### 5. Oracle Comparison (Simpler reference implementation)

```javascript
// Compare fast implementation against slow-but-correct reference
fc.assert(
  fc.property(fc.array(fc.integer()), arr => {
    expect(fastSort(arr)).toEqual(referenceSort(arr));
  })
);
```

### 6. Metamorphic Relations

```javascript
// If input changes in a known way, output changes in a predictable way
fc.assert(
  fc.property(fc.array(fc.integer()), arr => {
    const sorted = sort(arr);
    const sortedWithExtra = sort([...arr, Number.MAX_SAFE_INTEGER]);
    expect(sortedWithExtra[sortedWithExtra.length - 1]).toBe(Number.MAX_SAFE_INTEGER);
  })
);
```

## Agent-Studio Specific Examples

### Path Normalization (targets SE-01 from sharp-edges)

```javascript
import fc from 'fast-check';
const { normalizePath } = require('.claude/lib/utils/path-constants.cjs');

// Property: normalized path never contains backslashes
fc.assert(
  fc.property(fc.string(), path => {
    expect(normalizePath(path)).not.toMatch(/\\/);
  })
);

// Property: idempotent
fc.assert(
  fc.property(fc.string(), path => {
    expect(normalizePath(normalizePath(path))).toEqual(normalizePath(path));
  })
);
```

### Safe JSON Parser (targets SE-02 from sharp-edges)

```javascript
const { safeParseJSON } = require('.claude/lib/utils/safe-json.cjs');

// Property: never throws, always returns { success, data }
fc.assert(
  fc.property(fc.string(), input => {
    const result = safeParseJSON(input, null);
    expect(result).toHaveProperty('success');
    expect(typeof result.success).toBe('boolean');
  })
);

// Property: prototype pollution not possible
fc.assert(
  fc.property(fc.string(), input => {
    const before = Object.prototype.toString;
    safeParseJSON(input, null);
    expect(Object.prototype.toString).toBe(before);
  })
);
```

### Glob-to-Regex (targets SE-05 from sharp-edges)

```javascript
// Property: patterns with **/dir/** match root-level dir
fc.assert(
  fc.property(fc.constantFrom('foo', 'bar', 'baz'), dir => {
    const pattern = `**/${dir}/**`;
    const regex = globToRegex(pattern);
    expect(`${dir}/file.js`).toMatch(regex); // root-level match
    expect(`a/${dir}/file.js`).toMatch(regex); // nested match
  })
);
```

### Routing Logic

```javascript
// Property: routing is deterministic (same input -> same agent)
fc.assert(
  fc.property(fc.string(), intent => {
    expect(route(intent)).toEqual(route(intent));
  })
);

// Property: routing never returns null/undefined
fc.assert(
  fc.property(fc.string(), intent => {
    expect(route(intent)).toBeTruthy();
  })
);
```

## Installation

```bash
pnpm add -D fast-check
```

## Running Property Tests

```bash
# Run all property tests
node --test tests/**/*.property.test.cjs

# Run with verbose output (shows counterexamples on failure)
FAST_CHECK_VERBOSE=true node --test tests/**/*.property.test.cjs
```

## Shrinkage (Automatic Counterexample Minimization)

fast-check automatically shrinks failing inputs to the minimal counterexample. Example:

- Test fails on: `"C:\\Users\\foo\\deep\\nested\\path"`
- fast-check shrinks to: `"a\\b"` (minimal backslash case)

This makes debugging far faster than traditional fuzzing.

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
