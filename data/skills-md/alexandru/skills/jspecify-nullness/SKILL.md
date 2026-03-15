---
name: jspecify-nullness
description: JSpecify nullness annotations for Java APIs and tooling. Use when adopting or migrating JSpecify annotations, designing null-safe Java signatures and generics, or interpreting tool conformance and Kotlin interop.
---

# JSpecify Nullness (Java)

## Quick start
- Use `@NullMarked` to make unannotated types non-null by default.
- Add `@Nullable` only where null is allowed; use `@NonNull` sparingly when you must override a nullable type variable use.
- Decide type parameter bounds up front: `<T extends @Nullable Object>` allows nullable type arguments, `<T>` does not.
- Use `@NullUnmarked` to opt out of `@NullMarked` in legacy or incremental areas.
- Keep annotations in recognized type-use positions (arrays, nested types, type arguments).
- Read `references/jspecify-nullness.md` for migration steps, syntax pitfalls, and tooling details.

## Workflow
1. Confirm tool support and constraints (nullness checker, Kotlin version, annotation processors).
2. Add the `org.jspecify:jspecify` dependency and expose it to consumers.
3. Annotate nullable types first, then add `@NullMarked` at class or package scope.
4. Fix generics: set bounds for type parameters and annotate type-variable uses as needed.
5. Run nullness analysis, resolve findings, and repeat for adjacent code.

## Rules of thumb
- Treat unannotated types outside `@NullMarked` as unspecified nullness, not non-null.
- Do not annotate local-variable root types; annotate only type arguments or array components there.
- For arrays, `@Nullable String[]` means nullable elements, while `String @Nullable []` means a nullable array.
- For nested types, use `Map.@Nullable Entry` to mark the nested type, not the outer type.
- Use `@Nullable` on a type variable usage only when null is allowed even if the type argument is non-null.

## Output expectations
- Provide annotated signatures and call-site implications.
- Call out tool-conformance limits rather than promising specific diagnostics.

## References
- Load `references/jspecify-nullness.md` for full guidance and examples.
