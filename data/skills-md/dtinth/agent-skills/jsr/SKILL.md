---
name: jsr
description: Create and maintain JSR (JavaScript Registry) packages. Use this whenever the user wants to publish a package to JSR, set up a new JSR project, configure exports, write documentation, or troubleshoot JSR publishing.
---

[JSR](https://jsr.io/) is a modern package registry for JavaScript and TypeScript. This skill covers creating, configuring, documenting, and publishing ESR packages with minimal overhead.

To create a package:

1. **Write code** in TypeScript as ESM (using `import`/`export`)
2. **Create config** - `jsr.json` (or add JSR properties to `deno.json`):
   ```json
   {
     "name": "@scope/package-name",
     "version": "1.0.0",
     "exports": "./mod.ts"
   }
   ```
3. **Publish** - `npx jsr publish` or `deno publish`

Key Differences from npm:

- **ESM-only**: No CommonJS. All modules must use `import`/`export`.
- **Direct specifiers in code**: Use `npm:lodash@4` or `jsr:@std/encoding@1` directly in imports without package.json entries.
- **TypeScript source preferred**: Publish `.ts` files directly, not compiled `.js` + `.d.ts`. JSR handles compilation and auto-generates docs.
- **Auto-generated docs**: JSDoc comments on functions, interfaces, classes become your package documentation. No need for separate docs.

## Publishing

```bash
# Validate before publishing
npx jsr publish --dry-run # Shows files to publish, validates rules, doesn't publish

# Publish from local machine
npx jsr publish # Opens browser for auth, publishes when approved

# (or use GitHub Actions, see below)
```

### GitHub Actions (OIDC)
1. Link repo to package in JSR settings (jsr.io → package → settings → GitHub repo)
2. Create `.github/workflows/publish.yml`:
```yaml
name: Publish
on:
  push:
    branches: [main]
jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v6
      - run: npx jsr publish
```
No secrets needed.

## Configuration (`jsr.json` or `deno.json`)

**Minimal:** (preferred for new packages as it is the most simple)
```json
{
  "name": "@scope/pkg",
  "version": "1.0.0",
  "exports": "./mod.ts"
}
```

**Equivalent to:**
```json
{
  "name": "@scope/pkg",
  "version": "1.0.0",
  "exports": {
    ".": "./mod.ts"
  }
}
```

**With file filtering:**
```json
{
  "name": "@scope/pkg",
  "version": "1.0.0",
  "exports": "./mod.ts",
  "publish": {
    "include": ["LICENSE", "README.md", "src/**/*.ts"],
    "exclude": ["src/**/*.test.ts"]
  }
}
```

**Un-gitignoring files** (e.g., publish `dist/` even if in `.gitignore`):
```json
{
  "publish": {
    "exclude": ["!dist"]
  }
}
```

## Documentation (JSDoc)

All JSDoc comments in exported symbols generate package docs visible on jsr.io and in editor completions.

**Module documentation** (top of file):
```ts
/**
 * Utilities for searching the database.
 *
 * @example
 * ```ts
 * import { search } from "@scope/db";
 * search("query")
 * ```
 *
 * @module
 */
```

**Function documentation:**
```ts
/**
 * Search the database.
 * @param query Search string (max 50 chars for performance)
 * @param limit Number of results. Defaults to 20.
 * @returns Array of matched items
 */
export function search(query: string, limit?: number): string[]
```

**Interfaces & Classes:**
```ts
/** Options for search behavior */
export interface SearchOptions {
  /** Max results to return */
  limit?: number;
  /** Skip first N results (pagination) */
  skip?: number;
}

export class Database {
  /** The database name */
  name: string;
  constructor(name: string) { this.name = name }
  /** Close the connection */
  close(): void { }
}
```

Use `{@link symbol}` to link between documented symbols.

## Full Documentation

- Publishing: https://jsr.io/docs/publishing-packages
- Writing docs: https://jsr.io/docs/writing-docs
- Package configuration: https://jsr.io/docs/package-configuration (jsr.json file)
- JSDoc tags: https://docs.deno.com/runtime/reference/cli/doc/#supported-jsdoc-tags
- Why JSR: https://jsr.io/docs/why
- Troubleshooting: https://jsr.io/docs/troubleshooting
- npm compatibility: https://jsr.io/docs/npm-compatibility
- About slow types: https://jsr.io/docs/about-slow-types
