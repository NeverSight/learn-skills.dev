---
name: dart-optimization
description: Master Dart/Flutter performance optimization including efficient code patterns, data structure selection, and compilation benefits.
metadata:
    platforms: "cross-platform"
    languages: "dart"
    category: "optimization"
---

# Optimization

Performance in Dart goes beyond UI rendering; it's about efficient execution and smart resource utilization.

## Dart Performance Patterns
- **Standardize Types**: Avoid `dynamic`. Use explicit types or `Object?`. Statically typed code allows the compiler to perform far better optimizations.
- **Efficient Collections**:
  - Use `Set` for average O(1) containment checks.
  - Use `List` for ordered indexing.
  - Prefer `Iterable` methods (`map`, `where`) for readability, but use `for` loops in performance-critical hot paths.
- **Inlining**: Small getters and trivial functions are often inlined by the VM/AOT, but keeping them simple ensures this optimization happens.

## Compile-Time Optimizations
- **Final & Const**: Declare variables as `final` whenever possible. Use `const` constructors for widgets and data models to enable compile-time allocation and reduce runtime garbage collection pressure.
- **Ternary vs If-Else**: In Dart, they are generally equivalent, but prioritize readability. Use `switch` expressions (Dart 3+) for exhaustive and efficient pattern matching.

## Hot Paths & Loops
- **Minimize Work in Loops**: Extract calculations and object creations outside of loops.
- **Collection Literals**: Use literal syntax `[]` or `{}` instead of constructors like `List()` for brevity and minor performance gains.

## Profiling
- **DevTools CPU Profiler**: Identify hot paths and "heavy" functions.
- **Benchmarking**: Use `package:benchmark_harness` for scientific performance measurement of non-UI logic.
