---
name: collaboration
description: Guide for collaborating on GitHub projects. This skill should be used when contributing to projects, creating PRs, reviewing code, or managing issues on GitHub.
license: MIT
---

# Collaboration

This skill documents how to collaborate on projects on GitHub.

## Working on Projects

### With write access

If you have write access to the project, you may work directly in the project.

### With read-only access

If you only have read-only access and cannot write directly to any branches:

1. Create a fork under your own GitHub user account
2. Work exclusively on the fork, not the original repository
3. The fork is your workspace for all development

## Making Changes

To submit changes to a project:

1. Create a new branch (never commit directly to main)
2. Make commits on this branch as work progresses
3. When ready, create a PR from the working branch towards the main branch (from one repo to another if it's a fork)

## Code Reviews

When asked to review code:

1. Do the review directly on the GitHub PR
2. Add comments inline in the code where they make sense
3. Use general PR comments only for overarching feedback

## Addressing Review Comments

When responding to review feedback:

1. Address comments on GitHub, not just in code
2. Reply to each comment explaining what was changed or why something was kept
3. Mark conversations as resolved when the feedback has been addressed

## After PR is Merged

Once a PR has been merged:

1. Switch back to the main branch
2. Pull from origin to sync with the merged changes

## Issues

Always create GitHub issues on the original repository, never on the fork. The fork is only for development work, if needed.
