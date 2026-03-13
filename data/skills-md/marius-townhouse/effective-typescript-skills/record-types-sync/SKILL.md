---
name: record-types-sync
description: Use when properties need synchronized configuration. Use when adding new properties requires updates elsewhere. Use when implementing optimization checks. Use when building property validators. Use when maintaining parallel data structures.
---

# Use Record Types to Keep Values in Sync

## Overview

When you have parallel data structures that need to stay synchronized - like a type and a configuration object for that type's properties - use `Record<keyof T, V>` to enforce that every property is accounted for. This technique ensures that when you add a new property to a type, you get a compile error reminding you to update related code.

This pattern is invaluable for optimization checks, property validators, and any code that needs to enumerate or configure all properties of a type.

## When to Use This Skill

- Properties need synchronized configuration
- Adding new properties requires updates elsewhere
- Implementing shouldComponentUpdate-style optimizations
- Building property validators or transformers
- Maintaining parallel data structures

## The Iron Rule

**Use `Record<keyof T, V>` to enforce that all properties of T are accounted for in related configuration objects.**

## Detection

Watch for these maintenance hazards:

```typescript
// RED FLAGS - Manual synchronization
interface Props {
  data: Data;
  onClick: () => void;
}

function shouldUpdate(old: Props, new: Props) {
  // Manual checks - easy to miss new properties
  return old.data !== new.data;  // Forgot onClick!
}

// Comments that won't be read:
// Note: if you add a property here, update shouldUpdate!
```

## The Problem

```typescript
interface ScatterProps {
  xs: number[];
  ys: number[];
  xRange: [number, number];
  yRange: [number, number];
  color: string;
  onClick?: () => void;
}

// "Fail open" - might redraw too often
function shouldUpdate(old: ScatterProps, new: ScatterProps) {
  for (const k in old) {
    if (old[k] !== new[k]) {
      if (k !== 'onClick') return true;  // Forgot new event handlers!
    }
  }
  return false;
}

// "Fail closed" - might miss necessary redraws
function shouldUpdate(old: ScatterProps, new: ScatterProps) {
  return (
    old.xs !== new.xs ||
    old.ys !== new.ys ||
    // Forgot xRange, yRange, color!
    // Also forgot to exclude onClick
  );
}
```

## The Solution: Record Types

```typescript
const REQUIRES_UPDATE: Record<keyof ScatterProps, boolean> = {
  xs: true,
  ys: true,
  xRange: true,
  yRange: true,
  color: true,
  onClick: false,  // false = change doesn't require redraw
};

function shouldUpdate(old: ScatterProps, new: ScatterProps) {
  for (const k in old) {
    const key = k as keyof ScatterProps;
    if (old[key] !== new[key] && REQUIRES_UPDATE[key]) {
      return true;
    }
  }
  return false;
}
```

Now adding a new property forces you to decide:

```typescript
interface ScatterProps {
  // ... existing properties
  onDoubleClick?: () => void;  // New property added
}

// COMPILE ERROR: Property 'onDoubleClick' is missing
const REQUIRES_UPDATE: Record<keyof ScatterProps, boolean> = {
  // ... existing entries
  // Error reminds you to add: onDoubleClick: ???
};
```

## Property Validators

```typescript
interface UserInput {
  name: string;
  email: string;
  age: number;
}

// Enforce that every field has a validator
const validators: Record<keyof UserInput, (value: unknown) => boolean> = {
  name: (v) => typeof v === 'string' && v.length > 0,
  email: (v) => typeof v === 'string' && v.includes('@'),
  age: (v) => typeof v === 'number' && v >= 0 && v < 150,
};

// Adding a field forces adding a validator
```

## Default Values

```typescript
interface Config {
  timeout: number;
  retries: number;
  debug: boolean;
}

// Enforce defaults for all properties
const defaults: Record<keyof Config, Config[keyof Config]> = {
  timeout: 5000,
  retries: 3,
  debug: false,
};

function loadConfig(partial: Partial<Config>): Config {
  return { ...defaults, ...partial };
}
```

## Property Labels

```typescript
interface FormData {
  firstName: string;
  lastName: string;
  email: string;
}

// Enforce labels for all fields
const labels: Record<keyof FormData, string> = {
  firstName: 'First Name',
  lastName: 'Last Name',
  email: 'Email Address',
};

// Use in UI
Object.entries(formData).map(([key, value]) => (
  <label>{labels[key as keyof FormData]}</label>
));
```

## Pressure Resistance Protocol

When maintaining parallel structures:

1. **Identify coupling**: Which structures must stay synchronized?
2. **Use Record<keyof T, V>**: Enforce complete coverage
3. **Choose meaningful value types**: boolean, function, string, etc.
4. **Document the pattern**: Explain why Record is used
5. **Handle optional properties**: Use `keyof Required<T>` if needed

## Red Flags

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Comments saying "update X when Y changes" | Won't be enforced | Record type |
| Manual property enumeration | Easy to miss properties | Record with keyof |
| Optional config entries | Might forget required ones | Make all required |

## Common Rationalizations

### "I'll remember to update it"

**Reality**: You won't. Your coworkers won't. The compiler will enforce it with Record types.

### "It's just a small config"

**Reality**: Small configs grow. Record types scale with zero maintenance burden.

### "Some properties don't need configuration"

**Reality**: Explicitly setting them to null/false/empty is better than forgetting them.

## Quick Reference

| Use Case | Record Type | Example Value |
|----------|-------------|---------------|
| Optimization flags | `Record<keyof T, boolean>` | `true`/`false` |
| Validators | `Record<keyof T, ValidatorFn>` | validation function |
| Defaults | `Record<keyof T, T[keyof T]>` | default value |
| Labels | `Record<keyof T, string>` | display name |
| Transformers | `Record<keyof T, TransformFn>` | transform function |

## The Bottom Line

Use `Record<keyof T, V>` to enforce that parallel data structures stay synchronized with your types. The compiler will remind you to update related code when you add new properties.

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 61: Use Record Types to Keep Values in Sync
