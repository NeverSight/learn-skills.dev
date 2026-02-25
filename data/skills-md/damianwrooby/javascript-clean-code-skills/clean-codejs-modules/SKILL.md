---
name: clean-codejs-modules
description: Module and file-structure patterns for clean JavaScript architecture.
---

# Clean Code JavaScript – Module Patterns

## Table of Contents
- One Responsibility per Module
- Export Patterns
- Folder Structure

## One Responsibility per Module

```js
// ❌ Bad
// user.js
export function createUser() {}
export function connectToDb() {}
```

```js
// ✅ Good
// user.service.js
export function createUser() {}
```

## Export Patterns

```js
// ✅ Prefer named exports
export function parseDate() {}
export function formatDate() {}
```

## Folder Structure

```
/users
  user.service.js
  user.repository.js
  user.controller.js
```
