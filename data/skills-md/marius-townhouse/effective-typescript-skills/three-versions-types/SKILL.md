---
name: three-versions-types
description: Use when publishing type declarations. Use when dealing with version conflicts. Use when libraries have types. Use when managing @types packages. Use when debugging type mismatches.
---

# Understand the Three Versions Involved in Type Declarations

## Overview

When working with TypeScript types, three versions must align: the version of the package you're using, the version of its type declarations (@types), and the version of TypeScript itself. Misalignment between these versions can cause confusing type errors even when the code works at runtime.

Understanding these three versions helps diagnose and prevent type compatibility issues.

## The Three Versions

1. **Package version** - The runtime library (e.g., lodash@4.17.21)
2. **@types version** - Type declarations (e.g., @types/lodash@4.14.191)
3. **TypeScript version** - Your TypeScript compiler (e.g., typescript@5.2.2)

## When to Use This Skill

- Publishing type declarations
- Debugging version conflicts
- Working with @types packages
- Managing library dependencies
- Type errors that don't match runtime behavior

## The Iron Rule

**Keep package, @types, and TypeScript versions compatible. Update them together to avoid mysterious type errors.**

## Common Version Issues

```typescript
// Package updated but @types not updated
import { newFeature } from 'library';  // Runtime works
// Error: Module 'library' has no exported member 'newFeature'

// TypeScript too old for new type features
// Error: Type instantiation is excessively deep
// (Newer @types use features old TS doesn't support)

// @types too new for package version
// Types reference features not in actual package
```

## Best Practices

```json
// package.json
{
  "dependencies": {
    "lodash": "^4.17.21"
  },
  "devDependencies": {
    "@types/lodash": "^4.14.191",
    "typescript": "^5.2.2"
  }
}
```

## Checking Versions

```bash
# Check all three versions
npm ls lodash @types/lodash typescript

# Check for outdated packages
npm outdated

# Update together
npm update lodash @types/lodash typescript
```

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 66: Understand the Three Versions Involved in Type Declarations
