---
name: type-system
description: "Apply when you design types or a signature, or write code in a typed language."
disable-model-invocation: true
license: MIT
compatibility: "No tools needed."
---

# Type-system

Let the compiler reject wrong states, so that reviews and tests do not have to.

- Parse external data once, at the boundary, with the project's schema tool. Inside, trust the typed value.
- Derive a type from the schema that owns the shape. When two languages hold the same model, one is the source, and a test fails when the other differs.
- Give each state its own type. No optional field that is "set only when", no nullable value that cannot be null, no tuple where names say more.
- When two values have the same primitive type and different meanings, give each its own type.
- Use no cast, non-null assertion or `any` to silence a missing check.
- Let return types be inferred. Keep inputs read-only. Check a fixed mapping with a typed record, so that a missing case does not compile.
- Handle every variant, so that a new variant is a compile error.
