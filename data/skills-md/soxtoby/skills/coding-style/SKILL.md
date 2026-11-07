---
name: coding-style
description: General code style advice. Use when writing any code, reviewing code for style consistency, or when the user asks to follow the coding style guide.
---

# Apply Coding Style

## General
- Use American English spelling for both code and user-facing text.
- Use sentence case for all user-facing text.
- Keep comments sparse and useful. Use them to explain why, not to narrate what the code already says.

## Code structure
- Functions should always be defined below (after) where they are used in the same file, so control flow reads from top to bottom.
- Functions should contain roughly a single level of abstraction. For example, a function that fetches data from an API should not be dealing with low-level HTTP request details, and a function that handles low-level HTTP requests should not be concerned with how the data is used after it is fetched.
- Prefer method chaining (for example, `map`/`filter`) over explicit loops. However, do not use `reduce`/`aggregate`; use an explicit loop instead when a fold is needed.
- Lean on available native methods, helper methods, and library functions and their behavior, rather than writing custom implementations. For example, if a library function throws an argument error when given an invalid input, don't check for that invalid input and throw your own error. Instead, let the library function throw the error and handle it appropriately.
- Use blank lines to separate logical sections of code within functions for better readability.
- If a file grows over 500 lines, consider splitting it into multiple smaller files.

## Naming
- Give related names a shared term for what they have in common, plus a differentiating term for how they contrast: `sourcePath`/`destinationPath`, `minWidth`/`maxWidth`.
- Qualify every variable called `name` with the kind of name it holds: `displayName`, `fileName`, `loginName`.
- Suffix measurements with their unit: `sizeMb`, `timeoutMs`, `widthPx`.
- Name a primitive that references something after the thing it references and the kind of reference: a GUID pointing at a parent resource is `parentResourceId`.
- Case constants like any other member of the same kind: `maxRetries` as a module-level TypeScript constant, `MaxRetries` as a C# `const` field.

## Common code style
- Early returns should only appear at the top of functions, and should have simple conditions. Otherwise, avoid returns scattered at varying depths; structure the function with if/else branches so that all non-early returns occur at the same nesting depth (ideally as the final statement of each branch).
- Lean on structured programming, and avoid goto-like control flow like `break`, `continue`, and `return` statements in the middle of loops where possible.

## C# style
- Use immutable `record`s for data classes instead of `class` when possible.
- Prefer `{ get; init; }` properties in records with many properties or optional properties.

## TypeScript style
- Prefer `let` over `const`.
- Use double equals (`==`) for equality checks unless type coercion makes it necessary to use triple equals (`===`).

## StyleMap
This only applies when using the `stylemap` NPM package for styling.
- Put all `stylemap` `style`s at the end of the file.
- Avoid `Style` suffix in style names unless necessary for clarity or to avoid naming conflicts.
- Follow SMACSS naming conventions for names:
  - Styles for major page layout components are prefixed with `l-`.
  - Modules/Component names are camelCase and sub-components are separated with a single dash (`-`).
  - State styles that modify the appearance based on user interaction or other conditions are prefixed with `is-` and suffixed with `-state` in the form `is-componentName-state`.

## Tests
See the writing-tests skill for general advice on writing tests.