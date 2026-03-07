---
name: git-pr-reviewer
description: Review pull requests for code quality, security issues, and best practices. Use when reviewing PRs, checking code changes, or analyzing diffs before merge.
allowed-tools: Read, Grep, Glob, Bash
---

# Git PR Reviewer

## Instructions

When reviewing a pull request:

1. **Get the diff**: Run `git diff main...HEAD` or `git diff <base-branch>...HEAD`
2. **Analyze changed files**: Identify all modified, added, and deleted files
3. **Review each file** for:
   - Logic errors and bugs
   - Security vulnerabilities (SQL injection, XSS, hardcoded secrets)
   - Performance issues (N+1 queries, unnecessary re-renders, memory leaks)
   - Code style and consistency
   - Missing error handling
   - Test coverage gaps

## Review Checklist

### Security
- [ ] No hardcoded credentials or API keys
- [ ] Input validation on user data
- [ ] Proper authentication/authorization checks
- [ ] No SQL injection vulnerabilities
- [ ] XSS prevention in place

### Code Quality
- [ ] Functions are small and focused
- [ ] No code duplication
- [ ] Clear variable/function naming
- [ ] Proper error handling
- [ ] No unused imports or dead code

### Performance
- [ ] No unnecessary database queries
- [ ] Efficient algorithms used
- [ ] Proper caching where needed
- [ ] No memory leaks

### Testing
- [ ] New code has tests
- [ ] Edge cases covered
- [ ] Tests are meaningful, not just for coverage

## Output Format

```markdown
## PR Review Summary

### Overview
[Brief summary of changes]

### Issues Found
#### Critical
- [Issue description + file:line]

#### Warnings
- [Issue description + file:line]

#### Suggestions
- [Improvement ideas]

### Approval Status
[APPROVE / REQUEST CHANGES / NEEDS DISCUSSION]
```

## Example

```bash
# Review current branch against main
git diff main...HEAD --stat
git diff main...HEAD
```
