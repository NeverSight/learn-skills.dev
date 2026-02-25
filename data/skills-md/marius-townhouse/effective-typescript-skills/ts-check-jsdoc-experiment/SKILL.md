---
name: ts-check-jsdoc-experiment
description: Use when experimenting with TypeScript. Use when migrating JavaScript gradually. Use when adding types to JS files. Use when teams are learning TypeScript. Use when validating JavaScript with types.
---

# Use @ts-check and JSDoc to Experiment with TypeScript

## Overview

You can add TypeScript type checking to JavaScript files without converting them to TypeScript. Use `@ts-check` at the top of a JS file and JSDoc annotations to add types. This lets you experiment with TypeScript gradually without committing to the full conversion.

## When to Use This Skill

- Experimenting with TypeScript
- Gradually migrating JavaScript
- Adding types to JS files
- Teams learning TypeScript
- Validating JavaScript with types

## The Iron Rule

**Use `@ts-check` and JSDoc to add TypeScript checking to JavaScript files without full conversion.**

## Example

```javascript
// @ts-check

/**
 * @param {string} name
 * @param {number} age
 * @returns {string}
 */
function greet(name, age) {
  return `Hello ${name}, you are ${age}`;
}

greet('Alice', 30); // OK
greet('Alice', '30'); // Type error!

/** @type {string[]} */
const names = ['Alice', 'Bob'];

/** @typedef {{ x: number, y: number }} Point */
/** @type {Point} */
const point = { x: 1, y: 2 };
```

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 80: Use @ts-check and JSDoc to Experiment with TypeScript
