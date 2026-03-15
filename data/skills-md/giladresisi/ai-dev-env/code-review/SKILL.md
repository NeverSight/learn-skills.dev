---
name: code-review
description: Use when performing a technical pre-commit code review on recently changed files for bugs, security issues, and standards compliance
---

Perform technical code review on recently changed files.

## Core Principles

Review Philosophy:

- Simplicity is the ultimate sophistication - every line should justify its existence
- Code is read far more often than it's written - optimize for readability
- The best code is often the code you don't write
- Elegance emerges from clarity of intent and economy of expression

## What to Review

Start by gathering codebase context to understand the codebase standards and patterns.

Start by examining:

- CLAUDE.md (project-specific, usually at project root or `.claude/CLAUDE.md`) and `~/.claude/CLAUDE.md` (global user standards)
- README.md
- Standards documentation: look for `/docs`, `/core`, or any dedicated standards directories — not all projects use this convention; the primary source is always CLAUDE.md

After you have a good understanding

Run these commands:

```bash
git status
git diff HEAD
git diff --stat HEAD
```

Then check the list of new files:

```bash
git ls-files --others --exclude-standard
```

Read each new file in its entirety. Read each changed file in its entirety (not just the diff) to understand full context.

For each changed file or new file, analyze for:

1. **Logic Errors**
   - Off-by-one errors
   - Incorrect conditionals
   - Missing error handling
   - Race conditions

2. **Security Issues**
   - SQL injection vulnerabilities
   - XSS vulnerabilities
   - Insecure data handling
   - Exposed secrets or API keys
   - **Hardcoded endpoint URLs** — any new `http://localhost:…` or `http://<host>:…` literal is a mandatory spot-check: verify the path matches the server's registered routes (check `main.py` mount/router registrations). Incorrect URLs cause silent tool-call failures; flag as **high** severity if unverified.

3. **Performance Problems**
   - N+1 queries
   - Inefficient algorithms
   - Memory leaks
   - Unnecessary computations

4. **Code Quality**
   - Violations of DRY principle
   - Overly complex functions
   - Poor naming
   - Missing type hints/annotations

5. **Adherence to Codebase Standards and Existing Patterns**
   - Adherence to standards documented in the /docs directory
   - Linting, typing, and formatting standards
   - Logging standards
   - Testing standards

## Verify Issues Are Real

- Run specific tests for issues found
- Confirm type errors are legitimate
- Validate security concerns with context

**Before reporting test failures as issues:**
Determine whether the failure is pre-existing (existed before this changeset) by:
1. Checking for an execution report at `.agents/execution-reports/` — it will note pre-existing failures if the executor ran a baseline test
2. Running `git stash && <test command> && git stash pop` if no execution report exists

Do not report pre-existing test failures as issues introduced by the current changeset. Mark them separately as "Pre-existing Failures" with a brief root cause note.

## Output Format

Save a new file to `.agents/code-reviews/[appropriate-name].md`

**Stats:**

- Files Modified: 0
- Files Added: 0
- Files Deleted: 0
- New lines: 0
- Deleted lines: 0

**For each issue found:**

```
severity: critical|high|medium|low
file: path/to/file.py
line: 42
issue: [one-line description]
detail: [explanation of why this is a problem]
suggestion: [how to fix it]
```

If no issues found: "Code review passed. No technical issues detected."

## Important

- Be specific (line numbers, not vague complaints)
- Focus on real bugs, not style
- Suggest fixes, don't just complain
- Flag security issues as CRITICAL