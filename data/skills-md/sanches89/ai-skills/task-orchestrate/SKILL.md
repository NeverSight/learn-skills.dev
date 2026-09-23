---
name: task-orchestrate
description: Runs a whole task end to end, one commit per subtask, then refactor rounds. Use when the user wants a task with subtasks implemented or orchestrated from an item or a task file.
license: MIT
argument-hint: <task id | task file>
---

# Task Orchestration

Take one task and run every subtask through the `task-work` skill, one at a
time, each in its own subagent and each with one commit. Then clean the
result up: the `task-refactor` skill writes a refactor task and the same
jobs run it, for up to three rounds. Carry every fact from one job to the
next, and ask nothing. Prove the task and keep the plan and every report
with the task.

## Terms

These words have exactly one meaning in this skill.

- **Job**: one task or subtask together with the `task-work` run that
  implements it.
- **Record**: where this run keeps its plan, every work report, and the
  orchestration report.
- **Probe**: a run of given commands in the tree the plan names, kept to
  one line of pass or fail per command.
- **Round**: one `task-refactor` run over the code this run changed, and
  the jobs of the refactor task it writes.

## Hard rules

1. **Every change comes from a job or a round.** Never edit project code
   yourself, and
   never edit a task file, a subtask file, or the body of an item. Put a
   wrong or stale fact found in one in the record as a fact.
2. **One job at a time.** Never run two jobs at once: they share one working
   tree.
3. **Never ask.** Every job works from its target, the code, the docs, and
   the connected tools, and reports `blocked` when its target lacks a
   fact. Settle every choice of this skill by the rules below.
4. **Keep only the result.** Keep from each job its work report, and
   nothing else.
5. **No outward actions beyond the record and the commits.** Never push or
   open a pull request. Change an item's status or comment on an item only
   as the record rules of Step 1 state. Do more only when the request that
   invoked this skill says so.
6. **Delegate every read and run.** Run in a subagent (in Claude Code, the
   `Agent` tool) every step that reads a task, an item, a manifest, or a
   doc. Run in a subagent every build, lint, type-check, test, and
   Verification command. The subagent returns only what the step names.
   The context window then holds the plan, the record, and those returns,
   and stays small over a long run. Without subagents, follow the step
   yourself and keep only what it names.

## Workflow

### Step 1: Load the target

**Tracker.** The tracker is the issue tracker the project uses, reached
through an MCP server or through `gh`, the GitHub CLI. Find it once, in
this order, and take the first that applies:
1. the tracker that README, CLAUDE.md, AGENTS.md, CONTRIBUTING, or
   `docs/README.md` names, when an MCP server or `gh` reaches it. When
   the docs name one that nothing reaches, no tracker is connected;
2. the tracker of an MCP server whose tools read and write issues. List
   the MCP tools of the agent (in Claude Code they are deferred: search
   them with `ToolSearch` for
   `issue ticket project linear jira notion asana github`). With several,
   the first listed;
3. GitHub Issues through `gh`, when `git remote get-url origin` prints a
   `github.com` URL and `gh auth status` exits 0. Then
   `gh issue view <number> --comments` reads an item,
   `gh api repos/{owner}/{repo}/issues/<number>/sub_issues` lists its
   children, and `gh issue create`, `gh issue edit`, `gh issue comment`,
   and `gh issue close` write. A POST with `gh api -X POST` to that
   `sub_issues` path with `-F sub_issue_id=<id>` links a child, where
   `<id>` is the `id` that `gh api repos/{owner}/{repo}/issues/<child>`
   prints. A closed issue is in a completed status, and `gh` has no other
   status;
4. else no tracker is connected.

By hard rule 6, run the tracker rule in a subagent that returns the
tracker and the way it is reached, and nothing else.

The target is the task this skill runs. Resolve the invocation text, or the
task given in the conversation, as one source:
- **An item identifier or URL** (`PAY-212`, `#128`, an issue link) in the
  tracker. Source: *tracker*. With no tracker connected, end with one
  line: no tracker holds the item, give a task file path. Write no report.
- **A task file**, a file named `task.md`. Its folder is the task folder.
  Source: *file*.
- **A subtask file**, a file named `###-<subtask-slug>.md` next to a
  `task.md`. Source: *file*.
- **Free text**, the path of any other file, or nothing: end with one
  line: no task to run, give a task file path or an item identifier. Write
  no report. The `task-create` skill writes a task from text.

**Summary.** Never open the target yourself. Run a subagent with this
prompt, the placeholders filled, and nothing else. Without subagents,
follow the prompt yourself and keep only its return:

```
Read <task file path | subtask file path | item identifier and URL> in
full. A subtask of a task is a subtask file in its task folder, a child
of its item, or an entry of its Subtasks section other than `None.`.
Read every subtask of a task, and the task file or parent item of a
subtask. List the subtasks in the order of the task's Subtasks section,
else ordered so that each comes after every subtask on its Depends on
line, ties by number or identifier, lowest first. Return this summary
and nothing else:

title: <the target's title>
subtasks: none | one per line below
- <number or identifier> <title>; depends on: <numbers | none>;
  verification: <its Verification section, word for word>;
  new: <every path its Changes section marks (new)> | none
commands: <the build, lint, type-check, and test commands from the
  target's Context section, or its task's for a subtask; a command the
  tasks do not give, from the project's manifest, Makefile, CI
  configuration, or docs>
verification: <the target's Verification section, word for word>
new: <every path the target's Changes section marks (new)> | none
```

The target has subtasks when the `subtasks` line is not `none`.

**Record.** The record is the first of these that applies:
- source *tracker*, when the tracker can add a comment to an item: the
  items. The plan, every fact, and the orchestration report are comments
  on the target's item. Each work report is a comment on its job's item.
  A job's state is its item's status: in progress when the job starts,
  completed on `done`, unchanged on `skipped` and `blocked`. A status the
  tracker lacks stays unchanged. The target's item is completed when the
  result is `done`;
- source *file*: `orchestration.md` (new) in the target's task folder.
  When the task folder is in the repository, write it in the tree the
  jobs run in, at the same relative path. It holds the plan, then each
  work report under `## Report: <job>`, then the orchestration report. A
  job's state is its line in the plan;
- else `<scratch-dir>/orchestration.md`, with the same content.

A scratch directory outside the repository (in Claude Code, the scratchpad
directory) is written `<scratch-dir>` in commands. When the record holds a
plan from an earlier run, copy its facts into the new plan.

### Step 2: Plan the jobs

**Jobs.** With subtasks, one job per subtask, in the order of the
summary's subtask lines. Without subtasks, one job: the target itself.

**Tree.** In a git repository, the jobs run in a worktree when one of these
holds:
- the request asks for a worktree;
- `git status --porcelain` prints anything;
- the current branch is the default branch: the one
  `git symbolic-ref --short refs/remotes/origin/HEAD` prints, else `main`
  when it exists, else `master`.

In every other case the jobs run in the current working tree on the
current branch. Outside a git repository, they run in the current working
tree without commits.

**Branch.** The worktree gets a new branch from `HEAD`. Name it by the
project's branch convention when the docs state one, else
`task/<task folder name>` for source *file* and `task/<identifier>` in
lowercase for source *tracker*.

Draft the plan:

```
# Plan: <target title>
target: <path | identifier and URL>
tree: current | <scratch-dir>/worktree, because <reason>
branch: <name> | none: no git repository
base: <commit, filled in Step 3>
baseline: <command>: pass | fail (<failing checks>), filled in Step 3
jobs:
1. <subtask number or identifier> <title>: pending
2. <...>
rounds:
facts:
```

State the jobs, the tree with its reason, and the branch in chat, and
continue.

### Step 3: Prepare the tree

1. **Worktree.** When the plan names one, run
   `git worktree add -b <branch> <scratch-dir>/worktree HEAD`. When the
   branch already exists, continue on it with
   `git worktree add <scratch-dir>/worktree <branch>` and add
   `, continued` to the plan's `branch` line. From here on, run every
   command in the tree the plan names, written `<tree>`.
2. **Baseline.** Fill `base` with `git rev-parse --short HEAD` in
   `<tree>`. Fill `baseline` with a probe of the summary's `commands`. A
   probe runs in a subagent given this prompt, the placeholders filled,
   and nothing else. Without subagents, follow the prompt yourself and
   keep only its return:

   ```
   Run each command or step below in <tree>, in order. Return one line
   per command or step, `<it>: pass | fail (<every failing check by
   name>)`, and nothing else: no output, no log, no fix.
   <commands or steps>
   ```

3. **Record the plan.** Write the plan to the record.

### Step 4: Run the jobs

Run the jobs in plan order, one at a time. Read
`references/job-prompt-template.md` once, before the first job. For each
job:

1. **Skip a done job.** The job's target is done when, for source
   *tracker*, its item is in a completed status; for source *file*, a
   probe of the job's `verification` and of `test -e <path>` for each of
   its `new` paths passes on every line. Mark the job `skipped` in the
   record and continue with the next job.
2. **Start.** Mark the job `running` in the record. Note the output of
   `git status --porcelain` in `<tree>` as the job's start.
3. **Write the prompt.** Fill the template: the job's target, `<tree>`,
   the branch, and every fact in the record.
4. **Run the job.** When the agent offers subagents, run the job in a new
   subagent. Give it the prompt and nothing else. Without subagents,
   follow the prompt yourself with the `task-work` skill and continue here
   with its result.
5. **Read the result.** The result is one of:
   - **A work report**, which starts with `# Work report:`. Save it in the
     record.
   - **Anything else**: an empty result, an error, or a message that is
     no work report. In a git repository, restore `<tree>` to the job's
     start: for every path that `git status --porcelain` lists now and
     the job's start does not, run `git checkout -- <path>` when git
     tracks it, else delete it. Run the job once more with the same
     prompt. On a second one, mark the job `blocked` in the record with
     the cause and go to Step 7 with the result `blocked`.
6. **On `done`.** When `git status --porcelain` in `<tree>` lists a path
   that the job's start does not, commit it as the job's commit. Use the
   project's commit convention, with the job's title as the subject. Add
   every bullet under *Deviations* and *Affects other work* of the report
   to the record as a fact, prefixed with the job's number. Mark the job
   `done` in the record with the hashes on the report's *Commits* line and
   `git rev-parse --short HEAD`. Continue with the next job.
7. **On `blocked`.** Mark the job `blocked` in the record and go to Step 7
   with the result `blocked`. Run no further job.

### Step 5: Refactor rounds

Run up to three rounds after the last job. The limit only stops an endless
loop: a third round is no failure, and the run continues to Step 6 after
it. For each round:

1. **Review.** Run a subagent with this prompt, the placeholders filled,
   and nothing else. Keep the `Save to files.` line only for source
   *file*. Without subagents, follow the prompt yourself and keep only
   its return:

   ```
   Use the task-refactor skill on <the git range <base>..HEAD | the
   paths under Changes of every work report so far>. Work in <tree>:
   every command runs there and every file is read and written there.
   Save to files.
   Return your final recap and nothing else.
   ```

2. **Round result.** Add `R<round>: <task file path | identifier | none>`
   under `rounds` in the record. When the recap names no task file path
   and no item identifier, the round is empty: go to Step 6. Otherwise,
   for source *file* in a git repository, when the task file path is
   inside `<tree>`, commit the new task files alone on the branch. Use
   the project's commit convention, with the subject
   `Add <refactor task title>`.
3. **Load.** Load the refactor task by the summary prompt of Step 1. Add
   one job per subtask under `jobs` in the record, as
   `R<round>.<n> <title>: pending`, in the order of the summary's subtask
   lines.
4. **Run.** Run the new jobs by Step 4, with the target's record. Then
   start the next round.

### Step 6: Prove the target

Run one probe of, in this order:
1. the summary's `verification`;
2. every command on the summary's `commands` line.

The proof passes when the `verification` passes and no command fails
beyond the failures the baseline records. On a failure, the result is
`blocked`, and the failing command and check go into the prompt of
Step 7.

### Step 7: Finish

1. **Report.** Read `references/quality-checklist.md` now and confirm
   every check under *Run* from this run. Then run a subagent with this
   prompt, the placeholders filled, and nothing else. `<skill-dir>` is
   the folder holding this `SKILL.md`. Without subagents, follow the
   prompt yourself and keep only its return:

   ```
   Read the record: <path of orchestration.md | the comments on item
   <identifier> and on its children>. Read the target
   <task file path | item identifier and URL> and its subtasks. Read
   <skill-dir>/references/orchestration-report-template.md and
   <skill-dir>/references/quality-checklist.md. Fill the orchestration
   report from the record and from git in <tree>. The proof is
   <pass | fail: <command> (<failing check>) | not run>. Run every check
   in the checklist except those under Run, grep helper included, and
   fix every failure. Return the report and nothing else.
   ```

   Save the orchestration report in the record, and on `done` mark the
   target's item completed.
2. **Commit the record.** For source *file* in a git repository, when the
   record is inside `<tree>`, commit `orchestration.md` alone on the
   branch. Use the project's commit convention, with the subject
   `Record the orchestration of <target title>`.
3. **Worktree.** On `done` with a worktree, run
   `git worktree remove <scratch-dir>/worktree` and keep the branch. On
   `blocked`, keep the worktree, so that the change so far stays in it.
4. **Send.** Send the orchestration report as the final message, unchanged.
   Ask nothing and offer nothing after it.
