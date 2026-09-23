---
name: task-breakdown
description: Splits an existing task into commit-sized subtasks. Use when a task, ticket, issue, or spec is too big for one change and the user wants it broken down.
license: MIT
argument-hint: <task id | task file | task text>
---

# Task Breakdown

Take one task and split it into subtasks that an agent can implement one at a
time without asking a question. The implementing agent asks nothing and
stops on a missing fact: put every fact it needs in the subtask.

## Terms

These words have exactly one meaning in this skill.

- **Guard**: what hides behavior that later subtasks complete: a feature flag,
  a disabled route, an unexported symbol.

## Hard rules

1. **Read-only on the project.** Write only the task file and the subtask
   files, in Step 8. Write drafts in a scratch directory outside the
   repository (in Claude Code, the scratchpad directory), written
   `<scratch-dir>` in paths.
2. **Never ask what research can answer.** Consult code, docs, tests, and
   connected tools first.
3. **Never assume.** When a decision changes a subtask and research cannot
   settle it, ask the user.
4. **Write nothing before the user approves the full breakdown text**
   (Step 7).
5. **Only the task goes in.** The breakdown holds what the original task
   needs and the *Out of scope* entries, nothing else. A question or
   remark from the user on any other topic gets an answer in chat and no
   line in the breakdown. When it deserves a task of its own, say so in
   chat and write nothing about it in the breakdown.

## Workflow

### Step 1: Load the task

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

Resolve the invocation text, or the task in the conversation, as one of:
- **An item identifier or URL** (`PAY-212`, `#128`, an issue link) in the
  tracker. Source: *tracker*. Fetch the item and its children. When no
  tracker is connected, ask one question: give the task as a task file path
  or as text.
- **A task file**, a file named `task.md`. Its folder is the task folder.
  Source: *file*. Read it and every subtask file, `###-<subtask-slug>.md`,
  in its task folder.
- **Free text**, or the path of any other file, whose content is then the
  text. Source: *text*.
- **Nothing**: ask for the task first.

The task already has subtasks when its item has children, its task folder
holds subtask files, or its Subtasks section holds entries other than `None.`.
Then ask one question: replace them, or abort. On replace, Step 8 deletes
them, or closes them when the tracker cannot delete. On abort, stop.

Write one sentence: *The task is to <change> so that <outcome>.* Ask the user
to confirm or correct it before any research.

### Step 2: Research

**2a. The original task.** Read it in full. Treat every decision, success
criterion, and scope statement in it as a fact. Never ask about it again.

**2b. Codebase.** Read the code the task touches, not only file names.
Record, with paths and line numbers:
- the entry points, modules, and symbols the change touches or calls;
- how the project builds similar changes: patterns, naming, error handling,
  configuration, guards;
- the test conventions, where tests for the touched areas live, and the
  command that runs them in isolation;
- the build, lint, type-check, and test commands.
Use a read-only subagent for broad sweeps when the agent offers one (in
Claude Code, the `Explore` subagent).

**2c. Project docs.** Read README, CLAUDE.md, AGENTS.md, CONTRIBUTING,
`docs/`, and ADRs. Record the conventions and constraints that affect the
task. Then find `<tasks-dir>` and read the tasks, plans, and specs in it
that touch the same areas.

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

**2d. Tracker and MCP servers.** Use the tracker of Step 1. List the other
MCP tools of the agent (in Claude Code they are deferred: search them with
`ToolSearch` for `context7`). Then:
- **Tracker**: fetch related items and record their identifiers. Record the
  relation the tracker uses for children (sub-issue, child, parent field)
  and the fields a child item requires. Record the team, project, or board
  that the docs name.
- **Context7**: for every external library the task depends on, fetch the
  documentation of the version pinned in the manifest or lockfile. Record
  the API facts the subtasks rely on.
- **Other MCP servers**: use them when they hold facts the breakdown needs.
Never ask the user to install or connect anything.

**2e. Research notes.** Write a private file in the scratch directory with
two parts:
1. *Facts*: each with the path and line, identifier, or URL it came from.
2. *Open decisions*: every decision research did not settle, with the
   subtask it affects.

### Step 3: Interview

Order the open decisions: task scope first, then behavior, then technical
choices, then split choices (guards, ordering), then delivery details. Ask
delivery details only when the source is *text* and the breakdown goes to
the tracker by the rule of Step 8: the team, project, or board, and the
required field values research did not settle.

For each open decision:
- State it in one sentence, with what in the breakdown depends on it.
- Give 2 to 4 options grounded in research:
  `Add the retry loop in PaymentService.send() at src/payments/service.ts:88`,
  never `add retries`.
- Name the option you recommend.

After each answer, record the decision as a fact in the research notes and
add every new decision the answer creates. When the answer introduces an
adjacent topic, one a reader would expect in this task, ask one question:
in the task, or under *Out of scope*. Never expand or drop it in silence.

When the user asks a question or makes a remark on any other topic, answer
it in chat and record nothing from it: not in the research notes, not in
the breakdown, not under *Out of scope*. When it deserves a task of its
own, say so in chat once, then go on with the interview.

Never ask about what the original task, the code, the docs, or a project
convention settles: follow the convention and record it as a decision. Never
ask about a preference that changes no subtask. Continue until no open
decision remains.

### Step 4: Split

Produce the subtask list. Every subtask is one reviewable change with one
verification command, mergeable on its own: after it, the project builds and
every test, existing and new, passes. Make every subtask meet these
constraints too:
- **One concern.** Split again a subtask that needs two verification
  commands, or whose title needs the word "and".
- **Size.** Estimate the lines each subtask adds plus the lines it
  deletes, outside the test locations recorded in Step 2b. Split again
  a subtask above 1000 lines when the parts meet every other constraint
  in this list. Otherwise keep it: 1000 is a target for small reviews,
  not a cap, and never a reason to refuse a task.
- **Ordered by dependency.** Subtask N depends only on subtasks with lower
  numbers. The order is the implementation order.
- **Verifiable alone.** When no command can verify two consecutive subtasks
  separately, merge them.
- **Behavior-free subtasks** (refactor, scaffolding, migration,
  configuration): allow one only when a later subtask needs it, with a
  verification command too.
- **Tests ship with the change they verify.** Write no subtask of only
  tests, only documentation, or only "integration" or "wiring".
- **Incomplete behavior stays hidden.** When a subtask would expose behavior
  that later subtasks complete, give it a guard that follows the project's
  convention. Remove the guard in the subtask that completes the behavior.
  Without a guard convention, ask about the guard in Step 3.
- **Coverage.** Map every success criterion of the task to at least one
  subtask. Make the union of the subtasks' Changes sections equal the task's
  Approach section, nothing more.

Then fill the task's Subtasks section and confirm that the task's
Verification section proves the whole task after the last subtask.

### Step 5: Write

Read `references/task-template.md` now and fill every section for the task
and for each subtask, in the scratch directory. Writing rules:
- Write decisions as facts:
  `Retries use exponential backoff from 500 ms, at most 5 attempts.`, never
  `We decided that...` or `Retries should probably...`.
- **The task contains everything.** Place every fact, requirement, and
  success criterion of the original task in the matching section. Add what
  research and the interview settled, and the ordered subtask list.
- **Each subtask is self-contained.** An agent given only that subtask and
  the repository can implement it. Restate the decisions and facts it needs.
  Never write `see task`, `as above`, or `same as subtask 2`.
- Use the paths and symbols verified in Step 2. Mark new files `(new)`.
- In *Changes*, name the functions to add or change, their inputs and
  outputs, and the behavior on error. Include code only when its exact shape
  is a decision: a schema, an interface, a CLI flag, an endpoint signature.
  Never implementation code.
- Write acceptance criteria that are binary: someone else can answer yes or
  no.
- In a subtask's *Verification*, write exactly one command, or one numbered
  manual sequence when no command can prove it.
- Add no section beyond the template: no Risks, Considerations,
  Alternatives, Future work, Nice to have, or Notes. Add no estimate,
  priority, or timeline unless the user asks for them.
- Make every line serve the original task or an *Out of scope* entry. Write
  no remark or question from the conversation on another topic, and no
  mention of another task to create.
- Write at most 25 words per sentence, and only lines the implementing agent
  needs.

### Step 6: Quality check

Run every check in `references/quality-checklist.md`, grep helpers included,
over the draft. Fix every failure. When a failure needs a decision, return to
Step 3 for that decision, then run the checks again.

### Step 7: Approval

Show the complete breakdown in chat: the task, then every subtask. Name
each subtask above the 1000-line target of Step 4 with the constraint that
every split of it breaks. Ask whether the user approves it as written or
wants a change. Apply each change, run Step 6 again, and ask again until
the user approves.

### Step 8: Save

Choose the destination by the source:
- *tracker*: the tracker, into the same item.
- *file*: files, into the same task folder.
- *text*: files, in a new task folder, when no tracker is connected or the
  user asked for files at any point. Otherwise the tracker, at the
  destination of Step 3. Never ask which.

**To the tracker:**
1. Source *tracker*: replace the item's body with the approved task and keep
   its title unless a decision changed it. Source *text*: create a new item
   with the approved title and body.
2. When replacing subtasks, delete the existing children, or close them when
   the tracker cannot delete.
3. Create one child item per subtask, in order, so that later children can
   link to earlier siblings by their created identifiers. Use the subtask
   title as the title and the approved subtask as the body. Put the task's
   item link on the `Task` line and sibling links on the `Depends on` line.
   Link each child to the task's item with the tracker's relation. Without a
   parent-child relation, put child links in the task's body and the task's
   link in each child body.
4. Update the task's Subtasks section with the child links.

**To files**, by the numbering rule below:
1. Task folder, `<tasks-dir>/###-<task-slug>/`: for source *file*, the
   existing task folder. For source *text*, a new task folder with the next
   free number, with `<tasks-dir>` from Step 2c.
2. Task: write the approved task to `task.md` in the task folder. For source
   *file*, overwrite the previous task file.
3. Subtasks: write one subtask file per subtask, `###-<subtask-slug>.md` in
   the task folder, numbered `001` upward in subtask order. When replacing,
   delete the previous subtask files first. Link the `Task` line to
   `./task.md` and the `Depends on` line to the sibling files. Link the
   task's Subtasks section to each subtask file.

**Numbering rule.** `###` is a zero-padded three-digit sequence from `001`:
for a task, the next free number across every entry of `<tasks-dir>` whose
name starts with three digits. For subtasks, the next free numbers inside
the task folder. `<task-slug>` is the task title and `<subtask-slug>` the
subtask title, in kebab-case: lowercase ASCII letters and digits, every
other run of characters replaced by one hyphen, cut to 60 characters, with
no leading or trailing hyphen. The `task-create` skill shares this layout
and writes the task file.

Finish with a short recap: every item identifier and URL created or updated,
or every path written, absolute when outside the repository, and the number
of subtasks. Ask nothing else.
