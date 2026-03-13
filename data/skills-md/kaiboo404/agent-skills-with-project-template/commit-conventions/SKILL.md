---
name: commit-conventions
description: Generates structured commit messages following the project's conventions.md. Use when committing code changes.
version: 1.0.0
---

# Commit Conventions

Generates standardized commit messages following the conventions defined in `.context/conventions.md`. Ensures consistent git history with zero developer effort.

## When to Use This Skill

- When preparing a git commit
- When squashing commits before merge
- When writing PR/MR descriptions
- When reviewing commit message quality

## Commit Message Generation

### Input
Analyze the staged diff (`git diff --staged`) and any active spec context to determine:
1. **Type** — What category of change is this?
2. **Scope** — Which module or feature is affected?
3. **Description** — What was changed and why?

### Output Format

```
<type>(<scope>): <short description>

<body — what and why, not how>

<footer — references, breaking changes>
```

### Type Detection Rules

| Diff Pattern | Detected Type |
|---|---|
| New files with business logic | `feat` |
| Modified files fixing incorrect behavior | `fix` |
| Only `.md` or comment changes | `docs` |
| Whitespace, formatting, linting only | `style` |
| Same behavior, different structure | `refactor` |
| Benchmark or optimization changes | `perf` |
| Test files added or modified | `test` |
| `package.json`, build config changes | `build` |
| CI/CD workflow files | `ci` |

### Scope Detection Rules
- Detect from the directory path: `src/core/auth/` → scope is `auth`
- If changes span multiple modules, use the primary module or omit scope
- If changes are in `.context/`, scope is `context`

## Examples

### Feature Commit
```
feat(auth): add JWT refresh token rotation

Implements automatic token refresh when access token expires within
5 minutes of a request. Uses sliding window strategy to minimize
re-authentication.

Refs: feat-user-auth.md
```

### Bug Fix
```
fix(payment): handle timeout on slow connections

Previous implementation used a 3s timeout which failed on mobile
networks. Increased to 10s with exponential backoff retry.

Fixes #142
```

### Multi-file Refactor
```
refactor(core): extract validation into dedicated module

Moved scattered validation logic from 6 service files into
src/core/validation/ with shared schemas. Reduces duplication
by ~200 lines.

BREAKING CHANGE: ValidationError now requires error code parameter
```

## PR/MR Description Generation

When asked, generate a PR description from the branch's commit history:

```markdown
## Summary
{One paragraph summarizing all changes}

## Changes
- {Bullet list of logical changes, not file-by-file}

## Testing
- {How changes were tested}

## Related
- Spec: `.context/specs/feat-{name}.md`
- Closes #{issue_number}
```

## Quality Rules
- Subject line must be ≤72 characters
- Body wraps at 80 characters
- No period at end of subject line
- Use imperative mood ("add" not "added")
- Breaking changes must include `BREAKING CHANGE:` footer
