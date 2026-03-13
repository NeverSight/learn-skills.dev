---
name: developing-packages-r
description: |
  Building robust R packages with modern tidyverse patterns. Use this skill when creating or maintaining R packages, designing APIs, choosing dependencies, implementing input validation, writing error messages, or deciding between internal and exported functions. Covers dependency strategy, tidyverse API design patterns, validation approaches, error handling with cli/rlang, testing levels, and documentation priorities.
---

# Developing Packages R

This skill covers building robust R packages with modern patterns and best practices.

## Dependency Strategy

### When to Add Dependencies vs Base R

**Add dependency when:**
- Significant functionality gain
- Maintenance burden reduction
- User experience improvement
- Complex implementation (regex, dates, web)

**Use base R when:**
- Simple utility functions
- Package will be widely used (minimize deps)
- Dependency is large for small benefit
- Base R solution is straightforward

See [dependency-decisions.md](references/dependency-decisions.md) for example decisions.

### Tidyverse Dependency Guidelines

| Category | Packages | Guidance |
|----------|----------|----------|
| **Core** (usually worth it) | dplyr, purrr, stringr, tidyr | Complex manipulation, functional programming |
| **Specialized** (evaluate carefully) | lubridate, forcats, readr, ggplot2 | Only if heavy usage |
| **Heavy** (use sparingly) | tidyverse, shiny | Meta-package or interactive apps only |

## API Design Patterns

### Modern Tidyverse API

See [api-design.md](references/api-design.md) for:
1. Use `.by` for per-operation grouping
2. Use `{{ }}` for user-provided columns
3. Use `...` for flexible arguments
4. Return consistent types (tibbles, not data.frames)

## Input Validation Strategy

Validation level depends on function type:

| Function Type | Validation Level |
|---------------|-----------------|
| **User-facing** | Comprehensive - check all inputs |
| **Internal** | Minimal - assume valid, check invariants |
| **vctrs-based** | Type-stable - automatic checking |

See [validation-patterns.md](references/validation-patterns.md) for examples.

## Error Handling Patterns

**Good error messages are:**
- Specific - say what went wrong
- Actionable - say how to fix it
- Traceable - include function context

See [error-handling.md](references/error-handling.md) for:
- cli package for user-friendly messages
- rlang for developer tools
- Including function name in errors

## Internal vs Exported Functions

### Export Function When:

- Users will call it directly
- Other packages might want to extend it
- Part of the core package functionality
- Stable API that won't change often

### Keep Function Internal When:

- Implementation detail that may change
- Only used within package
- Complex implementation helpers
- Would clutter user-facing API

See [internal-vs-exported.md](references/internal-vs-exported.md) for examples.

## Testing Strategy

### Testing Levels

| Level | Purpose | Example |
|-------|---------|---------|
| **Unit tests** | Individual functions | Edge cases, error handling |
| **Integration tests** | Workflow combinations | End-to-end pipelines |
| **Property-based tests** | Invariants | Function properties hold |

See [testing-patterns.md](references/testing-patterns.md) for examples.

## Documentation Priorities

### Must Document:

- All exported functions
- Complex algorithms or formulas
- Non-obvious parameter interactions
- Examples of typical usage

### Can Skip Documentation:

- Simple internal helpers
- Obvious parameter meanings
- Functions that just call other functions

source: Sarah Johnson's gist https://gist.github.com/sj-io/3828d64d0969f2a0f05297e59e6c15ad
