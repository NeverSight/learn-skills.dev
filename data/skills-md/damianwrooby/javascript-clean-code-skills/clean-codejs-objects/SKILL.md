---
name: clean-codejs-objects
description: Object and class design patterns following Clean Code JavaScript.
---

# Clean Code JavaScript – Object & Class Patterns

## Table of Contents
- Encapsulation
- Immutability
- Cohesion

## Encapsulation

```js
// ❌ Bad
user.name = 'John';

// ✅ Good
user.rename('John');
```

## Immutability

```js
// ❌ Bad
user.age++;

// ✅ Good
const updatedUser = user.withAge(user.age + 1);
```

## Cohesion

```js
// ❌ Bad
class User {
  calculateTax() {}
}

// ✅ Good
class TaxCalculator {
  calculate(user) {}
}
```
