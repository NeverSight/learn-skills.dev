---
name: webflux-reactive-patterns
description: Expert guidance for Java Spring WebFlux reactive programming. Enforces pure reactive flows, lazy error handling with Mono.defer(), proper use of flatMap/map/filter, parallel operations with Mono.zip(), and elimination of imperative patterns. Use when developing reactive Java applications with WebFlux, handling Mono/Flux streams, refactoring imperative code to reactive style, reviewing reactive code for anti-patterns, debugging reactive issues (streams not executing, blocking calls, memory leaks), implementing error handling strategies, optimizing reactive performance, or converting blocking code to non-blocking. Always use this skill when you see Mono, Flux, WebFlux, reactive streams, or Project Reactor mentioned, even if the user doesn't explicitly ask for reactive patterns guidance.
license: MIT
metadata:
  author: jheison.martinez
  version: "1.1"
  framework: Spring WebFlux
  language: Java
  category: reactive-programming
  last_updated: "2026-03-12"
---

# WebFlux Reactive Patterns

This skill provides comprehensive guidance for writing idiomatic, production-ready reactive code with Spring WebFlux in Java. It enforces pure reactive programming patterns and eliminates common anti-patterns that break reactive streams.

## When to Use This Skill

Activate this skill when:
- Developing or refactoring Spring WebFlux applications
- Working with Mono and Flux reactive types
- Implementing reactive REST APIs or microservices
- Converting imperative code to reactive patterns
- Reviewing reactive code for anti-patterns
- Handling asynchronous operations in Java

## Core Principles

### 1. Analysis Before Implementation
Before writing any code, analyze existing code, define an implementation plan, ask clarifying questions, and make explicit design decisions. See [references/BEFORE_CODING.md](references/BEFORE_CODING.md) for the complete workflow.

### 2. Pure Reactive Flow
Never use imperative constructs (`if`, `throw`, nested operations). Replace with reactive operators (`filter`, `flatMap`, `switchIfEmpty`, `Mono.error()`). All errors must be lazy using `Mono.defer()`. See [references/REACTIVE_PATTERNS.md](references/REACTIVE_PATTERNS.md) for detailed patterns.

### 3. No Literals
Never use string or number literals in code. Use constants for all values and enums for error messages. This ensures maintainability and type safety.

### 4. Helper Methods
Extract complex operations into single-responsibility helper methods. Main methods should read as high-level reactive flows. Includes builders, validations, and collection searches.

### 5. Parallel Operations
Use `Mono.zip()` for independent parallel validations. Use `Flux.merge()` for independent parallel operations. Never serialize what can run in parallel.

### 6. Clean Imports and Types
Always use short imported names, never fully qualified class names. Organize imports: Java standard library → external libraries → project classes. Let the compiler infer types when obvious.

## Quick Reference

**Common Anti-Patterns to Avoid:**
- ❌ `if (condition) { ... } else { ... }` → ✅ Use `filter()`, `switchIfEmpty()`
- ❌ `throw new Exception()` → ✅ Use `Mono.defer(() -> Mono.error())`
- ❌ `.then(Mono.just(x))` mid-flow → ✅ Breaks fail-fast, restructure flow
- ❌ Nested `flatMap` chains → ✅ Extract to helper methods
- ❌ `Mono<Void>` mid-flow → ✅ Only at final return
- ❌ String literals → ✅ Use constants or enums

**Essential Patterns:**
```java
// Lazy error handling (mandatory pattern)
return Optional.ofNullable(data)
    .filter(d -> !d.isEmpty())
    .map(Mono::just)
    .orElse(Mono.defer(() -> Mono.error(BusinessType.EMPTY_DATA.build())));

// Repository with fallback
return repository.findById(id)
    .switchIfEmpty(Mono.defer(() -> Mono.error(BusinessType.NOT_FOUND.build(id))));

// Parallel validations
return Mono.zip(
    validateField1(data),
    validateField2(data),
    validateField3(data)
).then(Mono.just(data));
```

## Detailed Documentation

For comprehensive guidance, refer to these resources:

- **[references/BEFORE_CODING.md](references/BEFORE_CODING.md)** - Pre-implementation analysis workflow and planning checklist
- **[references/REACTIVE_PATTERNS.md](references/REACTIVE_PATTERNS.md)** - Complete reactive patterns, anti-patterns, and transformations
- **[references/BEST_PRACTICES.md](references/BEST_PRACTICES.md)** - Code style, imports, constants, and organizational rules
- **[references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)** - Common issues, debugging techniques, and solutions
- **[assets/reactive-service-example.java](assets/reactive-service-example.java)** - Working example demonstrating all key patterns

## Operator Selection Guide

Use this decision tree to select the right operator:

**Is the operation synchronous (no I/O, no async calls)?**
- Yes → Use `map()`
- No → Continue

**Does it return Mono/Flux?**
- Yes → Use `flatMap()`
- No → Use `map()`

**Need to filter elements?**
- Use `filter()` + `switchIfEmpty()`

**Need to handle empty streams?**
- Use `switchIfEmpty()`

**Need to run operations in parallel?**
- Independent Monos → `Mono.zip()`
- Independent Fluxes → `Flux.merge()`

**Need to aggregate Flux to collection?**
- Use `collect()` or `collectList()`

**Need lazy evaluation (especially errors)?**
- Use `Mono.defer()`

### Quick Reference

- **`map()`** - Synchronous transformations (1:1)
- **`flatMap()`** - Asynchronous operations returning Mono/Flux (1:1)
- **`filter()`** - Conditional filtering based on predicates
- **`switchIfEmpty()`** - Fallback when stream is empty
- **`zip()`** - Combine multiple independent Monos in parallel
- **`merge()`** - Combine multiple Fluxes, emitting as they arrive
- **`collect()`** - Aggregate Flux elements into collections
- **`defer()`** - Lazy evaluation (critical for error handling)

## Error Handling Philosophy

All errors must be lazy to maintain reactive semantics. Never use `throw` directly in reactive chains. Always wrap errors in `Mono.defer()` to ensure they're only evaluated when subscribed.

**Why lazy errors matter:**
- Preserves fail-fast behavior in reactive chains
- Allows proper error propagation through operators
- Enables retry and fallback strategies
- Maintains backpressure semantics

## Future Enhancements

This skill will be enhanced with validation scripts to automatically detect:
- Imperative patterns in reactive code
- Missing `Mono.defer()` in error handling
- Literal values that should be constants
- Opportunities for parallel execution

## Contributing

To extend this skill with additional patterns or examples, maintain the workflow-based organization and ensure all code examples are minimal and focused on demonstrating specific patterns.
