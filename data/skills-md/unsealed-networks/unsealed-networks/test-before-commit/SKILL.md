---
name: test-before-commit
description: Enforces running unit tests and linting before committing code changes in the unsealed-networks repository
---

# Test Before Commit

This skill ensures code quality by enforcing tests and linting before any git commit in the unsealed-networks repository.

## When This Skill Activates

This skill should activate automatically whenever you (Claude) are about to commit changes to the unsealed-networks repository.

## Pre-Commit Workflow

Before making any git commit in this repository, you MUST follow this workflow:

### 1. Verify Pre-commit Hooks Are Installed

Check if pre-commit hooks are installed:

```bash
ls -la .git/hooks/pre-commit
```

If not installed or if it's missing, run:

```bash
pre-commit install
```

### 2. Run Linting

Run ruff to check code quality:

```bash
uv run ruff check src/ tests/
```

**CRITICAL**: If linting fails:
- DO NOT proceed with the commit
- Inform the user about the linting errors
- Show the linting output
- Ask the user how they want to proceed (fix errors or skip this requirement)

### 3. Run All Unit Tests

Run the complete test suite:

```bash
uv run pytest -v
```

**CRITICAL**: If any tests fail:
- DO NOT proceed with the commit
- Inform the user about the test failures
- Show the test output
- Ask the user how they want to proceed (fix tests or skip this requirement)

### 4. Only Commit If Tests and Linting Pass

Only proceed with `git commit` if:
- ✅ Pre-commit hooks are installed
- ✅ Linting passes
- ✅ All tests pass

## Important Notes

- Pre-commit hooks will run automatically on commit and enforce linting/formatting
- This skill focuses on ensuring TESTS run before commit (which hooks don't do)
- The user wants to catch cases where you autonomously decide to commit
- If tests fail, this is a blocking issue - do not commit without user approval

## Example Workflow

```bash
# 1. Check hooks are installed
ls -la .git/hooks/pre-commit

# 2. Run linting
uv run ruff check src/ tests/

# 3. Run tests
uv run pytest -v

# 4. Only if linting and tests pass, proceed with commit
git add ... && git commit -m "..."
```
