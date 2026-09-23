---
name: task-refactor
description: Reviews code and writes a refactor task with one subtask per refactoring, and changes no code. Use when the user wants code refactored, simplified, or cleaned up, or says it is messy.
license: MIT
compatibility: Works in any project, with or without git. The measurements need Node.js 22.13 or newer with npx, network access on the first run, and read access to github.com/sanches89/code-measure. Complexity also needs uv, pipx, or a Python that has lizard. A missing tool skips its measurement and never blocks the review.
argument-hint: <path | symbol | git range | task or subtask id | file | text>
---

# Task Refactor

Review the code inside the refactor scope of one request. Find every smell,
pick the refactoring that removes it, and write the refactor task: one task
with one subtask per refactoring, in the format the `task-work` skill
implements. Every fact in it comes from reading, measuring, and running
commands on the unchanged code.

## Terms

These words have exactly one meaning in this skill.

- **Behavior**: what a caller or a user observes of the code: returned values,
  changed state, raised errors, written output, and calls to external systems.
- **Contract**: everything that code or people outside the refactor scope
  depend on. Exported symbols with their signatures, endpoints, command-line
  flags, file formats, database schemas, configuration keys, and the names of
  events, logs, and metrics.

## Hard rules

1. **Read-only on the project.** Write only the task file and the subtask
   files, in Step 9. Write drafts in a scratch directory outside the
   repository (in Claude Code, the scratchpad directory).
2. **Never ask.** Settle every choice from the code, the docs, the tests,
   the connected tools, and the rules below. Write the task without
   approval.

## Workflow

### Step 1: Load the request

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

Resolve the invocation text, or the request in the conversation, as exactly
one kind:
- **One or more paths** of files or folders that exist. Kind: *path*.
- **A symbol name**: a function or a module in the code. Kind: *symbol*.
  Search for its definition. With more than one, take every definition.
- **A git range**, such as `main..HEAD`, or words that name the uncommitted
  changes or the current branch. Kind: *range*.
- **A task or subtask**: an item identifier or URL (`PAY-212`, `#128`, an
  issue link) in the tracker, a task file, or a subtask file. A task file
  is a file named `task.md`, and its folder is the task folder. A subtask
  file is a file named `###-<subtask-slug>.md` next to a `task.md`. Kind:
  *task*. Read it with every subtask file in its task folder, or every
  child of its item. With no tracker connected, an identifier is kind
  *text*.
- **Free text**, or the path of any other file, whose content is then the
  text. Kind: *text*.
- **Nothing**: kind *path* with the repository root.

Write private notes in the scratch directory from this step on, written
`<scratch-dir>` in commands. Keep in them every list a later step reads.

### Step 2: Set the refactor scope and the contract

**Refactor scope.** Take the files from the request:
- *path*: every file under the paths;
- *symbol*: the file of every definition of the symbol;
- *range*: every file that `git diff --name-only <range>` prints and that
  still exists. For uncommitted changes, use `git status --porcelain`;
- *task*: every file that the Changes or Approach section of the requested
  task names, and every file that its subtasks' Changes sections name;
- *text*: the files that hold the code the text names, found by search.

With an empty refactor scope, finish as Step 6 states for no entry.

Remove from the refactor scope:
- generated code, vendored code, lockfiles, build output, and snapshot files;
- database migrations that already ran;
- test files, unless the request names them. An existing test still
  changes only in an import, a path, or a symbol name a refactoring moves
  or renames, never in an assertion.

**Bounds of a requested task.** For kind *task*, read the requested task and
every parent above it, in full. The parent of a subtask file is the task
file in its task folder. The parent of an item is the item the tracker's
parent relation points to. Record every *Out of scope* list and every
Decisions section. Never write a subtask that does what one of them lists
under *Out of scope*. Follow every decision.

**Contract.** List every part of the contract that the refactor scope holds:
- every symbol that code outside the refactor scope imports or calls, found
  with the agent's code search or `git grep`;
- in a library that others install, every exported symbol, with or without a
  caller in the repository;
- every endpoint, command-line flag, file format, database schema,
  configuration key, and name of an event, a log, or a metric.

### Step 3: Research

**3a. Conventions.** Read README, CLAUDE.md, AGENTS.md, CONTRIBUTING, and the
docs that cover the refactor scope. Record the naming, error handling,
module layout, and formatting rules. Then find `<tasks-dir>`.

**Tasks directory.** `<tasks-dir>` is the folder that holds the task
folders. It is the first of these that exists:
1. the folder that the request or the conversation names;
2. the folder that README, CLAUDE.md, AGENTS.md, CONTRIBUTING, or
   `docs/README.md` names as the place for tasks, plans, or specs;
3. the parent of a task folder: a folder named `###-<task-slug>`, three
   digits, a hyphen, and a slug, that holds a `task.md`, anywhere in the
   repository outside `node_modules`, `.git`, and `vendor`. With several
   parents, the shortest path, then the first in alphabetical order;
4. a folder named `tasks`, `plans`, or `specs` that holds a `.md` file at
   any depth. It sits at most three levels below the repository root,
   outside `node_modules`, `.git`, and `vendor`. With several, the
   shortest path, then the first in alphabetical order;
5. else `<scratch-dir>/tasks/`.

**3b. Commands.** Take the build, lint, type-check, and test commands from
the project's manifest, Makefile, CI configuration, or docs. For kind
*task*, prefer the commands in its Context section.

**3c. Test setup.** The project has a test setup when 3b found a test command
and the repository holds at least one test file. When it has one, record:
- the test framework and its version from the manifest or lockfile;
- where the tests for the refactor scope live and how they are named;
- the fixtures, factories, fakes, and helpers the existing tests use;
- the command that runs a single test file;
- the coverage command, when the project configures one.

**3d. Analysis tools.** Read `references/measurement-tools.md` now. Record
every analysis tool the project configures, with its command and limits.
Record the options that make the test command write a test report and a
coverage report.

**3e. Tracker.** When a tracker is connected, record its relation for
children (sub-issue, child, parent field) and the fields an item and a child
item require. Record the team, project, or board that the request, the
requested task, or the docs name.

### Step 4: Record the baseline

Record in the scratch directory:
- the output of `git status --porcelain`, when the project is a git
  repository;
- the result of each command from 3b, pass or fail, with the name of every
  failing check;
- the result of each analysis tool from 3d;
- the test report and the coverage report, written into the scratch
  directory by the test command with the options from 3d. Skip a report the
  test runner cannot write without a new dependency;
- the measurement summary, from the measure tool run at the project root:

```bash
<measure> <path>... \
  --test-report <scratch-dir>/junit.xml \
  --coverage-report <scratch-dir>/coverage.info \
  > <scratch-dir>/baseline.json
```

`<path>...` is the files or folders of the refactor scope. Leave out the
option of a report that does not exist. Pass `--ignore <globs>` for
generated and vendored code inside the paths, and the project's own limits
with `--ccn`, `--length`, and `--params` when 3d found them. `--help` lists
every option and exit code. When the measure command fails to start, follow
*Without any tool* in `references/measurement-tools.md`.

**Coverage of the refactor scope.** Record which functions in the refactor
scope a test covers:
- with a coverage report, a function is covered when the tests ran every
  line and every branch of it. `coverage.functions.top` lists every function
  that falls short, highest CRAP score first. Raise `--top` when the list is
  cut;
- a coverage report proves that a test runs the code, never that a test
  asserts its result. Read the tests of every function a finding names;
- without a coverage report, read the tests that import or call the code.

When a test that covers a part of the refactor scope fails in the baseline,
remove that part from the refactor scope. Name it under the task's *Out of
scope* with the failing test.

### Step 5: Find and rank

Read `references/smell-catalog.md` now. Then read every file in the refactor
scope in full. A number alone is never a finding. Record one finding per
smell and location:
- the smell and its location as `path:line`;
- the evidence: the clone, the measured value against its limit, or what the
  code shows;
- the refactoring that removes it;
- the risk. `high` when the change crosses modules or touches the contract.
  Else `low` when the refactoring is in the safe set, the refactorings
  allowed on code that no test covers: Rename, Extract Variable, Inline
  Variable, Extract Function, Move Function, and Remove Dead Code. Else
  `medium`;
- whether a test covers the code, from Step 4.

Findings come from four origins: what the request names, the `top` lists of
the measurement summary, the project's analysis tools, and reading the code.

Drop a finding when:
- its refactoring adds a feature, fixes a bug, or tunes performance;
- its refactoring changes a part of the contract that the request does not
  name;
- it is a clone whose copies change for different reasons;
- it needs a new layer, interface, or option with fewer than three users;
- a task from Step 2 puts it out of scope;
- its code is about to be deleted or replaced, as the request or the docs
  state.

Record every dropped finding with its reason, for the task's *Out of scope*.

Rank the findings: first what the request names, then by hotspot score of
the file, then `low` risk before `medium` before `high`.

### Step 6: Order the refactorings

Turn the ranked findings into entries, one refactoring each. Order the
entries by kind:
1. Remove Dead Code;
2. Rename;
3. refactorings inside one function;
4. refactorings that move code between functions and modules.

Inside one kind, keep the rank from Step 5. Place an entry after every entry
it depends on. Split a contract change that the request names into three
entries: add the new form, move the callers, remove the old form. Moving
those callers is the one reason an entry changes a file outside the
refactor scope.

Write each entry in the notes in this form:

```
<number>. <Refactoring>: `<path:line>` (<symbol>), depends on: <numbers>
   finding: <smell and evidence>
   result: <the structure after the change>
   risk: low | medium | high
   tests: covered | characterization tests first | none: safe set
   verification: <one command>
```

Without a test setup, keep only entries from the safe set, with
`tests: none: safe set`. Move every other finding to the task's *Out of
scope*, with the reason `no test setup`.

**Characterization tests.** Read `references/characterization-tests.md` now.
For every entry marked `characterization tests first`, record the test cases
for the behavior of the code the entry changes, and the seam that reaches
the code. With no seam, drop the entry and record the reason for the task's
*Out of scope*.

**Verification.** Give every entry one verification command: the single-file
test command from 3c over the tests that cover the entry, chained with one
structural check that observes the result of the refactoring. A structural
check is a search for a name that finds nothing, a count of matches, an
existing file, or a measurement value. Run the command on the current code
and confirm that it fails: a command that passes before the refactoring
proves nothing. Without a test setup, the structural check alone is the
command.

With no entry, write no task. Finish with a short recap: the refactor scope,
the baseline measurements, and the statement that no finding met the rules
of Step 5. Ask nothing else.

### Step 7: Write the refactor task

Read `references/task-template.md` now. Fill it in the scratch directory for
the task and for each entry, one subtask per entry in the order of Step 6.

**The task:**
- *Title*: `Refactor <refactor scope in a few words>`.
- *Summary*: the refactor scope, the smells found, and the structure after
  every subtask.
- *Success criteria*: one per command from 3b, passing with no failure
  beyond the baseline, each baseline failure named. One per part of the
  contract from Step 2: same name, signature, and format, except a change
  the request names. One per entry: the structure after the change. The
  test counts: total not below the baseline, failed and skipped not above
  it. The coverage counts: uncovered lines and branches not above the
  baseline. The duplication and complexity values the entries change, with
  the target value.
- *In scope*: every file of the refactor scope.
- *Out of scope*: every bug found, with its location and the statement that
  the code keeps it. Every finding dropped in Step 5 or Step 6, with its
  reason. Every part removed from the refactor scope in Step 4. Every part
  of the contract, as a statement that it stays. Every *Out of scope* entry
  of a requested task, restated.
- *Approach*: one bullet per entry, in order: path and symbol, then the
  structure after the change.
- *Decisions*: read `references/refactoring-rules.md` now and write the
  rules every entry follows, as that file states. The conventions from 3a
  and 3c. The rule that a subtask applies one refactoring and gets one
  commit.
- *Context*: the commands from 3b with the report options from 3d, and the
  single-file test command. The analysis tools with their limits, and the
  measure command from Step 4. The baseline: one line per measurement with
  its values, or `skipped` with the reason. The test coverage of every
  function the entries change. For kind *task*, the identifier or path of
  the requested task.
- *Subtasks*: one line per entry, in order, with its dependencies.
- *Verification*: the commands from 3b, then the test command with the
  report options, then the measure command from Step 4 over the same paths.

**Each subtask:**
- *Title*: the refactoring and the symbol, imperative, under 80 characters.
- *Goal*: the structure after the change, in one sentence.
- *Context*: the smell and its evidence, with every location as `path:line`.
  The tests that cover the code, or the statement that none does. The
  single-file test command. The rules from `references/refactoring-rules.md`
  and the conventions this refactoring follows, restated. Every part of the
  contract the change touches, as a statement that it stays. For a rename
  or a move across many files, the rewrite tool from
  `references/measurement-tools.md`.
- *Changes*: first, for an entry marked `characterization tests first`, the
  test file, `(new)` or existing, with every test case from Step 6 named.
  Then every file the refactoring changes, with the symbol and the structure
  after the change. A file it creates, marked `(new)`, with what it holds.
- *Acceptance criteria*: each named characterization test passes on the
  unchanged code and after the change. The structure after the change, as a
  binary check. The tests that cover the code pass. Every part of the
  contract the change touches keeps its name, signature, and format. No
  assertion of an existing test changed.
- *Verification*: the one command from Step 6.

Writing rules:
- Write decisions as facts:
  `The three copies of the business-day rule call isBusinessDay.`, never
  `We decided that...` or `The copies should probably...`.
- Make each subtask self-contained: restate every decision and fact an agent
  needs to implement it with the repository alone. Never write `see task`,
  `as above`, or `same as subtask 2`.
- Use the paths and symbols verified in Step 2 and Step 5. Mark new files
  `(new)`.
- In the Changes section, name the functions to add, move, rename, or
  remove, with their inputs and outputs. Never implementation code.
- Write acceptance criteria that are binary: someone else can answer yes or
  no.
- Add no sections beyond the template: no Risks, Considerations,
  Alternatives, Future work, Nice to have, or Notes.
- Write at most 25 words per sentence, and only lines the implementing agent
  needs.

### Step 8: Quality check

Run every check in `references/quality-checklist.md`, grep helpers included,
over the draft. Fix every failure.

### Step 9: Save

Save to files when no tracker is connected, or when the user asked for files
at any point. Otherwise save to the tracker of 3e. Never ask which.

**To the tracker:**
1. Use the destination and required field values from 3e. When research
   did not settle a required value, save to files instead.
2. Create the task as a new item with the task's title and body.
3. Create one child item per subtask, in order, so that later children can
   link to earlier siblings. The subtask title is the title. The subtask
   is the body, with the task's item link on the `Task` line and
   sibling item links on the `Depends on` line. Link each child to the
   task's item with the tracker's relation. When the tracker has none, put
   child links in the task's body and the task's link in each child body.
4. Update the task's Subtasks section with the child links.

**To files**, by the numbering rule below:
1. A folder with the same `<task-slug>` under any number stays untouched.
2. Create the task folder `<tasks-dir>/###-<task-slug>/` with the next free
   number, with `<tasks-dir>` from 3a.
3. Write the task to `task.md` in the task folder.
4. Write one subtask file per subtask, `###-<subtask-slug>.md` in the task
   folder, numbered `001` upward in subtask order. Link the `Task` line to
   `./task.md` and the `Depends on` line to the sibling files. Link the
   task's Subtasks section to each subtask file.

**Numbering rule.** `###` is a zero-padded three-digit sequence from `001`:
the next free number across every entry of `<tasks-dir>` whose name starts
with three digits. Give subtasks the next free numbers inside their task
folder. A slug is a title in kebab-case: lowercase ASCII letters and digits,
every other run of characters replaced by one hyphen, cut to 60 characters,
with no leading or trailing hyphen. Build `<task-slug>` from the task title
and `<subtask-slug>` from the subtask title. The `task-create` and
`task-breakdown` skills share this layout.

Finish with a short recap: every item identifier and URL created, or every
path written, absolute when outside the repository, and the number of
subtasks. Ask nothing else.
