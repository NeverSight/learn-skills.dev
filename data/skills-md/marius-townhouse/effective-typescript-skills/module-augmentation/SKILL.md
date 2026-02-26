---
name: module-augmentation
description: Use when extending third-party types. Use when adding properties to existing interfaces. Use when plugins extend core types. Use when declaration merging is needed. Use when augmenting global types.
---

# Use Module Augmentation to Improve Types

## Overview

Module augmentation allows you to add declarations to existing modules, including third-party libraries. This is useful when a library's types are incomplete or when you're extending a library with plugins. Use `declare module` to add properties, methods, or types to existing modules.

## When to Use This Skill

- Extending third-party types
- Adding properties to existing interfaces
- Plugins that extend core types
- Declaration merging needed
- Augmenting global types

## The Iron Rule

**Use module augmentation to add to existing types. Declare the same module name and add your declarations.**

## Example

```typescript
// Adding to an existing module
// types/vue.d.ts
declare module 'vue' {
  export interface ComponentCustomProperties {
    $myProperty: string;
    $myMethod(): void;
  }
}

// Now Vue components have these properties
// this.$myProperty works with type safety

// Augmenting global types
declare global {
  interface Window {
    myLib: MyLibrary;
  }
}

// Now window.myLib is typed
```

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 71: Use Module Augmentation to Improve Types
