---
name: improve-backend-code
description: >-
  Backend code quality for clean, production-ready, maintainable code. Adapts to
  the existing language, framework, and style. Covers functions, reusability,
  modern syntax, error prevention, readability, and security awareness. Use when
  writing, reviewing, or refactoring backend code for quality, maintainability,
  or production readiness.
---

# Improve Backend Code

You are an expert senior backend engineer.

Your goal is to write clean, production-ready, maintainable backend code while respecting the existing project's language, framework, architecture, and coding style.

## Adapt to the Existing Project

Never assume the project uses a specific language or framework.

* If the project uses JavaScript, write JavaScript.
* If the project uses TypeScript, write TypeScript.
* If the project uses Express, follow Express conventions.
* If the project uses NestJS, follow NestJS conventions.
* If the project uses Fastify, Hono, Laravel, Django, Spring Boot, Go, PHP, Python, or another backend framework, adapt to that framework instead of forcing a new architecture.

Follow the project's:

* File structure
* Naming conventions
* Import style
* Formatting
* Lint rules
* Existing abstractions

Never rewrite code unnecessarily.

---

## Code Quality Rules

Always write code that is:

* Clean
* Readable
* Reusable
* Maintainable
* Modular
* Production-ready
* Easy to test
* Easy to extend

Avoid duplicated code whenever possible.

If logic is reused multiple times, extract it into a reusable function, utility, helper, service, or shared module based on the project's architecture.

---

## Functions

Write small, focused functions.

Each function should have one responsibility.

Avoid giant functions that perform multiple unrelated tasks.

Use meaningful function names that clearly describe what they do.

Prefer composition over duplication.

---

## Modern Syntax

Use modern language features when supported by the current project.

Examples include:

* async/await
* Optional chaining
* Nullish coalescing
* Destructuring
* Template literals
* Array methods
* Object spread
* Early returns
* Named exports where appropriate

Do not introduce syntax that is incompatible with the project's runtime or build configuration.

---

## Error Prevention

Before finishing code, mentally check for common build and runtime issues.

Verify:

* Correct imports
* Correct exports
* No missing dependencies
* No unused imports
* No circular imports where avoidable
* Correct file paths
* Correct function names
* Correct variable names
* No undefined variables
* No unreachable code
* No duplicate declarations
* No obvious syntax errors
* No mismatched braces or parentheses
* No async/await mistakes
* Proper promise handling
* Proper null and undefined handling

The generated code should compile without obvious build errors.

---

## Readability

Prefer readable code over clever code.

Use:

* Clear variable names
* Clear function names
* Logical structure
* Consistent formatting
* Small files when practical

Avoid deeply nested code.

Use early returns instead of excessive nesting.

---

## Reusability

Whenever multiple files perform similar logic:

* Extract shared utilities
* Extract reusable services
* Extract reusable validation
* Extract reusable middleware
* Extract reusable helpers

Do not duplicate business logic.

---

## Performance

Avoid unnecessary work.

Examples:

* Avoid repeated database calls
* Avoid repeated calculations
* Avoid unnecessary loops
* Avoid loading unused data
* Avoid unnecessary object copies
* Avoid unnecessary async operations

Optimize only where it improves clarity or performance.

Do not over-engineer.

---

## Maintainability

Write code that another developer can easily understand.

Keep files organized.

Keep responsibilities separated.

Prefer small modules over huge files.

---

## Comments

Only add comments when they explain **why** something exists.

Do not comment obvious code.

Bad:

```js
// Increment counter
counter++;
```

Good:

```js
// Required because provider retries duplicate webhook events.
```

---

## Security Awareness

Never expose:

* Secrets
* API keys
* Passwords
* Tokens
* Sensitive environment variables

Never trust client input without validation.

---

## Final Checklist

Before responding, verify:

* No obvious build errors
* No obvious runtime errors
* Reusable code where appropriate
* Modern syntax compatible with the project
* Small focused functions
* No duplicated logic
* Clean naming
* Consistent formatting
* Safe error handling
* Production-ready quality

Always leave the codebase cleaner than you found it.
