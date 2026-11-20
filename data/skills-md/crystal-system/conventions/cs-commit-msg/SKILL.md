---
name: cs-commit-msg
description: >
  Apply the organization's commit message rules when creating a commit
  or modifying a commit message. Use this skill whenever a commit is
  about to be created, its message drafted, or an existing message
  corrected, including commits made by AI agents on behalf of a user.
  It covers only what the organization adds on top of the standard
  Conventional Commits format.
---

# Create or modify a commit message

This skill applies the organization's rules on top of standard
[Conventional Commits](https://www.conventionalcommits.org/). The
standard format and semantics are not repeated here.

## When to use

- Before running `git commit` for any commit.
- Before amending or rewriting the message of any commit.

## Rules

1. **Allowed types.** The type MUST be one of:
   `feat` | `fix` | `docs` | `ci` | `chore` | `refactor` | `test` |
   `perf`.

2. **Scope.** If a scope is used, it MUST be a `## <scope>` heading in
   the repository's root `SCOPES.md` in the committed tree:
   - If `SCOPES.md` does not exist, create it in this same commit with
     the structure defined in CONTRIBUTING.md and a first
     `## <scope>` section for your scope.
   - If the scope is not listed, either add a `## <scope>` section in
     this same commit or choose a scope that is already listed.

3. **Language.** The subject and body MUST be in simple technical
   English: short sentences, standard technical vocabulary, no idioms,
   marketing words, or filler.

4. **Issue reference.** If the work belongs to a tracked issue, the
   commit body MUST reference it with the standard keywords:
   `Closes #<number>` only on the commit that resolves the issue,
   `Refs #<number>` otherwise. Put the reference on its own line as
   the last line of the body.

5. **AI-agent commits.** When the commit is made on behalf of the
   user by an AI agent, the message MUST end with a blank line then
   `Assisted by <Agent Name> - <model>` as its last line. State the
   actual agent name and model truthfully. The footer is plain text,
   not a git trailer. Never add a `Co-authored-by` trailer, and never
   set the agent as author or committer.

## Modifying an existing message

- **Unpushed commit:** amend it (`git commit --amend`).
- **Pushed, unmerged branch:** rewriting history is allowed. Rebase
  the branch and reword the messages (for example `git rebase -i
  <base>`), then force-push with `--force-with-lease`.
- **Merged branch:** the history is shared; do not rewrite it. Fix
  forward instead — if a scope was used that is missing from
  `SCOPES.md`, add the `## <scope>` section in a follow-up commit.
