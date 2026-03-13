---
name: limit-optional-properties
description: Use when adding optional properties. Use when types have many optional fields. Use when considering required vs optional.
---

# Limit the Use of Optional Properties

## Overview

**Optional properties are convenient but costly.**

Every optional property creates uncertainty. Readers must check if it exists. Code paths multiply. Consider whether required properties or separate types are better.

## When to Use This Skill

- Adding new properties to existing types
- Designing interfaces with optional fields
- Migrating types from JavaScript
- Choosing between optional and required

## The Iron Rule

```
Required properties are simpler to work with.
Use optional properties only when absence is meaningful.
```

**Remember:**
- Optional = uncertainty in every usage
- Type narrowing is required for optional properties
- Multiple optionals = exponential complexity
- Consider: is absence a valid state?

## Detection: Optional Overload

```typescript
interface FormattedValue {
  value: number;
  units: string;
  unitSystem?: 'metric' | 'imperial';  // New optional property
}

function formatValue(val: FormattedValue): string {
  // Now EVERY usage must consider: is unitSystem set?
  if (val.unitSystem === 'metric') {
    // ...
  } else if (val.unitSystem === 'imperial') {
    // ...
  } else {
    // undefined case - what does it mean?
  }
}
```

## Combinatorial Explosion

With n optional properties, there are 2^n possible states:

```typescript
interface Config {
  host?: string;      // 2 states
  port?: number;      // x2 = 4 states
  timeout?: number;   // x2 = 8 states
  retries?: number;   // x2 = 16 states
}
```

Many combinations may be invalid!

## Alternative 1: Required with Defaults

```typescript
// Instead of optional properties
interface Config {
  host: string;
  port: number;
  timeout: number;
}

// Provide defaults at construction
function createConfig(overrides: Partial<Config>): Config {
  return {
    host: 'localhost',
    port: 8080,
    timeout: 5000,
    ...overrides
  };
}
```

Now Config always has all properties. Simpler to use!

## Alternative 2: Separate Types

```typescript
// Instead of one type with optionals
interface BasicFormattedValue {
  value: number;
  units: string;
}

interface LocalizedFormattedValue {
  value: number;
  units: string;
  unitSystem: 'metric' | 'imperial';
}

type FormattedValue = BasicFormattedValue | LocalizedFormattedValue;
```

Now the relationship between properties is explicit.

## Alternative 3: Tagged Union

```typescript
type FormattedValue = 
  | { type: 'basic'; value: number; units: string }
  | { type: 'localized'; value: number; units: string; unitSystem: 'metric' | 'imperial' };

function format(val: FormattedValue): string {
  switch (val.type) {
    case 'basic':
      return `${val.value} ${val.units}`;
    case 'localized':
      // val.unitSystem is guaranteed to exist here
      return formatLocalized(val);
  }
}
```

## When Optional IS Appropriate

### Truly Independent Options

```typescript
interface RequestOptions {
  timeout?: number;   // Default behavior is fine
  headers?: Headers;  // No headers is valid
  cache?: boolean;    // Default is acceptable
}
```

These options are independently meaningful and have sensible defaults.

### Backward Compatibility

```typescript
// v1
interface User {
  name: string;
}

// v2 - adding optional to avoid breaking changes
interface User {
  name: string;
  email?: string;  // Old code still works
}
```

But consider: should you version the type instead?

## Group Related Optionals

If properties are related, group them:

```typescript
// Bad: related properties are separately optional
interface Person {
  name: string;
  birthPlace?: string;  // If one is set...
  birthDate?: Date;     // ...the other probably should be too
}

// Good: grouped together
interface Person {
  name: string;
  birth?: {
    place: string;
    date: Date;
  };
}
```

Now both are present or neither is. See Item 33.

## Avoid "God Object" Interfaces

```typescript
// Bad: too many optionals
interface UserProfile {
  id: string;
  name?: string;
  email?: string;
  avatar?: string;
  preferences?: Preferences;
  settings?: Settings;
  lastLogin?: Date;
  // ... 20 more optional fields
}

// Better: compose specific types
interface User {
  id: string;
  name: string;
}

interface UserWithProfile extends User {
  email: string;
  avatar: string;
}

interface UserWithPreferences extends User {
  preferences: Preferences;
}
```

## Pressure Resistance Protocol

### 1. "Optional is Easier"

**Pressure:** "Just make it optional, then we don't have to change existing code"

**Response:** You're trading short-term convenience for long-term complexity.

**Action:** Evaluate: is absence meaningful, or just convenient?

### 2. "It Might Not Always Be Present"

**Pressure:** "The data isn't always available"

**Response:** Model that explicitly with a union type or separate interface.

**Action:** Make the state explicit, not implicit via optionality.

## Red Flags - STOP and Reconsider

- More than 3-4 optional properties on an interface
- Optional properties that must be checked together
- Comments explaining "if X is set, then Y must be too"
- `?.` chains accessing optional properties repeatedly

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's backward compatible" | Create a new type version instead |
| "Not all users need it" | Different users = different types |
| "It's just one more optional" | Each one doubles complexity |

## Quick Reference

```typescript
// DON'T: Many independent optionals
interface Bad {
  a?: number;
  b?: string;
  c?: boolean;
  d?: Date;
}

// DO: Required with defaults
interface Good {
  a: number;
  b: string;
}
const good: Good = { a: 1, b: '', ...overrides };

// DO: Group related properties
interface Person {
  name: string;
  contact?: { email: string; phone: string };
}

// DO: Use union for different shapes
type Value = SimpleValue | DetailedValue;
```

## The Bottom Line

**Optional properties create hidden complexity.**

Each optional property doubles the number of possible states. Prefer required properties with defaults, grouped optional objects, or explicit union types. Use optional properties only when absence is a meaningful, independent state.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 37: Limit the Use of Optional Properties.
