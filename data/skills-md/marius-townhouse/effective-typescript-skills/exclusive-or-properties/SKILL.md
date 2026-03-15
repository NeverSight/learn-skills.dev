---
name: exclusive-or-properties
description: Use when exactly one of several properties should be present. Use when modeling mutually exclusive options. Use when building component props with alternative configurations. Use when designing API parameters that have variants.
---

# Use Optional Never Properties to Model Exclusive Or

## Overview

Sometimes you need a type where exactly one of several properties must be present, but not more than one. This "exclusive or" (XOR) pattern is common in component props, API parameters, and configuration objects. Using optional properties with `never` types enforces this constraint at compile time.

This technique provides better type safety than unions of objects and clearer intent than runtime checks.

## When to Use This Skill

- Exactly one of several properties must be present
- Modeling mutually exclusive configuration options
- Component props with alternative configurations
- API parameters that have exclusive variants
- Preventing invalid combinations of properties

## The Iron Rule

**Use optional `never` properties to enforce "exactly one of" constraints. Each variant makes its property required and others `never`.**

## Detection

Watch for these invalid combinations:

```typescript
// RED FLAGS - Invalid combinations allowed
interface Config {
  url?: string;
  filePath?: string;
  content?: string;
}
// Can pass none, one, or all - too permissive!

// Runtime validation needed:
if ((config.url ? 1 : 0) + (config.filePath ? 1 : 0) + (config.content ? 1 : 0) !== 1) {
  throw new Error('Exactly one source required');
}
```

## The Problem

```typescript
interface LoadConfig {
  url?: string;      // Load from URL
  filePath?: string; // Load from file
  content?: string;  // Load from string
}

// All these are allowed, but shouldn't be:
const bad1: LoadConfig = {};  // No source specified
const bad2: LoadConfig = { url: '...', filePath: '...' };  // Two sources
const bad3: LoadConfig = { url: '...', filePath: '...', content: '...' };  // All three

// Runtime check required
function load(config: LoadConfig) {
  const sources = [config.url, config.filePath, config.content].filter(Boolean);
  if (sources.length !== 1) {
    throw new Error('Exactly one source required');
  }
  // ...
}
```

## The Solution: Optional Never Properties

```typescript
type LoadConfig =
  | { url: string; filePath?: never; content?: never }
  | { url?: never; filePath: string; content?: never }
  | { url?: never; filePath?: never; content: string };

// Valid - exactly one source:
const good1: LoadConfig = { url: 'https://example.com' };
const good2: LoadConfig = { filePath: '/path/to/file' };
const good3: LoadConfig = { content: 'raw content' };

// Invalid - caught at compile time:
const bad1: LoadConfig = {};  // Error: missing required property
const bad2: LoadConfig = { url: '...', filePath: '...' };  // Error: filePath must be undefined
const bad3: LoadConfig = { url: '...', content: '...' };   // Error: content must be undefined
```

## Component Props Example

```typescript
type ButtonProps = {
  label: string;
  onClick: () => void;
} & (
  | { href: string; to?: never; onPress?: never }      // External link
  | { href?: never; to: string; onPress?: never }     // Router link
  | { href?: never; to?: never; onPress: () => void } // Custom action
);

// Usage
<Button label="External" href="https://example.com" />
<Button label="Internal" to="/dashboard" />
<Button label="Action" onPress={handlePress} />

// Error: can't combine variants
<Button label="Bad" href="..." to="..." />  // Error!
```

## API Parameters Example

```typescript
type SearchParams = {
  limit?: number;
  offset?: number;
} & (
  | { query: string; filters?: never }
  | { query?: never; filters: Filter[] }
);

// Valid
search({ query: 'typescript' });
search({ filters: [{ field: 'status', value: 'active' }] });
search({ query: 'typescript', limit: 10 });

// Invalid
search({});  // Error: need query or filters
search({ query: '...', filters: [...] });  // Error: can't have both
```

## Generic XOR Helper

```typescript
type XOR<A, B> =
  | (A & { [K in keyof B]?: never })
  | (B & { [K in keyof A]?: never });

// Usage
type Config = XOR<
  { url: string },
  XOR<
    { filePath: string },
    { content: string }
  >
>;

// Or for exactly one of many:
type ExactlyOne<T> = {
  [K in keyof T]: { [P in K]: T[K] } & {
    [P in Exclude<keyof T, K>]?: never;
  };
}[keyof T];

type LoadConfig2 = ExactlyOne<{
  url: string;
  filePath: string;
  content: string;
}>;
```

## Pressure Resistance Protocol

When enforcing exclusive properties:

1. **Identify exclusivity**: Which properties are mutually exclusive?
2. **Create variants**: Each variant has one required, others `never`
3. **Union the variants**: Combine with `|` operator
4. **Test combinations**: Ensure invalid combos fail
5. **Document the pattern**: Explain why certain combos are invalid

## Red Flags

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| All optional properties | Allows none or many | Optional never pattern |
| Runtime validation only | Errors at runtime, not compile time | Type-level enforcement |
| Comments saying "use only one" | Not enforced | Make it a type error |

## Common Rationalizations

### "I'll validate at runtime"

**Reality**: Runtime validation catches bugs later. Type-level enforcement catches them immediately.

### "This is too verbose"

**Reality**: Use helper types like `XOR` or `ExactlyOne` to reduce repetition.

### "Users might want multiple options"

**Reality**: If that's valid, don't use XOR. If it's not, enforce it at the type level.

## Quick Reference

| Pattern | Syntax | Meaning |
|---------|--------|---------|
| XOR (2 props) | `{ a: T, b?: never } \| { a?: never, b: T }` | Exactly one |
| XOR (3+ props) | Union of variants | Exactly one |
| Helper type | `XOR<A, B>` | Reusable pattern |

## The Bottom Line

Use optional `never` properties to enforce "exactly one of" constraints at compile time. This eliminates an entire class of runtime errors and makes invalid states unrepresentable.

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 63: Use Optional Never Properties to Model Exclusive Or
