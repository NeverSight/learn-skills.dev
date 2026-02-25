---
name: clean-codejs-comments
description: Commenting patterns that improve readability and maintainability.
---

# Clean Code JavaScript – Comment Patterns

## Table of Contents
- When to Comment
- When Not to Comment
- Examples

## When to Comment
- Explain **why**, not **what**
- Document complex business rules

## When Not to Comment
- Obvious code
- Outdated explanations

## Examples

```js
// ❌ Bad
// Increment i by 1
i++;

// ✅ Good
// Retry once to handle flaky network condition
retryRequest();
```
