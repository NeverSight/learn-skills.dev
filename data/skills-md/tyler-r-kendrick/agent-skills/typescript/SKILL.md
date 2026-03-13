---
name: typescript
description: |
  Use when working with TypeScript projects, tooling, and ecosystem. Covers the type system, project configuration, package management, CLI development, and library packages.
  USE FOR: TypeScript language features, choosing build tools, package managers, project structure, type system guidance, runtime selection
  DO NOT USE FOR: specific tool configuration details (use the sub-skills: project-system, package-management, cli, packages)
license: MIT
metadata:
  displayName: "TypeScript"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "TypeScript Documentation"
    url: "https://www.typescriptlang.org"
  - title: "TypeScript GitHub Repository"
    url: "https://github.com/microsoft/TypeScript"
  - title: "typescript npm Package"
    url: "https://www.npmjs.com/package/typescript"
---

# TypeScript

## Overview

TypeScript is a statically typed superset of JavaScript that compiles to plain JavaScript. It adds optional type annotations, interfaces, generics, and advanced type-level programming to JavaScript, enabling safer refactoring, better tooling, and self-documenting code. TypeScript has become the default choice for professional JavaScript development across frontend frameworks, backend services, CLIs, and serverless functions.

## Knowledge Map

```
typescript/
├── project-system/       # tsconfig.json, build tools, bundlers, compilation
├── package-management/   # npm, yarn, pnpm, bun, workspaces, publishing
├── cli/                  # Commander, yargs, oclif, ink, chalk, CLI tooling
└── packages/             # Popular libraries (Express, Next.js, Zod, Prisma, etc.)
```

## Choosing Guide

| Problem | Sub-Skill | Notes |
|---------|-----------|-------|
| Configure tsconfig.json or compiler options | `project-system` | Covers target, module, strict, paths, and all compiler flags |
| Choose or configure a bundler (Vite, esbuild, etc.) | `project-system` | Build tool comparison with speed, features, and config examples |
| Set up monorepo with project references | `project-system` | Composite projects, tsc --build, path aliases |
| Choose a package manager (npm, pnpm, yarn, bun) | `package-management` | Feature comparison, lockfiles, disk usage, monorepo support |
| Configure workspaces for a monorepo | `package-management` | npm/yarn/pnpm/bun workspace patterns and turborepo integration |
| Publish a package to npm | `package-management` | Publishing workflow, provenance, package.json exports |
| Build a CLI tool | `cli` | Commander, yargs, oclif, ink for TUI, packaging strategies |
| Add interactive prompts or terminal styling | `cli` | inquirer, prompts, chalk, ora, listr2 |
| Choose or use a specific library | `packages` | Express, Fastify, Next.js, Zod, Prisma, tRPC, and more |

## TypeScript Version Landscape

| Version | Key Features |
|---------|-------------|
| **4.0** | Variadic tuple types, labeled tuple elements, class property inference from constructors |
| **4.1** | Template literal types, key remapping in mapped types, recursive conditional types |
| **4.2** | Leading/middle rest elements in tuples, stricter `in` operator checks |
| **4.3** | `override` keyword, template literal type improvements, `static` index signatures |
| **4.4** | Control flow analysis of aliased conditions, symbol and template literal index signatures |
| **4.5** | `Awaited` type, tail-recursive conditional types, `type` modifiers on import names |
| **4.6** | Control flow analysis for destructured discriminated unions, `--target es2022` |
| **4.7** | `extends` constraints on `infer`, instantiation expressions, `moduleSuffixes` |
| **4.8** | Improved intersection reduction, `--build` mode `--watch`, template literal narrowing |
| **4.9** | `satisfies` operator, `in` narrowing for unlisted properties, auto-accessors |
| **5.0** | Decorators (TC39 standard), `const` type parameters, `--moduleResolution bundler` |
| **5.1** | Easier implicit returns for `undefined`, unrelated types for getters/setters, `@param` JSDoc linking |
| **5.2** | `using` declarations (explicit resource management), decorator metadata |
| **5.3** | Import attributes, `--resolution-mode` in `/// <reference>`, narrowing in `switch (true)` |
| **5.4** | `NoInfer` utility type, preserved narrowing in closures, `Object.groupBy` / `Map.groupBy` |
| **5.5+** | Inferred type predicates, `isolatedDeclarations`, regex syntax checking |

## Core Language Features Quick Reference

### Type System Fundamentals

```typescript
// Union types — value can be one of several types
type Result = "success" | "error" | "pending";
type ID = string | number;

// Intersection types — combine multiple types
type Employee = Person & { employeeId: string };

// Generics — parameterized types
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}

// Conditional types — type-level if/else
type IsString<T> = T extends string ? true : false;

// Mapped types — transform properties
type Readonly<T> = { readonly [K in keyof T]: T[K] };
type Optional<T> = { [K in keyof T]?: T[K] };

// Template literal types — string manipulation at the type level
type EventName<T extends string> = `on${Capitalize<T>}`;
type ClickEvent = EventName<"click">; // "onClick"

// satisfies operator — validate type without widening
const palette = {
  red: [255, 0, 0],
  green: "#00ff00",
} satisfies Record<string, string | number[]>;

// const assertions — narrow to literal types
const routes = ["home", "about", "contact"] as const;
type Route = (typeof routes)[number]; // "home" | "about" | "contact"

// Discriminated unions — tagged union pattern
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "rectangle":
      return shape.width * shape.height;
  }
}
```

### Key Utility Types

| Utility | Purpose | Example |
|---------|---------|---------|
| `Partial<T>` | Make all properties optional | `Partial<User>` |
| `Required<T>` | Make all properties required | `Required<Config>` |
| `Readonly<T>` | Make all properties readonly | `Readonly<State>` |
| `Pick<T, K>` | Select specific properties | `Pick<User, "id" \| "name">` |
| `Omit<T, K>` | Remove specific properties | `Omit<User, "password">` |
| `Record<K, V>` | Object type with key/value types | `Record<string, number>` |
| `Exclude<T, U>` | Remove types from a union | `Exclude<Status, "deleted">` |
| `Extract<T, U>` | Keep only matching union members | `Extract<Event, { type: "click" }>` |
| `NonNullable<T>` | Remove null and undefined | `NonNullable<string \| null>` |
| `ReturnType<T>` | Extract function return type | `ReturnType<typeof fetch>` |
| `Parameters<T>` | Extract function parameter types | `Parameters<typeof setTimeout>` |
| `Awaited<T>` | Unwrap Promise types | `Awaited<Promise<string>>` |
| `NoInfer<T>` | Prevent inference on a type parameter | `NoInfer<T>` in default args |

## Runtime Options

| Runtime | Key Strengths | TypeScript Support |
|---------|--------------|-------------------|
| **Node.js** | Largest ecosystem, widest deployment, mature tooling | Via `tsc`, `ts-node`, `tsx`, `esbuild`, or `swc` |
| **Deno** | Built-in TypeScript, secure by default, web-standard APIs | Native — no build step required |
| **Bun** | Fastest startup, built-in bundler/test runner/package manager | Native — runs `.ts` files directly |
| **Cloudflare Workers** | Edge computing, V8 isolates, global deployment | Via Wrangler with esbuild under the hood |

### Choosing a Runtime

- **Building a production server or API?** Node.js has the broadest library support and hosting options.
- **Want built-in TypeScript with no config?** Deno runs `.ts` natively with LSP and formatter included.
- **Need maximum startup speed or an all-in-one tool?** Bun combines runtime, bundler, package manager, and test runner.
- **Deploying at the edge?** Cloudflare Workers provide sub-millisecond cold starts globally.

## Best Practices

1. **Enable `strict` mode** in every project. It enables `strictNullChecks`, `noImplicitAny`, `strictFunctionTypes`, and other flags that catch real bugs.

2. **Avoid `any`** — it disables all type checking. Use `unknown` when the type is truly unknown, then narrow with type guards.

3. **Prefer `unknown` over `any`** for values of uncertain type:
   ```typescript
   function parse(input: unknown): Config {
     if (typeof input === "object" && input !== null && "port" in input) {
       return input as Config;
     }
     throw new Error("Invalid config");
   }
   ```

4. **Use type narrowing** instead of type assertions:
   ```typescript
   // Prefer this
   if (typeof value === "string") {
     console.log(value.toUpperCase());
   }
   // Over this
   console.log((value as string).toUpperCase());
   ```

5. **Use branded types** for domain identifiers to prevent mixing:
   ```typescript
   type UserId = string & { __brand: "UserId" };
   type OrderId = string & { __brand: "OrderId" };

   function getUser(id: UserId): User { /* ... */ }
   // getUser(orderId) — compile error!
   ```

6. **Use `satisfies`** to validate object shapes without widening types.

7. **Use `const` assertions** for literal tuples and objects that should not be widened.

8. **Use discriminated unions** for state machines and variant types instead of optional properties.

9. **Enable `noUncheckedIndexedAccess`** to force undefined checks on dynamic property access.

10. **Keep `any` out of library boundaries** — validate external data at the edge with Zod, io-ts, or similar runtime validators.
