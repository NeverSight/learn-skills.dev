---
name: parse-dont-validate
description: >-
  Type-driven design principle: transform unstructured data into structured types at system
  boundaries, making illegal states unrepresentable. Use when writing or reviewing code that
  validates input, designs data types, defines function signatures, handles errors, or models
  domain logic. Use when you see validation functions that return void/undefined, redundant
  null checks, stringly-typed data, boolean flags controlling behavior, or functions that can
  receive data they shouldn't. Triggers on: "parse don't validate", "type-driven design",
  "make illegal states unrepresentable", "input validation", "data modeling", "refactor types",
  "strengthen types", "smart constructor", "newtype", "branded type".
---

# Parse, Don't Validate

Based on Alexis King's article: https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/

A parser is a function that consumes less-structured input and produces more-structured output.
Validation checks a property and throws it away. Parsing checks a property and *preserves it
in the type system*. Always prefer parsing.

## The Core Idea

```ts
// VALIDATION: checks a property, returns nothing useful
function validateNonEmpty(list: string[]): void {
  if (list.length === 0) throw new Error("list cannot be empty");
}

// PARSING: checks the same property, returns proof in the type
function parseNonEmpty<T>(list: T[]): [T, ...T[]] {
  if (list.length === 0) throw new Error("list cannot be empty");
  return list as [T, ...T[]];
}
```

Both check the same thing. But `parseNonEmpty` gives the caller access to what it learned.
`validateNonEmpty` throws the knowledge away, forcing every downstream function to either
re-check or hope for the best.

## The Two Strategies

When a function is partial (not defined for all inputs), there are exactly two ways to make
it total:

### 1. Weaken the output (add Maybe/null)

```ts
function head<T>(list: T[]): T | undefined {
  return list[0];
}
```

Easy to implement, annoying to use. Every caller must handle `undefined` even if they already
know the list is non-empty. Leads to redundant checks and `// should never happen` comments.

### 2. Strengthen the input (narrow the type) -- PREFER THIS

```ts
function head<T>(list: [T, ...T[]]): T {
  return list[0];
}
```

The check happens once, at the boundary, when the data enters the system. After that, the
type carries the proof. No redundant checks. No impossible branches. If the validation logic
changes, the compiler catches every affected call site.

**Always try strategy 2 first. Fall back to strategy 1 only when 2 is impractical.**

## Practical Rules

### 1. Make illegal states unrepresentable

Use the most precise data structure you reasonably can. Don't model things you shouldn't allow.

```ts
// BAD: allows duplicate keys, order might matter or might not
type Config = Array<[string, string]>;

// GOOD: duplicates impossible by construction
type Config = Map<string, string>;

// or even better if keys are known:
type Config = { host: string; port: number; debug: boolean };
```

### 2. Push parsing to the boundary

Parse data into precise types as soon as it enters your system. The boundary between your
program and the outside world is where parsing belongs.

```ts
// BAD: raw data flows deep into the system, validated ad-hoc
function processUser(data: unknown) {
  // 50 lines later...
  if (typeof data.email !== "string") throw new Error("invalid email");
}

// GOOD: parse at the boundary, use precise types everywhere else
interface User { name: string; email: string; age: number; }

function parseUser(data: unknown): User {
  // validate and parse here, once
}

function processUser(user: User) {
  // no validation needed -- the type guarantees it
}
```

### 3. Treat `void`-returning validators with deep suspicion

A function whose primary purpose is checking a property but returns `void` is almost always
a missed opportunity. It should return a more precise type instead.

```ts
// SUSPICIOUS: checks something, returns nothing
function validateAge(age: number): void {
  if (age < 0 || age > 150) throw new Error("invalid age");
}

// BETTER: returns proof of validity as a branded type
type ValidAge = number & { readonly __brand: "ValidAge" };
function parseAge(age: number): ValidAge {
  if (age < 0 || age > 150) throw new Error("invalid age");
  return age as ValidAge;
}
```

### 4. Use branded/opaque types as "fake parsers"

When making an illegal state truly unrepresentable is impractical (e.g., "integer in range
1-100"), use branded types with smart constructors to fake it:

```ts
type EmailAddress = string & { readonly __brand: "EmailAddress" };

function parseEmail(input: string): EmailAddress {
  if (!input.includes("@")) throw new Error("invalid email");
  return input as EmailAddress;
}

// Now functions can demand EmailAddress instead of string
function sendEmail(to: EmailAddress, body: string): void { /* ... */ }
```

The type system won't let you pass a raw `string` where `EmailAddress` is expected.
You must go through `parseEmail` first.

### 5. Let types inform code, not vice versa

Don't stick a `boolean` in a record because your current function needs it. Design the
types first, then write functions that transform between them.

```ts
// BAD: boolean flag controlling behavior
interface Request { url: string; isAuthenticated: boolean; token?: string; }

// GOOD: discriminated union makes invalid state impossible
type Request =
  | { kind: "anonymous"; url: string }
  | { kind: "authenticated"; url: string; token: string };
```

### 6. Avoid denormalized data

Duplicating the same information in multiple places creates a trivially representable
illegal state: the copies getting out of sync. Strive for a single source of truth.

If denormalization is necessary for performance, hide it behind an abstraction boundary
where a small, trusted module keeps representations in sync.

### 7. Parse in multiple passes if needed

Avoiding shotgun parsing means don't *act on* data before it's fully parsed. It doesn't
mean you can't use some input data to decide how to parse other input data.

```ts
// Fine: first parse the header to determine the format, then parse the body
const header = parseHeader(raw);
const body = parseBody(raw, header.format);
```

## Shotgun Parsing -- The Anti-Pattern

Shotgun parsing is when validation code is mixed with and spread across processing code.
Checks are scattered everywhere, hoping to catch all bad cases without systematic
justification.

The danger: if a late-discovered error means some invalid input was already partially
processed, you may need to roll back state changes. This is fragile and error-prone.

Parsing avoids this by stratifying the program into two phases:
1. **Parsing phase** -- failure due to invalid input can only happen here
2. **Execution phase** -- input is known-good, failure modes are minimal

## Code Review Checklist

When reviewing code, watch for these smells:

- [ ] Function accepts `string` where a more specific type exists (URL, email, ID)
- [ ] Validation function returns `void` instead of a refined type
- [ ] Same property checked in multiple places (redundant validation)
- [ ] `// should never happen` or `// impossible` comments
- [ ] Raw `unknown`/`any`/`object` flowing past the system boundary into business logic
- [ ] Boolean fields that could be discriminated unions
- [ ] Optional fields that are actually always present after a certain point
- [ ] Arrays where non-empty arrays are required
- [ ] `null` checks deep in business logic for data validated at entry
