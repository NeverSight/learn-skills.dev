---
name: dom-hierarchy
description: Use when working with DOM APIs. Use when typing element references. Use when creating DOM utilities. Use when handling events. Use when manipulating the DOM.
---

# Understand the DOM Hierarchy

## Overview

TypeScript's DOM types accurately model the browser's DOM hierarchy. Understanding this hierarchy - Element extends Node, HTMLElement extends Element, etc. - helps you write correct DOM code. Use the most specific type possible for better autocompletion and type safety.

## When to Use This Skill

- Working with DOM APIs
- Typing element references
- Creating DOM utilities
- Handling DOM events
- Manipulating the DOM

## The Iron Rule

**Use the most specific DOM type possible. HTMLElement for HTML elements, HTMLInputElement for inputs, etc.**

## DOM Type Hierarchy

```
EventTarget
  └── Node
       └── Element
            └── HTMLElement
            │    └── HTMLInputElement
            │    └── HTMLButtonElement
            │    └── etc.
            └── SVGElement
```

## Example

```typescript
// BAD: Too general
const el: Element = document.getElementById('input');
el.value; // Error: Property 'value' doesn't exist on Element

// GOOD: Specific type
const input = document.getElementById('input') as HTMLInputElement;
input.value; // OK - value exists on HTMLInputElement

// Even better: Use querySelector with type parameter
const button = document.querySelector<HTMLButtonElement>('button.submit');
button?.disabled; // Typed correctly
```

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 75: Understand the DOM Hierarchy
