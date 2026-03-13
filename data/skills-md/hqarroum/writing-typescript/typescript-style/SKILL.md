---
name: typescript-style
description: Enforces TypeScript coding standards including naming, code structure, type safety, error handling, and project setup. Use when writing, reviewing, or refactoring TS files, or initializing new TS projects.
license: MIT
metadata:
  author: Halim Qarroum
  version: 1.1.0
---

# TypeScript Code Guidelines

## Naming Conventions

- Files and directories: `kebab-case.ts`.
- Classes, interfaces, types, enums: `PascalCase`.
- Functions, variables, methods: `camelCase`.
- Constants: `UPPER_SNAKE_CASE`.
- Booleans: prefix with `is`, `has`.
- Functions: start with, or consist of, a verb (`get`, `resolve`, `create`).
- Use simple variable and function names `const user = getUser()`.

## Type Safety

- No `any`.
- When the type is genuinely unknown at compile time, use `unknown` and narrow via [type guards](https://www.w3schools.com/typescript/typescript_type_guards.php).
- Omit explicit return types when TypeScript can infer them unambiguously.
- Prefer `satisfies` over `as`, validates the type at the assignment site while preserving the narrower inferred type.
- Use `readonly` for properties that are never reassigned after construction.
- Use `as const` for literal objects and arrays that should not change.
- Use `import type` when importing symbols used only as types.

## Code Style

### Syntax

- 2 spaces for indentation.
- Single quotes for strings.
- Template literals for multi-line strings and interpolation.
- Arrow functions for functions and callbacks.
- Use `const` by default. Use `let` only when reassignment is required. No `var`.
- Only `===` and `!==` for comparisons.
- Parentheses around return values (Opinionated):
- Variable declarations at the top of their scope.

```ts
const work = () => {
  const x = 1;
  const y = 2;

  // Do work.

  return (x + y);
};
```

### Imports

- Use ES modules.
- Group imports in the following order:
  1. Built-in modules (e.g. `fs`, `path`)
  2. External libraries (e.g. `react`, `lodash`)
  3. Internal modules (e.g. `./utils`, `../components/Button`)
  4. Type imports (e.g. `import type { User } from './types'`)
  5. Multiple imports.

```ts
import { readFile } from 'node:fs';
import { useState } from 'react';
import { debounce } from 'lodash';
import type { Request, Response } from 'express';
import type { Client } from './sdk';

import {
  orderByDate,
  orderByPrice
} from './components/orders';
import {
  User,
  Product
} from './models';
```

- Use engine-specific protocols for module imports:

```ts
import { readFile } from 'node:fs';
```

### Structure

- Prefer `async`/`await` over `.then()` chains.
- Use early returns to reduce nesting.
- Keep functions small and focused.
- Use higher-order functions (`map`, `filter`, `reduce`) over imperative loops.
- Use one variable per declaration statement.
- Prefer `for...of` when iterating objects.
- Prefer simple, concise code.
- No default exports, always use named exports.
- Use [discriminated unions](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#discriminated-unions) over optional properties for more complex types.
- Break statements across multiple lines:

```ts
// Wrong.
this.emit('agent:status', { state: 'thinking', message: 'Processing your request…' });

// Right.
this.emit('agent:status', {
  state: 'thinking',
  message: 'Processing your request…'
});
```

- When using declarative code, for example, using `Zod` or `Drizzle` schemas, write the declarative code by formatting it with each property or method on a new line. For example:

```ts
/**
 * Schema for validating user data.
 */
const UserSchema = z.object({
  
  /**
   * The unique identifier for the user.
   * @uuid
   */
  id: z
    .string()
    .uuid()
    .describe('The unique identifier for the user.'),

  /**
   * The name of the user.
   * @min 1 character
   * @max 100 characters
   */
  name: z
    .string()
    .min(1)
    .max(100)
    .describe('The name of the user.'),

  /**
   * The email of the user.
   */
  email: z
    .string()
    .email()
    .describe('The email of the user.')
});
```

### Enums vs. Types

Prefer TypeScript `type` over `enum`. Use `union` for simple value sets and as `const` objects when you need both runtime values and type inference.

```ts
// Simple.
type Status = 'active' | 'inactive';

// Multi-line.
type UserRole =
  | 'admin'
  | 'editor'
  | 'viewer'
  | 'guest';
```

### Function Chaining

When chaining multiple function calls using a fluent interface:

```ts
const result = object
  .map(arg1, arg2)
  .reduce(arg3)
  .pipe(arg4);
```

### Object Literals

When defining object literals, format the code with each property on a new line.

```ts
const obj = {
  prop1: value1,
  prop2: value2,
  prop3: value3
};
```

### Curly Braces

Always use curly braces for blocks.

For example:

```ts
// Wrong.
if (condition) order();

// Wrong.
if (condition)
  order();

// Right.
if (condition) {
  order();
}
```

### Organization

- Types are always co-located with their implementation and define a single type, or multiple closely related types. Avoid "types-only" files that export unrelated types.
- Organize code by feature or module under specific directories.
- Avoid global type augmentation when possible.
- Store code in a `src/` directory, with subdirectories for features or modules.

### Comments

- Use JSDoc comments for functions, types, enums, classes, methods, and class properties. Class properties are always defined at the top of the class, before the constructor. Example:

```ts
/**
 * Calculates the area of a rectangle.
 * @param width - The width of the rectangle.
 * @param height - The height of the rectangle.
 * @returns The area of the rectangle.
 */
const calculateArea = (width: number, height: number) => {
  return (width * height);
};
```

```ts
/**
 * Properties for a custom order.
 */
export type CustomOrderProps = {

  /**
   * The unique identifier for the order.
   */
  id: string;

  /**
   * The product being ordered.
   */
  product: string;

  /**
   * The quantity to be ordered.
   */
  quantity: number;
};

/**
 * The `CustomOrder` class represents a custom order in the system.
 */
export class CustomOrder {

  /**
   * Creates a new custom order.
   * @param props - The properties of the custom order.
   * @constructor
   */
  constructor(private props: CustomOrderProps) {}

  /**
   * Computes the total price of the order.
   * @returns The total price of the order.
   */
  getTotalPrice() {
    // Implementation goes here.
  }
}
```

- Only use `@type` in JSDoc comments when the type or unit is non-obvious.

```ts
/**
 * The default timeout for API requests.
 * @type {number} in milliseconds
 */
const DEFAULT_TIMEOUT = 5_000;
```

- Do not use decorative separators (e.g., `-`, `// --------`, `// ========`) in comments.

- Use inline comments to explain *what* the code is doing and *why*.

```ts
/**
 * Issues an API request to the given URL and returns the response data.
 * @param url - The URL to send the request to.
 * @returns The response data from the API.
 */
const request = async (url: URL) => {
  const response = await fetch(url);
    
  // Check for successful response.
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  // Validate response with Zod.
  const result = ResponseSchema.safeParse(
    await response.json()
  );
  if (!result.success) {
    throw new Error(`Invalid response format: ${result.error.message}`);
  }
  
  return (result.data);
};
```

- Do not comment the top of files with a description of the file's purpose.
- Do not use single-line block comments (`/** ... */`) for function or type declarations. Use multi-line JSDoc comments instead.

#### Globals

Use multi-line comments for global variables or constants. Globals should be defined at the top of the file, after imports and before any other code.

```ts
/**
 * The default timeout for API requests.
 * @type {number} in milliseconds
 */
const DEFAULT_TIMEOUT = 5_000;
```

## Performance

- Prefer `Map` and `Set` over plain objects for frequent lookups.
- Avoid unnecessary spread copies in hot paths.
- Use `Promise.all()` for independent async operations; `Promise.allSettled()` when dealing with partial failure.

## Anti-Patterns

- No `Object` or `Array` constructors — use literals `{}` and `[]`.
- No `eval()` or `Function` constructor.
- No `with` statements.
- No deep nesting of callbacks or conditionals.
- Avoid non-null assertions (`!`).
- No over-annotation of inferred types when not necessary.
- Avoid Barrel files as they break tree-shaking, slow down bundlers and IDE indexing, create circular dependency traps, and inflate bundle sizes.
- No static-only classes.
- No nested ternaries — max one level deep.
- No magic numbers / strings — extract to named constants.
- No prototype manipulation.
- No unbounded or user-supplied regular expressions — avoid catastrophic backtracking (ReDoS). Prefer simple patterns, use non-backtracking quantifiers, or validate regex complexity before execution.

## Logging

See [the reference guide](references/typescript-logging.md) for details.

## Architecture

See [the reference guide](references/typescript-architecture.md) for details.

## Security

See [the reference guide](references/typescript-security.md) for details.

## Testing

- Use `vitest` for unit and integration testing.
- Use supertest for HTTP endpoint testing when a headless browser is not needed.
- Write tests per feature or component in a dedicated `tests/` directory within each associated package. For monorepos, each package should have its own `tests/` directory and test configuration.
- Under the `tests/` directory, organize tests by type (e.g., `unit/`, `integration/`, `e2e/`).

## Environment

For every project using environment variables, always use an `env.ts` file that defines and exports all expected environment variables with proper types. Use `zod` to validate these variables at runtime.

```ts
/**
 * Environment variable schema definition.
 */
const envSchema = z.object({

  /**
   * The Supabase region where the function is executing.
   * Automatically set by Supabase runtime.
   * @optional Available only in deployed environments
   */
  SB_REGION: z
    .string()
    .optional(),

  /**
   * Unique identifier for the current function execution.
   * Automatically set by Supabase runtime.
   * @optional Available only in deployed environments
   */
  SB_EXECUTION_ID: z
    .string()
    .optional(),

  /**
   * The current environment (development, staging, production).
   * Used for conditional logic and logging.
   * @default "development"
   */
  ENVIRONMENT: z
    .enum(['development', 'staging', 'production'])
    .default('development')
});

/**
 * Parse and validate environment variables.
 * @throws {z.ZodError} If validation fails, with detailed error messages
 * @returns Validated and typed environment variables
 */
const parseEnv = (): Env => {
  try {
    return envSchema.parse({
      SB_REGION: process.env.SB_REGION,
      SB_EXECUTION_ID: process.env.SB_EXECUTION_ID,
      ENVIRONMENT: process.env.ENVIRONMENT
    });
  } catch (error) {
    // Log the error with details for debugging.
    throw error;
  }
};

/**
 * Validated environment variables.
 *
 * Import this constant to access typed, validated environment variables
 * throughout your Edge Functions.
 */
export const env = parseEnv();
```

## Tooling

### Code Quality & Type Safety

| Tool | Purpose |
|------|---------|
| `Zod` | Runtime validation and type inference for complex data structures. |
| `oxlint` | Code linter. |
| `oxfmt` | Code formatter. |
| `tsc` | TypeScript compiler for type checking and transpilation. |
| `tsx` | TypeScript execution environment for running TS files directly. |

### Tests

| Tool | Purpose |
|------|---------|
| `vitest` | Fast and lightweight testing framework with built-in TypeScript support. |
| `supertest` | HTTP assertions for testing API endpoints without a headless browser. |

#### HTTP Stress Testing

| Tool | Purpose |
|------|---------|
| `wrk` | High-performance HTTP benchmarking tool for load testing APIs. |
| `k6` | Modern load testing tool with scripting in JavaScript/TypeScript. |
| `autocannon` | Fast HTTP/1.1 benchmarking tool for stress testing APIs. |

#### Web Page Testing

| Tool | Purpose |
|------|---------|
| `playwright` | End-to-end testing framework for web applications with TypeScript support. |
| `puppeteer` | Headless Chrome Node API for web page testing and automation. |

### Database & ORMs

| Need | Use | Why |
|------|-----|-----|
| ORM | Drizzle | SQL-like API, fully type-safe, zero overhead, supports Postgres/MySQL/SQLite |
| Query builder | Kysely | Type-safe raw SQL builder, no magic, great for complex queries |

### Zod-specific Guidelines

- Define schemas in dedicated files.
- Use `z.infer<typeof Schema>` to derive types from Zod schemas.
- Use `.describe()` to add descriptions to schema properties.

### Package Managers

| Package Manager | Use Case |
|-----------------|----------|
| `pnpm` | Default for Node.js projects. |
| `bun` | Use when the project is Bun-based. |
| `npm` | Use when the project is Node.js-based and there's a specific reason to choose npm. |

### Files

Add the following files to your project.

| File | Purpose |
|------|---------|
| `.oxfmtrc.json` | Oxlint configuration in `references/config/` |
| `.oxlintrc.json` | Oxfmt configuration in `references/config/` |
| `tsconfig.json` | TypeScript configuration in `references/config/`. |
| `.gitignore` | Specifies files and directories to ignore in version control. |
| `nx.json` or `turbo.json` | Configuration for monorepo management with Nx or Turborepo. |
| `.nvmrc` | Specifies the Node.js version for the project. |

### CI/CD

| Tool | Purpose |
|------|---------|
| `GitHub Actions` | CI/CD pipelines for automated testing, linting, and deployment. |
| `tsc --noEmit` | Type-check step — run in CI to catch type errors before merge. |
| `vitest run` | Run tests. |

### Reference Files

The `references/config` directory contains starter configurations:
- `.oxlintrc.json` — Oxlint configuration with rules for TypeScript projects.
- `.oxfmtrc.json` — Oxfmt configuration for consistent code formatting.
- `tsconfig.json` — TypeScript compiler options with `strict: true`.
