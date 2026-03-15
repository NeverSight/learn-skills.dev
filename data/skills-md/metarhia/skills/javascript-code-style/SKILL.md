---
name: javascript-code-style
description: Apply Metarhia JavaScript style. Use when writing or editing .js, .mjs, .ts files (with certain corrections for typescript), formatting code, or when the user asks about code style or linting.
---

# JavaScript Code Style

Use following conventions for JavaScript and TypeScript code.

## Preparations

- Add to dev dependencies in package.json if not added:
  - eslint-config-metarhia
  - eslint, prettier
- Add scripts in package.json if not added:
  - "lint": "eslint . && prettier --check \"**/\*.js\" \"**/_.json\" \"\*\*/_.md\" \"\*_/_.ts\""
  - "fix": "eslint . --fix && prettier --write \"**/\*.js\" \"**/_.json\" \"\*\*/_.md\" \"\*_/_.ts\""
- Before and after code analisys with AI run `npm run lint` and `npm t`
- Use `npm run fix` if errors/warnings detected to auto-fix when possible

## Formatting

- Use single quotes and semicolons
- Keep max line length 80 (ignore URLs)
- Use trailing commas in multiline arrays, objects, and params
- Keep one empty line between semantic blocks
- Follow Prettier and eslint-config-metarhia for spacing, braces, and indentation

## Naming

- Use `camelCase` for variables and parameters
- Use `UpperCamelCase` for classes and types
- Use `UPPER_SNAKE_CASE` for constants
- Use `new` with capitalized constructor names
- Use `error` in catch blocks, not `err`
- Use short names (`e`, `i`) only in short one-line callbacks
- Use descriptive names in multiline callbacks (`event`, `index`, `item`)
- Use boolean prefixes: `is`, `has`, `can`, `should`
- Use singular names for entities and plural names for collections
- Use verb names for functions and handlers (`parse`, `create`, `handle`, `on`)
- Include units in numeric names (`timeoutMs`, `sizeBytes`)

## Best practices

- Prefer `const`, minimize `let`, never use `var`
- Prefer arrow functions (except prototype/class methods)
- Do not mutate input parameters
- Keep functions small and single-purpose
- Decompose long expressions into intermediate variables
- Prefer explicit loops (`for`, `for..of`) in hot paths
- Use array methods when they improve readability
- Use `===` and `!==` only
- Keep return types consistent
- Avoid nested ternaries and deep callback nesting
- Self-documented and self-descriptive code: do not add
  obvious comments, code should be clear without comments
- Use iteration methods like `.map`, `.filter`, `.reduce` if it is good for code semantic
- Try to avoid `.forEach` except case when passed callback
  do not read something from outer context

## Optimizations

- Keep object shapes stable: same keys, types, and key order
- Change shape only in constructors and creational patterns; avoid mix-ins and `delete`
- Use shape mutations only for metaprogramming
- Use `null` for empty reference types; use `undefined` for empty primitives
- Avoid array destructuring in assignments and loops; object destructuring is ok
- Keep hot functions monomorphic: stable arg count, types, and return types
- Avoid reading the same property from many unrelated object shapes
- Prefer string or number literals for status/codes; avoid mixing primitives with objects in one variable
- Keep objects that share a property to the same shape; avoid polymorphic hotspots
- Prefer fixed property access (`obj.x`) over dynamic keys (`obj[key]`) in hot paths
- Keep arrays dense, avoid holes and mixed element kinds
- Initialize object fields in constructor/factory once and in one order
- Set field to `null` or `undefined` instead of `delete` in hot paths
- Move reusable callbacks outside hot loops
- Keep `try/catch`, spread/rest, and `arguments` away from hot loops
- Use `Map` for dynamic key dictionaries, plain objects for fixed schemas
- Use `Object.create(null)` for pure dictionaries
- Use typed arrays for numeric and binary workloads
- Reduce GC pressure: reuse arrays, objects, and buffers when safe
