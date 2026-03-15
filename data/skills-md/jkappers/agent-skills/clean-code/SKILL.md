---
name: clean-code
description: Cleans up code files by removing dead code, simplifying structure, and eliminating redundancy without changing behavior. Use when (1) cleaning up code after implementation, (2) reducing complexity in a file or function, (3) removing dead code and unused imports, (4) simplifying control flow and expressions, (5) applying modern language idioms to legacy patterns, or (6) improving readability of dense or convoluted code.
argument-hint: "<file paths, glob patterns, or 'git:staged'>"
---

# Code Cleanup

Clean up code files by removing dead code, simplifying structure, and eliminating redundancy while preserving exact behavior. Language-agnostic. Applies project conventions when available.

When invoked with arguments, clean the files specified by `$ARGUMENTS`. When invoked without arguments, clean files changed in the current git working tree.

## Workflow

1. **Resolve targets**: Determine the set of files to clean
   - File paths or glob patterns: expand and validate each path exists
   - `git:staged`: clean files in the git staging area
   - `git:branch`: clean files changed on the current branch vs the base branch
   - No arguments: run `git diff --name-only` and `git diff --cached --name-only` to collect modified files
   - Skip binary files, generated files (lock files, build output, `.min.*`), and vendored dependencies
2. **Load context**: Read project conventions from `CLAUDE.md`, `.editorconfig`, linter configs, and formatter configs in the project root. These override any default assumptions
3. **Read and analyze**: For each target file, read the full contents and identify cleanup opportunities from the catalog below
4. **Apply cleanup**: Edit each file, applying all applicable cleanup passes. Preserve all existing behavior
5. **Validate**: Run the project's existing linter and test commands if configured. If validation fails, revert the change that caused the failure and continue with remaining files
6. **Report**: Summarize changes per file using the output format below

## Output Format

After completing all cleanup:

```text
## Cleanup Report
| File | Passes Applied | Lines Changed |
|------|---------------|---------------|
| path/to/file.ts | dead code removal, early returns | -12 |
| path/to/other.py | import cleanup, expression simplification | -5 |

Total: N files cleaned, M net lines removed
```

## Cleanup Catalog

Apply passes in this order. Earlier passes are safer and create opportunities for later passes.

### Pass 1: Dead Code Removal

| Target | Action |
|--------|--------|
| Unused imports | Remove the import statement |
| Unused variables and parameters | Remove if safe; prefix with `_` when removal changes a public interface |
| Unreachable code after return/throw/break/continue | Remove the unreachable statements |
| Commented-out code blocks | Remove entirely. Version control preserves history |
| Empty blocks (catch, if, else) with no side effects | Remove the block and its condition if applicable |
| Unused private methods/functions | Remove the definition |
| Redundant type assertions that match the inferred type | Remove the assertion |

### Pass 2: Import and Dependency Cleanup

Sort imports by category: standard library, external packages, internal modules. Remove duplicate imports. Consolidate multiple imports from the same module into a single statement.

Follow the project's import convention if one is defined. Otherwise, detect the dominant pattern in the file.

### Pass 3: Structure Simplification

**Reduce nesting with early returns.** Convert deeply nested conditionals into guard clauses that return/throw/continue early.

```python
# Before
def process(item):
    if item is not None:
        if item.is_valid():
            if item.status == "active":
                return handle(item)
    return None

# After
def process(item):
    if item is None:
        return None
    if not item.is_valid():
        return None
    if item.status != "active":
        return None
    return handle(item)
```

**Flatten unnecessary wrappers.** Remove single-use wrapper functions that add no abstraction value — functions whose body is a single call to another function with the same arguments.

**Collapse single-branch conditionals.** An `if` with no `else` that wraps the entire function body becomes a guard clause.

**Replace nested ternaries.** Convert nested ternary/conditional expressions into `if/else` chains, `switch`/`match` statements, or lookup tables.

### Pass 4: Redundancy Elimination

| Pattern | Resolution |
|---------|------------|
| Duplicate logic across branches | Extract to a shared block before/after the conditional |
| Redundant boolean comparisons (`== true`, `== false`) | Use the expression directly or negate it |
| Redundant null/nil checks before optional chaining | Remove the outer check |
| Repeated string/number literals (3+ occurrences) | Extract to a named constant |
| Identity transformations (`map(x => x)`, `.filter(() => true)`) | Remove the no-op call |
| Unnecessary intermediate variables used once and immediately returned | Return the expression directly |
| Re-assignment to self (`x = x`) | Remove the statement |

### Pass 5: Expression Simplification

Simplify boolean logic:
- `!(!x)` → `x`
- `a && a` → `a`
- `if (cond) return true; else return false;` → `return cond;`
- `x !== null && x !== undefined` → use nullish checks when the language supports them

Simplify arithmetic:
- `x * 1` → `x`, `x + 0` → `x`, `x * 0` → `0`

Simplify string operations:
- `str + ""` → `str` (when already a string)
- Consecutive string concatenations → template literals or format strings when the language supports them

### Pass 6: Modern Idiom Adoption

Apply modern language features **only when the project's target runtime supports them**. Check `tsconfig.json`, `pyproject.toml`, `.tool-versions`, `Cargo.toml`, or equivalent for version constraints.

| Legacy Pattern | Modern Replacement | Condition |
|---------------|-------------------|-----------|
| `var` declarations | `const`/`let` | JavaScript/TypeScript |
| `for (i=0; i<arr.length; i++)` | `for...of` or array methods | JavaScript/TypeScript, when index is unused |
| `.then().catch()` chains | `async`/`await` | JavaScript/TypeScript, when the function can be async |
| `string.format()` or `%` formatting | f-strings | Python 3.6+ |
| Manual resource cleanup | Context managers (`with`) | Python |
| Manual null checks in chain | Optional chaining (`?.`) | JavaScript/TypeScript ES2020+, C# 6+, Kotlin, Swift |
| `StringBuilder` loops for simple cases | String interpolation | C#, Java 15+, Kotlin |

**Do not adopt idioms that reduce clarity.** A `for` loop with complex break logic is clearer than a chained `.reduce()`.

## Constraints

- **Never change observable behavior.** Inputs, outputs, side effects, error behavior, and public interfaces remain identical. When in doubt, skip the optimization.
- **Never change formatting conventions.** Indentation style, line endings, and brace placement follow the existing file style, not personal preference. Formatting is the formatter's job.
- **Never add new dependencies or imports.** Cleanup uses only what is already available in the file and project.
- **Never remove code that has side effects.** A function call that appears unused may produce side effects. Only remove calls to pure functions with unused return values when purity is certain.
- **Never clean generated code.** Skip files with `@generated`, `auto-generated`, or equivalent markers.
- **Never clean test assertions.** Test code prioritizes explicitness over brevity. Skip test files unless explicitly included in arguments.
- **Preserve git blame utility.** Make the minimum set of changes needed. Do not rewrite entire files when targeted edits suffice.

## Scope Boundaries

This skill cleans up existing code. Do not use for:
- Adding new features or functionality
- Refactoring architecture (moving code between files, changing module boundaries)
- Adding documentation, comments, or type annotations
- Formatting (use a formatter instead)
- Performance optimization (algorithmic changes, caching, parallelism)
- Security hardening (input validation, authentication)
