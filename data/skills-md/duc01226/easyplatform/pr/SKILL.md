---
name: pr
description: '[Git & Release] ⚡ Create a pull request with standard format'
argument-hint: [options]
---

# Create Pull Request: $ARGUMENTS

Create a pull request with the standard EasyPlatform format.

## Steps

1. **Check current branch status:**
    - Run `git status` to see all changes
    - Run `git diff` to review modifications
    - Ensure all changes are committed

2. **Analyze commits:**
    - Run `git log --oneline -10` to see recent commits
    - Identify all commits to include in the PR

3. **Create PR with standard format:**

    ```
    gh pr create --title "[Type] Brief description" --body "$(cat <<'EOF'
    ## Summary
    - Bullet points describing changes

    ## Changes
    - List of specific changes made

    ## Test Plan
    - [ ] Unit tests added/updated
    - [ ] Manual testing completed
    - [ ] No regressions introduced

    ## Related Issues
    - Closes #issue_number (if applicable)

    Generated with Claude Code
    EOF
    )"
    ```

4. **PR Title Format:**
    - `[Feature]` - New functionality
    - `[Fix]` - Bug fix
    - `[Refactor]` - Code improvement
    - `[Docs]` - Documentation only
    - `[Test]` - Test changes only

## Notes

- Ensure branch is pushed before creating PR
- Target branch is usually `develop` or `master`
- Add reviewers if specified in $ARGUMENTS

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
