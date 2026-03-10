---
name: review-typescript
description: Review TypeScript/JavaScript code for type safety, async patterns, error handling, and module design. Atomic skill; output is a findings list.
tags: [eng-standards]
related_skills: [review-diff, review-codebase, review-code]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review typescript, review ts]
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# Skill: Review TypeScript

## Purpose

Review **TypeScript and JavaScript** code for **language and runtime conventions** only. Do not define scope (diff vs codebase) or perform security/architecture analysis; those are handled by scope and cognitive skills. Emit a **findings list** in the standard format for aggregation. Focus on type safety and type system usage, async patterns and Promise handling, error handling, module design, runtime correctness, API and interface design, and performance and memory considerations.

---

## Core Objective

**Primary Goal**: Produce a TypeScript/JavaScript language findings list covering type safety, async patterns, error handling, module design, runtime correctness, API/interface design, and performance/memory for the given code scope.

**Success Criteria** (ALL must be met):

1. ✅ **TypeScript/JavaScript language-only scope**: Only TypeScript and JavaScript language and runtime conventions are reviewed; no scope selection, security, or architecture analysis performed
2. ✅ **All seven language dimensions covered**: Type safety, async patterns, error handling, module design, runtime correctness, API/interface design, and performance/memory are assessed where relevant
3. ✅ **Findings format compliant**: Each finding includes Location, Category (`language-typescript`), Severity, Title, Description, and optional Suggestion
4. ✅ **File/line references**: All findings reference specific file:line or symbol name
5. ✅ **Non-TS/JS code excluded**: Non-TypeScript/JavaScript files are not analyzed for TS/JS-specific rules unless explicitly in scope

**Acceptance Test**: Does the output contain a TypeScript/JavaScript-focused findings list with file/line references covering all relevant language dimensions without performing security, architecture, or scope analysis?

---

## Scope Boundaries

**This skill handles**:

- Type safety and type system usage (strict mode, proper typing, `any` avoidance, discriminated unions, type guards, generics)
- Async patterns (async/await, Promise handling, error propagation, race conditions, unhandled rejections)
- Error handling (try/catch patterns, custom error types, error boundaries, exhaustive error handling)
- Module design (ESM vs CJS, barrel exports, circular dependencies, tree-shaking, side effects)
- Runtime correctness (null/undefined handling, equality checks, coercion traps, prototype pollution)
- API and interface design (function signatures, overloads, branded types, readonly correctness)
- Performance and memory (closure leaks, event listener cleanup, WeakRef/WeakMap usage, bundle size impact)

**This skill does NOT handle**:

- Scope selection — scope is provided by the caller
- Security analysis (injection, secrets, XSS) — use `review-security`
- Architecture analysis — use `review-architecture`
- Framework conventions (Vue, React, Angular) — use framework-specific skills (e.g. `review-vue`)
- Full orchestrated review — use `review-code`

**Handoff point**: When all TypeScript/JavaScript findings are emitted, hand off to `review-code` for aggregation. For injection risks or secrets in code, note them and suggest `review-security`.

---

## Use Cases

- **Orchestrated review**: Used as the language step when [review-code](../review-code/SKILL.md) runs scope → language → framework → library → cognitive for TypeScript/JavaScript projects.
- **TypeScript-only review**: When the user wants only TypeScript/JavaScript language conventions checked.
- **Pre-PR language checklist**: Ensure type safety, async correctness, and module design are sound before merging.

**When to use**: When the code under review is TypeScript or JavaScript and the task includes language quality. Scope is determined by the caller or user.

---

## Behavior

### Scope of this skill

- **Analyze**: TypeScript and JavaScript language and runtime conventions in the **given code scope** (files or diff provided by the caller). Do not decide scope; accept the code range as input.
- **Do not**: Perform scope selection, security review, or architecture review; do not review non-TS/JS files for TS/JS rules unless in scope.

### Review checklist (TypeScript/JavaScript language only)

1. **Type safety and type system usage**: Enforce `strict` mode; prefer explicit types over `any`; use discriminated unions for state modeling; apply type guards and narrowing; leverage generics for reuse without sacrificing type information; avoid type assertions (`as`) where narrowing is possible.
2. **Async patterns**: Ensure proper async/await usage and Promise chaining; verify error propagation through async boundaries; detect race conditions and unhandled Promise rejections; check for dangling Promises (missing `await`); validate concurrent patterns (`Promise.all`, `Promise.allSettled`).
3. **Error handling**: Verify try/catch placement and specificity; prefer custom error types over raw strings/Error; ensure exhaustive error handling (switch/if-else covers all cases); check that errors carry sufficient context; validate cleanup in finally blocks.
4. **Module design**: Prefer ESM (`import`/`export`) over CJS (`require`/`module.exports`); audit barrel exports for tree-shaking impact; detect circular dependencies; check for unintended side effects at module scope; validate consistent module resolution.
5. **Runtime correctness**: Check for null/undefined handling (optional chaining, nullish coalescing); enforce strict equality (`===`/`!==`); detect coercion traps (implicit type conversions); check for prototype pollution risks; validate iterator/generator correctness.
6. **API and interface design**: Review function signatures for clarity and consistency; validate overloads are ordered correctly and are non-ambiguous; check branded/opaque types for domain safety; enforce `readonly` where mutation is unintended; verify index signatures and mapped types.
7. **Performance and memory**: Detect closure-based memory leaks; verify event listener and subscription cleanup; check WeakRef/WeakMap usage for cache patterns; assess bundle size impact of imports; identify hot-path inefficiencies (e.g. unnecessary allocations in loops).

### Tone and references

- **Professional and technical**: Reference specific locations (file:line or symbol name). Emit findings with Location, Category, Severity, Title, Description, Suggestion.

---

## Input & Output

### Input

- **Code scope**: Files or directories (or diff) containing TypeScript or JavaScript code (.ts, .tsx, .js, .jsx, .mts, .mjs, .cts, .cjs). Provided by the user or scope skill.

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output contract**.
- Category for this skill is **language-typescript**.

---

## Restrictions

### Hard Boundaries

- **Do not** perform scope selection, security, or architecture review. Stay within TypeScript/JavaScript language and runtime conventions.
- **Do not** give conclusions without specific locations or actionable suggestions.
- **Do not** review non-TS/JS code for TS/JS-specific rules unless explicitly in scope.

### Skill Boundaries

**Do NOT do these** (other skills handle them):

- Do NOT select or define the code scope — scope is determined by the caller or `review-code`
- Do NOT perform security analysis (injection, secrets) — use `review-security`
- Do NOT perform architecture analysis — use `review-architecture`
- Do NOT review framework-specific conventions (Vue, React, Angular) — use the respective framework skill

**When to stop and hand off**:

- When all TypeScript/JavaScript findings are emitted, hand off to `review-code` for aggregation
- When injection risks or secrets are found, note them and suggest `review-security`
- When the user needs a full review (scope + language + cognitive), redirect to `review-code`

---

## Self-Check

### Core Success Criteria

- [ ] **TypeScript/JavaScript language-only scope**: Only TypeScript and JavaScript language and runtime conventions are reviewed; no scope selection, security, or architecture analysis performed
- [ ] **All seven language dimensions covered**: Type safety, async patterns, error handling, module design, runtime correctness, API/interface design, and performance/memory are assessed where relevant
- [ ] **Findings format compliant**: Each finding includes Location, Category (`language-typescript`), Severity, Title, Description, and optional Suggestion
- [ ] **File/line references**: All findings reference specific file:line or symbol name
- [ ] **Non-TS/JS code excluded**: Non-TypeScript/JavaScript files are not analyzed for TS/JS-specific rules unless explicitly in scope

### Process Quality Checks

- [ ] Was only the TypeScript/JavaScript language dimension reviewed (no scope/security/architecture)?
- [ ] Are type safety, async patterns, error handling, module design, runtime correctness, API design, and performance covered where relevant?
- [ ] Is each finding emitted with Location, Category=language-typescript, Severity, Title, Description, and optional Suggestion?
- [ ] Are issues referenced with file:line or symbol name?

### Acceptance Test

Does the output contain a TypeScript/JavaScript-focused findings list with file/line references covering all relevant language dimensions without performing security, architecture, or scope analysis?

---

## Examples

### Example 1: Unsafe use of `any`

- **Input**: Module with function parameters typed as `any` and no runtime validation.
- **Expected**: Emit a finding (major) for unsafe `any` usage; suggest replacing with a proper type, generic, or `unknown` with type narrowing. Category = language-typescript.

### Example 2: Missing `await` on async call

- **Input**: Async function that calls another async function without `await`, discarding the Promise.
- **Expected**: Emit a finding (critical/major) for dangling Promise; suggest adding `await` or explicitly handling the returned Promise. Category = language-typescript.

### Edge case: Mixed ESM and CJS in the same project

- **Input**: Project with some files using `import`/`export` and others using `require`/`module.exports`.
- **Expected**: Emit findings for inconsistent module system usage; suggest migrating to a single module system (preferably ESM) or documenting the reason for mixed usage. Category = language-typescript.

---

## Appendix: Output contract

Each finding MUST follow the standard findings format:

| Element | Requirement |
| :--- | :--- |
| **Location** | `path/to/file.ts` or `.js` (optional line or range). |
| **Category** | `language-typescript`. |
| **Severity** | `critical` \| `major` \| `minor` \| `suggestion`. |
| **Title** | Short one-line summary. |
| **Description** | 1–3 sentences. |
| **Suggestion** | Concrete fix or improvement (optional). |

Example:

```markdown
- **Location**: `src/services/userService.ts:42`
- **Category**: language-typescript
- **Severity**: major
- **Title**: Unsafe `any` type in function parameter
- **Description**: Parameter `data` is typed as `any`, bypassing all type checking and allowing silent runtime errors.
- **Suggestion**: Replace `any` with `unknown` and add type narrowing, or define a specific interface for the expected shape.
```
