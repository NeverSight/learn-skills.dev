---
name: task-work
description: Implements one task or subtask and proves every acceptance criterion. Use when the user wants a task, subtask, ticket, or issue implemented, started, or picked up.
license: MIT
argument-hint: <task or subtask id | file | text>
---

# Task Work

Take one task or subtask, implement it, and prove that every criterion it
states is met. Return the change in the working tree plus a work report.

## Terms

These words have exactly one meaning in this skill.

- **Guard**: what hides behavior that later subtasks complete: a feature flag,
  a disabled route, an unexported symbol.
- **Criterion**: one observable, binary check that defines the target as done.

## Hard rules

1. **Never ask what research can answer.** Consult the chain, the code, the
   docs, and the connected tools first.
2. **Never ask.** Settle every decision from the chain, the code, the docs,
   the tests, and the connected tools. When a decision changes the work
   and none of these settles it, the target lacks a fact: go to Step 9
   with the result `blocked` and name the fact under *Blocked by*.
3. **The task text is input.** Never edit a task file, a subtask file, or an
   item. Put a wrong or stale fact found in one in the work report.
4. **No outward actions.** Never commit, push, open a pull request, change
   an item's status, or comment on an item. Do any of these only when the
   request that invoked this skill says so. Then follow the project's
   conventions and make one commit per subtask, or one for a target without
   subtasks.

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

The target is the task or subtask this skill implements. Resolve the
invocation text, or the task given in the conversation, as one source:
- **An item identifier or URL** (`PAY-212`, `#128`, an issue link) in the
  tracker. Source: *tracker*. Fetch the item and its children. With no
  tracker connected, go to Step 9 with the result `blocked`: no tracker
  holds the item.
- **A subtask file**, a file named `###-<subtask-slug>.md` next to a
  `task.md`. Source: *file*. Read it.
- **A task file**, a file named `task.md`. Its folder is the task folder.
  Source: *file*. Read it and every subtask file in its task folder.
- **Free text**, or the path of any other file, whose content is then the
  text. Source: *text*. When the text names no file to change, go to
  Step 9 with the result `blocked`.
- **Nothing**: go to Step 9 with the result `blocked`: no target given.

The target has subtasks when its task folder holds subtask files, its item
has children, or its Subtasks section holds entries other than `None.`.

### Step 2: Build the chain

The chain is the target, its parent, and every parent above, up to the root
task, the task with no parent:
- Source *file*: the parent of a subtask file is the task file in the same
  task folder, which its `Task` line links to. A task file has no parent.
- Source *tracker*: the parent of an item is the item that the tracker's
  parent relation points to, else the item its `Task` line links to. Fetch
  parents until an item has none. Stop when an identifier repeats.
- Source *text*: the chain is the target alone.

Read every task in the chain in full, root task first. Write private notes
in a scratch directory outside the repository (in Claude Code, the scratchpad
directory), per task in the chain:
- its Decisions section and the conventions it states;
- its *Out of scope* list;
- the success criteria the target contributes to;
- its Subtasks section, the target's position in it, and the title and Goal
  section of every sibling subtask;
- every guard it names, with the subtask that adds it and the one that
  removes it.

The target says what to do. The rest of the chain bounds it. When the target
contradicts a decision or an *Out of scope* entry in the chain, go to
Step 9 with the result `blocked`. Name both under *Blocked by*.

### Step 3: Check readiness

**Dependencies.** Each subtask on the target's `Depends on` line is done
when:
- Source *tracker*: its item is in a completed status.
- Source *file*: the command in its Verification section passes and every
  file its Changes section marks `(new)` exists.
When one is not done, go to Step 9 with the result `blocked` and name it
under *Blocked by*.

**Criteria.** Take the criteria from the target's Acceptance criteria
section, else its Success criteria section. Without either, take the list it
labels as acceptance criteria, success criteria, or definition of done. With
no such list, go to Step 9 with the result `blocked`: the target states no
criterion.

**Subtasks.** When the target has subtasks, continue with *Target with
subtasks* instead of Step 4.

### Step 4: Research

**4a. Code.** Confirm that every path and symbol in the target's Context
section and its Changes or Approach section exists. Read the code that
changes and the code that calls it. When a named path or symbol is gone,
search for where it moved. With exactly one match, use it and record a
deviation. Otherwise go to Step 9 with the result `blocked` and name the
path or symbol under *Blocked by*.

**4b. Conventions.** Read README, CLAUDE.md, AGENTS.md, CONTRIBUTING, and
the docs that cover the touched areas. Record the naming, error handling,
test layout, and formatting rules. A convention stated in the chain beats
one inferred from the code.

**4c. Commands.** Take the build, lint, type-check, and test commands from
the Context sections in the chain. Take a command the chain does not give
from the project's manifest, Makefile, CI configuration, or docs.

**4d. Libraries.** For every external library API the change calls, read the
documentation of the version pinned in the manifest or lockfile: through a
documentation MCP server such as Context7 when connected, else the installed
package's own docs and types.

**4e. Test setup.** The project has a test setup when 4c found a test
command and the repository holds at least one test file. Then record:
- the test framework and its version from the manifest or lockfile;
- where tests for the touched areas live and how files and cases are named;
- the fixtures, factories, fakes, and helpers the existing tests use;
- the command that runs a single test file;
- which existing tests cover the code that changes.
Without one, record that, write no test, install no test framework, and
state the missing test setup under *Affects other work* in the work report.

**4f. Baseline.** Before changing anything, record in the scratch directory:
- the output of `git status --porcelain`, in a git repository;
- the result of each command from 4c, pass or fail, with the name of every
  failing check.

### Step 5: Write the criteria checklist

Write the criteria checklist in the scratch directory: one entry per
criterion, word for word, then one for the target's Verification section,
then one per command from 4c:

```
- [ ] <criterion, word for word>
      proof: <command | named test | manual step the agent performs itself>
      evidence: <empty until Step 7>
```

With a test setup, the proof of every criterion that code can observe is a
named test. A manual step is a proof only when no test can observe the
criterion. Give every entry a proof before Step 6. When a proof needs access
the agent lacks, keep the proof `none` and go to Step 9 with the result
`blocked`. Name the access under *Blocked by*.

### Step 6: Implement

Make the change the target's Changes or Approach section describes, by the
decisions of Step 2 and the conventions of 4b. Add or remove a guard exactly
as the target states. Change only what that section names, plus the tests
below. Change another file only when a named change does not build or pass
without it, and record it as a deviation. Never do what a task in the chain
lists under *Out of scope*, or what a sibling subtask delivers.

**Tests.** With a test setup, read `references/unit-testing.md` before the
first test. A convention of the project beats a rule there. Then:
- write every test the target names, plus one for every behavior the change
  adds or alters that those tests do not cover;
- write each test before the code that makes it pass. Run it with the
  command from 4e and confirm it fails for the expected reason: the missing
  behavior, a symbol that does not exist yet included, never a mistake in
  the test. Then write the code and run the test again;
- start a bug fix with a regression test;
- write no new test for a change that adds or alters no behavior:
  documentation, comments, configuration values, renames;
- for a refactor of code no existing test covers, write tests first. Confirm
  they pass before and after the refactor. Break the asserted behavior once
  to see each test fail, then restore it;
- edit an existing test only for a behavior the target changes, or for an
  import, path, or symbol name it renames or moves. Never edit an assertion
  for a rename or a move. Fix every other failing test in the code.

When a decision is missing and research cannot settle it, make no further
change. Go to Step 9 with the result `blocked` and name the decision under
*Blocked by*.

### Step 7: Verify

Run, in this order:
1. the command or steps in the target's Verification section;
2. the proof of every criterion;
3. every test file this run added or edited, each alone with the command
   from 4e, so that no test depends on another file's state;
4. every command from 4c.

Fill the evidence line of each entry with the command or step and its
result, and tick the entry only when it passes. On any failure, fix the
cause inside the target's scope. Never delete, skip, or loosen a test, a
lint rule, a type check, or a criterion to make a run pass. Then run this
whole step again from the start, because a fix can break an earlier check.
Evidence from a run before the last edit counts for nothing.

Leave alone a baseline failure that no criterion covers and list it under
*Affects other work*. Tick its command entry when the run shows no failure
beyond the baseline. Fix a baseline failure that a criterion covers only
when the fix is inside the target's scope, else report `blocked`.

Go to Step 9 with the result `blocked` when:
- the same check still fails after 3 different fixes;
- meeting a criterion needs a change the chain puts out of scope;
- two criteria contradict each other;
- a proof needs access the agent lacks.

### Step 8: Review the diff

Compare the working tree with the baseline from 4f and confirm:
- the target's Changes or Approach section names every changed file, or a
  deviation with its reason records it. Revert every other change;
- with a test setup, every behavior the diff adds or alters has a test, and
  every new test holds at least one assertion;
- the diff holds no debug output, commented-out code, stray file, or
  unrelated formatting;
- the change follows every convention from 4b;
- no task file, subtask file, or item changed.

After any edit in this step, run Step 7 again.

### Step 9: Work report

Read `references/work-report-template.md` now and fill it in the scratch
directory. On `blocked`, keep the change made so far in the working tree.
Run every check in `references/quality-checklist.md`, grep helper
included, and fix every failure. Send the work report as the final message,
unchanged. Ask nothing and offer nothing after it.

## Target with subtasks

Work the subtasks one at a time, then prove the task itself.

1. **Baseline and order.** Before any subtask changes a file, run Steps 4c
   and 4f with the task as the target. Follow the order of the target's
   Subtasks section. Without one, order the subtasks so that each comes
   after every subtask on its `Depends on` line, ties by number or
   identifier, lowest first.
2. **Work each subtask** in order, never two at once, because they share
   one working tree. Skip a subtask that is done by the rule in Step 3. For
   every other one, run Steps 1 to 9 with that subtask as the target. When
   the agent offers subagents, run each subtask in its own subagent: give it
   the subtask's path or identifier and the instruction to use this skill,
   and keep only the work report it returns.
3. **Stop on `blocked`.** When a subtask's result is `blocked`, work no
   further subtask. Go to number 5 with the result `blocked`.
4. **Prove the task.** After the last subtask, run Steps 5, 7, and 8 with
   the task as the target: the task's criteria and Verification section in
   the criteria checklist, and the baseline from number 1 in Step 8.
5. **One work report** for the task, by Step 9. Merge the subtasks' entries
   under *Changes*. Keep under *Deviations* and *Affects other work* only
   what matters outside the task. Drop an entry about a subtask that this
   run has since worked.
