---
name: push-null-to-perimeter
description: Use when designing data structures with nullable values. Use when null checking is scattered throughout code. Use when related values have implicit null relationships.
---

# Push Null Values to the Perimeter of Your Types

## Overview

**Design types so values are either completely null or completely non-null, not a mix.**

Mixed null states create implicit relationships that are hard to track and lead to scattered null checks and bugs.

## When to Use This Skill

- Designing types with multiple nullable fields
- Finding null checks scattered throughout code
- Related values that are null together
- Debugging "undefined is not an object" errors
- Refactoring types with many optional properties

## The Iron Rule

```
NEVER design types where null values have implicit relationships.
```

**No exceptions:**
- Not for "it's simpler"
- Not for "we check at runtime"
- Not for "the fields are independent"

## Detection: The "Mixed Null" Smell

If two values are null together or non-null together, express that in the type.

```typescript
// ❌ VIOLATION: Implicit relationship between min and max
function extent(nums: number[]) {
  let min: number | undefined;
  let max: number | undefined;
  
  for (const num of nums) {
    if (min === undefined) {
      min = num;
      max = num;
    } else {
      min = Math.min(min, num);
      max = Math.max(max, num);  // Error! max might be undefined
    }
  }
  return [min, max];  // [number | undefined, number | undefined]
}

// Caller has to deal with all four combinations:
const [min, max] = extent([1, 2, 3]);
// min defined + max defined
// min undefined + max undefined
// min defined + max undefined  <- Impossible but allowed by type!
// min undefined + max defined  <- Impossible but allowed by type!
```

## Solution: All-or-Nothing Types

```typescript
// ✅ CORRECT: Result is either fully present or fully absent
function extent(nums: number[]): [number, number] | null {
  let result: [number, number] | null = null;
  
  for (const num of nums) {
    if (!result) {
      result = [num, num];
    } else {
      result = [Math.min(num, result[0]), Math.max(num, result[1])];
    }
  }
  return result;
}

// Caller only has two cases:
const result = extent([1, 2, 3]);
if (result) {
  const [min, max] = result;  // Both guaranteed to exist
}
```

## Example: User with Posts

```typescript
// ❌ BAD: Mixed nullability
class UserPosts {
  user: UserInfo | null;
  posts: Post[] | null;
  
  constructor() {
    this.user = null;
    this.posts = null;
  }
  
  async init(userId: string) {
    this.user = await fetchUser(userId);
    this.posts = await fetchPosts(userId);
  }
}

// At any moment, four states are possible:
// user null + posts null      (before init)
// user null + posts non-null  (during init - race condition!)
// user non-null + posts null  (during init - race condition!)
// user non-null + posts non-null  (after init)

// ✅ GOOD: All-or-nothing
class UserPosts {
  user: UserInfo;
  posts: Post[];
  
  private constructor(user: UserInfo, posts: Post[]) {
    this.user = user;
    this.posts = posts;
  }
  
  static async create(userId: string): Promise<UserPosts> {
    const [user, posts] = await Promise.all([
      fetchUser(userId),
      fetchPosts(userId),
    ]);
    return new UserPosts(user, posts);
  }
}

// Only two states: no instance, or fully loaded instance
const userPosts = await UserPosts.create(userId);
console.log(userPosts.user.name);  // Always safe!
```

## Example: API Response

```typescript
// ❌ BAD: Data and error both optional
interface ApiResponse {
  data?: ResponseData;
  error?: Error;
  loading: boolean;
}

// Confusing states are possible:
const bad: ApiResponse = {
  data: someData,
  error: someError,  // Both data AND error?
  loading: true,     // Still loading but has data?
};

// ✅ GOOD: Each state is complete
type ApiResponse =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: ResponseData }
  | { status: 'error'; error: Error };

// No confusion possible:
function handleResponse(response: ApiResponse) {
  switch (response.status) {
    case 'idle':
      return null;
    case 'loading':
      return <Spinner />;
    case 'success':
      return <Data data={response.data} />;  // data guaranteed
    case 'error':
      return <Error error={response.error} />;  // error guaranteed
  }
}
```

## The Boundary Pattern

Handle nullability at the boundaries of your system, not throughout:

```typescript
// ❌ BAD: Null checks everywhere
function processUser(userId: string | null) {
  if (!userId) return null;
  const user = getUser(userId);
  if (!user) return null;
  const posts = getPosts(user);
  if (!posts) return null;
  return formatUserWithPosts(user, posts);
}

// ✅ GOOD: Check at boundary, then work with clean types
function processUser(userId: string | null): UserWithPosts | null {
  // Handle null at the boundary
  if (!userId) return null;
  
  const user = getUser(userId);
  if (!user) return null;
  
  // After validation, work with non-null types
  return formatUserWithPosts(user);  // Takes User, not User | null
}

function formatUserWithPosts(user: User): UserWithPosts {
  // No null checks needed inside - user is guaranteed non-null
  const posts = user.posts;  // Always exists
  return { ...user, posts: posts.map(formatPost) };
}
```

## Class Design: Fully Initialized or Not At All

```typescript
// ❌ BAD: Partially initialized state
class Connection {
  socket: Socket | null = null;
  protocol: Protocol | null = null;
  
  async connect() {
    this.socket = await createSocket();
    this.protocol = await negotiateProtocol(this.socket);
  }
  
  send(data: string) {
    if (!this.socket || !this.protocol) {
      throw new Error('Not connected');
    }
    this.protocol.send(this.socket, data);
  }
}

// ✅ GOOD: Factory ensures complete initialization
class Connection {
  private constructor(
    private socket: Socket,
    private protocol: Protocol,
  ) {}
  
  static async create(): Promise<Connection> {
    const socket = await createSocket();
    const protocol = await negotiateProtocol(socket);
    return new Connection(socket, protocol);
  }
  
  send(data: string) {
    // No null checks - always initialized
    this.protocol.send(this.socket, data);
  }
}
```

## Pressure Resistance Protocol

### 1. "We Need Partial States"

**Pressure:** "The object needs to exist before all data is loaded"

**Response:** Create a separate type for the partial state, or use a factory.

**Action:** Use discriminated unions or async factories.

### 2. "It's More Complex"

**Pressure:** "One type with optional fields is simpler"

**Response:** Scattered null checks are more complex than clean types.

**Action:** Invest in the type design upfront.

## Red Flags - STOP and Reconsider

- Multiple optional fields that are null together
- Null checks scattered throughout a class
- Race conditions in async initialization
- Comments like "X is only set when Y is set"
- "Impossible" states that the type allows

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's simpler" | Scattered null checks aren't simple. |
| "We check at runtime" | Types catch errors at compile time. |
| "Fields are independent" | If they're null together, they're related. |

## Quick Reference

| Pattern | Solution |
|---------|----------|
| Two values null together | Return tuple or null |
| Object with loading state | Use discriminated union |
| Class with async init | Use static factory method |
| Mixed nullable properties | Group into nested object |

## The Bottom Line

**Make null an all-or-nothing proposition.**

Design types so a value is either completely present or completely absent. Push null handling to the boundaries of your code. The result is cleaner types, fewer null checks, and fewer bugs.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 33: Push Null Values to the Perimeter of Your Types.
