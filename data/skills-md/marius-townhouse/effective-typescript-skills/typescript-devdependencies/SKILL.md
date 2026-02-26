---
name: typescript-devdependencies
description: Use when setting up TypeScript projects. Use when installing @types packages. Use when configuring package.json. Use when publishing libraries. Use when managing dependencies.
---

# Put TypeScript and @types in devDependencies

## Overview

TypeScript is a development tool - it doesn't exist at runtime. Similarly, @types packages contain only type declarations, not runtime code. Both should be installed as devDependencies, not dependencies. This keeps production builds lean and prevents version conflicts.

Understanding the distinction between dependencies and devDependencies is crucial for library authors and application developers alike.

## When to Use This Skill

- Setting up a new TypeScript project
- Installing @types packages
- Configuring package.json dependencies
- Publishing TypeScript libraries
- Managing project dependencies

## The Iron Rule

**TypeScript and @types packages belong in devDependencies. They are development-only tools and don't exist at runtime.**

## Detection

Watch for these package.json issues:

```json
{
  "dependencies": {
    "typescript": "^5.0.0",      // WRONG: Should be devDependency
    "@types/node": "^20.0.0",    // WRONG: Should be devDependency
    "@types/react": "^18.0.0"    // WRONG: Should be devDependency
  }
}
```

## Correct Setup

```json
{
  "devDependencies": {
    "typescript": "^5.2.2",
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0"
  },
  "dependencies": {
    "react": "^18.2.0"  // Runtime dependency
  }
}
```

## Installation Commands

```bash
# TypeScript itself - dev dependency
npm install --save-dev typescript

# @types for runtime dependencies - also dev dependency
npm install react                    # Runtime dependency
npm install --save-dev @types/react  # Type definitions

# @types for Node.js built-ins
npm install --save-dev @types/node
```

## Why devDependencies?

```typescript
// TypeScript compiles away - not in output
const greeting: string = "Hello";  // Type annotation
// Compiles to:
const greeting = "Hello";  // No types in JS output

// @types packages contain only .d.ts files
// No runtime code - safe to exclude from production
```

## Library Publishing

```json
{
  "name": "my-library",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "dependencies": {
    "lodash": "^4.17.0"  // Runtime dependency
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "@types/lodash": "^4.14.0"
  },
  "peerDependencies": {
    "react": "^18.0.0"  // User provides this
  },
  "peerDependenciesMeta": {
    "react": {
      "optional": true
    }
  }
}
```

## Checking Your Setup

```bash
# See what's in dependencies vs devDependencies
npm list --prod        # Production dependencies only
npm list --dev         # Dev dependencies only

# Check for misplaced TypeScript dependencies
npm ls typescript @types/*
```

## Pressure Resistance Protocol

When setting up dependencies:

1. **Ask: Does this run in production?** TypeScript and @types don't
2. **Use --save-dev for types**: Always for @types packages
3. **Check before publishing**: npm pack shows what gets published
4. **Review package.json**: Ensure correct categorization

## Red Flags

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| `typescript` in dependencies | Bloats production | Move to devDependencies |
| `@types/*` in dependencies | Unnecessary in production | Move to devDependencies |
| Missing @types for deps | No type safety | Add @types as devDependency |

## Common Rationalizations

### "I want TypeScript available globally"

**Reality**: Use `npx tsc` to run the project's TypeScript version. Global installs cause version mismatches.

### "@types should match the runtime package"

**Reality**: The runtime package goes in dependencies, @types goes in devDependencies. They work together but serve different purposes.

### "It doesn't matter for applications"

**Reality**: It keeps node_modules smaller and makes intent clear. Good practice everywhere.

## Quick Reference

| Package Type | Install With | Example |
|--------------|--------------|---------|
| TypeScript | `--save-dev` | `npm i -D typescript` |
| @types/* | `--save-dev` | `npm i -D @types/node` |
| Runtime library | `--save` | `npm i lodash` |
| Types for library | `--save-dev` | `npm i -D @types/lodash` |

## The Bottom Line

TypeScript and @types are development tools. Install them as devDependencies to keep production builds lean and avoid confusion about what runs at runtime.

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 65: Put TypeScript and @types in devDependencies
