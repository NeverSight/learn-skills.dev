---
name: typescript-coding-standards
license: MIT
description: >-
  Apply shared coding standards when writing, reviewing, or refactoring
  TypeScript in apps, services, workers, and shared packages. Use before editing
  TypeScript functions, types, exports, error handling, or documentation, and
  React components and hooks. Includes conditional React and Next.js rules;
  backend repositories do not require either framework.
---

# TypeScript Coding Standards

Apply these conventions when writing, reviewing, or refactoring TypeScript in
frontend apps, backend services, workers, and shared libraries.

Read the target repository's `AGENTS.md`, package scripts, and lint/test
configuration first. Explicit local requirements take precedence over these
shared defaults. Keep changes within the requested scope; existing violations
do not justify an unrelated repository-wide migration.

## Guides

Read the guides relevant to the change before editing.

| Guide | Read when |
| --- | --- |
| [TypeScript contracts](rules/typescript.md) | Writing or reviewing functions, arguments, types, or constants. |
| [File naming and size](rules/file-naming-and-size.md) | Creating, renaming, or splitting files. |
| [Comments and JSDoc](rules/comments.md) | Documenting functions, types, or non-obvious logic. |
| [Modules and organization](rules/modules.md) | Choosing exports, import boundaries, or where code belongs. |
| [Runtime behavior](rules/runtime.md) | Handling errors, external data, service dependencies, or backend import boundaries. |
| [React and Next.js](rules/react.md) | Changing components, callbacks, or hooks; read the Next.js section only in Next.js apps. |
| [Testing](rules/testing.md) | Deciding whether a test is useful, adding coverage, or reviewing assertions. |
| [Tooling and verification](rules/tooling.md) | Selecting tools or validating a code change. |

For backend-only work, skip the React guide. Use the consumer's existing tooling
and runtime conventions; the skill does not require adopting another repo's
framework, formatter, or dependencies.
