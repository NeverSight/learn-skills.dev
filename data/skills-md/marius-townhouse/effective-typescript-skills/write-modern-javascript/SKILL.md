---
name: write-modern-javascript
description: Use when writing TypeScript that compiles to JavaScript. Use when configuring tsconfig target. Use when choosing language features. Use when supporting older browsers. Use when optimizing bundle size.
---

# Write Modern JavaScript

## Overview

TypeScript compiles to JavaScript, and the quality of that output depends on your target configuration and coding style. Write modern JavaScript (ES2020+) and let TypeScript handle compatibility through downleveling. Modern features often produce cleaner, more efficient code than manually implementing fallbacks.

Avoid TypeScript features that compile to verbose JavaScript when standard modern features exist.

## When to Use This Skill

- Writing TypeScript that compiles to JavaScript
- Configuring tsconfig.json target
- Choosing which language features to use
- Supporting older browsers through compilation
- Optimizing bundle size

## The Iron Rule

**Write modern JavaScript (ES2020+) and let TypeScript downlevel for older environments. Prefer standard features over TypeScript-specific ones that compile to verbose code.**

## Detection

Watch for outdated patterns:

```typescript
// RED FLAGS - Outdated patterns
var x = 1;                    // Use const/let
function Person() { }         // Use class
Promise.resolve().then(...);  // Use async/await
Object.assign({}, obj);       // Use spread: { ...obj }
```

## Modern Features to Prefer

```typescript
// Use const/let instead of var
const PI = 3.14159;
let count = 0;

// Use arrow functions for callbacks
const doubled = numbers.map(n => n * 2);

// Use destructuring
const { name, age } = person;
const [first, ...rest] = items;

// Use spread instead of Object.assign
const merged = { ...defaults, ...options };
const combined = [...arr1, ...arr2];

// Use async/await instead of Promise chains
async function fetchData() {
  const response = await fetch('/api/data');
  const data = await response.json();
  return data;
}

// Use optional chaining
const street = user?.address?.street;

// Use nullish coalescing
const value = input ?? 'default';
```

## Configure Target Appropriately

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",      // Modern target for modern output
    "lib": ["ES2020", "DOM"], // Include modern APIs
    "module": "ESNext",      // Use ES modules
    "moduleResolution": "node"
  }
}
```

## Let TypeScript Handle Compatibility

```typescript
// Write modern code:
class Person {
  name: string;
  #age: number;  // Private field
  
  constructor(name: string, age: number) {
    this.name = name;
    this.#age = age;
  }
  
  async celebrate() {
    return `${this.name} is ${this.#age}!`;
  }
}

// TypeScript compiles for target: ES2015
// or passes through for target: ES2022
```

## Avoid Verbose TypeScript Patterns

```typescript
// AVOID: TypeScript parameter properties
class Point {
  constructor(public x: number, public y: number) {}
}
// Compiles to verbose code with assignments

// PREFER: Standard class fields (ES2022+)
class Point {
  x: number;
  y: number;
  
  constructor(x: number, y: number) {
    this.x = x;
    this.y = y;
  }
}
// Cleaner output, standard JavaScript
```

## Pressure Resistance Protocol

When writing TypeScript:

1. **Use latest target**: Set target to ES2020 or later
2. **Write modern JS**: Use current JavaScript features
3. **Let TS handle compatibility**: Trust the compiler
4. **Review output**: Check compiled code occasionally
5. **Avoid TS-only features**: Unless necessary

## Red Flags

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| `var` declarations | Outdated, scoping issues | Use `const`/`let` |
| Manual Promise chains | Harder to read | Use async/await |
| `Object.assign` | Verbose | Use spread operator |
| `Array.prototype` methods | Verbose | Use modern array methods |

## Common Rationalizations

### "I need to support old browsers"

**Reality**: Configure target appropriately and let TypeScript downlevel. Don't write outdated code manually.

### "I'm used to the old way"

**Reality**: Modern JavaScript is cleaner and more maintainable. Take time to learn current patterns.

### "It compiles to the same thing"

**Reality**: Often it doesn't. Modern features can produce more efficient code.

## Quick Reference

| Instead Of | Use | Benefit |
|------------|-----|---------|
| `var` | `const`/`let` | Block scope, no hoisting issues |
| `function` callbacks | Arrow functions | Lexical `this`, cleaner |
| `.then()` chains | `async`/`await` | Readable, easier error handling |
| `Object.assign()` | Spread `{...obj}` | Cleaner, standard |
| `arr.indexOf() !== -1` | `arr.includes()` | Clearer intent |
| Manual loops | `map`, `filter`, `reduce` | Declarative, functional |

## The Bottom Line

Write modern JavaScript and let TypeScript handle compatibility. Modern features produce cleaner code and TypeScript's downleveling ensures it works where needed.

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 79: Write Modern JavaScript
