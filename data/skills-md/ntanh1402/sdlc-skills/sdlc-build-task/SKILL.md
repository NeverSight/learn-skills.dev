---
name: sdlc-build-task
description: Write the code and unit tests of one wiki Task in one code repository, against the project wiki - read the Task's acceptance and planned scope, the contracts of the Design files it covers and the Application's conventions, plan the files, write them in a git worktree on a branch of their own, check them against the wiki and commit with a Task trailer, without pushing. Use when a developer asks to build, implement or code a Task of the project wiki. Not for coding without a wiki Task, for changing the wiki, for running tests, for pushing or opening a pull request, or for closing the Task.
---

# Build a Task

This skill writes the code of one Task. Its input is a Task key and one code
folder. Its output is one commit on a new branch of that code repository, in
a worktree of its own, not pushed. The commit message ends with the line
`Task: <Task key>`, which `sdlc-close-task` later uses to find the merged
code.

It writes code, never the wiki: section 8 lists what it never does.

## Before you start

Read, in this skill's folder, `references/read-protocol.md`,
`references/flow.md` and `references/code-checks.md`. `flow.md` gives the
steps of the run and the three gates; this file says what is this skill's own
at each step. This skill has no write protocol and makes no draft: where
`flow.md` says "the worktree", it is a git worktree of the code repository
(section 3).

Find the wiki as the read protocol says, and check that it matches this
skill. `RELEASE`, next to this file, holds one line such as `1.0.0`:

```bash
cd "$WIKI" && $T copy check --release "<the line in RELEASE>"
```

Any `status` but `current` stops the run: say which side is older, and that
`sdlc-setup-wiki` upgrades the wiki. Then read the schema pages `task.md`,
`convention.md` and the page of each Design type in the Task's scope, in the
wiki's `.wiki-llm/schema/`.

Other requests go elsewhere; say so and stop:

| Request | Answer |
|---|---|
| Code with no Task in the wiki | Not this skill: plan the Task first with `sdlc-plan-tasks` |
| Review a code change | `sdlc-review-code` |
| Record that the code is merged | `sdlc-close-task` |
| Change the requirements, the design, the user stories or a Task | `sdlc-write-spec`, `sdlc-design-arch`, `sdlc-write-stories`, `sdlc-plan-tasks` |
| Runnable code for a TestCase, or running tests | Not an sdlc-skills skill |
| Push, open a pull request, merge | The person does that |

## 1. Look up: the Task, the wiki and the code

**The input.** One Task key and one code folder. The user names the folder;
"this folder" is an answer. Never guess it. A Task changes one repository, so
a second folder is a second run.

Find the Task on the wiki's default branch:
`git ls-tree -r --name-only "$DEFAULT" -- wiki | grep '/TASK-<name>.md$'`.
When several Applications have a Task with that key, ask which.

**Refuse**, naming the reason and what to do instead, when:

| Case | Say |
|---|---|
| The Task is not on the default branch | Name the draft that holds it (`git branch -a --list 'wiki/tasks-*'`) and ask to merge it first; with no such draft, `sdlc-plan-tasks` |
| The Task is `Done` | Its code is merged. A further change is a new Task or a ChangeRequest |
| The parent Feature is `Released` or `Deprecated`, or the parent ChangeRequest is `Implemented` or `Rejected` | The work is closed |
| The code folder is not a git repository | `git -C "$SRC" rev-parse --show-toplevel` prints nothing |

A refusal is not a question.

**A spec that is not agreed yet.** When the parent is not `Approved` (a
Feature `Draft` or `ReqApproved`, a ChangeRequest `Proposed` or
`ReqApproved`), or `$T outdated` lists this Task (its `basedOn` is older than
the parent's `version`), say so in the first round and go on only when the
person says so: the Requirements may still change, and `sdlc-close-task`
records the Task as done only once the parent is `Approved` and the Task's
`basedOn` is current.

**A blocker that is not `Done`.** When a Task under `# Blocked by` is `Todo`,
say so in the first round and go on only when the person says so: its code
may be merged and not yet closed in the wiki.

Uncommitted changes in the code folder do not matter. This skill works in a
worktree of its own and leaves the person's checkout as it is.

**Read**, on the wiki's default branch:

- the Task: `# Acceptance`, the Requirements it links, `# Planned scope`,
  and the user stories under `# Stories`, for the actor's goal and the
  scenarios its code must satisfy (read only);
- each Design file in the scope: its contract, which is the target, and its
  `# Pending changes` entry for this Task's parent;
- the parent's `# Architecture` or `# Delta`, and the decisions it links;
- `<app>/conventions.md`: coding standards, branching, testing policy,
  definition of done;
- the References the Task, its parent and its Design files link under
  `# References`, and those in `<app>/references/index.md` about the scope:
  each overview, then the content or the code at `resource` it points to.
  Follow what each note says to take from it. A Reference is an example, not
  a contract: where it differs from the Task, a Design file or
  `conventions.md`, those win.

Take every rule under `# Validations` and every exit of `# Flowchart` of
each Endpoint and Subscription in scope as a checklist: the plan names where
each is coded and the unit test that covers it, and the check before the
commit ticks each one off.

Note the wiki commit you read: `READ=$(git -C "$WIKI" rev-parse "$DEFAULT")`.

Then read the code folder: how it is laid out, where each scope item lives or
will live, how its unit tests are written, and what the default branch is:

```bash
SRC=<the code folder>
git -C "$SRC" fetch --quiet origin 2>/dev/null
BASE=$(git -C "$SRC" symbolic-ref --quiet --short refs/remotes/origin/HEAD \
  || { git -C "$SRC" show-ref --verify --quiet refs/heads/main && echo main; } \
  || echo master)
```

`BASE` is the remote's default branch, else a local `main`, else `master`, so
a repository with no remote still works.

## 2. Questions and the Intent gate

Ask in rounds, as `references/flow.md` section 4 says. The first round names
the Task, its parent and the code folder, and puts to the person:

- the branch name and the worktree path (section 3);
- where each scope item goes in the code, when the code allows more than one
  place, with your recommendation and the file paths it rests on;
- a scope item that is not in this folder: it belongs to another repository,
  and is listed, not built;
- a blocker that is not `Done`;
- the wiki question. This skill never writes the wiki, so every answer but
  "nothing" goes under "For other skills".

Do not ask what the Task, a Design file or `conventions.md` already settles.

**Intent gate.** Restate the Task, the code folder, the branch name and the
worktree path, and what will not be built here. Ask for approval.

## 3. The worktree and the Run plan

| Name | Value |
|---|---|
| `NAME` | The Task key without `TASK-`: `coupon-api` |
| The branch | `task/<NAME>`, unless `conventions.md` says how branches are named; then that rule |
| The worktree | `<code folder>/.worktrees/<NAME>/` |
| The Run plan | `plan.md` at the root of the worktree; `sdlc-plan.md` when the repository tracks a `plan.md` of its own there |

Use plain git, not the wiki's tool. Before the worktree is added, make git
ignore the worktrees and the Run plan through the repository's
`info/exclude`. That file is local and never committed, so the repository's
own `.gitignore` is not touched:

```bash
PLAN=plan.md
git -C "$SRC" cat-file -e "$BASE:plan.md" 2>/dev/null && PLAN=sdlc-plan.md
EXCLUDE="$(git -C "$SRC" rev-parse --path-format=absolute --git-common-dir)/info/exclude"
mkdir -p "$(dirname "$EXCLUDE")"
for line in ".worktrees/" "/$PLAN"; do
  grep -qxF "$line" "$EXCLUDE" 2>/dev/null || echo "$line" >> "$EXCLUDE"
done
git -C "$SRC" worktree add -b "<branch>" "$SRC/.worktrees/$NAME" "$BASE"
```

An ignore rule does not hide a file git already tracks. That is why a
repository with its own `plan.md` gets `sdlc-plan.md`: its file is never
overwritten, deleted or committed by this skill.

**A resumed build.** When the branch or the worktree already exists, an
earlier run started this Task. Never delete either. Show the branch's commits
(`git -C "$SRC" log --oneline "$BASE..<branch>"`) and the Run plan when there
is one, and go on as `flow.md` section 5 ("Resuming") says. A branch with no
worktree gets one: `git -C "$SRC" worktree add "$SRC/.worktrees/$NAME" "<branch>"`.
With no Run plan, write a new one for what is left.

**The Run plan.** Write it as `flow.md` section 5 says. For code it is the
design, so nothing else is shown at the Design gate. Under `## Files`, one
line per code file and per unit-test file: the path, added or changed, what
it does, and the scope item and the acceptance item it serves:

```markdown
## Files
- [ ] src/api/coupons.py (add: POST /coupons/apply; EP-apply-coupon; acceptance 1 and 2)
- [ ] src/api/test_coupons.py (add: unit tests for the 200, 404 and 409 paths; acceptance 1 to 3)
- [ ] db/migration/V7__coupons.sql (add: table coupons; TBL-coupons)

## Not built here
- WEB-storefront, the coupon field: not in this folder
```

`## Not built here` lists each scope item the plan does not cover, with the
reason. Leave it out when every item is covered.

## 4. Design gate

Show the Run plan in full. Ask for approval. On rejection, remove a worktree
and a branch this run made (`git -C "$SRC" worktree remove --force
"$SRC/.worktrees/$NAME"`, then `git -C "$SRC" branch -D "<branch>"`); leave
those of a resumed build as they are.

## 5. Write

In the worktree, write the code and its unit tests as `conventions.md`
requires, ticking each file in the Run plan. Match the code around it: its
layout, its names, its way of testing.

Never run the tests, the build or the code. Whether they pass is the
pipeline's and the reviewer's to say, and the wiki records no test result.

Write no runnable test for a TestCase of the wiki, and touch no TestSuite:
unit tests only.

**When the design is wrong.** The code cannot meet a Design file's contract,
or needs a contract the wiki does not have. Stop at that point; never code
past a contract that differs from the Design file. Show the difference with
the code location and the wiki path, and name the remedy:

- the design should change: a ChangeRequest with `sdlc-write-spec`;
- the wiki is wrong about code that exists: a correction with `sdlc-import`
  on this folder.

The person may tell you to go on without that part. Then leave it out, move
its line to `## Not built here`, and list it in the summary under "Not done"
and "For other skills".

## 6. Self review and the Change-set gate

First check that the input did not change: `git -C "$WIKI" fetch --quiet
origin 2>/dev/null`, then `git -C "$WIKI" diff --stat "$READ" "$DEFAULT" --
<the Task file and each Design file in its scope>`. If it prints anything,
show it and go back to the Design gate.

Do the self review of `flow.md` section 6, by reading only, with the checks
of `references/code-checks.md`: acceptance, contract, outside the scope and
convention. Fix what they find and record each fix. What you cannot fix, and
everything under "Not checked", is shown at the gate.

**Change-set gate.** In the worktree, `git add -A`, then show
`git diff --cached --stat` and the diff, the commit message, and what the
self review could not fix. The commit message follows `conventions.md` and
ends with the trailer, after an empty line:

```text
Add the apply-coupon endpoint

Task: TASK-coupon-api
```

Ask for approval. A change returns to section 5, or to the Design gate if the
plan changes. On approval, delete the Run plan file and commit on the branch.
Do not push.

## 7. Summary

"Done" names the branch and the worktree and says the commit is not pushed.
"Next" says: push the branch, open the pull request, have it reviewed
(`sdlc-review-code` checks it against the wiki), merge it, then close the
Task with `sdlc-close-task`.

```text
Done: task/coupon-api in ../orders-svc/.worktrees/coupon-api, 1 commit, not pushed.
Not done: the coupon field of WEB-storefront (not in this folder)
Next: push, open the pull request, review, merge; then sdlc-close-task.
```

## 8. What this skill never does

- It never writes to the wiki, and never changes a Task's status.
- It never touches a TestCase or a TestSuite.
- It never runs tests, the build or the code.
- It never pushes, opens a pull request, or calls a hosting service or a
  Tracker.
- It never changes the person's checkout, the repository's `.gitignore`, or
  a file named `plan.md` that the repository tracks.

## Done when

- The Task, the code folder, the branch and the worktree were approved at the
  Intent gate, and the Run plan at the Design gate.
- Every file of the Run plan is written, or is listed as not built with its
  reason.
- The checks of `code-checks.md` were made by reading, and what they could
  not settle was shown at the Change-set gate.
- One commit on the branch ends with `Task: <Task key>`; the Run plan file is
  not in it; nothing was pushed.
- Nothing in the wiki changed.
