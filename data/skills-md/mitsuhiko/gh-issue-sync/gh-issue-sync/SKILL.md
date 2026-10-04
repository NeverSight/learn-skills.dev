---
name: gh-issue-sync
description: "Manage GitHub issues locally as Markdown files. Use for triaging, searching, editing, and creating issues without leaving your editor or terminal."
---

# gh-issue-sync

Syncs GitHub issues to local Markdown files in `.issues/open/` and `.issues/closed/`.

## Commands

```
gh-issue-sync init              # Initialize in git repo
gh-issue-sync pull              # Fetch open issues (--all for closed too)
gh-issue-sync push              # Push local changes (--dry-run to preview)
gh-issue-sync list              # List issues (supports gh issue list flags + --search)
gh-issue-sync new "Title"       # Create issue (--label, --edit)
gh-issue-sync close 42          # Close (--reason completed|not_planned)
gh-issue-sync reopen 42
gh-issue-sync status            # Show local changes
gh-issue-sync diff 42           # Show diff (--remote to re-fetch)
```

## File Format

`.issues/open/42-fix-login-bug.md`:
```markdown
---
title: Fix login bug
labels: [bug, priority:high]
assignees: [alice]
milestone: v1.0
state: open
# For closed: state_reason: completed|not_planned
# Optional: parent: 10, blocked_by: [11, 12], blocks: [15]
---

Issue body in Markdown.
```

Issue number is derived from the filename, not stored in frontmatter.

## Temporary Issues

New issues get a `T`-prefixed ID (e.g., `T1a2b3c`). The filename must start with `T`:
```
.issues/open/T1a2b3c-my-new-issue.md
```

On `push`, the file is renamed to the real issue number (e.g., `42-my-new-issue.md`) and `number:` in frontmatter is updated. Any `#T1a2b3c` references in other issues are also updated to `#42`.

## Comments

To post a comment when pushing, create a `.comment.md` file next to the issue:
```
.issues/open/42.comment.md
.issues/open/42-fix-login-bug.comment.md
```

Content is plain Markdown. The file is deleted after the comment is posted.

## Notes

- Pull skips conflicts; use `--force` to overwrite local
