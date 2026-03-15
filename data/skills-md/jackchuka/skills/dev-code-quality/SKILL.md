---
name: dev-code-quality
description: >
  Systematic codebase quality scan for identifying duplication, redundancy, and improvement opportunities.
  Use when reviewing a repo's architecture, finding refactoring targets, or assessing code health.
  Triggers: "scan the repo", "find code duplication", "suggest improvements", "code quality review",
  "is there redundant code", "refactoring plan", "architecture review".
argument-hint: "[directory or scope]"
compatibility: NA
metadata:
  author: jackchuka
  scope: generic
---

# Code Quality Scan

Systematic codebase scan that identifies duplication, redundancy, architectural issues, and improvement opportunities. Produces a prioritized action plan.

## Workflow

### Step 1: Scope Definition

Determine the scan scope:

- **Full repo**: Scan everything (default)
- **Directory**: Scan a specific package/module
- **Post-change**: Scan only files changed since last commit or compared to a branch

### Step 2: Structural Analysis

1. **Project layout**: Map the directory structure and identify the architecture pattern (flat, layered, hexagonal, etc.)
2. **Dependency graph**: Trace imports between packages to identify:
   - Circular dependencies
   - Unexpected cross-layer dependencies
   - Packages that import too many others (high fan-out)
   - Packages imported by too many others (high fan-in, potential God package)
3. **File size distribution**: Flag unusually large files (likely candidates for splitting)

### Step 3: Duplication Detection

Search for code duplication across the codebase:

1. **Structural duplication**: Similar function signatures, similar struct/type definitions
2. **Logic duplication**: Repeated patterns (error handling, validation, formatting)
3. **Cross-package duplication**: Same utility reimplemented in multiple packages

For each duplication found, report:

- Location (files and line ranges)
- Nature of duplication (exact copy, similar pattern, same concept)
- Suggested refactoring (extract function, create shared package, use interface)

### Step 4: Redundancy Check

1. **Dead code**: Functions, types, or constants that are never referenced
2. **Unused imports/dependencies**: Check go.mod, package.json for unused entries
3. **Overlapping abstractions**: Multiple types or interfaces serving the same purpose
4. **Unnecessary complexity**: Over-abstracted code, premature generalization

### Step 5: Architecture Assessment

Evaluate the overall design:

1. **Separation of concerns**: Are layers (CLI, domain, storage, etc.) cleanly separated?
2. **API surface**: Are internal details leaking through public interfaces?
3. **Error handling**: Is error handling consistent? Are errors wrapped with context?
4. **Naming consistency**: Are naming conventions consistent across the codebase?

### Step 6: Report & Prioritize

Present findings as a prioritized list:

```
Code Quality Scan Results:

High Priority:
1. [Issue] — [Location] — [Impact] — [Suggested fix]
2. ...

Medium Priority:
3. [Issue] — [Location] — [Impact] — [Suggested fix]
4. ...

Low Priority (nice to have):
5. ...
```

**Prioritization criteria**:

- **High**: Bugs, security issues, significant duplication, architectural violations
- **Medium**: Code quality improvements, moderate duplication, naming inconsistencies
- **Low**: Style preferences, minor optimizations, cosmetic improvements

Ask the user which items to address, then work through them.

## What NOT to Flag

- Minor style differences that don't affect readability
- Test file duplication (test fixtures often intentionally repeat setup)
- Generated code
- Vendor/third-party code

## Common Findings

- **Formatter/display code duplicated across CLI commands**: Extract to shared `output` or `formatter` package
- **Similar validation logic in multiple handlers**: Create a validation middleware or shared validator
- **Multiple config parsing approaches**: Consolidate into a single config package
- **Type overlap between layers**: Domain types leaked into CLI or storage layers
- **N+1 patterns**: Loop with individual API/DB calls instead of batch operations

## Examples

**Example 1: Full repo scan**

```
User: "scan the repo and suggest improvements"
Action:
1. Map project structure
2. Trace dependencies between packages
3. Search for duplicated patterns
4. Check for dead code
5. Assess architecture
6. Present prioritized report
```

**Example 2: Post-refactor validation**

```
User: "find code duplications and refactoring plan"
Action:
1. Focus on structural and logic duplication
2. Identify extraction candidates
3. Propose concrete refactoring steps with file references
4. Estimate scope of each refactoring
```
