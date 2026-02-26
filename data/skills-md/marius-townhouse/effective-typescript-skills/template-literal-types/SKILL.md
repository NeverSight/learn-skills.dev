---
name: template-literal-types
description: Use when modeling structured string patterns. Use when parsing DSLs like CSS selectors. Use when transforming string types. Use when validating string formats. Use when combining with mapped types.
---

# Use Template Literal Types to Model DSLs and String Relationships

## Overview

Template literal types bring the power of JavaScript template literals to TypeScript's type system. They allow you to model structured subsets of strings, parse domain-specific languages (DSLs), and capture relationships between string types. Combined with conditional types and the `infer` keyword, they enable sophisticated string manipulation at the type level.

This skill is essential for bringing type safety to string-heavy APIs and for building powerful type transformations.

## When to Use This Skill

- Modeling structured string patterns (IDs, paths, URLs)
- Parsing domain-specific languages (CSS selectors, query languages)
- Transforming string types (camelCase, snake_case conversion)
- Validating string formats at compile time
- Combining with mapped types for key transformations

## The Iron Rule

**Use template literal types to model structured string subsets and DSLs. Combine with `infer` for parsing and mapped types for transformations.**

## Detection

Watch for these opportunities:

```typescript
// RED FLAGS - Untyped strings that could be precise
type EventType = string;  // Could be 'click' | 'hover' | etc.
function query(selector: string): Element;  // Could parse CSS selectors
type CSSProperty = string;  // Could validate property names
```

## Basic Template Literal Types

```typescript
// Match strings starting with a prefix
type PseudoString = `pseudo${string}`;
const science: PseudoString = 'pseudoscience';  // OK
const alias: PseudoString = 'pseudonym';        // OK
const physics: PseudoString = 'physics';        // Error!

// Match specific patterns
type DataAttribute = `data-${string}`;
type HTTPSUrl = `https://${string}`;
type VersionString = `v${number}.${number}.${number}`;
```

## Index Signatures with Template Literals

```typescript
// Allow data-* attributes while keeping type safety
interface Checkbox {
  id: string;
  checked: boolean;
  [key: `data-${string}`]: unknown;
}

const check: Checkbox = {
  id: 'subscribe',
  checked: true,
  'data-listIds': 'all-the-lists',  // OK
  value: 'yes',  // Error: not data-* and not known property
};
```

## Parsing with `infer`

Extract parts of strings using conditional types with `infer`:

```typescript
// Extract event name from handler type
type EventName<T> = T extends `on${infer Name}` ? Name : never;

type ClickEvent = EventName<'onClick'>;      // 'Click'
type HoverEvent = EventName<'onMouseEnter'>; // 'MouseEnter'
type BadEvent = EventName<'handleClick'>;   // never

// Extract path parameters
type PathParams<T> = T extends `/users/${infer UserId}/posts/${infer PostId}`
  ? { userId: UserId; postId: PostId }
  : never;

type Params = PathParams<'/users/123/posts/456'>;
// { userId: '123'; postId: '456' }
```

## String Transformations

Build recursive types to transform strings:

```typescript
// Convert snake_case to camelCase
type CamelCase<S extends string> =
  S extends `${infer Head}_${infer Tail}`
    ? `${Head}${Capitalize<CamelCase<Tail>>}`
    : S;

type T1 = CamelCase<'foo'>;           // 'foo'
type T2 = CamelCase<'foo_bar'>;      // 'fooBar'
type T3 = CamelCase<'foo_bar_baz'>;  // 'fooBarBaz'

// Apply to object keys
type CamelCaseKeys<T> = {
  [K in keyof T as CamelCase<K & string>]: T[K]
};

type SnakeCase = { user_name: string; email_address: string };
type Camel = CamelCaseKeys<SnakeCase>;
// { userName: string; emailAddress: string }
```

## Real-World Example: CSS Selectors

```typescript
// Enhance querySelector with precise types
type HTMLTag = keyof HTMLElementTagNameMap;

declare global {
  interface ParentNode {
    // Simple tag selector
    querySelector<TagName extends HTMLTag>(
      selector: TagName
    ): HTMLElementTagNameMap[TagName] | null;
    
    // Tag#id selector
    querySelector<TagName extends HTMLTag>(
      selector: `${TagName}#${string}`
    ): HTMLElementTagNameMap[TagName] | null;
  }
}

// Usage
const img = document.querySelector('img#hero');
// Type: HTMLImageElement | null
// Can access img?.src, img?.alt, etc.

const div = document.querySelector('div#container');
// Type: HTMLDivElement | null
```

## Combining with Mapped Types

```typescript
// Create event handler types from event names
type EventMap = {
  click: MouseEvent;
  keydown: KeyboardEvent;
  submit: SubmitEvent;
};

type EventHandlers<Events extends Record<string, Event>> = {
  [K in keyof Events as `on${Capitalize<K & string>}`]?: 
    (event: Events[K]) => void;
};

type Handlers = EventHandlers<EventMap>;
// {
//   onClick?: (event: MouseEvent) => void;
//   onKeydown?: (event: KeyboardEvent) => void;
//   onSubmit?: (event: SubmitEvent) => void;
// }
```

## Pressure Resistance Protocol

When pressured to use simple `string` types:

1. **Identify patterns**: What structure do the strings have?
2. **Start simple**: Use unions of literal types first
3. **Add templates**: Use template literals for infinite but structured sets
4. **Consider parsing**: Use `infer` to extract information
5. **Test edge cases**: Ensure your types are accurate, not just precise

## Red Flags

| Anti-Pattern | Why It's Bad |
|--------------|--------------|
| `type ID = string` | Misses validation opportunity |
| Complex template types without testing | May be inaccurate |
| Parsing without escape hatches | Complex selectors need fallback |
| Overly precise types | Can break legitimate use cases |

## Common Rationalizations

### "String is good enough"

**Reality**: Template literals catch typos and invalid formats at compile time. `'user-123'` vs `'users-123'` can be caught immediately.

### "This is too complex"

**Reality**: Start simple with prefix patterns, then add complexity as needed. Even basic template literals provide value.

### "It will hurt performance"

**Reality**: Template literal types are evaluated at compile time. They have no runtime cost.

## Quick Reference

| Pattern | Syntax | Use Case |
|---------|--------|----------|
| Prefix | `` `data-${string}` `` | data attributes |
| Suffix | `` `${string}Event` `` | event names |
| Middle | `` `${string}.${string}` `` | file extensions |
| Extract | `` `on${infer Name}` `` | parsing |
| Transform | `` `${Head}${Capitalize<Tail>}` `` | camelCase |

## The Bottom Line

Template literal types bring type safety to string-heavy code. Use them to model structured strings, parse DSLs, and transform types. Combined with `infer` and mapped types, they enable powerful type-level string manipulation.

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 54: Use Template Literal Types to Model DSLs and Relationships Between Strings
