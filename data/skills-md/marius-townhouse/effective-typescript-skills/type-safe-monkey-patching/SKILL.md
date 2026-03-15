---
name: type-safe-monkey-patching
description: Use when adding properties to window, document, or DOM elements. Use when extending built-in objects at runtime. Use when working with jQuery or D3 globals. Use when migrating JavaScript that uses global variables.
---

# Type-Safe Approaches to Monkey Patching

## Overview

Monkey patching - adding properties to built-in objects at runtime - is a JavaScript pattern that becomes problematic in TypeScript. TypeScript doesn't know about properties you've added to `window`, `document`, or DOM elements, leading to type errors. While `as any` is the quick fix, it sacrifices type safety entirely. There are better approaches that maintain type checking while modeling your runtime modifications.

## When to Use This Skill

- Adding global variables to `window` or `document`
- Attaching data to DOM elements
- Working with libraries that require global state (jQuery, D3)
- Migrating JavaScript code that uses monkey patching
- Storing application state on global objects

## The Iron Rule

**Never use `(obj as any).property` for monkey patching. Use interface augmentation or narrower type assertions that preserve type safety.**

## Detection

Watch for these patterns:

```typescript
// RED FLAGS - Untyped monkey patching
(window as any).myApp = { /* ... */ };
(document as any).user = currentUser;
(element as any).customData = data;

// These lose all type safety
(window as any).usr = user;  // Typo not caught
(window as any).user = /regex/;  // Wrong type not caught
```

## Type-Safe Approaches

### Approach 1: Interface Augmentation (Global)

Best when the property is truly global and always available:

```typescript
// types/global.d.ts
interface User {
  name: string;
  id: number;
}

declare global {
  interface Window {
    /** The currently logged-in user */
    user: User;
  }
}

// Usage - fully type-safe
window.user = { name: "Alice", id: 1 };  // OK
window.user = { name: "Alice" };  // Error: missing 'id'
window.usr = user;  // Error: typo caught
console.log(window.user.name);  // Autocomplete works
```

### Approach 2: Augmentation with undefined (Safer)

When the global might not be set:

```typescript
declare global {
  interface Window {
    /** The currently logged-in user - may not be set */
    user: User | undefined;
  }
}

// Forces handling of undefined
function greetUser() {
  if (window.user) {
    alert(`Hello ${window.user.name}!`);  // OK after check
  }
}

// Or use optional chaining
alert(`Hello ${window.user?.name ?? 'Guest'}!`);
```

### Approach 3: Custom Type Assertion (Scoped)

When you don't want to pollute the global Window type:

```typescript
type MyWindow = typeof window & {
  /** The currently logged-in user */
  user: User | undefined;
};

// Assignment
(window as MyWindow).user = currentUser;

// Access
const user = (window as MyWindow).user;
if (user) {
  console.log(user.name);
}
```

### Approach 4: DOM Element Data (Type-Safe)

For attaching data to DOM elements:

```typescript
// Define extended element type
interface ExtendedElement extends HTMLElement {
  customData?: {
    initialized: boolean;
    value: number;
  };
}

// Use with type assertion
const el = document.getElementById('myElement') as ExtendedElement;
el.customData = { initialized: true, value: 42 };

// Better: Use data attributes or WeakMap
const elementData = new WeakMap<HTMLElement, { initialized: boolean; value: number }>();
elementData.set(el, { initialized: true, value: 42 });
```

## Pressure Resistance Protocol

When pressured to use `as any` for quick monkey patching:

1. **Evaluate need**: Is monkey patching truly necessary, or can you restructure?
2. **Choose approach**: Interface augmentation for global, custom type for scoped
3. **Add undefined**: Unless you're certain the value is always present
4. **Document**: Add JSDoc comments explaining the monkey patch
5. **Consider alternatives**: Can you use a module-level variable instead?

## Red Flags

| Anti-Pattern | Why It's Bad |
|--------------|--------------|
| `(window as any).prop` | No type safety, typos not caught |
| `(document as any).data` | Wrong types not caught |
| Global augmentation for page-specific data | Lies about availability |
| Missing `undefined` in augmentation | Hides race conditions |

## Common Rationalizations

### "It's just one property"

**Reality**: Every `as any` is a potential runtime error. One property today becomes twenty tomorrow, all unchecked.

### "I'll be careful"

**Reality**: Your colleagues won't know about the property. They'll misspell it. Type-safe augmentation documents and enforces the contract.

### "Augmentation is too much boilerplate"

**Reality**: A three-line interface declaration saves hours of debugging typos and wrong types.

### "It's legacy code, we'll fix it later"

**Reality**: Interface augmentation takes the same time as `as any` but gives you safety immediately.

## Better Alternatives to Monkey Patching

Consider these before monkey patching:

```typescript
// 1. Module-level state
let currentUser: User | undefined;
export function setUser(user: User) { currentUser = user; }
export function getUser() { return currentUser; }

// 2. Context/dependency injection
class AppContext {
  user: User | undefined;
}
const context = new AppContext();

// 3. React Context, Vue provide/inject, etc.
const UserContext = createContext<User | undefined>(undefined);

// 4. WeakMap for DOM data
const elementState = new WeakMap<Element, ElementState>();
```

## Quick Reference

| Scenario | Recommended Approach |
|----------|---------------------|
| Global always available | Interface augmentation |
| Global sometimes available | Augmentation with `\| undefined` |
| Page-specific global | Custom type assertion |
| DOM element data | WeakMap or data attributes |
| Library requires global | Interface augmentation + documentation |

## The Bottom Line

Monkey patching in JavaScript requires explicit typing in TypeScript. Use interface augmentation for global properties and custom type assertions for scoped modifications. Never use `as any` - it defeats the purpose of TypeScript. Always consider whether monkey patching is truly necessary; often there's a cleaner architectural solution.

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 47: Prefer Type-Safe Approaches to Monkey Patching
