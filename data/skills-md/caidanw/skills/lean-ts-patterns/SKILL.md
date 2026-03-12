---
name: lean-ts-patterns
description: >-
  Patterns for building lightweight, zero-dependency TypeScript tools and libraries.
  Use when building new CLI tools, libraries, or utilities from scratch. Use when refactoring
  existing TypeScript projects to remove unnecessary dependencies. Use when writing fetch wrappers,
  CLI parsers, loggers, config merging, string utilities, or any infrastructure code that should
  be lean and self-contained. Triggers on: "build a CLI", "write a logger", "fetch wrapper",
  "remove dependencies", "lightweight", "zero-dep", "inline utility", "refactor to be simpler".
---

# Lean TypeScript Patterns

Patterns for building lightweight, zero-dependency TypeScript/Bun tools. Distilled from studying
exemplary repos: unjs/citty (CLI), unjs/consola (logging), unjs/ofetch (HTTP), unjs/defu (merging),
unjs/scule (strings), unjs/pathe (paths), antfu/taze (package updates).

## The 7 Principles

### 1. Zero Dependencies by Design

Inline tiny utils. Use `node:` builtins. Vendor at build time if needed.

- CLI parsing: `node:util.parseArgs` (not commander/yargs)
- Colors: 22 lines of ANSI codes (not chalk/picocolors)
- Path utils: 7-line normalizer (not `path` polyfills)
- HTTP: `globalThis.fetch` wrapper (not axios)
- Object merging: 40-line recursive merge (not lodash.merge)

### 2. Identity Functions as Type Helpers

`defineCommand`, `defineConfig` return their argument unchanged. Their only job is type inference:

```ts
function defineCommand<const T extends ArgsDef>(def: CommandDef<T>): CommandDef<T> {
  return def;
}
```

The `const` modifier preserves literal types. Without it, `{ type: "boolean" }` widens to `{ type: string }`.

### 3. One Core Primitive, Compose Everything

Every library has one core function. Everything else is a thin wrapper:

- scule: `splitByCase()` -> camelCase, kebabCase, pascalCase, snakeCase, trainCase
- pathe: `normalizeWindowsPath()` -> join, resolve, normalize, relative, etc.
- defu: `_defu()` -> defu, defuFn, defuArrayFn
- consola: `_logFn()` -> .info(), .error(), .warn(), .debug(), etc.

### 4. Factory Pattern Over Classes

Closures that capture config and return composable instances:

```ts
function createFetch(globalOpts = {}) {
  const $fetch = async (url, opts) => { /* ... */ };
  $fetch.create = (defaults) => createFetch({ ...globalOpts, defaults });
  return $fetch;
}
```

Used by: ofetch (`createFetch`), consola (`createConsola`), defu (`createDefu`), citty (`createMain`).

### 5. Resolvable<T> for Lazy/Async Values

One type that enables lazy loading everywhere:

```ts
type Resolvable<T> = T | Promise<T> | (() => T) | (() => Promise<T>);

function resolveValue<T>(input: Resolvable<T>): T | Promise<T> {
  return typeof input === "function" ? (input as any)() : input;
}
```

Use for subcommands, config, metadata -- anything that might be expensive to compute upfront.

### 6. Smart Defaults, Escape Hatches

- ofetch: Retries default to 0 for POST/PUT/DELETE, 1 for GET
- citty: Positional args default to required, named args to optional
- consola: Fancy reporter in TTY, basic in CI, browser reporter in devtools
- defu: `null`/`undefined` = "not set", let defaults fill in

### 7. Types Mirror Runtime

If the runtime dispatches on a discriminant, the type system should too:

```ts
// Runtime: switch on type
if (arg.type === "boolean") { /* ... */ }

// Types: conditional on same discriminant
type ParsedArg<T> =
  T["type"] extends "boolean" ? boolean :
  T["type"] extends "string" ? string :
  T["type"] extends "enum" ? T["options"][number] :
  never;
```

## Copy-Paste Patterns

### ANSI Colors (22 lines, zero deps)

```ts
const noColor = (() => {
  const env = globalThis.process?.env ?? {};
  return env.NO_COLOR === "1" || env.TERM === "dumb" || env.CI;
})();

type ColorFn = (t: string) => string;
const _c = (c: number, r = 39): ColorFn => (t) =>
  noColor ? t : `\u001b[${c}m${t}\u001b[${r}m`;

export const bold = _c(1, 22);
export const dim = _c(2, 22);
export const red = _c(31);
export const green = _c(32);
export const yellow = _c(33);
export const blue = _c(34);
export const cyan = _c(36);
export const gray = _c(90);
```

### isPlainObject (10 lines)

```ts
function isPlainObject(value: unknown): value is Record<string, unknown> {
  if (value === null || typeof value !== "object") return false;
  const proto = Object.getPrototypeOf(value);
  if (proto !== null && proto !== Object.prototype
      && Object.getPrototypeOf(proto) !== null) return false;
  if (Symbol.iterator in value) return false;
  if (Symbol.toStringTag in value)
    return Object.prototype.toString.call(value) === "[object Module]";
  return true;
}
```

### MaybeArray + callHooks (10 lines)

```ts
type MaybeArray<T> = T | T[];
type MaybePromise<T> = T | Promise<T>;

async function callHooks<C>(
  context: C,
  hooks: MaybeArray<(ctx: C) => MaybePromise<void>> | undefined,
): Promise<void> {
  if (!hooks) return;
  for (const hook of Array.isArray(hooks) ? hooks : [hooks]) {
    await hook(context);
  }
}
```

### normalizeWindowsPath (7 lines)

```ts
const DRIVE_RE = /^[A-Za-z]:\//;
function normalizeWindowsPath(input = "") {
  if (!input) return input;
  return input
    .replace(/\\/g, "/")
    .replace(DRIVE_RE, (r) => r.toUpperCase());
}
```

## Quick Reference

| Need | Pattern | Reference |
|---|---|---|
| CLI argument parsing | `node:util.parseArgs` + typed layer | [cli-patterns.md](references/cli-patterns.md) |
| Colored terminal output | ANSI helper above | Inline above |
| HTTP client with retries | Fetch factory + interceptors | [fetch-patterns.md](references/fetch-patterns.md) |
| Logger with levels/reporters | Single-method reporter interface | [logging-patterns.md](references/logging-patterns.md) |
| Deep object merging | Defaults-first recursive merge | [data-utils.md](references/data-utils.md) |
| String case conversion | `splitByCase` + join variants | [data-utils.md](references/data-utils.md) |
| Type-safe definitions | `const` generic + conditional types | [typescript-tricks.md](references/typescript-tricks.md) |
| Lazy loading | `Resolvable<T>` + dynamic import | Inline above |
| Cross-platform paths | `normalizeWindowsPath` at every entry | [data-utils.md](references/data-utils.md) |

## Anti-Patterns to Avoid

- **Don't** pull in chalk/picocolors for colors -- 22 lines of ANSI codes suffice
- **Don't** use commander/yargs -- `node:util.parseArgs` covers 95% of CLI needs
- **Don't** use axios -- native fetch + a thin wrapper handles retries, interceptors, auto-parsing
- **Don't** use lodash for one function -- inline the 10-40 lines you need
- **Don't** use class hierarchies for config -- factory functions with closures are simpler
- **Don't** add "flexibility" or "configurability" that wasn't requested
- **Don't** make abstractions for single-use code
- **Don't** export from barrel files things that should be internal -- use `_` prefix convention
