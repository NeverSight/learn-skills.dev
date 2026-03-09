---
name: create-pr
description: Use this skill when the user asks to create a PR, open a pull request, "create-pr", "submit a pull request", or "open a merge request". Requires Gitee MCP Server to be configured.
version: 1.0.0
requires:
  mcp-servers:
    - gitee
---

> **Note**: If you have `mcporter` installed locally, you should use `mcporter` to invoke the MCP tool instead of directly calling the MCP tool. The `mcporter` CLI provides a more convenient interface and better error handling.

# Create PR via Gitee MCP

Generate a well-structured Pull Request description based on the current changes and submit it to Gitee.

## Prerequisites

- Gitee MCP Server configured (tools: `create_pull`, `get_file_content`, `list_repo_issues`, `compare_branches_tags`)
- User must provide: repository owner, repository name, source branch, target branch (usually main/master)
- Optional: linked Issue number

## Steps

### Step 1: Gather Information

Confirm with the user or infer from context:
- Source branch (head branch)
- Target branch (base branch, default: master or main)
- Core purpose of this PR (if not stated, infer from commit messages or file changes)
- Whether to link an Issue (optional)

### Step 2: Analyze the Changes

Use `compare_branches_tags` to fetch the diff between the source branch and target branch:
- `base`: target branch (e.g., `main` or `master`)
- `head`: source branch

Analyze the returned diff to determine:
- Which core files were changed
- What functionality was added or modified
- Whether there are any breaking changes

### Step 3: Generate PR Title

Follow the Conventional Commits format:

```
<type>(<scope>): <subject>
```

Available types:
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring
- `docs`: Documentation update
- `test`: Test-related changes
- `chore`: Build / dependency / toolchain changes

Example: `feat(auth): add OAuth2 login support`

### Step 4: Generate PR Description

Use the following template for a structured description:

```markdown
## Summary

[Clear description of the purpose of this PR and the problem it solves]

## Changes

- [Change 1]
- [Change 2]
- [Change 3]

## Testing

- [ ] Unit tests pass
- [ ] Functional tests pass
- [x] [Completed test item]

## Related Issue

closes #[issue number] (if applicable)

## Notes

[Breaking changes, dependency upgrades, deployment considerations, etc. (if any)]
```

### Step 5: Create the PR

Use `create_pull` to create the PR with these parameters:
- `title`: title generated in Step 3
- `body`: description generated in Step 4
- `head`: source branch
- `base`: target branch

After successful creation, output the PR link for the user.

## Notes

- If the user specifies a linked Issue, append `closes #N` to the description so the Issue is automatically closed when the PR is merged
- Keep the PR title concise (under 50 characters) — put details in the description
- If the user hasn't provided enough information, ask before creating, to avoid opening a PR with an empty description
