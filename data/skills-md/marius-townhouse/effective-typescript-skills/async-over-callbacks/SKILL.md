---
name: async-over-callbacks
description: Use when writing asynchronous code. Use when tempted to use callbacks. Use when composing multiple async operations.
---

# Use async Functions Instead of Callbacks

## Overview

**Prefer async/await over callbacks for cleaner code and better type flow.**

Callbacks create nested, hard-to-follow code. Promises and async/await flatten the structure, make types flow naturally, and enable better error handling.

## When to Use This Skill

- Writing any asynchronous code
- Tempted to use callback-style APIs
- Chaining multiple async operations
- Need to compose concurrent operations
- Working with APIs that return Promises

## The Iron Rule

```
ALWAYS prefer async/await over callbacks for new code.
```

**Remember:**
- async/await is syntactic sugar over Promises
- Types flow through Promises automatically
- Error handling is cleaner with try/catch
- Concurrent operations compose easily

## Detection: The Callback Pyramid

If you see nested callbacks (the "pyramid of doom"), refactor to async/await:

```typescript
// ❌ Callback hell - hard to read, types don't flow well
fetchURL(url1, function(response1) {
fetchURL(url2, function(response2) {
fetchURL(url3, function(response3) {
// ... deeply nested
console.log(1);
});
console.log(2);
});
console.log(3);
});
console.log(4);
// Logs: 4, 3, 2, 1 (confusing order!)
```

## The async/await Solution

```typescript
// ✅ Clean, flat, readable
async function fetchPages() {
const response1 = await fetch(url1);
const response2 = await fetch(url2);
const response3 = await fetch(url3);
// Execution order matches code order
}
```

## Why Types Flow Better

### Callbacks Require Manual Type Annotations

```typescript
// ❌ Callbacks - you must annotate types
function fetchUser(
  id: string,
  callback: (user: User | null, error?: Error) => void
) {
  // ...
}

fetchUser('123', (user, error) => {
  if (error) { /* handle */ }
  if (user) { /* use user */ }
});
```

### Promises Carry Types Automatically

```typescript
// ✅ Promises - types flow through
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  return response.json();  // TypeScript knows this returns Promise<User>
}

const user = await fetchUser('123');
//    ^? const user: User
```

## Composing Async Operations

### Sequential Operations

```typescript
async function getFullUserData(id: string) {
  const user = await fetchUser(id);
  const posts = await fetchPosts(user.id);
  const comments = await fetchComments(posts);
  return { user, posts, comments };
}
// Return type is automatically inferred
```

### Concurrent Operations with Promise.all

```typescript
async function fetchAllPages() {
  // Run all fetches concurrently, wait for all to complete
  const [page1, page2, page3] = await Promise.all([
    fetch(url1),
    fetch(url2),
    fetch(url3),
  ]);
  // Types are inferred: [Response, Response, Response]
}
```

### Race Conditions with Promise.race

```typescript
async function fetchWithTimeout(url: string, ms: number) {
  return Promise.race([
    fetch(url),
    new Promise<never>((_, reject) =>
      setTimeout(() => reject(new Error('Timeout')), ms)
    ),
  ]);
}
```

## Error Handling

### Callbacks: Error-First Convention (Manual)

```typescript
// ❌ Manual error handling, easy to forget
fetchData(url, (error, data) => {
  if (error) {
    console.error(error);
    return;
  }
  // use data
});
```

### async/await: Natural try/catch

```typescript
// ✅ Standard exception handling
async function fetchData(url: string) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Fetch failed:', error);
    throw error;  // Re-throw or handle
  }
}
```

## Common Patterns

### Always Return Promises from async Functions

```typescript
// ❌ Inconsistent return type
function getQuote(ticker: string) {
  if (cache[ticker]) {
    return cache[ticker];  // Returns number
  }
  return fetch(`/quote?t=${ticker}`)
    .then(r => r.json());  // Returns Promise<number>
}
// Type: number | Promise<number> - confusing!

// ✅ Consistent Promise return
async function getQuote(ticker: string): Promise<number> {
  if (cache[ticker]) {
    return cache[ticker];  // Automatically wrapped in Promise
  }
  const response = await fetch(`/quote?t=${ticker}`);
  return response.json();
}
```

### Annotate Return Types for Clarity

```typescript
// ✅ Explicit return type catches mistakes
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  // TypeScript ensures we return a User
  return response.json();
}
```

### Use Promise.allSettled for Partial Failures

```typescript
async function fetchAllUsers(ids: string[]) {
  const results = await Promise.allSettled(
    ids.map(id => fetchUser(id))
  );
  
  // Handle both successes and failures
  const users: User[] = [];
  for (const result of results) {
    if (result.status === 'fulfilled') {
      users.push(result.value);
    } else {
      console.error('Failed:', result.reason);
    }
  }
  return users;
}
```

## Converting Callbacks to Promises

### Using util.promisify (Node.js)

```typescript
import { promisify } from 'util';
import { readFile } from 'fs';

const readFileAsync = promisify(readFile);

async function loadConfig() {
  const data = await readFileAsync('config.json', 'utf-8');
  return JSON.parse(data);
}
```

### Manual Promisification

```typescript
function fetchURLAsync(url: string): Promise<string> {
  return new Promise((resolve, reject) => {
    fetchURL(url, (response, error) => {
      if (error) {
        reject(error);
      } else {
        resolve(response);
      }
    });
  });
}
```

## Immediate Execution in async Functions

```typescript
// async functions return a Promise, even with immediate values
async function getValue(): Promise<number> {
  return 42;  // Wrapped in Promise.resolve(42)
}

// To unwrap, you must await
const value = await getValue();
//    ^? const value: number
```

## Pressure Resistance Protocol

### 1. "Callbacks Are Faster"

**Pressure:** "Promises have overhead, callbacks are more performant"

**Response:** The overhead is negligible. Code clarity and type safety matter more.

**Action:** Use async/await. Profile if you suspect performance issues.

### 2. "The API Only Supports Callbacks"

**Pressure:** "This library uses callbacks, we have to use them too"

**Response:** Wrap callback APIs in Promises.

**Action:** Use promisify or create a Promise wrapper.

### 3. "We're Already Using Callbacks Everywhere"

**Pressure:** "Consistency with existing code"

**Response:** Gradually migrate. New code should use async/await.

**Action:** Wrap old APIs, write new code with async/await.

## Red Flags - STOP and Reconsider

- Nested callbacks (pyramid of doom)
- Functions that sometimes return values, sometimes Promises
- Manual error handling with error-first callbacks
- Mixing async/await with .then() chains unnecessarily

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "Callbacks are simpler" | async/await is more readable and maintainable |
| "Promise overhead is too high" | Negligible in practice, clarity wins |
| "Our team knows callbacks" | async/await is standard modern JavaScript |

## Quick Reference

| Pattern | Callbacks | async/await |
|---------|-----------|-------------|
| Sequential ops | Nested callbacks | Sequential await |
| Concurrent ops | Manual tracking | Promise.all |
| Error handling | Error-first convention | try/catch |
| Type inference | Manual annotations | Automatic flow |
| Composition | Difficult | Natural |

## The Bottom Line

**async/await produces cleaner code with better type inference.**

Callbacks create pyramids of nested code where types don't flow well. Promises and async/await flatten the structure, compose naturally, handle errors with standard try/catch, and let TypeScript infer types automatically. Use async/await for all new async code.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 27: Use async Functions Instead of Callbacks to Improve Type Flow.
