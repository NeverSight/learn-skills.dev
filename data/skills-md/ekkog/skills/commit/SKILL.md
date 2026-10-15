---
name: commit
description: Create focused, reviewable local Git commits requested by the user or active workflow. Provides scope isolation, commit shaping, staging, message, and reporting guidance. Do not use for pushing, branch creation, or pull requests.
---

# Commit Changes

Create the requested commit from the supplied scope and available validation
evidence.

Commit only the requested changes. Never push, create a branch, open a pull
request, amend, or rewrite history unless the user separately requests that
operation.

## Workflow

1. Inspect `git status --short`, staged and unstaged diffs, and recent commit
   subjects.
2. Resolve the requested scope and preserve unrelated user changes. If changed
   files cannot be safely attributed or isolated, report the ambiguity before
   staging them.
3. Choose a practical commit shape. Prefer one commit for one coherent change.
   Split clearly independent concerns when that materially improves review, but
   do not split by file type or create cosmetic micro-commits.
4. Use validation evidence supplied by the caller. Run only checks explicitly
   requested for the commit, required by repository instructions, or enforced
   by commit hooks; do not repeat an engineering acceptance workflow merely to
   create the commit. Report failures and never bypass hooks.
5. Stage explicit paths for each commit group. Avoid `git add .`, `git add -A`,
   and `git add --all` when the worktree contains changes outside the requested
   scope.
6. Review `git diff --cached` before committing.
7. Write the commit message using these rules:
   - Follow explicit repository message requirements. Otherwise use
     `type(scope): subject` with a concise imperative subject; omit the scope
     when it adds no useful information.
   - Include a concise body for substantive changes. For fixes, explain the
     problem or cause and the solution. For features or refactors, explain the
     purpose and main approach. Title-only messages are appropriate for
     self-explanatory trivial changes such as spelling or formatting.
   - Include relevant validation from available evidence, compatibility impact,
     and material limitations when applicable.
   - Use recent commit messages as a reference for naming and language while
     retaining the body requirements above.
8. After committing, report each commit hash and subject, the evidence relied
   on or checks run, and any remaining uncommitted changes.
