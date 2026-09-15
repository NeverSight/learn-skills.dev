---
name: bridge-js
description: Export Swift to JavaScript and import JavaScript/TypeScript into Swift using BridgeJS; type-safe bindings via @JS and related macros or bridge-js.d.ts; setup, config, AOT. Use when using or setting up BridgeJS, exporting Swift APIs to JS, importing JS/TS APIs into Swift, writing bridge-js.d.ts, configuring BridgeJS, or debugging BridgeJS boundaries.
---

# BridgeJS

BridgeJS is a code-generation layer in JavaScriptKit that makes Swift–JavaScript interop faster and easier than raw `JSObject`/`JSValue`: you declare the API shape in Swift (or TypeScript), and the tool generates glue code. Two directions: **export Swift to JavaScript** and **import JavaScript into Swift**.

## Referencing official docs

When you need details, read DocC from the **checked-out JavaScriptKit repository**: `Sources/JavaScriptKit/Documentation.docc/` when inside the JavaScriptKit repo, or `.build/checkouts/JavaScriptKit/Sources/JavaScriptKit/Documentation.docc/` when in a project that depends on JavaScriptKit.

## Two directions

- **Export Swift**: Use `@JS` (and `@JS(namespace:enumStyle:identityMode:)`) on functions, classes, structs, enums, closures, protocols, etc. JavaScript then calls into your Swift code. See [references/exporting.md](references/exporting.md).
- **Import JavaScript**: (1) Declare bindings in Swift with `@JSFunction`, `@JSClass`, `@JSGetter`, `@JSSetter`; use `@JSGetter(from: .global)` for globals like `document`/`console`; inject other implementations via `getImports()`. See [references/importing.md](references/importing.md). (2) Or use `bridge-js.d.ts` to generate the same Swift bindings. See [references/importing-ts.md](references/importing-ts.md).

## Key concepts

- **Type mapping**: Primitives, `Optional` ↔ `null`, `JSUndefinedOr` ↔ `undefined`, arrays, `Record<string, V>` ↔ `[String: V]`, `JSTypedArray<T>` ↔ TypedArray (by reference), unbridged → `JSObject`/`JSValue`. See [references/types.md](references/types.md) if present.
- **Semantics**: classes, protocols, `JSTypedArray`, and closures cross by reference; structs, enums, and plain arrays cross by copy.
- **Errors**: Only `throws(JSException)` is supported at the bridge; plain `throws` is not.
- **Async**: Exported `async` functions/methods/closures become `Promise`-returning JS functions (require `JavaScriptEventLoop.installGlobalExecutor()`). Imported standalone `@JSFunction` cannot be async, but imported async **callbacks** (closure parameters) are supported.
- **Preview interfaces**: For **previewing d.ts → Swift** locally, run the ts2swift script from the checked-out JavaScriptKit: from a project that depends on JavaScriptKit use `node .build/checkouts/JavaScriptKit/Plugins/BridgeJS/Sources/TS2Swift/JavaScript/bin/ts2swift.js <input.d.ts> [options]`; Run with `--help` for usage.
- **Closures**: Use **JSTypedClosure** when passing or returning Swift closures to JS, and call `release()` when the closure is no longer needed by JS. Plain Swift closure types also work as parameters/returns, released automatically via `FinalizationRegistry`. Closure signatures may be `throws(JSException)` and/or `async`. When receiving callbacks from JS (e.g. imported APIs), use regular closure types in Swift (`(Args) -> Return`).

## References

- [Project setup and config](references/project_setup.md)
- [Exporting Swift to JS](references/exporting.md)
- [Importing JS into Swift (macros)](references/importing.md)
- [Generating from TypeScript](references/importing-ts.md)
- [Supported types](references/types.md) (optional)
- [Testing](references/testing.md)
- [Limitations](references/unsupported.md)
