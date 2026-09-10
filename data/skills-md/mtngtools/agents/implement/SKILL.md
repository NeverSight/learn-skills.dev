---
name: implement
description: Build a settled ticket — base the work correctly, do it in a worktree of its own, test it, review it, commit it.
argument-hint: "The ticket (issue URL or number), or the spec to build"
disable-model-invocation: true
metadata:
  type: skill
  invocation: human-only
  applies-to: [building, tickets, worktrees, git, tests]
---

# Implement

> **human-only.** Start this only when a human asks for it by name. If you arrived here from another skill, stop and get explicit confirmation before running any step.

The last step of the pipeline: `/wayfinder` charts the decisions, `/decisions-to-specs` settles them into specs, `/specs-to-tickets` slices those into build tickets, and this skill builds one. The ticket and its specs are the plan — this skill does not re-decide them, and a ticket that still needs a decision belongs back on the map, not here.

Implement the work described by the user in the spec or tickets.

Adapted from Matt Pocock's `/implement`; the build method — TDD at pre-agreed seams, the test cadence, the `/code-review` pass before committing — is his. Steps 1 and 2 are this repo's addition.

**Where the work is based is decided before it is written.** Steps 1 and 2 are not setup to be hurried through: a session that starts typing in the primary checkout has already committed to a base nobody chose, and no amount of good building fixes that afterwards.

## Process

### 1. Settle the base before creating anything

**The default base is a freshly fetched `origin/main` — never the local `main`, never the current `HEAD`.** Sessions share the primary checkout, so whatever it is sitting on is nobody's chosen base, and the local `main` is only as old as the last pull. Either one silently makes someone else's work the base of yours, and it surfaces later as a PR diff full of commits this ticket never touched.

**`origin/main` is the default, not the only option.** Work that needs a change still sitting in an open PR belongs on top of that PR. Base it on `main` anyway and you either rewrite what that PR already did or write against files it is about to move.

So look, before you create a branch or a worktree:

```
git fetch origin
git worktree list
gh pr list --state open
```

- **`git worktree list`** — a worktree for *this* ticket is yours to resume. A worktree for a neighbouring ticket usually means another session is building something this work touches.
- **`gh pr list --state open`** — an open PR whose files or ticket overlap this one is a candidate base.

**Nothing overlaps:** branch from `origin/main`, and say so in one line as you go.

**Something overlaps:** stop and ask the human — one question, with these options, and do not decide it yourself:

- **Branch from `origin/main`** — the overlap is incidental; deal with the conflict at merge time.
- **Stack on `<branch>` (PR #n)** — this work needs what that PR hasn't merged yet. Branch from `origin/<branch>`, and the PR you open targets that branch too, not `main`.
- **Wait for #n to merge first** — the dependency is total, and stacking would only be a rebase later.

**Never build in another session's worktree.** Reuse one only when it is this ticket's own and you are the one who left it there; a `locked` entry or a directory this session did not create is someone's work in progress.

**Done when:** you can name the base branch and say in one line why it is the base — the default taken, or the human's answer to the stacking question.

### 2. Work in a worktree

```
git worktree add .claude/worktrees/<ticket> -b <branch> <base>
```

**Inside the repo, not beside it.** A path outside the working directory makes the harness ask the human to trust it — a permission prompt that has nothing to do with the work, and that no allowlist suppresses. **If you are Claude Code**, enter it with `EnterWorktree` and its `path` argument, which needs the worktree to already appear in `git worktree list` — hence the order above. **Any other agent** — make that directory your working directory by whatever mechanism your harness provides, or pass the path explicitly (`git -C <worktree-path> …`) on every command rather than building in the primary checkout by accident.

Some harnesses refuse shell redirection inside a worktree. If a heredoc or `>` is refused, use file-writing tools and plain single-purpose commands rather than fighting it.

**Done when:** the session is working inside the worktree, on its own branch, off the base settled in step 1.

### 3. Build it

Use `/tdd` where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

**Done when:** the ticket's acceptance criteria are met and the repo's gate is green.

### 4. Review, then commit

Once done, use `/code-review` to review the work.

Commit to the current branch — the worktree's branch. **Never commit to `main`.**

**Done when:** the work is committed on its own branch, and you have said which branch that is and what it is based on.

## Where this sits in the flow

`/specs-to-tickets` writes the ticket; **`/implement`** builds it; `/create-pr-for-branch` opens the PR; `/review-pr-in-worktree` judges it; `/squash-merge-and-clean-up` lands it. This skill stops at the commit — opening the PR is a separate door a human opens.

`/whats-next` is what usually hands a ticket here, as a two-line prompt naming the ticket and the worktree. That prompt is a reminder, not the authority: the base rules in step 1 hold whether or not the paste mentioned them.
