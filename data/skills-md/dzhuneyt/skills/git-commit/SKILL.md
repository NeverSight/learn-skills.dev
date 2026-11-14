---
name: git-commit
description: Analyze uncommitted changes and suggest a conventional commit message with option to commit and push
allowed-tools: [Bash, Edit, Read, Grep]
disable-model-invocation: true
---

Execute the following steps:
0. Always navigate to the project root directory.
1. Run `git fetch` to get the latest changes from the remote.
2. Use local `git` to view staged and unstaged changes. Prefer a one-liner that lists files and diffs.
3. Based on the changes, generate a concise commit message suggestion, that follows the conventional commit format.
4. ALWAYS ask for confirmation before executing the commit and push. The confirmation should follow the format specified below.

*Confirmation format:*
- Commit message: <commit message>
- Changed files:
    - **<filename1>** (<concise info about added/modified/removed files, use emojis to indicate "added" and "removed" and avoid unnencessary text>) - <max 10 words summary of what and why was changed in this file>
    - Same as above for <filename2>, <filename3>, ... up to 10 files.

The commit message should be:
- Under 50 characters for the subject line
- Clear and descriptive of what actually changed
- Follow conventional commit format: `type(scope): description`

Rules to follow:
- NEVER add Co-Authored-By lines to commit messages
- Try to execute commands from the project root directory, when possible
- When pre-commits fail, try to fix them and commit again
- Try chaining commands when possible (e.g. `git diff` of multiple files)
- If the project has a pre-commit hook, try to execute the pre-commit hook commands locally and only then move forward with the commit and push.
- If the project has "quality checks" or other similar requirements, try to execute them locally and only then move forward with the commit and push.
