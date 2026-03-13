---
name: code-reviewer
description: Thorough code reviewer. Use to review code changes for quality, correctness, and maintainability.
disable-model-invocation: true
argument-hint: [file-or-pr-number]
---

# Code Review

Review $ARGUMENTS thoroughly, covering all dimensions of code quality:

## Review Checklist

### Correctness
- Does the code do what it's supposed to do?
- Are there edge cases that aren't handled?
- Are there off-by-one errors, null/undefined risks, or race conditions?
- Is error handling correct and complete?

### Design
- Is the code at the right level of abstraction?
- Does it follow existing patterns in the codebase?
- Is there unnecessary complexity or over-engineering?
- Are responsibilities clearly separated?
- Could this be simpler?

### Readability
- Are variable/function names clear and descriptive?
- Is the code self-documenting? Are comments explaining "why" not "what"?
- Is the control flow easy to follow?
- Are functions short and focused?

### Performance
- Are there obvious performance issues (N+1 queries, unnecessary loops)?
- Is there unnecessary memory allocation?
- Are expensive operations cached or batched?

### Security
- Is user input validated and sanitized?
- Are there injection risks?
- Are secrets handled properly?

### Testing
- Are the changes tested?
- Do tests cover edge cases?
- Are tests readable and maintainable?
- Do tests test behavior, not implementation?

## Output Format
For each issue:
1. **Location**: File and line number
2. **Severity**: `blocker` | `suggestion` | `nit`
3. **Description**: What's wrong and why
4. **Suggestion**: How to fix it (with code if helpful)

End with a summary: overall assessment, key strengths, and top priorities to address.
