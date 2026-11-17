---
name: generate-commit-message
description: Draft a Git commit message that satisfies OneDev branch and pull request requirements. Use for standalone drafting. OneDev work and submission skills compose their own messages.
---

# Generate a OneDev commit message

Use configured `tod` in the repository containing the change.

1. Run `tod get-commit-message-requirement` for the current branch. If the
   commit belongs to a PR, also run
   `tod pr get-commit-message-requirement --target-project <project> --target-branch <branch>`.
   For an existing PR, take the target from `tod pr get <pr>`. For a planned
   PR, use its planned flags, leaving any planned defaults unspecified.
   Empty output means that command supplied no requirement.
2. Read `git status --short` and `git diff --cached`. If nothing is staged,
   read `git diff` and inspect any untracked files intended for the commit.
3. Write a short imperative subject that describes the main change. When
   useful, add a blank line and a body explaining why the change was made
   and any important impact or trade-offs. Follow all non-empty OneDev
   requirements. Include trailers when required or explicitly requested
   and permitted by repository policy.
4. Check the message against the diff and requirements, then show the full
   draft. Run `git commit` only when the user requests it and confirms the
   message.
