---
name: code-review
description: Provide actionable feedback on code changes. Focuses on bugs, security issues, and structural problems.
---

# Code Review

Review code changes using THREE (3) to FIVE (5) parallel subagents and correlate results into a summary ranked by severity.

Use the provided user guidance to steer the review and focus on specific code paths, changes, and/or areas of concern.

**User Guidance:** $ARGUMENTS

## Default Behavior

1. Review **uncommitted changes** by default (`git diff` and `git diff --staged`)
2. If no uncommitted changes exist, review the **last commit** (`git show HEAD`)
3. If the user provides a **pull request number or link**, use `gh pr diff <number>` to fetch changes

## Workflow

1. First, determine what to review based on the rules above
2. Check if the changes include AWS infrastructure files:
   - Terraform files (`*.tf`) containing AWS patterns (`provider "aws"`, `aws_` resources, or `hashicorp/aws`)
   - CDK files (TypeScript files containing `aws-cdk`, `@aws-cdk`, `cdk.Stack`, `cdk.App`, or `Construct` patterns)
3. Check if the changes add new dependencies by looking for additions in:
   - `package.json` (new entries in `dependencies` or `devDependencies`)
   - `requirements.txt`, `pyproject.toml`, `setup.py`, `setup.cfg`
   - `Cargo.toml` (new entries in `[dependencies]` or `[dev-dependencies]`)
   - `go.mod` (new `require` entries)
   - `Gemfile`, `*.gemspec`
   - `composer.json`
   - Any other language-specific dependency manifest
   - **Only trigger on newly added dependencies**, not version bumps of existing ones
4. Launch parallel Task agents:
   - THREE agents with `subagent_type: general-purpose`, each instructed to:
     - Read the full file context (not just diffs) to understand surrounding logic
     - Focus on different aspects: bugs/logic, security/auth, and patterns/structure
     - Follow the detailed review guidelines below
   - If AWS infrastructure detected: ONE additional agent with `subagent_type: aws-limits` to review AWS service quota violations in the changed infrastructure files
   - If new dependencies detected: ONE additional agent with `subagent_type: general-purpose` to verify license compliance:
     - Extract the list of newly added dependency names and versions from the diff
     - For each new dependency, determine its license (use the package registry API or repository metadata — e.g. `npm view <pkg> license`, `pip show <pkg>`, `cargo info <pkg>`, or check the project's GitHub repo)
     - Flag any dependency whose license is **not** in the permissive allowlist: `MIT`, `ISC`, `BSD-2-Clause`, `BSD-3-Clause`, `Apache-2.0`, `0BSD`, `Unlicense`, `CC0-1.0`, `BlueOak-1.0.0`
     - For flagged dependencies, report: package name, detected license, and why it may be problematic (e.g. copyleft, proprietary, unknown)
     - Severity: **Critical** for proprietary/unknown licenses, **High** for copyleft (GPL, AGPL, LGPL, MPL), **Medium** for weak copyleft or uncommon licenses
5. Collect all findings and produce a **consolidated summary**
6. Rank issues by severity: Critical > High > Medium > Low
7. Include file paths and line numbers for each finding
8. Suggest fixes where appropriate

## Review Guidelines

**Diffs alone are not enough.** Read the full file(s) being modified to understand context. Code that looks wrong in isolation may be correct given surrounding logic.

### What to Look For

#### Bugs — Primary focus
- Logic errors, off-by-one mistakes, incorrect conditionals
- Missing guards, unreachable code paths, broken error handling
- Edge cases: null/empty inputs, race conditions
- Security: injection, auth bypass, data exposure

#### Structure — Does the code fit the codebase?
- Follows existing patterns and conventions?
- Uses established abstractions?
- Excessive nesting that could be flattened?

#### Performance — Only flag if obviously problematic
- O(n²) on unbounded data, N+1 queries, blocking I/O on hot paths

### Before You Flag Something

- **Be certain.** Don't flag something as a bug if you're unsure — investigate first.
- **Don't invent hypothetical problems.** If an edge case matters, explain the realistic scenario.
- **Don't be a zealot about style.** Some "violations" are acceptable when they're the simplest option.
- Only review the changes — not pre-existing code that wasn't modified.

### Output Guidelines

- Be direct about bugs and why they're bugs
- Communicate severity honestly — don't overstate
- Include file paths and line numbers
- Suggest fixes when appropriate
- Matter-of-fact tone, no flattery

### Severity Levels

- **Critical**: Security vulnerabilities, data loss, crashes in production
- **High**: Bugs that will cause incorrect behavior, broken functionality
- **Medium**: Code that works but has issues (poor error handling, edge cases)
- **Low**: Style issues, minor improvements, suggestions

## Output Format

```
## Code Review Summary

### Critical Issues
- [file:line] Description of critical bug/security issue

### High Priority
- [file:line] Description

### Medium Priority
- [file:line] Description

### Low Priority / Suggestions
- [file:line] Description

### AWS Service Limits (if applicable)
- [file:line] Description of limit concern

### License Compliance (if applicable)
- [package-name] License: <license> — Reason flagged

### Summary
Brief overall assessment of the changes.
```
