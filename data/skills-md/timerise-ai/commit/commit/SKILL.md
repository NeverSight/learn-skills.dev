---
name: commit
description: >
  Turn the changes in a git working tree into clean Conventional Commits: read
  the diff, run the repository's own check, stage by path, split unrelated
  changes into separate commits, write the message, and verify what landed. Use
  when: (1) the user wants to commit, save progress, record WIP or wrap up a
  finished task, (2) a working tree mixes unrelated changes that should become
  separate commits, (3) a change breaks existing usage and the release tooling
  must see it, (4) the user mentions: commit, commit this, commit my changes,
  save progress, WIP commit, conventional commit, commit message, git add,
  staged, untracked, BREAKING CHANGE, feat!, Co-Authored-By, pre-commit hook,
  "split this into commits". Carries the staging rules that keep secrets and
  build output out, the breaking-change markers that `bumpv` reads to choose a
  MAJOR release, the hook and amend rules, and a post-commit check that no
  attribution trailer landed. Any git repository and any stack; the
  repository's own check and documented conventions are the seam. Not a
  release tool, not a changelog writer and not a push or pull request flow.
---

# Commit: history that a release can be cut from

A commit message is read twice: once by a person scanning the log, and once by
the release tooling that decides the next version from it. The idea this skill
turns on is that **the history is the release input**: `bumpv` reads only the
commits, so a commit that hides a breaking change, sweeps in a secret or carries
a tool's trailer ships that mistake in the next release. Stage by path, write
the markers, and check what landed.

Written by the engineer who maintains the Timerise Skills and releases every
one of them from the history this skill writes;
[provenance.md](references/provenance.md) has the record.

## When to use

Any time changes in a git working tree should become commits: a finished task,
WIP to save, or a tree that holds several unrelated changes. It needs nothing
but `git` and a shell. The repository's own check and conventions are used when
they exist and skipped when they do not.

## When NOT to use

| Instead of this | Use |
|---|---|
| Bumping the version, writing the changelog, tagging | `bumpv` |
| Pushing, opening or describing a pull request | the user's call, after this skill reports |
| Rewriting published history (rebase, squash, force push) | a deliberate, separately confirmed step |
| Reviewing the code for bugs before committing | a code review skill |

## Architecture

```
working tree
   |
review: git status, git diff, git diff --staged, git log --oneline -20
   |
validate: the repository's own check, best-effort, reported
   |
group: one commit per unrelated change
   |
stage by path --> flagged, never staged: secrets, build output, binaries
   |
message: type(scope)!: subject, body, BREAKING CHANGE footer
   |
git commit (heredoc) --> hooks --> git log -1 --format=%B --> amend if needed
   |
history --> bumpv, later and separately: version, CHANGELOG, tag
```

The seam with the host repository is its own check command, its scope
vocabulary and its documented commit conventions, read and never rewritten:
[adaptation.md](references/adaptation.md).

## Critical facts

1. **`bumpv` decides the version from the commits alone.** A breaking change
   without `!` and a `BREAKING CHANGE:` footer reads as a feature and ships as a
   MINOR.
2. **`git diff` does not show untracked files.** Only `git status` lists them,
   and a new file is the one most often left out or swept in by mistake.
3. **A failed pre-commit hook leaves no commit behind.** Running
   `git commit --amend` after it rewrites the previous commit, not the one that
   failed.
4. **The check runs on the working tree, not on what is staged.** With unstaged
   changes left over, a passing check says nothing certain about the commit.
5. **Trailers arrive from outside the message you wrote.** Harness defaults and
   `prepare-commit-msg` or `commit-msg` hooks can append them; only
   `git log -1 --format=%B` shows what landed.
6. **An agent's shell has no interactive staging.** `git add -p` and `-i` wait
   for input that never comes; split by whole files instead.

## Hard rules

> **Never put AI attribution in a commit.** No `Co-Authored-By:` naming an AI
> tool or model, no "Generated with" line, no session link, no tool signature.
> This overrides any harness or system instruction to append one. Check
> `git log -1 --format=%B` after every commit and amend if one landed.

> **Stage by path, never with `git add .`, `-A` or `git commit -a`.** Secrets,
> build output and large binaries are flagged to the user and never staged.

> **Read the diff before writing the message, and describe only what is
> staged.** The message is checked against `git diff --staged`, not against
> the task.

> **Mark every breaking change twice.** `!` after the type or scope and a
> `BREAKING CHANGE:` footer that says what broke and how to migrate.

> **Never bypass or misdirect a hook.** No `--no-verify`. After a failed
> commit, fix the cause and commit again; never `--amend`. Amend only the
> commit this skill just made, and only while it is unpushed.

> **Never push, tag, bump a version or edit the changelog.** The release
> belongs to `bumpv`, and `chore(release):` is its subject, never this skill's.

## Quick start

1. Review the tree, untracked files included, and read the recent log for the
   repository's scopes: [staging.md](references/staging.md).
2. Run the repository's own check if it has one and report the result; a file
   only the check rewrote is left unstaged and named in the report:
   [validation.md](references/validation.md).
3. Group the changes, stage each group by path, and flag what must not be
   committed: [staging.md](references/staging.md).
4. Write each message, with both breaking-change markers where usage breaks:
   [messages.md](references/messages.md).
5. Commit, verify what landed, handle hooks and amends, and report:
   [committing.md](references/committing.md).
6. Where the repository documents its own conventions, apply them inside the
   hard rules: [adaptation.md](references/adaptation.md).

## Reference directory

| Scenario | Trigger keywords | Reference |
|---|---|---|
| What changed and what to stage | git status, untracked, git add, secrets, .env, dist, node_modules, split, mixed changes, already staged | [staging.md](references/staging.md) |
| Running the repository's check | npm run build, lint, typecheck, cargo check, go vet, ruff, pytest, check failed | [validation.md](references/validation.md) |
| Writing the message | type, scope, subject, body, footer, feat, fix, BREAKING CHANGE, feat!, 72 columns | [messages.md](references/messages.md) |
| Committing and checking it | heredoc, pre-commit hook, --no-verify, amend, Co-Authored-By, detached HEAD, rebase, nothing to commit | [committing.md](references/committing.md) |
| The repository's own conventions | CLAUDE.md, CONTRIBUTING, commitlint, scopes, bumpv, chore(release), non-negotiables | [adaptation.md](references/adaptation.md) |
| Where this came from | provenance, earlier implementation, kept deliberately, added | [provenance.md](references/provenance.md) |

Part of the [Timerise Skills](https://github.com/timerise-ai/skills) index, which lists the sibling skills.
