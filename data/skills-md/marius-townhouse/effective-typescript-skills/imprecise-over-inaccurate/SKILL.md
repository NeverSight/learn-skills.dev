---
name: imprecise-over-inaccurate
description: Use when types become too complex. Use when precision causes false positives. Use when accuracy is uncertain.
---

# Prefer Imprecise Types to Inaccurate Types

## Overview

**An imprecise type that's correct is better than a precise type that's wrong.**

When you make types more precise, you risk making them inaccurate. Inaccurate types cause false positives (valid code rejected) or false negatives (invalid code accepted). Both erode trust in the type system.

## When to Use This Skill

- Making types "more precise"
- Getting unexpected type errors
- Types that reject valid use cases
- Debugging complex generic types

## The Iron Rule

```
Types should never reject valid code.
When in doubt, be less precise.
```

**Remember:**
- False positives (rejecting valid code) erode trust
- False negatives (accepting invalid code) cause bugs
- Imprecise but correct > precise but wrong
- Complex types are harder to debug

## Detection: Over-Precise Types

```typescript
// Attempt to precisely type CSS colors
type CSSColor =
  | 'red' | 'blue' | 'green' | 'yellow' // named colors
  | `#${string}`                        // hex colors
  | `rgb(${number}, ${number}, ${number})`; // rgb

function setColor(color: CSSColor) { /* ... */ }

// But this valid CSS is rejected:
setColor('rgb(255,255,255)');  // Error: no spaces around commas!
setColor('rgba(0, 0, 0, 0.5)');  // Error: didn't account for rgba!
```

The precise type is inaccurate - it rejects valid CSS.

## Better: Imprecise but Accurate

```typescript
// Less precise, but accepts all valid CSS colors
function setColor(color: string) { /* ... */ }

setColor('rgb(255, 255, 255)');  // OK
setColor('rgba(0, 0, 0, 0.5)');  // OK
setColor('invalid');             // OK (imprecise)
```

The string type is imprecise (accepts invalid colors) but accurate (never rejects valid colors).

## Middle Ground: Partial Precision

```typescript
// Provide known values, allow escape hatch
type CSSColor = 
  | 'red' | 'blue' | 'green' | 'yellow'
  | (string & {});  // Allows any string with autocomplete for known values

setColor('red');     // Autocomplete works
setColor('custom');  // Still allowed
```

## Real Example: JSON Schema

```typescript
// Trying to precisely type JSON Schema
interface JSONSchema {
  type: 'string' | 'number' | 'object' | 'array' | 'boolean' | 'null';
  properties?: Record<string, JSONSchema>;
  items?: JSONSchema;
  // ... 50 more properties
}

// But real JSON Schema is more flexible:
const schema: JSONSchema = {
  type: ['string', 'null'],  // Error: type can be array!
  // ...
};
```

The "precise" type is inaccurate. A simpler type might be better:

```typescript
interface JSONSchema {
  type?: string | string[];
  [key: string]: unknown;  // Allow any other properties
}
```

## When Precision Pays Off

Precision is worth it when:

1. **You control all the inputs** (internal types)
2. **The domain is well-defined** (finite, known values)
3. **Errors are caught early** (development time)
4. **The type is simple enough to be obviously correct**

```typescript
// Good use of precision: finite, known values
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';

// Good use of precision: simple domain
type PositiveInteger = number;  // (Could use branded type)
```

## When to Back Off

Back off from precision when:

1. **External data is involved** (APIs, user input)
2. **The domain is complex** (CSS, HTML, regex)
3. **The type rejects valid use cases**
4. **The type is complex and hard to verify**

```typescript
// Over-precise: might reject valid CSS
type CSSLength = `${number}px` | `${number}em` | `${number}rem`;

// Better: trust the developer
type CSSLength = string;

// Or: document the expected format
/** CSS length value, e.g., "10px", "2em" */
type CSSLength = string;
```

## False Positives vs False Negatives

| Problem | Impact | Solution |
|---------|--------|----------|
| False Positive | Valid code rejected | Make type less precise |
| False Negative | Invalid code accepted | Validate at runtime |

False positives are worse because they:
- Block legitimate work
- Require workarounds (`as any`)
- Erode trust in TypeScript

## Progressive Refinement

Start imprecise, add precision as needed:

```typescript
// V1: Start broad
interface Config {
  [key: string]: unknown;
}

// V2: Add known properties
interface Config {
  port?: number;
  host?: string;
  [key: string]: unknown;  // Still allow extras
}

// V3: Remove index signature if confident
interface Config {
  port: number;
  host: string;
}
```

## Pressure Resistance Protocol

### 1. "More Precise is Better"

**Pressure:** "Types should be as specific as possible"

**Response:** Only if they're also accurate. Precise + wrong = worse.

**Action:** Check: does this precision reject valid code?

### 2. "We Should Catch All Errors"

**Pressure:** "The type should prevent all invalid values"

**Response:** You can't type-check everything. Runtime validation exists.

**Action:** Type what you can accurately. Validate the rest at runtime.

## Red Flags - STOP and Reconsider

- Complex types with many unions/intersections
- Type errors on code you know is valid
- Frequent use of `as any` to work around types
- Types that are hard to explain

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "The type is technically correct" | If it rejects valid code, it's not correct |
| "Users should write better code" | Types should match reality, not ideals |
| "We can add exceptions" | Exceptions mean the type is wrong |

## Quick Reference

```typescript
// DON'T: Over-precise type that rejects valid code
type Color = 'red' | 'blue' | `#${string}`;
setColor('rgb(0,0,0)');  // Error - but it's valid!

// DO: Imprecise type that accepts all valid code
type Color = string;
setColor('rgb(0,0,0)');  // OK

// BETTER: Partial precision with escape hatch
type Color = 'red' | 'blue' | (string & {});
setColor('red');         // Autocomplete works
setColor('rgb(0,0,0)');  // Still allowed
```

## The Bottom Line

**Accuracy trumps precision.**

A type that accepts some invalid values is better than a type that rejects valid values. When making types more precise, verify they remain accurate. If precision causes false positives, back off.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 40: Prefer Imprecise Types to Inaccurate Types.
