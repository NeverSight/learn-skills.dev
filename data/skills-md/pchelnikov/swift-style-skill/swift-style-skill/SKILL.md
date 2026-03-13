---
name: swift-style-skill
description: >
  Enforce consistent, idiomatic Swift style when generating, reviewing, or
  refactoring Swift code. Use when writing new Swift code, reviewing code for
  style violations, or enforcing team style standards. Covers file structure,
  naming, formatting, and programming practices. Based on the Google Swift
  Style Guide (https://google.github.io/swift/), which is itself grounded in
  Apple's Swift standard library style and widely adopted across the Swift
  community.
---

# Swift Style Guide

## Overview

Use this skill to ensure Swift code is consistently styled, readable, and
idiomatic. It covers source file structure, naming conventions, general
formatting, construct-specific formatting, and programming practices. This skill
focuses on style and correctness — it does not enforce architecture or
framework-specific patterns.

## Workflow Decision Tree

### 1) Generate new Swift code
- Apply naming conventions before writing any symbol (see [Naming](#naming))
- Structure the file with imports first, then types, using `// MARK:` for organisation (see `references/FILE_STRUCTURE.md`)
- Keep lines within 100 characters; wrap function signatures and calls vertically (see `references/FORMATTING.md`)
- Use `guard` for early exits; avoid force unwrapping (see `references/PRACTICES.md`)
- Write documentation comments for all public API surface (see `references/FILE_STRUCTURE.md`)

### 2) Review existing Swift code
- Check naming: UpperCamelCase for types, lowerCamelCase for everything else (see [Quick Reference](#quick-reference-violations--corrections))
- Verify imports are explicit, minimal, and lexicographically ordered (see `references/FILE_STRUCTURE.md`)
- Check formatting: 100-char limit, K&R braces, no semicolons, no horizontal alignment (see `references/FORMATTING.md`)
- Check practices: no force unwraps, no IUOs, access levels specified explicitly, guard for early exits (see `references/PRACTICES.md`)
- Run through the [Review Checklist](#review-checklist) systematically

### 3) Enforce style on a specific category
- **Formatting only** → `references/FORMATTING.md`
- **Naming only** → `references/NAMING.md`
- **File/import structure** → `references/FILE_STRUCTURE.md`
- **Programming practices** → `references/PRACTICES.md`

### 4) Answer questions about style rules
- Identify which category the question belongs to
- Route to the appropriate reference file for the full rule and examples
- When a rule has a rationale, include it briefly

## Core Guidelines

### Naming

- **Use UpperCamelCase** for types (classes, structs, enums, protocols) and enum cases.
- **Use lowerCamelCase** for functions, methods, properties, parameters, and local variables.
- **Use all-caps for acronyms** only when the entire name is an acronym (`URL`, `HTTPSConnection`); otherwise apply casing rules normally (`urlString`, `httpRequest`).
- **Name for clarity at the call site**, not at the declaration site. Prefer `insert(element, at: index)` over `insert(element, position: index)`.
- **Omit needless words.** Don't repeat type information in names: prefer `users.remove(at: index)` over `users.removeElement(atIndex: index)`.
- **Prefix delegate method names** with the name of the delegating type: `func sessionDidExpire(_ session: Session)`.
- **Do not use naming conventions as access control.** A leading underscore does not make something private — use `private`.

### Formatting

- **100-character column limit.** Wrap anything that would exceed it.
- **No semicolons.** Never use `;` to terminate or separate statements.
- **One statement per line.** Exceptions only for trivial single-statement blocks (e.g., `guard let x = x else { return }`).
- **K&R brace style.** Opening brace on the same line; closing brace on its own line. `else` follows the closing brace: `} else {`.
- **2-space indentation.** No tabs.
- **No horizontal alignment.** Do not add extra spaces to align tokens across lines.
- **Vertical comma-delimited lists.** When wrapping, each element gets its own line at +2 indent; do not mix horizontal and vertical in the same list.

### File Structure

- **One primary type per file**, named after that type. Protocol extensions use `Type+Protocol.swift`.
- **Explicit, minimal imports.** Import exactly what you need — no more, no less. Do not rely on transitive imports.
- **Lexicographic import ordering** with a blank line between groups: standard modules first, then third-party, then `@testable`.
- **Use `// MARK:`** comments to label logical sections within a type. Use `// MARK: -` for a visual divider in Xcode's navigation bar.
- **Document all public API** with documentation comments (`///`). Single-line summary first; parameters/returns/throws tags after a blank line.

### Programming Practices

- **Resolve all compiler warnings.** Warnings are errors waiting to happen.
- **No force unwrap (`!`) except in tests and `fatalError` paths.** Use `guard let`, `if let`, or `??` instead.
- **No implicitly unwrapped optionals (IUOs)** except for `@IBOutlet`/`@IBAction` and values that cannot be set in `init`.
- **Use `guard` for early exits.** Prefer `guard` over deeply nested `if` for precondition checking.
- **Specify access levels explicitly.** Do not rely on the `internal` default — make intent clear.
- **Prefer `for`-`where` over nested `if` inside a loop** when filtering iteration.
- **Use shorthand type names** (`[String]`, `[String: Int]`, `String?`) over their longhand equivalents.
- **Avoid `fallthrough` in `switch`** unless absolutely necessary. Prefer separate cases or comma-joined patterns.

## Quick Reference: Violations → Corrections

| ❌ Avoid | ✅ Prefer | Rule |
|---------|----------|------|
| `class myViewController` | `class MyViewController` | UpperCamelCase for types |
| `var URL: String` | `var url: String` | lowerCamelCase for properties |
| `enum direction { case North }` | `enum Direction { case north }` | UpperCamelCase for types and cases |
| `let HTTPSUrl` | `let httpsURL` | Acronyms follow casing rules |
| `func removeElement(atIndex i: Int)` | `func remove(at i: Int)` | Omit needless words |
| `var _name: String` (as privacy) | `private var name: String` | Use access control, not underscores |
| `import UIKit; import Foundation` | One import per line, no semicolons | No semicolons |
| `if x == 0 { return }; doWork()` | Two lines, no semicolons | One statement per line |
| `} else {` on new line | `} else {` on same line | K&R braces |
| `let x  = 1` (aligned with `let yy = 2`) | `let x = 1` | No horizontal alignment |
| `let name = user!.name` | `guard let name = user?.name else { return }` | No force unwrap |
| `var delegate: MyDelegate!` (no IBOutlet) | `var delegate: MyDelegate?` | No IUO outside IBOutlet/init |
| `import UIKit.UITableView` | `import UIKit` | Whole-module imports preferred |
| `let arr: Array<String>` | `let arr: [String]` | Shorthand type names |
| `let dict: Dictionary<String, Int>` | `let dict: [String: Int]` | Shorthand type names |
| `let opt: Optional<User>` | `let opt: User?` | Shorthand type names |
| Multiple statements, no `// MARK:` | Logical groups with `// MARK: - Section` | File organisation |
| Undocumented public API | `/// Summary line.` doc comment | Document public surface |

## Review Checklist

### Naming
- [ ] Types and enum cases: UpperCamelCase
- [ ] Functions, methods, properties, variables: lowerCamelCase
- [ ] Acronyms: all-caps only when entire identifier is an acronym
- [ ] No type-redundant words in names (`removeElement` → `remove`)
- [ ] Delegate methods prefixed with delegating type name
- [ ] No underscore-based privacy conventions

### File Structure
- [ ] File named after its primary type
- [ ] Imports: minimal, whole-module, no transitive reliance, lexicographically ordered
- [ ] `// MARK:` comments present for logical sections
- [ ] Overloaded declarations are grouped together, no interleaved code
- [ ] Extensions grouped with a logical rationale

### Formatting
- [ ] No line exceeds 100 characters
- [ ] No semicolons anywhere (except string literals or comments)
- [ ] One statement per line
- [ ] K&R brace style: `} else {`, `} catch {`
- [ ] 2-space indentation, no tabs
- [ ] No horizontal alignment of tokens across lines
- [ ] Multi-line comma-delimited lists: each element on its own line at +2 indent
- [ ] Trailing commas in multi-line lists (improves diffs)
- [ ] No extra parentheses around conditions: `if x == 0 {` not `if (x == 0) {`

### Constructs
- [ ] `switch` cases not using `fallthrough` unnecessarily
- [ ] Trailing closures used appropriately (not when it harms readability)
- [ ] Numeric literals use `_` separators for readability (e.g., `1_000_000`)
- [ ] Attributes (`@objc`, `@MainActor`) on their own line above the declaration

### Programming Practices
- [ ] No compiler warnings
- [ ] No force unwrap (`!`) outside tests/fatalError
- [ ] No IUOs outside `@IBOutlet`/init requirements
- [ ] `guard` used for early exits rather than nested `if`
- [ ] Explicit access levels on all declarations
- [ ] `for`-`where` used instead of nested `if` for filtered iteration
- [ ] Shorthand type names used (`[T]`, `[K: V]`, `T?`)
- [ ] No `fallthrough` without a compelling reason
- [ ] Pattern matching uses tuple patterns and value bindings correctly

### Documentation
- [ ] All `public` and `open` declarations have `///` doc comments
- [ ] Doc comment opens with a single-sentence summary
- [ ] Parameters, return values, and thrown errors documented with tags
- [ ] File comment present only if the file contains multiple unrelated abstractions

## References

- `references/FILE_STRUCTURE.md` — File naming, imports, type ordering, MARK comments, documentation comments
- `references/FORMATTING.md` — Column limit, braces, semicolons, line-wrapping, whitespace, parentheses, construct-specific formatting
- `references/NAMING.md` — Casing rules, acronyms, clarity, delegate naming, access control vs naming
- `references/PRACTICES.md` — Compiler warnings, optionals, access levels, guard, switch, pattern matching, operators

## Philosophy

This skill focuses on **consistent, readable, idiomatic Swift** — not on opinions beyond what the style guide defines:

- **No architecture enforcement.** MVVM, TCA, VIPER, and similar patterns are out of scope.
- **No framework-specific rules.** SwiftUI, UIKit, and other framework idioms are not covered here.
- **Style guide grounded.** Every rule traces to the Google Swift Style Guide (https://google.github.io/swift/), itself based on Apple's Swift standard library style.
- **"Do this, not that" first.** Rules are stated prescriptively. Rationale is included only when it prevents common misunderstandings.
- **Practical over exhaustive.** The most commonly violated rules are surfaced first. Edge cases live in the reference files.
