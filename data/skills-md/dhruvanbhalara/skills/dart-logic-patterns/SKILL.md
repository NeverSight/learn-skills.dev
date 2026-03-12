---
name: dart-logic-patterns
description: Best practices for implementing efficient business logic on mobile using appropriate algorithms and data structures.
metadata:
    platforms: "cross-platform"
    languages: "generic"
    category: "logic"
---

# Algorithms & Logic

The efficiency of your business logic directly impacts battery life and responsiveness.

## Complexity Analysis
- **Big O Awareness**: Understand the cost of your operations. Avoid O(n²) or higher on the main thread for datasets larger than a few hundred items.
- **Data Structure Selection**:
  - `Map`: Fast key-based lookups.
  - `Set`: Fast unique item management.
  - `List`: Fast indexing and sequential access.
  - `LinkedHashSet/Map`: Preserves insertion order while providing fast lookups.

## Logic Patterns
- **Debouncing**: Delay execution until a user stops interacting (e.g., search-as-you-type).
- **Throttling**: Limit execution to at most once every interval (e.g., scrolling events).
- **Memoization**: Cache the results of expensive pure functions based on their arguments. Use `package:memoize` or custom implementations.

## Search & Sort
- **Binary Search**: Use for sorted lists to transform O(n) searches into O(log n).
- **Efficient Sorting**: Use Dart's built-in `list.sort()`, which uses highly optimized algorithms. Provide targeted `Comparable` implementations for custom objects.

## Business Logic Organization
- **Pure Functions**: Keep business logic in pure, testable functions outside of UI classes.
- **Fail Fast**: Use guard clauses to handle edge cases and invalid states early.
- **Validation Logic**: Keep complex validation in a separate domain layer, reusable across different screens.
