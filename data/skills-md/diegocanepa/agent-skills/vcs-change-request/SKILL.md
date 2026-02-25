---
name: vcs-change-request
description: 'Standardized workflow for creating clear and actionable Pull Requests (GitHub) or Merge Requests (GitLab).'
---

# MR/PR Description Manager

## Workflow

1. **Detect Platform**: Check if working on GitHub (PR) or GitLab (MR).
2. **Context**: Understand the changes and find the related issue number.
3. **Drafting**:
   - Write in **English only**.
   - Use **Markdown** (Titles, Subtitles, Code Snippets, Items).
   - Use **Emojis** for a friendly tone.
   - Use a template from [references/templates.md](references/templates.md).
4. **MITM Confirmation**: ALWAYS present the drafted description to the USER for approval.
5. **Execution**: Call the platform-specific tool.

## Technical Mapping

| Platform | Object | Tool Example |
|----------|--------|--------------|
| GitHub   | Pull Request (PR) | `mcp__github__create_pull_request` |
| GitLab   | Merge Request (MR) | `mcp__gitlab__create_merge_request` |

## Key Rules

- **Issue Reference**: Always link the issue (`Closes #123`, etc.) to automate status changes.
- **Title Format**: Use `feat`, `fix`, `refactor`, `docs`, `test`, `chore`.
- **Quality**: Refer to **DO/DON'T** in [references/guidelines.md](references/guidelines.md).
- **Token Efficiency**: Focus on value-added context. Skip obvious details.

## Examples
- **GitHub**: `feat: add oauth support (#123)`
- **GitLab**: `fix: resolve crash on upload (#456)`