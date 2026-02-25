---
name: clean-codejs-functions
description: Function design patterns emphasizing single responsibility and clarity.
---

# Clean Code JavaScript – Function Patterns

## Table of Contents
- Single Responsibility
- Function Size
- Parameters
- Side Effects

## Single Responsibility

```js
// ❌ Bad
function handleUser(user) {
  saveUser(user);
  sendEmail(user);
}

// ✅ Good
function saveUser(user) {}
function notifyUser(user) {}
```

## Function Size

Keep functions small (ideally < 20 lines).

## Parameters

```js
// ❌ Bad
function createUser(name, age, city, zip) {}

// ✅ Good
function createUser({ name, age, address }) {}
```

## Side Effects

```js
// ❌ Bad
let total = 0;
function add(value) {
  total += value;
}

// ✅ Good
function add(total, value) {
  return total + value;
}
```
