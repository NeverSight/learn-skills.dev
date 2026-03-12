---
name: biome-lint
description: 'Use when fixing Biome linter errors, TypeScript/tsgo type-check errors, or running lint/typecheck workflows'
---

# Biome Lint & TypeScript Type-Check

## Quick Reference

| Error | Fix |
|-------|-----|
| `noImplicitAnyLet` | Add type: `let x;` → `let x: Type;` |
| `noUnusedVariables` | Prefix `_`: `const foo` → `const _foo` |
| `noUnusedFunctionParameters` | Rename in destructure: `{ param }` → `{ param: _param }` |
| `noEmptyPattern` | Replace `{}` with `_opts: object` |
| `noUnreachable` | Remove dead code or wrap in block comment |
| `noInvalidUseBeforeDeclaration` | Move declaration before usage or extract to const |
| `TS2322` | Type assertion or filter: `as Record<string, string>` |
| `TS2345` | Non-null assertion or default: `value!` or `value ?? ''` |
| `TS7030` | Add explicit return: `return undefined;` |
| `TS2339` | Type assertion to extend: `as Type & { prop?: T }` |

## Workflow

### Biome Lint

```bash
# 1. Auto-fix
pnpm biome lint ./src --write

# 2. Check remaining errors
pnpm biome lint ./src

# 3. Fix import type issues
npx -y @biomejs/biome lint --only=style/useImportType ./src --write
```

### TypeScript Check

```bash
# Single package
pnpm tsgo -p tsconfig.json --skipLibCheck --maxNodeModuleJsDepth 0 --noEmit

# All packages
pnpm -r exec just typecheck
```

## Per-Package Rule Override

Create local `biome.json` to override rules:

```json
{
  "root": false,
  "extends": "//",
  "linter": {
    "rules": {
      "correctness": { "useHookAtTopLevel": "warn" },
      "a11y": { "useButtonType": "warn" }
    }
  }
}
```

## biome-ignore Comments

```typescript
// biome-ignore lint/suspicious/noSelfCompare: NaN check
return x !== x;

// biome-ignore lint/correctness/noConstructorReturn: proxy pattern
return new Proxy();
```

## Detailed Guides

- [Biome fixes](references/biome-fixes.md) — Full fix examples for each Biome rule
- [TypeScript fixes](references/typescript-fixes.md) — TS errors, ES version issues, cross-package deps
- [Breaking changes](references/breaking-changes.md) — Zod 4, vitest 4, react-router v7, etc.
