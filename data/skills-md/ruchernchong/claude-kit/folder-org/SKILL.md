---
name: folder-org
description: Project code structure and file organization. Use when creating files, organizing components, or deciding where code should live. (project)
---

# Folder Structure

## Core Principle: Colocation

> Place code as close to where it's relevant as possible. Things that change together should be located together.

## Organization Approaches

### Feature-Based (Recommended for Frontend)

Group by domain - all related code in one place:

```
src/features/
├── auth/
│   ├── components/
│   ├── hooks/
│   ├── auth.service.ts
│   └── auth.test.ts
├── users/
└── products/
```

### Layer-Based (Common for Backend)

Group by technical layer:

```
src/
├── controllers/
├── services/
├── models/
├── routes/
└── middleware/
```

### Monorepo

```
apps/           # Applications
├── web/
├── api/
packages/       # Shared libraries (by domain, not language)
├── types/
├── utils/
└── ui/
```

## Where to Put Things

| Type | Location |
|------|----------|
| Shared types | `types/` or `packages/types/` |
| Utilities | `lib/` or `utils/` (split by domain) |
| Config | `config/` or root |
| Unit tests | Colocate: `foo.test.ts` next to `foo.ts` |
| E2E tests | `e2e/` or `tests/e2e/` |
| Mocks/fixtures | `__mocks__/` or `test/mocks/` |

## Naming Conventions

| Type | Convention |
|------|------------|
| Files | `kebab-case.ts` |
| Unit tests | `*.test.ts` |
| E2E tests | `*.e2e.ts` |
| Schemas | `*.schema.ts` |

## Anti-Patterns

- **Catch-all files**: Avoid `utils.ts`, `helpers.ts` - split by domain
- **Deep nesting**: Keep < 4 levels, use descriptive names instead
- **Separated unit tests**: Don't put all in `__tests__/` - colocate instead
- **Language grouping**: In monorepos, group by domain not language
- **Bloated barrels**: Avoid `index.ts` with 50+ re-exports
