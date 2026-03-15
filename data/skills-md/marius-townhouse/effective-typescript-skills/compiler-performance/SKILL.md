---
name: compiler-performance
description: Use when build times are slow. Use when optimizing TypeScript projects. Use when configuring project references. Use when dealing with large codebases. Use when improving IDE responsiveness.
---

# Pay Attention to Compiler Performance

## Overview

TypeScript compilation can become slow in large projects. Monitor and optimize compiler performance using techniques like project references, proper tsconfig settings, and avoiding expensive type patterns. Fast compilation improves developer experience.

## When to Use This Skill

- Build times are slow
- Optimizing TypeScript projects
- Configuring project references
- Working with large codebases
- Improving IDE responsiveness

## The Iron Rule

**Monitor and optimize TypeScript performance. Use project references, avoid expensive type patterns, and keep compilation fast.**

## Performance Tips

```typescript
// AVOID: Expensive recursive types
type DeepPartial<T> = T extends object
  ? { [K in keyof T]?: DeepPartial<T[K]> }
  : T;

// PREFER: Iterative approaches, project references
// Split large projects using project references
```

```json
// tsconfig.json optimizations
{
  "compilerOptions": {
    "incremental": true,        // Incremental compilation
    "tsBuildInfoFile": ".tsbuildinfo"
  }
}
```

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 78: Pay Attention to Compiler Performance
