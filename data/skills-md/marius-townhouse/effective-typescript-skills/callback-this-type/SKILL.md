---
name: callback-this-type
description: Use when callbacks use this. Use when API provides this context. Use when typing event handlers. Use when library sets this in callbacks. Use when documenting callback context.
---

# Provide a Type for this in Callbacks if It's Part of Their API

## Overview

When a library calls a user-provided callback with a specific `this` context, that context is part of the API. TypeScript allows you to type `this` as the first parameter of a function, even though it's not a real parameter. This documents and enforces the expected context.

## When to Use This Skill

- Callbacks use `this`
- API provides `this` context
- Typing event handlers
- Library sets `this` in callbacks
- Documenting callback context

## The Iron Rule

**Type `this` as the first parameter when it's part of your callback API. This documents the expected context and enables autocompletion.**

## Example

```typescript
// BAD: this is untyped
interface EventEmitter {
  on(event: string, handler: (data: any) => void): void;
}

// User doesn't know what 'this' is:
emitter.on('click', function(data) {
  this.something; // What properties does this have?
});

// GOOD: this is typed
interface EventEmitter {
  on(
    event: string,
    handler: (this: EventContext, data: any) => void
  ): void;
}

interface EventContext {
  target: Element;
  timestamp: number;
  preventDefault(): void;
}

// User now gets autocompletion for 'this'
emitter.on('click', function(data) {
  this.target; // Autocomplete works!
  this.timestamp; // Typed as number
});
```

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 69: Provide a Type for this in Callbacks if It's Part of Their API
