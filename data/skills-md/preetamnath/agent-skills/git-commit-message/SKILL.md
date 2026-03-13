---
name: git-commit-message
description: Generate git commit messages in a specific bullet-point format with a conventional header.
---

# Git Commit Message Generation

When asked to generate a git commit message, satisfy the following rules:

1. **Gather Context** (read-only — do not stage anything):
   - Run `git status` to identify all modified, deleted, staged, and untracked files.
   - Run `git diff` to see all unstaged changes.
   - Run `git diff --cached` to see all already-staged changes.
   - **Untracked files**: Read the full content of new files.
   - **Deleted files**: Note the removal.
   - Combine all of the above to form a complete picture of what will be committed.

2. **Draft Message**:
   - Create a conventional commit message based on the *actual* changes found.
   - **Header**: Start with a Conventional Commit header (e.g., `feat:`, `fix:`, `refactor:`) that captures the key change.
   - **Body**: Leave one empty line after the header, then a list of details.
   - **Format**: Use a simple bulleted list (`-`) for the details.
   - **Style**: Use the imperative mood (e.g., "Create", "Update", "Fix", "Refactor").
   - **Quotes**: **NEVER use double quotes (")** in the commit message content. Use single quotes (') instead if you need to quote something.

3. **Execute**:
   - Construct the final command: `git add . && git commit -m "YOUR_MESSAGE_HERE"`.
   - **Output**: Present the final command in a markdown code block (`bash`) so the user can copy/paste if they reject the tool.
   - **Then**, immediately execute the command.

## Usage Example

**Input**: "Commit these changes."

**Context**: User has modified several files related to the layout.

**Output**:

```bash
git add . && git commit -m "refactor(learn): unify header layout and simplify access logic

- Create learn/layout.tsx shared layout file for learn routes
- Create LearnPagesHeader.tsx to consolidate title/breadcrumb and UserProfileDropDown.tsx across /learn and /learn/:slug routes
- Update code in UnpaidUserBanner.tsx and NoAccessToThisNote.tsx components
- Consolidate 'Paid User' and 'Valid Access Config' checks into unified logic blocks across pages
- Add JSDoc documentation to BreadcrumbLink.tsx, UserProfileDropdown.tsx and learn/layout.tsx"
```

**Action**: Agent then executes the command above.
