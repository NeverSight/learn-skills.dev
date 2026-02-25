---
name: reviewer-process
description: Run when the user asks for a review; use git CLI to list staged and unstaged changes, read GUIDELINES.md in this skill folder, produce a fix list, and offer to apply fixes after confirmation.
---

- Use git CLI to enumerate changed files, including both staged and unstaged (e.g., `git diff --name-only --cached` and `git diff --name-only`).
- If the user asks to review against a target branch (e.g., "review against main"), fetch the target branch if needed (e.g., `git fetch origin main`), then compare using:
	- `git diff --name-only <target>...HEAD` to list changed files
	- `git diff <target>...HEAD` to review actual changes
- Prefer the three-dot range (`<target>...HEAD`) so the diff is based on the merge-base with the target branch.
- Focus review on code folders; identify them dynamically from the repo structure and skip helper scripts or non-code folders unless the user requests otherwise.
- Read `GUIDELINES.md` in this skill folder and follow its rules when reviewing. Review ONLY based on the guidelines provided.
- Inspect only the changed files and produce a list of concrete fixes needed, ordered by severity.
- Recommend applying fixes and ask for confirmation before making changes.
- If the user confirms, apply fixes while following `GUIDELINES.md` and the repo editing constraints.
