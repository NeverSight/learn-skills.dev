---
name: using-jsdoc
description: Guide for documenting JavaScript and TypeScript code using JSDoc. Use when adding documentation to functions, classes, methods, variables, types, interfaces, modules, or any code element. Includes tag syntax, type expressions, patterns for parameters, returns, generics, and TypeScript-specific documentation. Trigger with phrases like "document this function", "add JSDoc", "document with JSDoc", or "add documentation comments".
license: MIT
---

# JSDoc Documentation Guide

Comprehensive guide for documenting JavaScript and TypeScript code using JSDoc standard comments.

## Overview

JSDoc is a markup language for annotating JavaScript source code with type information and documentation. This skill provides:

- Complete JSDoc tag reference based on [jsdoc.app](https://jsdoc.app/)
- Type expression syntax for both JavaScript and TypeScript
- Patterns for documenting functions, classes, types, and modules
- Best practices with good/bad examples
- Integration guidance for TypeScript projects

## Prerequisites

- Basic JavaScript or TypeScript knowledge
- Code editor (any that supports JSDoc comments)
- Optional: JSDoc CLI tool for generating documentation (`npm install -g jsdoc`)
- For TypeScript: `@types` packages for better IntelliSense

## Instructions

### 1. Use Basic JSDoc Syntax

Start JSDoc comments with `/**` and place them directly before the code element:

```javascript
/**
 * Brief description of the function.
 * @param {string} name - Parameter description.
 * @returns {boolean} Description of the returned value.
 */
function example(name) {
	return true;
}
```

### 2. Document Functions and Methods

```javascript
/**
 * Calculates the total with taxes.
 * @param {number} price - Base price.
 * @param {number} [tax=0.21] - Tax percentage (optional).
 * @returns {number} Price with tax applied.
 * @throws {Error} If the price is negative.
 * @example
 * calculateTotal(100);       // 121
 * calculateTotal(100, 0.10); // 110
 */
function calculateTotal(price, tax = 0.21) {
	if (price < 0) throw new Error("Invalid price");
	return price * (1 + tax);
}
```

### 3. Document Object Parameters

For functions accepting objects, document nested properties:

```javascript
/**
 * Creates a user.
 * @param {Object} config - User configuration.
 * @param {string} config.name - Full name.
 * @param {string} config.email - Contact email.
 * @param {number} [config.age] - Age (optional).
 */
function createUser({ name, email, age }) {}
```

### 4. Define Custom Types

Use `@typedef` for reusable type definitions:

```javascript
/**
 * @typedef {Object} User
 * @property {string} id - Unique identifier.
 * @property {string} name - User name.
 * @property {string} [avatar] - Avatar URL (optional).
 */

/**
 * Gets a user by ID.
 * @param {string} id
 * @returns {User}
 */
function getUser(id) {}
```

### 5. Document Classes

Include class-level docs and document constructor, properties, and methods:

```javascript
/**
 * Represents a database connection.
 * @class
 */
class DatabaseConnection {
	/**
	 * Creates a new connection.
	 * @param {string} connectionString - Connection URL.
	 */
	constructor(connectionString) {
		/** @type {string} */
		this.url = connectionString;

		/** @private */
		this._connected = false;
	}

	/**
	 * Executes a query.
	 * @param {string} sql - SQL query.
	 * @returns {Promise<Object[]>} Results.
	 * @async
	 */
	async query(sql) {}
}
```

### 6. Use Type Expressions

JSDoc supports rich type syntax:

| Expression                    | Meaning                        |
| ----------------------------- | ------------------------------ |
| `{string}`                    | String                         |
| `{number}`                    | Number                         |
| `{boolean}`                   | Boolean                        |
| `{Object}`                    | Generic object                 |
| `{Array}` or `{any[]}`        | Array                          |
| `{string[]}`                  | Array of strings               |
| `{(string\|number)}`          | String OR number (union)       |
| `{?string}`                   | String or null (nullable)      |
| `{!string}`                   | String, never null             |
| `{*}`                         | Any type                       |
| `{...number}`                 | Multiple numbers (rest params) |
| `{function}`                  | Generic function               |
| `{function(string): boolean}` | Function with signature        |
| `{Promise<User>}`             | Promise that resolves to User  |
| `{Map<string, number>}`       | Map with specific types        |

### 7. Integrate with TypeScript

In TypeScript, JSDoc complements native type annotations. Use mainly for:

- Parameter and return descriptions
- Usage examples
- Deprecation documentation
- Additional information (@see, @since, @author)

```typescript
/**
 * Formats a date according to the specified locale.
 * @param date - Date to format.
 * @param locale - Locale code (e.g., 'en-US').
 * @returns Formatted date as string.
 * @example
 * formatDate(new Date(), 'en-US'); // "2/9/2026"
 * @since 2.0.0
 * @see {@link https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat}
 */
function formatDate(date: Date, locale: string): string {
	return new Intl.DateTimeFormat(locale).format(date);
}
```

**Generics:**

```typescript
/**
 * Wraps a value in a Result object.
 * @template T - Type of the value.
 * @param value - Value to wrap.
 * @returns Result object with the value.
 */
function ok<T>(value: T): Result<T> {
	return { success: true, value };
}
```

### 8. Apply Best Practices

1. **Describe the "what" and "why"**, not the "how" (the code already shows that)
2. **Document optional parameters** with `[param]` or `[param=default]`
3. **Use @example** for non-obvious use cases
4. **Mark obsolete code** with `@deprecated` including an alternative
5. **In TypeScript**, prioritize native types over JSDoc annotations
6. **Keep documentation synchronized** with the code

For detailed examples of correct and incorrect usage, see [references/best-practices.md](references/best-practices.md).

## Tag Reference

For a complete list of available tags, see [references/tags.md](references/tags.md).

**Most used tags:**

- `@param` - Function parameters
- `@returns` / `@return` - Return value
- `@type` - Variable type
- `@typedef` - Define custom type
- `@property` / `@prop` - Object property
- `@throws` / `@exception` - Errors that can be thrown
- `@example` - Usage example
- `@deprecated` - Mark as obsolete
- `@async` - Async function
- `@template` - Generic parameter

**Quick Example:**

```javascript
// Bad - restates the code
/**
 * Adds two numbers and returns the result.
 * @param {number} a - First number.
 * @param {number} b - Second number.
 * @returns {number} The sum.
 */
function add(a, b) {
	return a + b;
}

// Good - explains purpose and edge cases
/**
 * Combines line items into a single total.
 * Handles currency rounding to avoid floating-point errors.
 * @param {number} subtotal - Pre-tax amount in cents.
 * @param {number} tax - Tax amount in cents.
 * @returns {number} Total in cents, always rounded to nearest integer.
 */
function calculateTotal(subtotal, tax) {
	return Math.round(subtotal + tax);
}
```

## Output

When documenting code with JSDoc, you create:

- **Inline documentation** - Comments directly in source files that IDEs can read
- **IntelliSense support** - Autocomplete and type hints in editors (VS Code, WebStorm, etc.)
- **Generated HTML documentation** - Beautiful API docs via JSDoc CLI (`jsdoc src/**/*.js`)
- **TypeScript type checking** - JSDoc can be used in `.js` files with `// @ts-check`
- **Better code navigation** - Jump to definitions and find references

## Examples

**Example: Document a utility function**

Request: "Add JSDoc documentation to this validation function"

```javascript
// Before
function validateEmail(email) {
	return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// After
/**
 * Validates email address format using RFC 5322 simplified regex.
 * Does not verify deliverability, only basic structure.
 * @param {string} email - Email address to validate.
 * @returns {boolean} True if format is valid, false otherwise.
 * @example
 * validateEmail('user@example.com');  // true
 * validateEmail('invalid-email');     // false
 */
function validateEmail(email) {
	return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
```

**Example: Document a class with TypeScript generics**

Request: "Document this generic cache class with JSDoc"

```typescript
/**
 * In-memory cache with TTL expiration.
 * @template K - Key type (must be string or number).
 * @template V - Value type to store.
 * @example
 * const userCache = new Cache<string, User>(5000);
 * userCache.set('user-1', userData);
 * const user = userCache.get('user-1');
 */
class Cache<K extends string | number, V> {
	/**
	 * Creates a new cache instance.
	 * @param ttl - Time to live in milliseconds.
	 */
	constructor(private ttl: number) {}

	/**
	 * Stores a value with expiration.
	 * @param key - Cache key.
	 * @param value - Value to cache.
	 */
	set(key: K, value: V): void {}

	/**
	 * Retrieves a cached value if not expired.
	 * @param key - Cache key.
	 * @returns Cached value or undefined if expired/missing.
	 */
	get(key: K): V | undefined {}
}
```

## Resources

- [Official JSDoc documentation](https://jsdoc.app/) - Complete tag reference and usage guides
- [TypeScript JSDoc support](https://www.typescriptlang.org/docs/handbook/jsdoc-supported-types.html) - TS-specific JSDoc features
- [Google Closure Compiler types](https://github.com/google/closure-compiler/wiki/Annotating-JavaScript-for-the-Closure-Compiler) - Advanced type expressions
- [JSDoc CLI tool](https://github.com/jsdoc/jsdoc) - Generate HTML documentation from JSDoc comments
- [Better Comments extension](https://marketplace.visualstudio.com/items?itemName=aaron-bond.better-comments) - VS Code syntax highlighting for comments
- [references/tags.md](references/tags.md) - Complete table of all JSDoc tags with examples
- [references/best-practices.md](references/best-practices.md) - Detailed good/bad examples and common mistakes
