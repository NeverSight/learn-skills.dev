---
name: vcs-issue-creator
description: 'Expert issue creation for GitHub and GitLab. Uses standardized templates and labels to file clear, actionable bugs, features, and tasks.'
---

# Issue Creation Manager (VCS Agnostic)

## Workflow

1. **Platform Detection**: Detect if repository is GitHub or GitLab.
2. **Duplicity Check**: Ensure the issue doesn't already exist.
3. **Drafting**:
   - Write in **English only**.
   - Use **Markdown** (Titles, Subtitles, Code Snippets, Items).
   - Use **Emojis** for a friendly tone.
   - Choose a template from [references/templates.md](references/templates.md).
4. **MITM Confirmation**: ALWAYS present the drafted issue to the USER for approval before creation.
5. **Execution**: Call the tool and report the issue URL/number.

## Creation Mapping

| Platform | Tool | Title Prefix | Body Field |
|----------|------|--------------|------------|
| **GitHub** | `mcp__github__create_issue` | `[Bug]`, `[Feature]`, etc. | `body` |
| **GitLab** | `mcp__gitlab__create_issue` | `[Bug]`, `[Feature]`, etc. | `description` |

## Parameters Reference

- **GitHub**: `owner`, `repo`, `title`, `body`, `labels`, `assignees`.
- **GitLab**: `project_id`, `title`, `description`, `labels`, `assignee_ids`.

## Guidelines

- **English Only**: All issues must be in English.
- **Rich Formatting**: Use Markdown (H2, H3, `code`, `- items`).
- **Friendly Reminder**: Use emojis (e.g., 🐛, ✨, 📅).
- **MITM Confirmation**: ALWAYS present the drafted issue to the USER for approval before creation.
- **Search First**: Avoid creating duplicate issues.
- **Atomic Issues**: One problem or feature per issue.
- **Labels**: Apply relevant labels from [references/labels.md](references/labels.md).
- **Efficiency**: Skip optional template sections if they provide no value.
- **Clear Context**: Reference other issues or commits if relevant (e.g., `Part of #123`).