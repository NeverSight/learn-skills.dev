---
name: currying-inference
description: Use when generic types aren't inferred. Use when builder patterns need better types. Use when creating new inference sites.
---

# Use Classes and Currying to Create New Inference Sites

## Overview

**When TypeScript can't infer generic types, create new inference opportunities.**

TypeScript infers generic type parameters at specific "inference sites." When it doesn't have enough information at one site, you can create additional sites using classes, currying, or helper functions.

## When to Use This Skill

- Generic type parameters aren't being inferred
- Builder pattern needs type inference
- Chained methods lose type information
- Creating APIs that guide type inference

## The Iron Rule

```
Create inference sites where TypeScript needs type information.
Classes and curried functions provide natural inference points.
```

**Remember:**
- Inference happens at function calls and class instantiation
- More inference sites = better type inference
- Currying splits inference across multiple calls
- Classes provide inference at construction

## Detection: Missing Inference

```typescript
declare function fetchData<T>(url: string, options: RequestOptions): Promise<T>;

// TypeScript can't infer T
const data = await fetchData('/api/users', { method: 'GET' });
//    ^? unknown

// Must specify explicitly
const data = await fetchData<User[]>('/api/users', { method: 'GET' });
```

The type parameter `T` has no inference site.

## Solution 1: Add Inference Site with Parameter

```typescript
declare function fetchData<T>(
  url: string,
  parser: (raw: unknown) => T
): Promise<T>;

const data = await fetchData('/api/users', (raw) => raw as User[]);
// ^? User[]
```

The `parser` function provides an inference site for `T`.

## Solution 2: Curried Functions

```typescript
// Single function: T not inferred
function makeRequest<T>(url: string): Promise<T>;

// Curried: inference at each call
function makeRequest<T>() {
  return (url: string): Promise<T> => {
    return fetch(url).then(r => r.json());
  };
}

// Usage creates inference site
const getUsers = makeRequest<User[]>();
const users = await getUsers('/api/users');
```

## Solution 3: Builder Pattern with Classes

```typescript
class RequestBuilder<T = unknown> {
  private url: string = '';
  
  setUrl(url: string): this {
    this.url = url;
    return this;
  }
  
  // New method creates new inference site
  withParser<U>(parser: (data: unknown) => U): RequestBuilder<U> {
    return this as unknown as RequestBuilder<U>;
  }
  
  async execute(): Promise<T> {
    const response = await fetch(this.url);
    return response.json();
  }
}

// Type inferred from parser
const users = await new RequestBuilder()
  .setUrl('/api/users')
  .withParser((data): User[] => data as User[])
  .execute();
// ^? User[]
```

## Practical Example: Event Emitter

```typescript
// Without inference sites
class EventEmitter {
  on<T>(event: string, handler: (data: T) => void): void;
  emit<T>(event: string, data: T): void;
}

// TypeScript can't connect the T's
emitter.on('user', (data) => {
  //                ^? unknown
});

// With type map
interface EventMap {
  user: User;
  message: Message;
}

class TypedEventEmitter<Events extends Record<string, any>> {
  on<K extends keyof Events>(
    event: K, 
    handler: (data: Events[K]) => void
  ): void;
  
  emit<K extends keyof Events>(
    event: K, 
    data: Events[K]
  ): void;
}

const emitter = new TypedEventEmitter<EventMap>();
emitter.on('user', (data) => {
  //                ^? User
});
```

## Factory Functions

```typescript
// Factory provides inference site
function createStore<T>(initial: T) {
  let state = initial;
  return {
    get: () => state,
    set: (newState: T) => { state = newState; }
  };
}

const userStore = createStore({ name: 'Alice', age: 30 });
// T inferred from initial value

userStore.set({ name: 'Bob', age: 25 }); // OK
userStore.set({ name: 'Charlie' }); // Error: missing age
```

## Method Chaining with Type Evolution

```typescript
class QueryBuilder<T = unknown, Selected = T> {
  select<K extends keyof T>(...keys: K[]): QueryBuilder<T, Pick<T, K>> {
    return this as any;
  }
  
  where(predicate: (item: T) => boolean): QueryBuilder<T, Selected> {
    return this as any;
  }
  
  execute(): Selected[] {
    // ...
  }
}

interface User { id: number; name: string; email: string; age: number; }

const results = new QueryBuilder<User>()
  .select('name', 'email')
  .where(u => u.age > 18)
  .execute();
// ^? { name: string; email: string; }[]
```

## Generic Constraints for Better Inference

```typescript
// Without constraint
function pluck<T, K>(items: T[], key: K): T[K][];
// K not constrained, inference poor

// With constraint
function pluck<T, K extends keyof T>(items: T[], key: K): T[K][] {
  return items.map(item => item[key]);
}

const names = pluck(users, 'name');
// ^? string[]
```

The constraint `K extends keyof T` helps TypeScript infer `K` from `T`.

## Avoiding Type Parameters in Return Position Only

```typescript
// Bad: T only in return position (no inference)
function parseJson<T>(): T {
  return JSON.parse(data);
}

// Good: T has inference site
function parseJson<T>(parser: (raw: unknown) => T): T {
  return parser(JSON.parse(data));
}

// Good: Factory pattern
function createParser<T>() {
  return {
    parse: (data: string): T => JSON.parse(data)
  };
}
const userParser = createParser<User>();
```

## Pressure Resistance Protocol

### 1. "Just Use Type Assertions"

**Pressure:** "I'll cast with `as T`"

**Response:** Assertions bypass type checking. Better to design for inference.

**Action:** Add inference sites through parameters or currying.

### 2. "Explicit Type Parameters Work"

**Pressure:** "Users can just write `fn<Type>(...)`"

**Response:** Inferred types are less work and less error-prone.

**Action:** Design APIs where inference works automatically.

## Red Flags - STOP and Reconsider

- Generic function with type parameter only in return type
- Users always need to specify generic parameters explicitly
- `unknown` or `any` appearing where specific types are expected
- Type assertions needed to get correct types

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "Users can specify the type" | Good API design infers types |
| "It's too complex" | Currying and factories are straightforward |
| "Type assertions work" | They bypass safety; inference is better |

## Quick Reference

```typescript
// BAD: No inference site for T
function fetch<T>(url: string): Promise<T>;

// GOOD: Parser provides inference site
function fetch<T>(url: string, parse: (raw: unknown) => T): Promise<T>;

// GOOD: Currying
function fetch<T>() {
  return (url: string): Promise<T> => ...;
}

// GOOD: Factory
function createFetcher<T>(parse: (raw: unknown) => T) {
  return (url: string): Promise<T> => ...;
}
```

## The Bottom Line

**Design APIs that give TypeScript inference opportunities.**

When generic types can't be inferred, add inference sites: parameters that use the type, curried functions, or class methods. Good API design makes explicit type parameters unnecessary.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 28: Use Classes and Currying to Create New Inference Sites.
