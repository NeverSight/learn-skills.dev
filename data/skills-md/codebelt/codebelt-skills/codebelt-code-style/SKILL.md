---
name: codebelt-code-style
description: Enforces the CodeBelt TypeScript and React code style guide for project structure, naming conventions, component patterns, service patterns, testing, and TypeScript rules. Use when writing, reviewing, or refactoring TypeScript or React code, creating new files or components, organizing project directories, writing tests, defining Zod schemas, or when the user mentions code style, conventions, linting, file organization, or naming patterns.
---

# CodeBelt Code Style Guide

Opinionated TypeScript and React code style for consistency, maintainability, and scalability. Apply these rules when writing new code, reviewing existing code, or refactoring.

## Quick Reference

### File Placement

| Code Type | Location |
|-----------|----------|
| React component | `components/pages/`, `components/shared/`, or `components/ui/` |
| API logic | `services/{provider}/{service}/` |
| Reusable function | `utils/{utilName}/` |
| React hook | `hooks/use{HookName}/` |
| Third-party config | `libs/{libraryName}/` |

### File Extensions

| Extension | Purpose |
|-----------|---------|
| `.ts{x}` | Main code (`.tsx` only when file contains JSX) |
| `.test.ts` | Tests |
| `.types.ts` | TypeScript types |
| `.utils.ts{x}` | Helper functions |
| `.utils.test.ts` | Tests for utility functions |
| `.schemas.ts` | Zod validation schemas |
| `.schemas.test.ts` | Tests for schemas |
| `.constants.ts{x}` | Static objects and constants |

### Naming Conventions

| Context | Convention | Example |
|---------|------------|---------|
| Component folders | camelCase | `userCard/` |
| Component files | PascalCase | `UserCard.tsx` |
| Everything else | camelCase | `httpClient.ts` |
| Variables/params | Descriptive (no single chars) | `event` not `e` |
| Constants | camelCase | `maxRetries` not `MAX_RETRIES` |

### Exports

All files use **named exports** only:

```typescript
export function Component() {}
```

No default exports. No barrel files in application code.

---

## Workflows

### Creating a New Component

1. Create folder: `components/{pages|shared|ui}/{componentName}/`
2. Create component file: `{ComponentName}.tsx` with Props type and JSX only
3. Extract types to `{ComponentName}.types.ts` (if needed beyond Props)
4. Extract constants to `{ComponentName}.constants.ts` (if any)
5. Extract helpers to `{ComponentName}.utils.ts` (if any)
6. Verify: one component per file, Props not exported, named export

### Creating a New Service

1. Create folder: `services/{provider}/{serviceName}/`
2. Create main file: `{serviceName}Service.ts` with fetch functions and query hooks
3. Create schema file: `{serviceName}Service.schemas.ts` with Zod schemas
4. Create constants file: `{serviceName}Service.constants.ts` with query keys
5. Verify: schema and type share same name, comment with HTTP method and path

### Creating a New Hook

1. Create folder: `hooks/use{HookName}/`
2. Create hook file: `use{HookName}.ts`
3. Create test file: `use{HookName}.test.ts`

### Creating a New Utility

1. Create folder: `utils/{utilName}/`
2. Create main utility file: `{utilName}.ts`
3. Optionally create helper file: `{utilName}.utils.ts` (for additional helpers, only if main file exists)
4. Create test files: `{utilName}.test.ts` and/or `{utilName}.utils.test.ts`

---

## Detailed References

- **Component patterns and hierarchy**: See [COMPONENTS.md](COMPONENTS.md)
- **Service and schema patterns**: See [SERVICES.md](SERVICES.md)
- **Testing patterns**: See [TESTING.md](TESTING.md)
- **Common mistakes to avoid**: See [MISTAKES.md](MISTAKES.md)
