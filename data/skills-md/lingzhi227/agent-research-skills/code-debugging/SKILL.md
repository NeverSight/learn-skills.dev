---
name: code-debugging
description: Debug experiment code with structured error analysis. Categorize errors, apply targeted fixes with retry logic, and use reflection to prevent recurring issues. Use when experiment code fails or produces incorrect results.
argument-hint: [error-or-code]
---

# Code Debugging

Systematically debug experiment code with structured error categorization and fix strategies.

## Input

- `$0` — Error message, stderr output, or code file with issues
- `$1` — Optional: the code that produced the error

## References

- Debug patterns and state machine: `~/.claude/skills/code-debugging/references/debug-patterns.md`

## Workflow

### Step 1: Categorize the Error

| Category | Examples | Severity |
|----------|----------|----------|
| SyntaxError | Invalid syntax, indentation | Low |
| ImportError | Missing module, wrong name | Low |
| RuntimeError | Division by zero, shape mismatch | Medium |
| TimeoutError | Infinite loop, too slow | Medium |
| OutputError | Missing files, wrong format | Medium |
| LogicError | Wrong results, 0% accuracy | High |

### Step 2: Analyze Root Cause
1. Read the error traceback (last 1500 chars if truncated)
2. Identify the exact line and variable causing the error
3. Check for common patterns:
   - Device mismatch (CPU vs GPU tensors)
   - Shape mismatch in matrix operations
   - Missing data normalization
   - Off-by-one errors in indexing
   - Incorrect loss function for task type

### Step 3: Apply Fix Strategy

**For syntax/import errors**: Direct fix, single attempt
**For runtime errors**: Fix and rerun, up to 4 retries
**For logic errors**: Reflect on approach, consider alternative methods
**For timeout**: Reduce dataset size, optimize bottleneck, add early stopping

### Step 4: Reflect and Prevent
After fixing:
1. Explain why the error occurred
2. Identify which lines caused it
3. Describe the fix line-by-line
4. Note patterns to avoid in future code

## Fix Strategy State Machine

```
Stage 0 (first attempt) → repost code as fresh
Stage 1 (second attempt) → repost or leave depending on severity
Stage 2 (third attempt) → regenerate from scratch if still failing
```

## Rules

- Prefer minimal targeted edits over full rewrites
- Maximum 4-5 fix attempts before changing approach
- Always truncate long error outputs to last 1500 characters
- After fixing, verify the fix doesn't introduce new errors
- Keep error history to avoid repeating the same mistakes
- If 0% accuracy: check accuracy calculation first, then check data pipeline

## Related Skills
- Upstream: [experiment-code](../experiment-code/)
- See also: [paper-to-code](../paper-to-code/), [data-analysis](../data-analysis/)
