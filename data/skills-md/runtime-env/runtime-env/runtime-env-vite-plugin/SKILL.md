---
name: runtime-env-vite-plugin
description: Guidance on using runtime-env with Vite to distinguish between runtime and build-time environment variables.
metadata:
  workflows:
    - ./references/01-setup.md
    - ./references/02-discovery.md
    - ./references/03-migration.md
  guides:
    - ./references/the-string-trap.md
---

# runtime-env-vite-plugin

This skill ensures that environment variables are handled correctly in Vite projects by distinguishing between build-time (static) variables and runtime (dynamic) variables. It enforces a sequential workflow to ensure proper analysis and clean implementation.

## When to apply

You **MUST** apply this skill when:

- Setting up a new Vite project that requires environment variables.
- Refactoring an existing Vite project to use runtime environment variables.
- Adding new environment variables to a project already using `@runtime-env/vite-plugin`.

## Execution Sequence

This skill **MUST** be executed in the following order. Do not skip steps:

1.  **[01 - Setup](./references/01-setup.md)**: Infrastructure, installation, and initial configuration.
2.  **[02 - Discovery](./references/02-discovery.md)**: Analyzing the codebase to identify variables and their true types (The "Think" phase).
3.  **[03 - Migration](./references/03-migration.md)**: Applying the schema and updating the source code (The "Act" phase).

## Pattern Guides

- **[The String Trap](./references/the-string-trap.md)**: How to avoid manual parsing and leverage `runtimeEnv` for type safety.

## Core Mandates

- **Never** assume a variable is a string just because it was one in a legacy file. Always perform discovery.
- **Always** remove manual parsing logic (`parseInt`, `JSON.parse`) during migration.
- **Always** run `npx runtime-env gen-ts` after updating the schema.
- **Always** place the script tag in `index.html` before the app entry point.

### Strict Prohibitions

- **NEVER** use the `default` keyword in `.runtimeenvschema.json`. All environment values must originate from the environment.
- **NEVER** modify or delete existing `.env` files. They are read-only sources of truth.
- **NEVER** add `import { runtimeEnv } from ...` or similar. `runtimeEnv` is a global.
- **NEVER** add redundant `gen-ts` or `gen-js` scripts to `package.json`.
