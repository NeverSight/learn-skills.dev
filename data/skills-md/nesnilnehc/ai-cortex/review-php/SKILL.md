---
name: review-php
description: "Review PHP code for language and runtime conventions: strict types, error handling, resource management, PSR standards, namespaces, null safety, generators, and testability. Language-only atomic skill; output is a findings list."
tags: [eng-standards]
related_skills: [review-diff, review-codebase, review-code]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# Skill: Review PHP

## Purpose

Review code in **PHP** for **language and runtime conventions** only. Do not define scope (diff vs codebase) or perform security/architecture analysis; those are handled by scope and cognitive skills. Emit a **findings list** in the standard format for aggregation. Focus on strict types and declarations, error handling, resource management, PSR standards (PSR-4, PSR-12), namespaces, null safety, generators and iterables, PHP version compatibility, and testability.

---

## Core Objective

**Primary Goal**: Produce a PHP language/runtime findings list covering strict types, error handling, resource management, PSR standards, namespaces, null safety, generators, version compatibility, and testability for the given code scope.

**Success Criteria** (ALL must be met):

1. ✅ **PHP-only scope**: Only PHP language and runtime conventions are reviewed; no scope selection, security, or architecture analysis performed
2. ✅ **All nine PHP dimensions covered**: Strict types, error handling, resource management, PSR standards, namespaces/autoloading, null safety, generators/iterables, PHP version compatibility, and testability are assessed where relevant
3. ✅ **Findings format compliant**: Each finding includes Location, Category (`language-php`), Severity, Title, Description, and optional Suggestion
4. ✅ **File:line references**: All findings reference specific file locations with line numbers
5. ✅ **Non-PHP code excluded**: Non-PHP files are not analyzed for PHP-specific rules unless explicitly in scope

**Acceptance Test**: Does the output contain a PHP-focused findings list with file:line references covering all relevant language/runtime dimensions without performing security, architecture, or scope analysis?

---

## Scope Boundaries

**This skill handles**:
- `declare(strict_types=1)`, typed properties, parameters, return types
- Exception handling (Throwable hierarchy, try-catch-finally, no empty catch)
- Resource management (fopen/fclose, database connections, try-finally patterns)
- PSR-4 autoloading and PSR-12 coding style
- Namespace and autoloading correctness
- Null coalescing (`??`), null-safe operator (`?->`), error suppression avoidance
- Generator and iterable correctness
- PHP version compatibility with composer.json constraints
- Testability (DI, static/singleton avoidance, constructor injection)

**This skill does NOT handle**:
- Scope selection — scope is provided by the caller
- Security analysis (injection, auth, CSRF) — use `review-security`
- Architecture analysis — use `review-architecture`
- SQL-specific analysis — use `review-sql`
- Full orchestrated review — use `review-code`

**Handoff point**: When all PHP findings are emitted, hand off to `review-code` for aggregation. For SQL injection or security vulnerabilities found in PHP code, note them and suggest `review-security`.

---

## Use Cases

- **Orchestrated review**: Used as the language step when [review-code](../review-code/SKILL.md) runs scope → language → framework → library → cognitive for PHP projects.
- **PHP-only review**: When the user wants only language/runtime conventions checked (e.g. after adding a new PHP file).
- **Pre-PR PHP checklist**: Ensure type safety, resource cleanup, and PSR compliance are correct.

**When to use**: When the code under review is PHP and the task includes language/runtime quality. Scope is determined by the caller or user.

---

## Behavior

### Scope of this skill

- **Analyze**: PHP language and runtime conventions in the **given code scope** (files or diff provided by the caller). Do not decide scope; accept the code range as input.
- **Do not**: Perform scope selection, security review, or architecture review; do not review non-PHP files for PHP-specific rules unless explicitly in scope.

### Review checklist (PHP dimension only)

1. **Strict types and declarations**: `declare(strict_types=1)` usage; typed properties and parameters; return type declarations; avoid implicit type coercion pitfalls.
2. **Error handling**: Exceptions vs errors; `Throwable` hierarchy; proper try-catch and rethrow; avoid empty catch or overly broad catch; `error_reporting` and error-to-exception conversion where relevant.
3. **Resource management**: `fopen`/`fclose`, database connections, streams; ensure resources are closed (try-finally or short-lived scope); avoid resource leaks.
4. **PSR standards**: PSR-4 autoloading and namespace-to-path mapping; PSR-12 coding style (indentation, braces, visibility); class and method naming.
5. **Namespaces and autoloading**: Proper `use` statements; avoid global namespace pollution; composer autoload alignment.
6. **Null safety**: Null coalescing (`??`), null-safe operator (`?->`); avoid `@` error suppression; `isset` vs `array_key_exists` for arrays.
7. **Generators and iterables**: Correct `yield` usage; proper iterator implementation; memory-efficient iteration for large datasets.
8. **PHP version compatibility**: Features used vs `php` constraint in composer.json; deprecated APIs and migration paths.
9. **Testability**: Dependency injection; static and singleton usage; constructor injection; seams for mocking.

### Tone and references

- **Professional and technical**: Reference specific locations (file:line). Emit findings with Location, Category, Severity, Title, Description, Suggestion.

---

## Input & Output

### Input

- **Code scope**: Files or directories (or diff) already selected by the user or by the scope skill. This skill does not decide scope; it reviews the provided PHP code for language conventions only.

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output contract**.
- Category for this skill is **language-php**.

---

## Restrictions

### Hard Boundaries

- **Do not** perform security, architecture, or scope selection. Stay within PHP language and runtime conventions.
- **Do not** give conclusions without specific locations or actionable suggestions.
- **Do not** review non-PHP code for PHP-specific rules unless explicitly in scope.

### Skill Boundaries

**Do NOT do these** (other skills handle them):
- Do NOT select or define the code scope — scope is determined by the caller or `review-code`
- Do NOT perform security analysis (SQL injection, XSS, CSRF) — use `review-security`
- Do NOT perform architecture analysis — use `review-architecture`
- Do NOT perform comprehensive SQL analysis — use `review-sql`

**When to stop and hand off**:
- When all PHP findings are emitted, hand off to `review-code` for aggregation
- When the user needs a full review (scope + language + cognitive), redirect to `review-code`
- When SQL injection or security issues are found, note them and suggest `review-security`

---

## Self-Check

### Core Success Criteria

- [ ] **PHP-only scope**: Only PHP language and runtime conventions are reviewed; no scope selection, security, or architecture analysis performed
- [ ] **All nine PHP dimensions covered**: Strict types, error handling, resource management, PSR standards, namespaces/autoloading, null safety, generators/iterables, PHP version compatibility, and testability are assessed where relevant
- [ ] **Findings format compliant**: Each finding includes Location, Category (`language-php`), Severity, Title, Description, and optional Suggestion
- [ ] **File:line references**: All findings reference specific file locations with line numbers
- [ ] **Non-PHP code excluded**: Non-PHP files are not analyzed for PHP-specific rules unless explicitly in scope

### Process Quality Checks

- [ ] Was only the PHP language/runtime dimension reviewed (no scope/security/architecture)?
- [ ] Are strict types, error handling, resources, PSR, namespaces, null safety, generators, version compatibility, and testability covered where relevant?
- [ ] Is each finding emitted with Location, Category=language-php, Severity, Title, Description, and optional Suggestion?
- [ ] Are issues referenced with file:line?

### Acceptance Test

Does the output contain a PHP-focused findings list with file:line references covering all relevant language/runtime dimensions without performing security, architecture, or scope analysis?

---

## Examples

### Example 1: Resource leak

- **Input**: PHP function that opens a file with `fopen()` and does not close it in all code paths.
- **Expected**: Emit a finding for resource management; suggest try-finally or ensure `fclose()` in all paths. Category = language-php.

### Example 2: Missing strict types

- **Input**: New PHP file without `declare(strict_types=1)` and parameters/return types missing.
- **Expected**: Emit finding(s) for type safety; suggest adding strict types and typed parameters where feasible. Category = language-php.

### Edge case: Mixed PHP and SQL

- **Input**: PHP file with embedded SQL strings for database queries.
- **Expected**: Review only PHP conventions (resource handling, error handling, types). Do not emit SQL-injection findings here; that is for review-security or review-sql.

---

## Appendix: Output contract

Each finding MUST follow the standard findings format:

| Element | Requirement |
| :--- | :--- |
| **Location** | `path/to/file.ext` (optional line or range). |
| **Category** | `language-php`. |
| **Severity** | `critical` \| `major` \| `minor` \| `suggestion`. |
| **Title** | Short one-line summary. |
| **Description** | 1–3 sentences. |
| **Suggestion** | Concrete fix or improvement (optional). |

Example:

```markdown
- **Location**: `src/Service/FileLoader.php:34`
- **Category**: language-php
- **Severity**: major
- **Title**: File handle not closed in exception path
- **Description**: The resource from fopen() may leak if an exception is thrown before fclose().
- **Suggestion**: Use try-finally to ensure fclose() is called, or use SplFileObject which manages the handle.
```
