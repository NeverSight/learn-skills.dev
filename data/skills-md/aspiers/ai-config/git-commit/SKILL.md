---
name: git-commit
description: Create well-formatted commits following conventional commits style with proper atomic commits and descriptive messages
---

# Git Commit Helper

## When to Use This Skill

Use this skill when:

- Creating git commits
- Writing conventional commit messages
- Working with staged changes that need to be committed
- Needing guidance on commit message structure and style

## Critical Rule

**NEVER STAGE OR UNSTAGE FILES WITHOUT EXPLICIT PERMISSION**

Do NOT run any of these commands WITHOUT user permission:

- `git add`
- `git stage`
- `git reset`
- `git restore --staged`
- Any command that modifies the staging area

Default behavior: Only work with files that are ALREADY staged by the user.

Exception: Only stage files if the user gives explicit permission when asked.

## Process

1. **FIRST**: Check which files are staged and unstaged with `git status`. (Do not mix these two categories up!)

   **ABSOLUTE REQUIREMENT**: Do NOT attempt to change what is staged, now or at any later point in this process!

   **FORBIDDEN COMMANDS**: `git add`, `git stage`, `git reset`, `git restore --staged`, or ANY staging commands WITHOUT explicit user permission!

   **IF NOTHING IS STAGED**: STOP immediately and ask the user: "No files are staged for commit. Would you like me to stage all modified files, or would you prefer to stage specific files yourself? If you want me to stage files, please give explicit permission."

2. Check historical commits to learn style and tone: `git log --oneline -40`

3. Analyze the diff to determine if multiple distinct logical changes are present.

4. If multiple distinct changes are detected, stop and ask the user whether to break the commit into multiple smaller commits.

5. Use the output of `git diff --cached --no-ext-diff` to understand what actual changes are staged.  Be careful not to confused staged with unstaged changes.

6. Commit to git using a descriptive commit message that:
   - Uses conventional commit format (`feat:`, `fix:`, `refactor:`, etc.) following existing style and tone
   - Roughly follows this template (wrap the body at 78 columns):

     ```
     feat: <what changed, keep under 75 characters>

     Without this patch, ... <describe the status quo relevant to this change>

     This is a problem because ... <describe *why* the change is needed>

     This patch solves the problem by ... <describe *how* the solution works>
     ```

   - Lists key changes and additions
   - References the task number and the task file it came from
   - Adds a "Co-authored-by:" footer which clarifies which AI agent helped create this commit, using an appropriate `noreply@...` email address

## Commit Style

- **Atomic commits**: Each commit should contain related changes that serve a single purpose.
- **Split large changes**: If changes touch multiple concerns, split them into separate commits. Always review the commit diff to ensure the message matches the changes.
- **Concise first line**: Keep the first line under 72 characters. Do not end the subject line with a period.
- **Present tense, imperative mood**: Use the imperative mood in the subject line.
