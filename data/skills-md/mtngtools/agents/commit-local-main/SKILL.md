---
name: commit-local-main
description: Commit straight onto local main in a repo where that is allowed — the invocation is the authorization, and the commit is never pushed.
disable-model-invocation: true
metadata:
  type: command
  invocation: human-only
  applies-to: [commits, git, main, local-only]
---

# Commit Local Main

> **human-only.** Start this only when a human types it by name. If you arrived here from another skill, or reasoned your way here because a commit was needed and the branch happened to be `main`, stop. Being on `main` is not a reason to run this skill; being asked for it is the only one.

Commit the current changes onto `main`, locally, in a repo whose owner has decided that is fine.

## The override

The [`git-and-github`](https://github.com/mtngtools/agents/blob/main/rules/git-and-github.md) rule says **"Never commit to `main` or protected branches."** That rule stands everywhere except here. **Invoking this skill by name is the human suspending it** — for this repo, for this commit, right now.

The authorization is the invocation and nothing else. It does not come from:

- the branch already being `main` when you looked
- the repo having no other branches, no remote, or no protection configured
- a previous session having committed to `main` here
- the change being small, local, docs-only, or obviously safe
- the human having authorized it in this repo yesterday, or an hour ago, for a different commit

Any of those without the human typing the skill means the ordinary rule applies: branch first, then commit.

**The override is this narrow:** one repo, the working tree in front of you, commits made now. It does not extend to the next repo, the next session, or the next change in this one.

## Never push

**This skill commits. The human pushes.** That is the whole shape of it — a local commit is reversible by the person sitting there; a push is not.

- No `git push`, with or without flags, for any reason.
- No PR, no `gh pr create`, no branch cut from the commit to push instead.
- No offering to push, and no "want me to push this?" at the end. The human knows how; they kept it deliberately.
- Nothing that rewrites what is already on the remote — no force, no amending a pushed commit, no rebase of `main` onto anything.

Report the SHA and the branch, and stop there.

## Before committing

1. **Confirm the branch** — `git branch --show-current`. If it is not `main`, do not switch to it. Say what branch you are on and ask; the human may have meant an ordinary commit on the branch they are standing on.
2. **Confirm the repo** — `git rev-parse --show-toplevel`. In a session with several working directories, commit in the one the human means, not the one the last command happened to run in.
3. **Look at what you are about to commit** — `git status --short` and `git diff`. Stage deliberately. A wide `git add -A` in a repo with other sessions in it sweeps up work that is not yours.

## The message

Conventional Commits, as the rule has it: `type(scope): subject (#issue-number)`.

- **Issue reference** if the repo tracks issues and one applies; omit it where there is none, as in [`commit-without-issue`](../commit-without-issue/SKILL.md). Committing to `main` changes nothing about the message.
- **Body:** what changed and why.
- **Breaking changes:** `BREAKING CHANGE`, or `!` after the type and scope.

Example:

```
docs(skills): correct the worktree path in the review flow

The path named .worktrees/, which no harness creates. Point it at
the directory the tooling already ignores.
```

## Afterwards

Say what landed: the SHA, the short subject, the branch, and that it is **unpushed**. If the repo has a remote and `main` now sits ahead of it, say by how many commits — that is the number the human is deciding whether to push.

Then stop. Do not poll the remote, do not check back later, and do not treat an unpushed commit as an unfinished task.
