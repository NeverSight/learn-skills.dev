---
name: typescript
description: "Use TypeScript for type-safe JavaScript: types, interfaces, generics, narrowing, tsconfig, modules, and strict mode. Use when writing or reviewing TypeScript, configuring tsconfig.json, defining types or interfaces, generics, type inference, or when the user mentions TypeScript, TS, or type checking."
---

# TypeScript

## Overview

TypeScript is JavaScript with static typing. It adds a **compile-time type checker**; runtime behavior is JavaScript. Learning JavaScript applies to TypeScript for runtime tasks (e.g. sorting a list, DOM, async). Use TypeScript for types, interfaces, generics, and better tooling.

**Core idea**: Types describe shape and contracts; the compiler catches type errors before run time. Enable `strict` in `tsconfig.json` as a best practice.

---

## Quick reference

| Concept | Syntax / note |
|--------|----------------|
| Type annotation | `let x: string`, `function f(n: number): void` |
| Interface | `interface User { name: string; id: number }` |
| Type alias | `type Id = string \| number` |
| Union | `string` or `number` (union types) |
| Optional | `prop?: string` or `prop: string \| undefined` |
| Generics | `function id<T>(x: T): T { return x }` |
| Infer type from schema | Use library (e.g. Zod: `z.infer<typeof schema>`) |

---

## Everyday types

- **Primitives**: `string`, `number`, `boolean`, `bigint`, `symbol`.
- **Arrays**: `number[]` or `Array<number>`.
- **Any**: `any` — disables checking; avoid when possible. Prefer `unknown` for truly unknown data and narrow before use.
- **Type annotations** (postfix): `const name: string = "x"`, `function greet(name: string): string { return "Hi " + name }`.
- **Object types**: `{ name: string; age?: number }` or `interface User { name: string; age?: number }`.
- **Unions**: `string | number`; **literal types**: `"a" | "b"`.

---

## Narrowing

Narrow types with conditionals so TypeScript can infer:

- **typeof**: `if (typeof x === "string") { ... }`
- **Truthiness**: `if (value) { ... }`
- **Equality**: `if (x === null) { ... }`
- **in**: `if ("name" in obj) { ... }`
- **Type guards**: `function isFish(pet: Fish | Bird): pet is Fish { ... }`
- **Discriminated unions**: Use a common literal field (e.g. `kind: "circle"`) and switch on it.

---

## Functions

- **Signatures**: `(a: string, b?: number) => boolean`; **void** for no return value.
- **Overloads**: Multiple call signatures + one implementation.
- **Generics**: `function first<T>(arr: T[]): T \| undefined`.
- **Constraints**: `function longest<T extends { length: number }>(a: T, b: T): T`.

---

## Object types & type manipulation

- **Interfaces**: `interface Point { x: number; y: number }`; `extends` for extension.
- **Index signatures**: `[key: string]: number`.
- **keyof**: `type K = keyof User` → union of keys.
- **typeof**: `type C = typeof config` (value → type).
- **Indexed access**: `type Name = User["name"]`.
- **Mapped types**: `type Readonly<T> = { readonly [K in keyof T]: T[K] }`.
- **Conditional types**: `type F = T extends string ? number : boolean`.
- **Template literal types**: `` type E = `on${Capitalize<Event>}` ``.
- **Utility types**: `Partial<T>`, `Required<T>`, `Pick<T, K>`, `Omit<T, K>`, `Record<K, V>`, `Exclude<T, U>`, `Extract<T, U>`, `NonNullable<T>`, `ReturnType<F>`, `Parameters<F>`.

---

## Classes

- **Members**: `class C { prop: number; method(): void {} }`.
- **Constructor**: `constructor(public name: string) {}` (parameter property).
- **Implements**: `class D implements I {}`.
- **Extends**: `class Child extends Parent {}`.
- **Readonly**, **private**, **protected** as needed.

---

## Modules

- **ES modules**: `import { x } from "./file"`, `export const x = 1`, `export type { T }`.
- **Default export**: `export default App`, `import App from "./App"`.
- **Namespace** (legacy): Prefer ES modules.

---

## Project configuration: tsconfig.json

- **strict**: Set `"strict": true` (recommended). Enables strictNullChecks, noImplicitAny, strictFunctionTypes, etc.
- **target**: e.g. `"ES2022"` or `"ESNext"`.
- **module**: e.g. `"ESNext"`, `"NodeNext"` for Node.
- **moduleResolution**: `"bundler"` (with bundler), `"NodeNext"` for Node.
- **paths**: `"@/*": ["./src/*"]` for path aliases.
- **include** / **exclude**: Which files are compiled.
- **References**: Use project references for large monorepos.

See [reference.md](reference.md) for official TSConfig Reference link.

---

## Best practices

- Enable **strict** mode.
- Prefer **interfaces** for object shapes that may be extended; **type** for unions, mapped types, and aliases.
- Prefer **const** and **readonly** where possible.
- Use **unknown** instead of **any** for external data; narrow before use.
- Use **generics** to keep functions reusable and type-safe.
- For runtime validation + types, use a schema library (e.g. **Zod**) and infer types with `z.infer<typeof schema>`.

---

## Common mistakes

- **any**: Avoid; use `unknown` and narrow, or proper types.
- **Non-null assertion (`!`)**: Use sparingly; prefer narrowing or optional chaining.
- **Type assertions (`as`)**: Prefer type guards or schema validation when data comes from outside.
- **Strict off**: Keep `strict: true`; fix errors rather than disabling.

---

## Additional resources

- [reference.md](reference.md) — Official documentation links (Handbook, Reference, TSConfig, Cheat Sheets).
- **Official**: https://www.typescriptlang.org/docs — Get Started, Handbook, Reference, TSConfig.
