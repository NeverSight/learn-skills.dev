---
name: pr-review
description: Review the current Pull Request that has been checked out locally with structured feedback on code quality, issues, testing, and suggestions. Use when you need a comprehensive code review of a PR branch.
disable-model-invocation: true
---

# PR Review

Review the current Pull Request that has been checked out locally.

## Instructions

0. ** Prerequisite **
   - Run `git fetch origin master` to ensure we have the latest main branch

1. **Get the PR changes**
   - Run `git diff $(git merge-base HEAD origin/master)..HEAD` to see all changes
   - If master doesn't exist, try origin/main
   - Run `git log --oneline $(git merge-base HEAD origin/main)..HEAD` to see commit messages

2. **Understand the context**
   - Examine the changed files to understand the PR's purpose
   - Look for any related documentation or comments

3. **Provide a structured code review**

   ### Summary
   - Brief overview of what this PR accomplishes
   - Number of files changed and scope

   ### Code Quality
   - Code organization and structure
   - Readability and maintainability
   - Adherence to best practices
   - Error handling

   ### Potential Issues
   - Bugs or logic errors
   - Unhandled edge cases
   - Performance concerns
   - Security vulnerabilities
   - Concurrency issues

   ### Testing
   - Adequacy of tests
   - Whether existing tests are updated
   - Suggested additional test cases

   ### Documentation
   - Clarity of code comments
   - Updated documentation (README, API docs)
   - Explanation of complex logic

   ### Suggestions
   - Specific improvements with code examples
   - Refactoring opportunities
   - Alternative approaches

4. **Output Format**
   - Use markdown formatting
   - Make it ready to paste into a Bitbucket PR comment
   - Be constructive and educational
   - Praise good practices while noting issues
