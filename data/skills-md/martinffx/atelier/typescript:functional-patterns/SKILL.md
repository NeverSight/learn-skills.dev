---
name: typescript:functional-patterns
description: Functional programming patterns for reliable TypeScript. Use when modeling state machines, discriminated unions, Result/Option types, branded types, or building type-safe domain models.
user-invocable: false
---

# Functional Patterns for Reliable TypeScript

Build reliable systems using Algebraic Data Types (ADTs), discriminated unions, Result/Option types, and branded types. These patterns enable the compiler to prove correctness, prevent runtime errors, and make illegal states unrepresentable.

## Why Functional Patterns?

**Reliability through types**: Use the type system to encode business rules, making invalid states impossible to construct. The compiler becomes your safety net, catching errors at build time rather than runtime.

**Key benefits:**
- Exhaustiveness checking prevents missing cases
- Impossible states become unrepresentable
- Business logic encoded in types, not runtime checks
- Refactoring becomes safe and mechanical
- Self-documenting code through types

## Quick Reference

For detailed patterns and examples, see:
- [ADTs (Algebraic Data Types)](./references/adts.md) - Sum types, product types, discriminated unions
- [Option & Result](./references/option-result.md) - Type-safe error handling and nullable values
- [Branded Types](./references/branded-types.md) - Smart constructors and nominal typing
- [Migration Guide](./references/migration-guide.md) - Step-by-step adoption playbook

## Core Patterns Overview

### 1. Discriminated Unions (Sum Types)

Model "one of several variants" with exhaustive pattern matching:

```typescript
type PaymentMethod =
  | { kind: "card"; last4: string; brand: string }
  | { kind: "ach"; accountNumber: string; routingNumber: string }
  | { kind: "wallet"; provider: "apple" | "google" }

function processPayment(method: PaymentMethod): void {
  switch (method.kind) {
    case "card":
      // TypeScript knows: method.last4 and method.brand exist
      return processCard(method.last4, method.brand)
    case "ach":
      // TypeScript knows: method.accountNumber and method.routingNumber exist
      return processACH(method.accountNumber, method.routingNumber)
    case "wallet":
      // TypeScript knows: method.provider exists
      return processWallet(method.provider)
    default:
      assertNever(method) // Compiler error if cases missing
  }
}
```

### 2. Option Type (Nullable Values)

Explicit handling of "value may be absent":

```typescript
type Option<T> = { _tag: "None" } | { _tag: "Some"; value: T }

function findUser(id: string): Option<User> {
  const user = database.get(id)
  return user ? Some(user) : None
}

const result = findUser("123")
switch (result._tag) {
  case "Some":
    console.log(result.value.name) // Type-safe access
    break
  case "None":
    console.log("User not found")
    break
}
```

### 3. Result Type (Error Handling)

Explicit error handling without exceptions:

```typescript
type Result<T, E> = { _tag: "Ok"; value: T } | { _tag: "Err"; error: E }

function parseConfig(raw: string): Result<Config, ParseError> {
  try {
    const data = JSON.parse(raw)
    return Ok(validateConfig(data))
  } catch (e) {
    return Err({ message: "Invalid JSON", cause: e })
  }
}

const result = parseConfig(rawConfig)
switch (result._tag) {
  case "Ok":
    startServer(result.value)
    break
  case "Err":
    logger.error(result.error.message)
    break
}
```

### 4. Branded Types (Type-Safe Units)

Prevent unit confusion and invalid values:

```typescript
type Brand<K, T> = K & { __brand: T }
type Cents = Brand<number, "Cents">
type Dollars = Brand<number, "Dollars">

const Cents = (n: number): Cents => {
  if (!Number.isInteger(n) || n < 0) throw new Error("Invalid cents")
  return n as Cents
}

const Dollars = (n: number): Dollars => {
  if (n < 0) throw new Error("Invalid dollars")
  return n as Dollars
}

// Compiler prevents mixing units:
const price: Cents = Cents(100)
const budget: Dollars = Dollars(10)
const total: Cents = price + budget // Type error! Cannot mix Cents and Dollars
```

## When to Use

### Use Discriminated Unions When:
- Modeling state machines (pending → settled → reconciled)
- Representing mutually exclusive variants (payment methods, user roles)
- Building domain models with distinct states
- Replacing boolean flags with explicit states

### Use Option When:
- Value may be absent (but absence is expected/valid)
- Replacing `null` or `undefined` checks
- Chaining operations that may fail to find values
- Making nullability explicit in APIs

### Use Result When:
- Operation may fail with recoverable errors
- You need to propagate error context
- Replacing try/catch for expected failures
- Building error handling into function signatures

### Use Branded Types When:
- Preventing unit confusion (cents vs dollars, ms vs seconds)
- Enforcing validation invariants (email format, positive numbers)
- Creating type-safe IDs (UserId vs OrderId)
- Domain-driven design with value objects

## Quick Start - Paste-Ready Helpers

Copy these into your project to start using functional patterns:

```typescript
// ============================================
// Option Type
// ============================================
type None = { _tag: "None" }
type Some<T> = { _tag: "Some"; value: T }
type Option<T> = None | Some<T>

const None: None = { _tag: "None" }
const Some = <T>(value: T): Option<T> => ({ _tag: "Some", value })

// Utilities
const isNone = <T>(opt: Option<T>): opt is None => opt._tag === "None"
const isSome = <T>(opt: Option<T>): opt is Some<T> => opt._tag === "Some"

const getOrElse = <T>(opt: Option<T>, defaultValue: T): T =>
  opt._tag === "Some" ? opt.value : defaultValue

const map = <T, U>(opt: Option<T>, fn: (value: T) => U): Option<U> =>
  opt._tag === "Some" ? Some(fn(opt.value)) : None

const flatMap = <T, U>(opt: Option<T>, fn: (value: T) => Option<U>): Option<U> =>
  opt._tag === "Some" ? fn(opt.value) : None

// ============================================
// Result Type
// ============================================
type Ok<T> = { _tag: "Ok"; value: T }
type Err<E> = { _tag: "Err"; error: E }
type Result<T, E> = Ok<T> | Err<E>

const Ok = <T>(value: T): Result<T, never> => ({ _tag: "Ok", value })
const Err = <E>(error: E): Result<never, E> => ({ _tag: "Err", error })

// Utilities
const isOk = <T, E>(result: Result<T, E>): result is Ok<T> => result._tag === "Ok"
const isErr = <T, E>(result: Result<T, E>): result is Err<E> => result._tag === "Err"

const mapResult = <T, U, E>(result: Result<T, E>, fn: (value: T) => U): Result<U, E> =>
  result._tag === "Ok" ? Ok(fn(result.value)) : result

const flatMapResult = <T, U, E>(
  result: Result<T, E>,
  fn: (value: T) => Result<U, E>
): Result<U, E> =>
  result._tag === "Ok" ? fn(result.value) : result

// ============================================
// Exhaustiveness Checking
// ============================================
const assertNever = (x: never): never => {
  throw new Error(`Unhandled variant: ${JSON.stringify(x)}`)
}

// ============================================
// Branded Types
// ============================================
type Brand<K, T> = K & { __brand: T }

// Example: Cents (integer cents to prevent floating point errors)
type Cents = Brand<number, "Cents">
const Cents = (n: number): Cents => {
  if (!Number.isInteger(n)) throw new Error("Cents must be integer")
  if (n < 0) throw new Error("Cents cannot be negative")
  return n as Cents
}

// Example: Email (validated email address)
type Email = Brand<string, "Email">
const Email = (s: string): Email => {
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s)) throw new Error("Invalid email")
  return s as Email
}

// Example: Millis (timestamp in milliseconds)
type Millis = Brand<number, "Millis">
const Millis = (n: number): Millis => {
  if (n < 0) throw new Error("Millis cannot be negative")
  return n as Millis
}
```

## Guidelines

### Pattern Matching Best Practices

1. **Always use `assertNever` in default case** for exhaustiveness checking:
   ```typescript
   switch (variant.kind) {
     case "a": return handleA(variant)
     case "b": return handleB(variant)
     default: assertNever(variant) // Compiler error if cases missing
   }
   ```

2. **Use discriminant field consistently** (`kind`, `type`, `_tag`):
   ```typescript
   // Good: consistent discriminant
   type Result<T, E> = { _tag: "Ok"; value: T } | { _tag: "Err"; error: E }

   // Avoid: mixing discriminants
   type Bad = { kind: "a" } | { type: "b" } // Inconsistent!
   ```

3. **Narrow types early** to unlock type safety:
   ```typescript
   if (result._tag === "Ok") {
     // TypeScript knows: result.value exists
     return result.value.data
   }
   ```

### Error Handling Strategy

1. **Use Option for expected absence**:
   ```typescript
   function findUser(id: string): Option<User>
   ```

2. **Use Result for recoverable errors**:
   ```typescript
   function parseConfig(raw: string): Result<Config, ParseError>
   ```

3. **Use exceptions for programmer errors**:
   ```typescript
   function unreachable(message: string): never {
     throw new Error(`Unreachable: ${message}`)
   }
   ```

### Branded Types Guidelines

1. **Validate in smart constructor**:
   ```typescript
   const PositiveInt = (n: number): PositiveInt => {
     if (!Number.isInteger(n) || n <= 0) throw new Error("Must be positive integer")
     return n as PositiveInt
   }
   ```

2. **Use branded types for domain concepts**:
   ```typescript
   type UserId = Brand<string, "UserId">
   type OrderId = Brand<string, "OrderId">
   // Compiler prevents: const userId: UserId = orderId
   ```

3. **Prevent unit confusion**:
   ```typescript
   type Seconds = Brand<number, "Seconds">
   type Millis = Brand<number, "Millis">
   // Compiler prevents: const s: Seconds = millis
   ```

### Migration Strategy

Start small and expand:
1. New features: Use functional patterns from day one
2. Bug fixes: Refactor to discriminated unions when touching code
3. High-risk areas: Prioritize financial calculations, state machines
4. Team adoption: Share paste-ready helpers, pair on first implementations

Enable TypeScript strict mode flags:
- `strictNullChecks: true` - Make nullability explicit
- `noImplicitReturns: true` - Ensure all code paths return
- `strictFunctionTypes: true` - Safer function signatures

## Examples by Domain

### State Machine (Transaction Lifecycle)
```typescript
type TxnState =
  | { kind: "pending"; createdAt: Millis }
  | { kind: "settled"; ledgerId: string; settledAt: Millis }
  | { kind: "failed"; reason: FailureReason; failedAt: Millis }
  | { kind: "reversed"; originalLedgerId: string; reversedAt: Millis }

function canReverse(state: TxnState): boolean {
  switch (state.kind) {
    case "pending": return false
    case "settled": return true
    case "failed": return false
    case "reversed": return false
    default: assertNever(state)
  }
}
```

### Configuration Parsing
```typescript
type ConfigError = { field: string; message: string }

function parsePort(raw: unknown): Result<number, ConfigError> {
  if (typeof raw !== "number") {
    return Err({ field: "port", message: "must be number" })
  }
  if (raw < 1 || raw > 65535) {
    return Err({ field: "port", message: "must be 1-65535" })
  }
  return Ok(raw)
}
```

### Financial Calculations
```typescript
type Cents = Brand<number, "Cents">

function addCents(a: Cents, b: Cents): Cents {
  return Cents(a + b) // Smart constructor validates result
}

function calculateFee(amount: Cents, bps: number): Cents {
  const feeAmount = Math.round((amount * bps) / 10000)
  return Cents(feeAmount)
}
```

## Further Reading

- [ADT Reference](./references/adts.md) - Deep dive on sum types, product types, and pattern matching
- [Option & Result Reference](./references/option-result.md) - Comprehensive error handling patterns
- [Branded Types Reference](./references/branded-types.md) - Advanced nominal typing techniques
- [Migration Guide](./references/migration-guide.md) - Step-by-step adoption playbook

## Credits

These patterns are inspired by **[Why Reliability Demands Functional Programming, ADTs, Safety and Critical Infrastructure](https://rastrian.com/why-reliability-demands-functional-programming-adts-safety-and-critical-infrastructure/)** by Rastrian. The blog post explores how functional programming techniques and Algebraic Data Types enable building reliable systems in critical infrastructure contexts.

## When This Skill Loads

This skill automatically loads when discussing:
- Discriminated unions and sum types
- State machine modeling
- Result/Option types and error handling
- Branded types and smart constructors
- Type-safe domain models
- Making illegal states unrepresentable
- Functional programming in TypeScript
