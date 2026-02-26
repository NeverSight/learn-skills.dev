---
name: hide-unsafe-assertions
description: Use when type assertions are necessary. Use when function implementations need any. Use when hiding unsafe code.
---

# Hide Unsafe Type Assertions in Well-Typed Functions

## Overview

**Keep type signatures clean; hide assertions in implementations.**

If a function needs a type assertion or `any` internally, that's OK - as long as the public signature is correct. Users see a well-typed API; the unsafe code is contained.

## When to Use This Skill

- Function implementations need type assertions
- TypeScript can't follow your logic
- Wrapping libraries with poor types
- Internal complexity, clean external API

## The Iron Rule

```
Never compromise type signatures for implementation convenience.
Hide assertions inside well-typed functions.
```

**Remember:**
- Type signatures are your API contract
- Implementations are hidden details
- Users shouldn't see assertions
- Test assertion-heavy code thoroughly

## Detection: Exposed Unsafety

```typescript
// Bad: unsafe return type exposes any
async function fetchPeak(peakId: string): Promise<unknown> {
  return checkedFetchJSON(`/api/peaks/${peakId}`);
}

// Every caller must assert:
const peak = await fetchPeak('denali') as MountainPeak;  // Tedious!
```

## Better: Hide the Assertion

```typescript
async function fetchPeak(peakId: string): Promise<MountainPeak> {
  return checkedFetchJSON(`/api/peaks/${peakId}`) as Promise<MountainPeak>;
}

// Callers get clean types:
const peak = await fetchPeak('denali');
//    ^? MountainPeak
```

The assertion is hidden inside; callers get a clean API.

## Validate Inside Hidden Assertions

```typescript
async function fetchPeak(peakId: string): Promise<MountainPeak> {
  const maybePeak = await checkedFetchJSON(`/api/peaks/${peakId}`);
  
  // Validation adds safety to the assertion
  if (!maybePeak || typeof maybePeak !== 'object' || !('name' in maybePeak)) {
    throw new Error(`Invalid peak data: ${JSON.stringify(maybePeak)}`);
  }
  
  return maybePeak as MountainPeak;
}
```

Now the assertion has runtime backup.

## When TypeScript Can't Follow

```typescript
function shallowEqual(a: object, b: object): boolean {
  for (const [k, aVal] of Object.entries(a)) {
    if (!(k in b) || aVal !== b[k]) {
      //                     ~~~~
      // Element implicitly has an 'any' type
      return false;
    }
  }
  return Object.keys(a).length === Object.keys(b).length;
}
```

We know `k in b` is true, but TypeScript doesn't connect this to `b[k]`.

### Wrong Fix: Weaken the Signature

```typescript
// DON'T: weakening b to any exposes unsafety
function shallowEqual(a: object, b: any): boolean {
  // ...
}

shallowEqual({x: 1}, null);  // No error! Crashes at runtime.
```

### Right Fix: Hide the Assertion

```typescript
function shallowEqual(a: object, b: object): boolean {
  for (const [k, aVal] of Object.entries(a)) {
    // Hidden assertion - we've checked k in b
    if (!(k in b) || aVal !== (b as any)[k]) {
      return false;
    }
  }
  return Object.keys(a).length === Object.keys(b).length;
}

shallowEqual({x: 1}, null);
//                   ~~~~
// Argument of type 'null' is not assignable to parameter of type 'object'.
```

Type signature stays clean; assertion is narrowly scoped.

## Function Overloads as Hidden Assertions

```typescript
// Overload presents clean signature to callers
async function fetchPeak(peakId: string): Promise<MountainPeak>;
async function fetchPeak(peakId: string): Promise<unknown> {
  return checkedFetchJSON(`/api/peaks/${peakId}`);
}

const denali = fetchPeak('denali');
//    ^? Promise<MountainPeak>
```

The implementation returns `unknown`, but callers see `MountainPeak`.

## Narrow Scope of Assertions

```typescript
// DON'T: Assertion on whole object
const config: Config = {
  a: 1,
  b: 2,
  c: { key: value }
} as any;  // No checking on a, b!

// DO: Assertion only on problem area
const config: Config = {
  a: 1,
  b: 2,  // These are still checked
  c: { key: value as any }  // Only this is unsafe
};
```

## Document Why Assertions Are Valid

```typescript
function shallowEqual(a: object, b: object): boolean {
  for (const [k, aVal] of Object.entries(a)) {
    // `(b as any)[k]` is safe because we've verified `k in b`
    if (!(k in b) || aVal !== (b as any)[k]) {
      return false;
    }
  }
  return Object.keys(a).length === Object.keys(b).length;
}
```

Comments help future maintainers understand the assertion.

## Test Thoroughly

Functions with hidden assertions need extra testing:

```typescript
describe('fetchPeak', () => {
  it('handles valid peak data', async () => {
    const peak = await fetchPeak('denali');
    expect(peak.name).toBe('Denali');
    expect(peak.elevationMeters).toBe(6190);
  });

  it('throws on invalid data', async () => {
    mockFetch({ invalid: 'data' });
    await expect(fetchPeak('unknown')).rejects.toThrow('Invalid peak');
  });

  it('handles missing fields', async () => {
    mockFetch({ name: 'Partial' });  // Missing fields
    await expect(fetchPeak('partial')).rejects.toThrow();
  });
});
```

## Pressure Resistance Protocol

### 1. "Just Change the Return Type"

**Pressure:** "Make it return unknown to avoid the assertion"

**Response:** That pushes unsafety to every caller.

**Action:** Keep clean signature; hide assertion in implementation.

### 2. "Assertions Are Dangerous"

**Pressure:** "We should avoid assertions entirely"

**Response:** Sometimes they're necessary. Contained and tested is OK.

**Action:** Hide, validate, document, and test.

## Red Flags - STOP and Reconsider

- Function signatures containing `any` or `unknown` for convenience
- Assertions scattered across calling code
- Changing signatures to avoid implementation errors
- Untested assertion-heavy code

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's more honest" | Pushing unsafety to callers is worse |
| "Assertions are bad" | Contained assertions are fine |
| "Users can narrow" | Users shouldn't have to |

## Quick Reference

```typescript
// DON'T: Expose unsafety in signature
function fetch(): Promise<unknown> { ... }
const data = await fetch() as Data;  // Assertion at every call site

// DO: Hide assertion in implementation
function fetch(): Promise<Data> {
  return api.fetch() as Promise<Data>;  // Hidden, one place
}

// DO: Narrow scope
const obj = { a: value as any };  // Not: whole object as any

// DO: Document and test
// This assertion is valid because... [explanation]
return data as Data;
```

## The Bottom Line

**Hide unsafe code; expose clean types.**

Type assertions and `any` types are sometimes necessary. Keep them in function implementations, not signatures. Document why they're valid. Test thoroughly.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 45: Hide Unsafe Type Assertions in Well-Typed Functions.
