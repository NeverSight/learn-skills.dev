---
name: faasjs-best-practices
description: FaasJS best practices - file conventions, defineFunc, database(knex).
---

Apply these rules when writing or reviewing FaasJS code.

## File conventions

See [File conventions](./file-conventions.md) for:
- Project structure and special files
- Route segments and fallback (`*.func.ts`, `index.func.ts`, `default.func.ts`)
- Verb naming semantics and list endpoint conventions

## defineFunc

See [defineFunc guide](./define-func.md) for:
- When to use `defineFunc` in `*.func.ts` files
- How plugin config from `faas.yaml` is auto-loaded
- A complete endpoint example with typed params

## Knex

See [Knex rules](./knex.md) for:
- Configuring Knex via `faas.yaml` and using query-builder methods over `knex.raw`

## Related skills

- Unit testing: [faasjs-unit-testing](../faasjs-unit-testing/SKILL.md)
