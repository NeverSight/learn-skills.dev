---
name: module-by-module-migration
description: Use when migrating large codebases. Use when converting JavaScript to TypeScript. Use when managing dependencies. Use when planning migration order. Use when teams are adopting TypeScript.
---

# Convert Module by Module Up Your Dependency Graph

## Overview

When migrating JavaScript to TypeScript, follow the dependency graph: start with leaf modules (those with no dependencies) and work upward. This ensures that when you convert a module, all its dependencies are already typed. This minimizes type errors and makes migration manageable.

## When to Use This Skill

- Migrating large codebases to TypeScript
- Converting JavaScript to TypeScript
- Managing dependencies during migration
- Planning migration order
- Teams adopting TypeScript

## The Iron Rule

**Migrate modules starting from leaves (no dependencies) and work up the dependency graph. This ensures dependencies are typed before dependents.**

## Migration Order

```
Leaf modules (no dependencies):
  - utils.js → utils.ts
  - constants.js → constants.ts
  - helpers.js → helpers.ts

Middle modules (depend on leaves):
  - api.js → api.ts
  - components.js → components.ts

Entry points (most dependencies):
  - app.js → app.ts
  - index.js → index.ts
```

## Example

```bash
# 1. Convert utilities first (no dependencies)
# utils.js → utils.ts
# constants.js → constants.ts

# 2. Then services (depend on utilities)
# api.js → api.ts
# store.js → store.ts

# 3. Finally entry points (depend on everything)
# app.js → app.ts
# main.js → main.ts
```

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 82: Convert Module by Module Up Your Dependency Graph
