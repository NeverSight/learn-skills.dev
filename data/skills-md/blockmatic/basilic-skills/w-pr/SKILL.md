---
name: w-pr
description: Create or update a reviewable pull request for the intended branch.
disable-model-invocation: true
---

Invocation requests publishing the intended branch and creating its PR. Follow [git publish](references/git-publish.md). The description is part of this playbook; do not use a separate generate-description step.

1. Ensure task-owned changes are committed and validated. Use [commit](../w-commit/SKILL.md) if needed. If this playbook must create a branch first, `git fetch origin` then `git switch -c <name> --no-track origin/main` — never skip fetch, never a stale local `main`.
2. Push the intended branch using [push](../w-push/SKILL.md).
3. Write a standalone description: problem, resulting behavior, verification evidence, and material limitations. Follow the repository template; never create an empty description. Use a conventional PR title when the repository requires it.
4. Reuse an existing PR for this branch rather than duplicating it. Use known applicable labels and requested reviewers; do not invent assignments.
5. With a CLI, write multiline text to a temporary file and pass the body-file option. Verify the resulting title, base, and description. Return the PR link. PR creation does not authorize merge or deployment.
