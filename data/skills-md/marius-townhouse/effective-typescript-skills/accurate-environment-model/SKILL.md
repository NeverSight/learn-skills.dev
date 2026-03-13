---
name: accurate-environment-model
description: Use when defining global types. Use when augmenting window. Use when typing environment variables. Use when working with build-time constants. Use when configuring type definitions.
---

# Create an Accurate Model of Your Environment

## Overview

Your TypeScript environment includes globals, environment variables, and platform-specific APIs. Create accurate type definitions for your environment using declaration files (.d.ts). This ensures type safety for platform-specific code and global variables.

## When to Use This Skill

- Defining global types
- Augmenting window or globalThis
- Typing environment variables
- Working with build-time constants
- Configuring type definitions

## The Iron Rule

**Model your environment accurately with .d.ts files. Declare globals, window properties, and environment variables that your code depends on.**

## Example

```typescript
// types/environment.d.ts
declare global {
  interface Window {
    APP_CONFIG: {
      apiUrl: string;
      version: string;
    };
  }
  
  const BUILD_TIMESTAMP: number;
}

// Usage
console.log(window.APP_CONFIG.apiUrl);
console.log(BUILD_TIMESTAMP);
```

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 76: Create an Accurate Model of Your Environment
