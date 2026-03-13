---
name: cmd-pr-sweep
description: Review changes for test gaps, simplification, naming consistency, reuse opportunities, and TODO quality
disable-model-invocation: true
---

# Code Review Sweep

Review all recent changes (staged, unstaged, or a specified branch diff) across five dimensions. Focus on actionable findings — skip nitpicks.

## Instructions

1. **Identify the change scope** — ask the user if unclear:
   - Uncommitted changes: `git diff HEAD`
   - Branch diff: `git diff main...HEAD`
   - Specific files: user-provided list

2. **Read all changed files in full** before reviewing. Understand the existing patterns, not just the diff.

3. **Review each dimension** below. For each finding, cite the file and line.

## Review Dimensions

### 1. Test Gaps

- Are there new code paths without corresponding tests?
- Are edge cases covered (empty inputs, error paths, boundary values)?
- Do existing tests still pass with the changes?
- Are there testable utilities or helpers that lack unit tests?

### 2. Simplification

- Can any conditional branches be collapsed or removed?
- Are there unnecessary abstractions (wrappers, factories, indirection) for single-use cases?
- Can complex expressions be broken into named variables for clarity?
- Are there redundant checks or defensive code that can't trigger?

### 3. Naming Consistency

- Do new names follow existing conventions in the codebase?
- Are abbreviations used consistently (don't mix `repo`/`repository`, `config`/`configuration`)?
- Do function names accurately describe what they do?
- Are similar concepts named similarly across files?

### 4. Reuse Opportunities

- Is there duplicated logic that could use an existing helper?
- Are there patterns repeated 3+ times that should be extracted?
- Can existing utilities, constants, or types be reused instead of redefined?
- Are there opportunities to consolidate similar functions?

### 5. TODO & Comment Quality

- Do TODOs follow the project's prefix convention (TODO, TODO_IMPROVE, TODO_TECHDEBT, etc.)?
- Does each TODO include **what** and **why**?
- Are there stale or resolved TODOs that should be removed?
- Are comments explaining "why" rather than "what"?
- Are there missing TODOs for known shortcuts or deferred work?

## Output Format

For each dimension, output:

```
### [Dimension Name]

- **[file:line]** — Finding description
  Suggestion: ...

- **[file:line]** — Finding description
  Suggestion: ...
```

If a dimension has no findings, output: `No issues found.`

## Final Summary

End with a prioritized list of the top 3-5 most impactful changes, ranked by effort-to-value ratio.
