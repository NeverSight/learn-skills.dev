---
name: create-design-discussion
description: Create or update a design discussion artifact from completed research and explicit user decisions.
disable-model-invocation: true
---

# Create a design discussion

Use this skill only when the user invokes it by name. Turn the request, task
artifacts, and repository evidence into a decision workshop: a reviewable design
whose unresolved choices remain open and whose resolved choices form a durable
decision ledger.

## 1. Load the task record

Resolve the task directory from the system context or the path named by the
user. Enumerate that exact directory with `ls -La`; `.agent-work/tasks` may be a
symlink, so work from explicit paths rather than recursive search. If the task
directory is still unknown, enumerate `.agent-work/tasks` and match the ticket
or task name case-insensitively. Create a task directory only in step 4.

In the main context, read every relevant file completely before delegating:

- the ticket (`ticket.md`, `task.md`, or equivalent);
- every completed research document;
- every existing design discussion;
- every file explicitly mentioned by the user or those artifacts.

Classify research-question documents as research-phase inputs and leave them
unloaded. Record conflicts using this precedence: latest design discussion,
then research, then ticket.

This step is complete when every file in the exact task directory is classified
as read or excluded, every mentioned file is read in full, and every conflicting
claim has a winning source.

## 2. Close evidence gaps

Continue directly when the loaded evidence supports the current state,
architecture, decisions, patterns, and test approach.

When the user asks how existing behavior works or requests implementation
detail, investigate before proposing an answer. Prefer the host's available
read-only agent or subagent mechanism for independent parallel work, assigning
these responsibilities when those roles exist:

- a **locator** finds relevant files and integration points;
- a **behavior analyzer** traces implementation behavior and dependencies;
- a **pattern finder** finds analogous implementations, tests, and conventions.

Ask each investigator for concrete file-and-line evidence. Straightforward user
feedback that only records a decision needs no new investigation.

If specialist agents are unavailable, perform the same bounded locator,
behavior, and pattern passes directly with repository search and file reading;
do not block the skill or weaken the evidence standard.

This step is complete when every assertion needed by the design is supported by
a loaded artifact, repository evidence, or an explicitly open design question,
and every investigation result used in the design has a concrete source.

## 3. Load the document contract

Before drafting or editing, read
[`references/design_discussion_template.md`](references/design_discussion_template.md)
in full. It is the single source of truth for metadata, sections, decision-state
transitions, diagrams, patterns, testing guidance, and Markdown fencing.

This step is complete when every applicable requirement in the template has a
planned location in the document and the initial-draft or feedback-update branch
has been selected.

## 4. Write the design discussion

For an existing discussion, edit that artifact in place. For a new discussion:

1. Use the resolved task directory, or create
   `.agent-work/tasks/TASK-SLUG/` when none exists.
2. Inspect the direct children of that directory and choose one greater than the
   highest two-digit document prefix; begin at `01` when no prefix exists.
3. Write `NN-design-discussion-DESCRIPTION.md`, where `DESCRIPTION` is a concise
   two-to-four-word kebab-case slug.

Examples:

- `.agent-work/tasks/ENG-1478-parent-child-tracking/03-design-discussion-parent-child-tracking.md`
- `.agent-work/tasks/improve-error-handling/03-design-discussion-error-handling.md`

Apply the loaded template exhaustively. On an initial draft, keep every design
question open even when one option is strongly recommended. On a feedback
update, treat any clear user choice as a decision: move that question to
Resolved Design Questions and preserve the selected rationale, rejected
options, and relevant implementation pattern. User decisions supersede earlier
artifacts.

This step is complete when the artifact exists at the correct path, every
template section is present, every claim or pattern that needs evidence has a
source, every question appears in exactly one state, and every explicit user
decision is recorded without closing any undecided question.

## 5. Determine the final state

Re-read the written artifact and account for every design question. If any
question remains under Design Questions, select the open-questions response. If
all questions are under Resolved Design Questions, select the resolved response.
If the host returns a permalink for the written artifact, use it; otherwise use
the local artifact path.

This step is complete when the number of open plus resolved questions equals the
total number of questions in the artifact, the selected response matches that
state, and a valid navigation target is available.

## 6. Return the exact next step

For an open design, read and render
[`references/design_discussion_final_answer.md`](references/design_discussion_final_answer.md).
For a fully resolved design, read and render
[`references/design_discussion_final_answer_resolved.md`](references/design_discussion_final_answer_resolved.md).
The rendered template is the entire final response.

This step is complete when exactly one response template has been rendered, all
placeholders and conditional lines have been resolved, and no text appears
outside that template.
