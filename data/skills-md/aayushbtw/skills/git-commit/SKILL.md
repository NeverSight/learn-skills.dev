---
name: git-commit
description: Stages files, analyzes the diff, and commits with a conventional commit message. Use this skill whenever the user wants to commit, says things like "commit this", "make a commit" or "ship it".
---

# Git Commit

## Workflow

IMPORTANT: Follow these steps in order. Do not skip or reorder unless a step explicitly says to.

1. Check what is staged and what isn't:
   ```bash
   git status --short
   ```
   - If nothing to commit at all, stop and tell the user.
   - If nothing is staged → run `git add -A` to stage everything.

2. Read the staged diff and analyze per the **Splitting commits** rules:
   ```bash
   git diff --cached
   ```
   - If there is **one group** → proceed to step 3.
   - If there are **multiple groups** → tell the user how many commits will be made, then unstage everything and stage only the first group's files:
     ```bash
     git reset HEAD
     git add <file1> <file2> ...
     ```

3. Generate a commit message per the **Commit message** rules and commit:
   ```bash
   git commit -m "<generated message>"
   ```
   If unstaged changes remain, repeat from step 1.

## Guidelines

### Commit message
- **Format**: `<type>(<scope>): <description>` where type is one of:
  - `feat`: A new capability or behavior the project didn't have before
  - `fix`: Correcting broken or incorrect behavior
  - `docs`: Changes to documentation only
  - `refactor`: Restructuring code without changing behavior
  - `perf`: Performance improvements
  - `chore`: Routine upkeep (e.g. versions, lockfiles, renaming, linting, formatting)
  - `test`: Adding or updating tests
  - `ci`: Changes to CI/CD pipelines or workflow files
  - `revert`: Undoing a previous commit
- **Scope**: ALWAYS include in parentheses (e.g. `feat(auth):`)
- **Description**: Present tense imperative, no period, ≤50 chars
- **Breaking changes**: Add `!` after type/scope (e.g. `feat!(scope):`)
- **No generic messages**: Never use "update code", "fix bug", "changes"
- **No attribution**: Never add `Co-Authored-By` trailers or footers
- **Examples:**
  - feat(auth): add OAuth2 login flow
  - fix(api): handle null response from payment gateway
  - docs(readme): add setup instructions
  - refactor(db): extract query builder into separate module
  - chore(deps): bump express to v5
  - chore(lint): apply prettier formatting
  - perf(search): add index on users.email column
  - test(auth): add unit tests for token refresh
  - ci(deploy): add staging environment workflow
  - feat!(api): change response format to JSON:API

### Splitting commits
- **Atomic commits**: Each commit must contain only related changes that serve a single purpose
- **Split large changes**: If changes touch different concerns, different types (feat vs fix vs refactor), different file categories (source vs docs), or are large enough that breaking them down aids review

### Git safety
- **No bypassing hooks**: Never use `--no-verify` or `--force`
- **No config changes**: Never modify git config
- **Sensitive files**: Never stage `.env`, credentials, or private keys
- **Pre-commit failures**: Stop and report the error — do not attempt to fix or bypass it
- **Empty staging**: If nothing is staged after `git add`, stop and tell the user
