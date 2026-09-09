---
name: git-commit
description: Commit changes using user's preferred conventions.
disable-model-invocation: true
---

Review the current changes and create commits.

Rules:

- Commit only files changed for this task.
- Use Conventional Commits.
- Keep the title concise and imperative.
- Each commit must have both a title and a description.
- Commits must be fully atomic and cherry-pickable.
- Do not include unrelated changes.
- Run relevant checks before committing.
- Never push commits to a remote unless explicitly asked.
