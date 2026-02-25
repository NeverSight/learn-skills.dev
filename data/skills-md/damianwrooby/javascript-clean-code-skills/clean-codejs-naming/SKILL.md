---
name: clean-codejs-naming
description: Naming patterns and conventions based on Clean Code JavaScript principles.
---

# Clean Code JavaScript – Naming Patterns

## Table of Contents
- Principles
- Variables
- Functions
- Booleans
- Bad vs Good Examples

## Principles
- Names should reveal intent
- Avoid abbreviations and mental mapping
- Use domain language consistently

## Variables

```js
// ❌ Bad
const d = 86400000;

// ✅ Good
const MILLISECONDS_PER_DAY = 86400000;
```

## Functions

```js
// ❌ Bad
function getUser(u) {}

// ✅ Good
function fetchUserById(userId) {}
```

## Booleans

```js
// ❌ Bad
if (!user.isNotActive) {}

// ✅ Good
if (user.isActive) {}
```

## Bad vs Good Examples

```js
// ❌ Bad
const data = getData();

// ✅ Good
const usersResponse = fetchUsers();
```
