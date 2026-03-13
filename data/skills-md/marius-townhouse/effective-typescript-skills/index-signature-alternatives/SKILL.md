---
name: index-signature-alternatives
description: Use when defining object types with dynamic keys. Use when tempted to use index signatures. Use when parsing CSV or JSON data.
---

# Prefer More Precise Alternatives to Index Signatures

## Overview

**Index signatures are imprecise. Use interfaces, Records, or Maps instead.**

Index signatures (`{[key: string]: T}`) allow any string key, don't require specific keys, and can't have different types for different keys. There are almost always better alternatives.

## When to Use This Skill

- Defining types with known property names
- Modeling data from APIs or configuration files
- Working with CSV or dynamic data
- Choosing between object types and Maps

## The Iron Rule

```
If you know the property names, DON'T use an index signature.
Use an interface, Record, or mapped type instead.
```

**Remember:**
- Index signatures allow any key (including typos)
- Index signatures don't require any specific keys
- Index signatures can't have distinct types per key
- Language services (autocomplete) don't work well with index signatures

## Detection: Index Signature Problems

```typescript
// Index signature: too permissive
type Rocket = { [property: string]: string };

const rocket: Rocket = {
  name: 'Falcon 9',
  variant: 'Block 5',
  thrust: '7,607 kN',
};

// Problems:
rocket.Name;    // Typo compiles (should be 'name')
const r: Rocket = {};  // Empty object is valid
rocket.thrust;  // Can't be a number, even though it should be
```

## Better Alternatives

### 1. Interface (Best for Known Properties)

```typescript
interface Rocket {
  name: string;
  variant: string;
  thrust_kN: number;  // Can have different types
}

const falconHeavy: Rocket = {
  name: 'Falcon Heavy',
  variant: 'v1',
  thrust_kN: 15200,
};

// Benefits:
// - Typos caught: rocket.Name is an error
// - Required fields enforced
// - Each field has its own type
// - Autocomplete works
```

### 2. Record (For Union of Known Keys)

```typescript
// Limited set of keys, same value type
type Vec3D = Record<'x' | 'y' | 'z', number>;
// Same as: { x: number; y: number; z: number }

type CSSColors = Record<'primary' | 'secondary' | 'accent', string>;
```

### 3. Optional Properties (For Partial Sets)

```typescript
// When you know possible keys but not all will be present
interface Row {
  a: number;
  b?: number;
  c?: number;
  d?: number;
}
```

### 4. Union Types (For Precise Combinations)

```typescript
// When specific combinations are valid
type Row =
  | { a: number }
  | { a: number; b: number }
  | { a: number; b: number; c: number };
```

### 5. Map (For Truly Dynamic Keys)

```typescript
// When keys are genuinely unknown at compile time
function parseCSV(input: string): Map<string, string>[] {
  const lines = input.split('\n');
  const [headerLine, ...rows] = lines;
  const headers = headerLine.split(',');
  
  return rows.map(rowStr => {
    const row = new Map<string, string>();
    rowStr.split(',').forEach((cell, i) => {
      row.set(headers[i], cell);
    });
    return row;
  });
}

const rockets = parseCSV(csvData);
const thrust = rockets[0].get('thrust_kN');
//    ^? const thrust: string | undefined  (safer!)
```

## When Index Signatures ARE Appropriate

### Allowing Additional Properties

```typescript
interface ButtonProps {
  title: string;
  onClick: () => void;
  [otherProps: string]: unknown;  // Allow any extra props
}

renderButton({
  title: 'Click me',
  onClick: () => {},
  theme: 'dark',  // OK now
  'data-testid': 'submit-btn',  // OK
});
```

### Template Literal Constraints

```typescript
// Only allow keys starting with 'data-'
interface DataProps {
  [key: `data-${string}`]: string;
}

const props: DataProps = {
  'data-testid': 'my-button',
  'data-value': '42',
  // 'theme': 'dark',  // Error! Key must start with 'data-'
};
```

## Map vs Object with Index Signature

| Feature | Map | Index Signature |
|---------|-----|-----------------|
| .get() returns | `T \| undefined` | `T` (unsafe) |
| Prototype issues | No | Yes |
| Iteration order | Guaranteed | Not guaranteed |
| Any key type | Yes | String/number/symbol only |
| TypeScript support | Good | Better autocomplete |

```typescript
// Map is safer for dynamic data
const scores = new Map<string, number>();
const score = scores.get('alice');
//    ^? const score: number | undefined

// Index signature pretends value always exists
const scoreObj: { [name: string]: number } = {};
const score2 = scoreObj['alice'];
//    ^? const score2: number  (but it's actually undefined!)
```

## Converting Dynamic Data to Types

```typescript
// Parse dynamic data, validate, return typed object
function parseRocket(map: Map<string, string>): Rocket {
  const name = map.get('name');
  const variant = map.get('variant');
  const thrust_kN = Number(map.get('thrust_kN'));
  
  if (!name || !variant || isNaN(thrust_kN)) {
    throw new Error(`Invalid rocket: ${JSON.stringify([...map])}`);
  }
  
  return { name, variant, thrust_kN };
}

// Now you have type safety
const rockets = parseCSV(csvData).map(parseRocket);
//    ^? const rockets: Rocket[]
```

## Pressure Resistance Protocol

### 1. "I Don't Know All the Keys"

**Pressure:** "The keys come from user input/API"

**Response:** Use Map for truly dynamic data, then validate into a typed interface.

**Action:** `Map<string, string>` for input, then parse to interface.

### 2. "Index Signatures Are Simpler"

**Pressure:** "Just use `{[k: string]: any}` and move on"

**Response:** You lose all type safety and autocomplete.

**Action:** Define the actual structure, even if it takes more code.

## Red Flags - STOP and Reconsider

- Index signature with known property names
- `[key: string]: any` anywhere
- Missing autocomplete when typing property names
- Typos in property names not caught by TypeScript

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "Keys are dynamic" | Often they're actually known at compile time |
| "Too many properties to list" | Record or mapped types handle this |
| "It's just config" | Config has a schema; define it |

## Quick Reference

```typescript
// DON'T: Index signature for known keys
type Bad = { [key: string]: string };

// DO: Interface for known keys
interface Good { name: string; value: string; }

// DO: Record for union of keys
type Colors = Record<'red' | 'green' | 'blue', number>;

// DO: Map for truly dynamic keys
const data = new Map<string, unknown>();

// DO: Index signature only for extra properties
interface Props {
  required: string;
  [extra: string]: unknown;
}
```

## The Bottom Line

**Index signatures sacrifice precision for flexibility you usually don't need.**

If you know the property names, use an interface. If you have a known set of keys, use Record. If keys are truly dynamic, use Map. Reserve index signatures for cases where you explicitly want to allow additional properties.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 16: Prefer More Precise Alternatives to Index Signatures.
