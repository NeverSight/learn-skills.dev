---
name: sync_to_github
description: Automate git commit and push. Use when user says "sync to github", "commit and push", "push my changes", "save to git", "submit my work", or invokes /sync_to_github. Stages all changes, generates a commit message, commits, and pushes to remote.
---

# sync_to_github

Run the bundled script to analyze changes, generate a commit message, commit, and push.

## Usage

```bash
SKILL_DIR="/root/.claude/skills/sync_to_github"

# Commit and push (default)
python3 "$SKILL_DIR/tools/git_sync.py"

# Commit only, no push
python3 "$SKILL_DIR/tools/git_sync.py" --no-push

# Preview message without committing
python3 "$SKILL_DIR/tools/git_sync.py" --dry-run
```

## Notes

- Stages **all** changes via `git add .` — if user wants selective staging, stage files first, then run with `--no-push` flow
- Commit message is generated from heuristics (file types, counts, statuses); if user wants a specific or richer message, generate it yourself and call `git commit -m` directly
- Push failure is non-destructive — commit is preserved, manual `git push` is all that's needed
