---
name: dry-types
description: Use when duplicating type definitions. Use when interfaces share common fields. Use when types can be derived from other types.
---

# Use Type Operations and Generic Types to Avoid Repeating Yourself

## Overview

**Apply DRY (Don't Repeat Yourself) to types, not just code.**

Type duplication causes the same problems as code duplication: inconsistency, maintenance burden, and bugs. Use TypeScript's type operations to derive types from other types.

## When to Use This Skill

- Copying fields between interfaces
- Multiple types share common properties
- Want one type to be a subset of another
- Types should stay in sync automatically
- Need to create optional/partial versions of types

## The Iron Rule

```
NEVER copy-paste type definitions. Derive types from a single source of truth.
```

**Remember:**
- `extends` for adding fields
- `Pick<T, K>` for selecting fields
- `Partial<T>` for making fields optional
- `keyof` for getting key types
- `typeof` for deriving types from values

## Detection: The Copied Type Problem

If you see similar types diverging:

```typescript
// ❌ Duplicated type definitions
interface Person {
  firstName: string;
  lastName: string;
}

interface PersonWithBirthDate {
  firstName: string;   // Duplicated!
  lastName: string;    // Duplicated!
  birth: Date;
}
```

What if you add `middleName` to Person? Now they're out of sync.

## Basic Techniques

### Use `extends` to Add Fields

```typescript
// ✅ Derive from base type
interface Person {
  firstName: string;
  lastName: string;
}

interface PersonWithBirthDate extends Person {
  birth: Date;
}
```

### Use `Pick` to Select Fields

```typescript
interface State {
  userId: string;
  pageTitle: string;
  recentFiles: string[];
  pageContents: string;
}

// ✅ Select only the fields you need
type TopNavState = Pick<State, 'userId' | 'pageTitle' | 'recentFiles'>;
```

### Use `Partial` for Optional Versions

```typescript
interface Options {
  width: number;
  height: number;
  color: string;
}

class UIWidget {
  constructor(init: Options) { /* ... */ }
  
  // ✅ All fields optional for updates
  update(options: Partial<Options>) { /* ... */ }
}
```

### Use `keyof` for Key Types

```typescript
type OptionsKeys = keyof Options;
//   ^? type OptionsKeys = "width" | "height" | "color"
```

### Use `typeof` to Derive from Values

```typescript
const DEFAULTS = {
  width: 640,
  height: 480,
  color: '#00FF00',
};

// ✅ Type derived from value
type Options = typeof DEFAULTS;
//   ^? type Options = { width: number; height: number; color: string; }
```

## Standard Library Utility Types

| Utility | Purpose | Example |
|---------|---------|---------|
| `Pick<T, K>` | Select properties | `Pick<User, 'id' \| 'name'>` |
| `Omit<T, K>` | Remove properties | `Omit<User, 'password'>` |
| `Partial<T>` | Make all optional | `Partial<Config>` |
| `Required<T>` | Make all required | `Required<PartialConfig>` |
| `Readonly<T>` | Make all readonly | `Readonly<State>` |
| `ReturnType<F>` | Function return type | `ReturnType<typeof fn>` |
| `Parameters<F>` | Function params | `Parameters<typeof fn>` |

## Advanced Patterns

### Mapped Types

```typescript
// Create optional version manually
type OptionsUpdate = {
  [K in keyof Options]?: Options[K]
};

// Equivalent to Partial<Options>
```

### Indexing into Union Types

```typescript
interface SaveAction { type: 'save'; /* ... */ }
interface LoadAction { type: 'load'; /* ... */ }
type Action = SaveAction | LoadAction;

// ✅ Extract discriminant type
type ActionType = Action['type'];
//   ^? type ActionType = "save" | "load"
```

### ReturnType for Function Results

```typescript
function getUserInfo(userId: string) {
  return {
    userId,
    name,
    age,
    // ... many fields
  };
}

// ✅ Derive type from function
type UserInfo = ReturnType<typeof getUserInfo>;
```

### Key Remapping with `as`

```typescript
interface ShortToLong {
  q: 'search';
  n: 'numberOfResults';
}

// Invert the mapping
type LongToShort = {
  [K in keyof ShortToLong as ShortToLong[K]]: K
};
//   ^? type LongToShort = { search: "q"; numberOfResults: "n"; }
```

## Homomorphic Mapped Types

Mapped types preserve modifiers when using `keyof`:

```typescript
interface Customer {
  /** How the customer would like to be addressed. */
  title?: string;
  /** Complete name as entered in the system. */
  readonly name: string;
}

// ✅ Preserves optional and readonly
type PickTitle = Pick<Customer, 'title'>;
//   ^? type PickTitle = { title?: string; }

type PickName = Pick<Customer, 'name'>;
//   ^? type PickName = { readonly name: string; }
```

## When NOT to Apply DRY

Don't factor out types that are only coincidentally similar:

```typescript
// ❌ Don't do this - coincidental similarity
interface NamedAndIdentified {
  id: number;
  name: string;
}

interface Product extends NamedAndIdentified {
  priceDollars: number;
}

interface Customer extends NamedAndIdentified {
  address: string;
}
```

**Why not?** Product.id and Customer.id are semantically different:
- Customer.id might become a UUID
- Product.name and Customer.name might evolve differently

**Rule of thumb:** If you can't name it meaningfully, it's probably premature abstraction.

## Common Patterns

### Base + Extensions

```typescript
// Shared base
interface Vertebrate {
  weightGrams: number;
  color: string;
  isNocturnal: boolean;
}

// Specific extensions
interface Bird extends Vertebrate {
  wingspanCm: number;
}

interface Mammal extends Vertebrate {
  eatsGardenPlants: boolean;
}
```

### Input/Output Types

```typescript
// Full type
interface User {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
}

// Input type derived
type CreateUserInput = Pick<User, 'email' | 'name'>;

// Or with Omit
type UpdateUserInput = Partial<Omit<User, 'id' | 'createdAt'>>;
```

### Function Signatures

```typescript
// ✅ Factor out common signatures
type HTTPFunction = (url: string, opts: Options) => Promise<Response>;

const get: HTTPFunction = (url, opts) => { /* ... */ };
const post: HTTPFunction = (url, opts) => { /* ... */ };
```

## Pressure Resistance Protocol

### 1. "Copy-Paste Is Faster"

**Pressure:** "Just duplicate the type, it's quicker"

**Response:** Technical debt accumulates. Types will drift apart.

**Action:** Take the time to use `extends`, `Pick`, or other derivations.

### 2. "The Types Are Different Enough"

**Pressure:** "They share fields by coincidence"

**Response:** Good point - verify they're semantically the same first.

**Action:** Only factor out types that represent the same concept.

## Red Flags - STOP and Reconsider

- Copy-pasting interface fields
- Multiple types with identical property subsets
- Updating one type but forgetting another
- Types named "...WithX" that duplicate base type

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's just a few fields" | A few fields × many types = maintenance nightmare |
| "I'll remember to update both" | You won't, or your teammates won't |
| "The derivation is confusing" | Less confusing than debugging drift |

## Quick Reference

```typescript
// Adding fields
interface Extended extends Base { newField: T; }

// Selecting fields
type Subset = Pick<Full, 'a' | 'b'>;

// Removing fields  
type WithoutPassword = Omit<User, 'password'>;

// Making optional
type Updates = Partial<Options>;

// Getting return type
type Result = ReturnType<typeof myFunction>;

// Getting key union
type Keys = keyof MyInterface;
```

## The Bottom Line

**Derive types from a single source of truth.**

Use TypeScript's type operations (`extends`, `Pick`, `Partial`, `keyof`, `typeof`, mapped types) to express relationships between types. This keeps types in sync and reduces maintenance burden. But only apply DRY when types are semantically related, not just structurally similar.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 15: Use Type Operations and Generic Types to Avoid Repeating Yourself.
