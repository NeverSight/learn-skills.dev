---
name: ticket-triage
description: >
  Evaluate whether a development ticket (user story, feature request, bug report, etc.)
  is ready for development, and provide specific, actionable feedback if it is not.
  Use this skill whenever the user asks to triage, evaluate, assess, review, or check
  the readiness of a ticket, story, issue, or work item. The ticket can come from
  anywhere: pasted inline, read from a file, fetched from Jira or another tracker via
  MCP, or any other source. Also use this when a user asks "is this ticket ready?" or
  "what's wrong with this ticket?" or wants to improve a ticket's specification.
license: CC0-1.0
compatibility: Designed for any coding agent (Claude Code, Codex, Cursor, OpenCode, etc.)
metadata:
  author: jwilger
  version: "1.0"
  requires: []
  context: []
  phase: plan
  standalone: true
---

# Ticket Triage

Evaluate a single ticket against six readiness criteria and produce a clear verdict with actionable remediation guidance.

## How to Get the Ticket

The user might provide the ticket in several ways. Adapt accordingly:

- **Pasted in the prompt**: The ticket text is right there. Use it directly.
- **File path**: Read the file.
- **Jira / Linear / GitHub Issue / other tracker**: If MCP tools are available for the tracker, use them to fetch the ticket. If not, ask the user to paste the content.
- **Multiple tickets**: If given multiple tickets, evaluate each one separately and produce a per-ticket assessment. Do not batch them into a single verdict.

If the ticket content is ambiguous or incomplete (e.g., just a title with no description), note that in your assessment but still evaluate what's there.

## Evaluation Posture

Before diving into the criteria, understand the right mindset for this evaluation. The question you are answering is: **"Could a developer pick up this ticket and build the right thing without needing to ask clarifying questions?"**

You are not looking for perfection. You are looking for sufficiency. A ticket with slightly informal language that nonetheless communicates the expected behavior clearly is FINE. Only fail a criterion when the gap would genuinely cause a developer to build the wrong thing, miss an important behavior, or be unable to verify their work.

When in doubt, pass the criterion and note an optional improvement. Reserve failures for genuine problems that would block development or lead to incorrect implementations.

## The Six Readiness Criteria

A ticket is **Ready for Development** only if it passes ALL six criteria. Failing even one makes it not ready.

### 1. Specific Acceptance Criteria

The ACs must communicate what the feature does concretely enough that a developer knows what to build. They should describe behaviors, not just restate the feature name.

**Passes**: "Dragging changes order in the UI" -- a developer knows what to implement: drag interaction that visually reorders items

**Passes**: "When a user submits a task with a title shorter than 3 characters, a validation error appears below the title field" -- very precise and detailed

**Fails**: "User can create a task" -- this is a feature summary, not an AC. It says nothing about what creating a task involves, what fields are shown, or what happens after creation

**Fails**: "Validation errors are displayed on the form" -- which errors? for which fields? where on the form?

The bar is "would a developer know what to build?" not "is every edge case documented?" ACs that clearly communicate the expected behavior pass even if they could be more detailed.

### 2. Appropriately Sliced

The ticket is a single, deliverable unit of work. Not an epic disguised as a story, nor an artificial slice that separates tightly coupled concerns (like creating a model in one ticket and adding its validations in another).

**Passes**: "Add drag-and-drop reordering to the task list" -- single feature, clear scope

**Fails**: "Build import and export functionality" -- two distinct features with different complexity

Red flags: 3+ distinct capabilities listed, "and" in the title joining unrelated concerns, question marks in the description suggesting the scope isn't decided.

### 3. Verifiable and Specific ACs

Each AC must be testable -- a QA engineer could determine pass or fail from the AC text. The key question is whether the AC contains subjective language that makes the pass/fail determination a matter of opinion.

**Passes**: "Order persists after page refresh" -- clear test: reorder, refresh, check

**Passes**: "A user only sees their own tasks" -- clear test: log in as user A, verify user B's tasks are not visible

**Fails**: "Query is reasonably performant with large data sets" -- "reasonably" is subjective, "large" is undefined

**Fails**: "Users perceive the app as more powerful" -- entirely subjective, no way to test

Subjective red-flag words that typically cause failures: "appropriately", "reasonably", "correctly", "clearly", "feels", "perceived", "intuitive", "meaningful". However, context matters -- "User can toggle theme" is fine even though "toggle" is slightly informal, because the behavior is obvious.

### 4. User-Verifiable Through the UI

The ticket as a whole must be verifiable by a user interacting with the application. Evaluate this at the **ticket level**, not per-AC.

**Passes**: A ticket where the core behavior is user-facing, even if one AC mentions an implementation detail. For example, if a ticket has 3 ACs and two describe UI behavior while one says "foreign key relationship exists", the ticket passes -- it IS user-verifiable. The implementation AC is a style issue to note as an optional improvement, not a criterion failure. If even ONE AC describes a user-observable behavior, the ticket passes this criterion.

**Fails**: A ticket where ALL ACs describe implementation details ("foreign key exists", "data is stored in the database", "migrations run successfully") with no user-observable behavior at all.

The question is: "Can a user verify this ticket is done by using the app?" If yes, it passes. Period.

### 5. Not Infrastructure-Only

The ticket delivers value that a user of the application can experience. Pure infrastructure, tooling, or devops tickets should be typed as "Chores" or "Tasks", not "Stories."

**Passes**: "User can see a task list page after the app starts" -- infrastructure + user value combined

**Fails**: "Docker Compose starts the app and database is reachable from Rails" -- developer/infra value only

Infrastructure work is necessary and valid. The criterion is about typing and framing, not dismissing the work. If a ticket is purely infrastructure, recommend reclassifying it as a Chore or merging it with a user-facing ticket so they ship together.

### 6. Validation Criteria for Data Models

This criterion applies when a ticket **introduces a new data model** (a new database table / entity) or **adds user-facing fields** to an existing model. When it applies, every user-facing field must have explicit validation rules: type, required/optional, min/max length or value, format, allowed values, default value.

**Passes**: A ticket that includes something like:

| Field | Type | Required | Constraints | Default |
|-------|------|----------|-------------|---------|
| title | string | Yes | Min 3 chars, max 255 chars | -- |
| status | enum | Yes | pending, in_progress, completed, archived | pending |

**Fails**: "Each task has: Title (string), Description (text), Status, Due date" -- field names and rough types but no validation rules

**N/A -- mark as Pass**: When the ticket does NOT introduce a new data model. Specifically:
- Adding a foreign key for a relationship (e.g., adding `user_id` to tasks) is a relationship change, not a new data model. Pass.
- Using fields that already exist on an established model (e.g., reordering tasks using a `position` field introduced in an earlier ticket) is not introducing new fields. Pass.
- Pure UI changes, behavioral changes, or features that don't touch data models. Pass.

The criterion only triggers when the ticket says something like "create a Comment model" or "each task should have: [list of new fields]" -- i.e., the ticket is defining what data gets stored and the developer needs to know the validation rules to build the forms and model correctly.

Watch for: tickets that mention data fields in the description but have no validation section, enum fields that list values without specifying the default, and fields whose validation rules are defined in a different ticket (this means the ticket isn't self-contained).

## Evaluation Process

For each ticket:

1. **Identify the ticket metadata**: title, type, priority (if available)
2. **Evaluate each criterion**: Determine pass/fail with specific reasoning that references the actual ticket text
3. **Determine the overall verdict**: Ready, Nearly Ready (fails exactly 1 minor criterion with a < 30 min fix), or Not Ready
4. **Identify specific gaps**: What exactly is missing or vague, with direct quotes from the ticket
5. **Provide remediation guidance**: Concrete steps the team needs to take, not generic advice

## Output Format

Present the assessment in a clear, scannable format:

```
## Ticket Triage: [Ticket Title]

**Verdict: [READY FOR DEVELOPMENT / NEARLY READY / NOT READY]**

### Criteria Assessment

| # | Criterion | Result | Notes |
|---|-----------|--------|-------|
| 1 | Specific Acceptance Criteria | Pass/Fail | [brief reason] |
| 2 | Appropriately Sliced | Pass/Fail | [brief reason] |
| 3 | Verifiable and Specific ACs | Pass/Fail | [brief reason] |
| 4 | User-Verifiable Through UI | Pass/Fail | [brief reason] |
| 5 | Not Infrastructure-Only | Pass/Fail | [brief reason] |
| 6 | Validation Criteria for Data Models | Pass/Fail/N/A | [brief reason] |
```

Then, based on the verdict:

**If READY**: Brief confirmation of why the ticket is good to go. Note any optional improvements (clearly marked as non-blocking).

**If NEARLY READY**: List the 1-2 specific, small changes needed. Provide the exact rewritten AC or addition so the team can copy-paste it.

**If NOT READY**: Include all three of these sections:

**Gaps** -- Bulleted list of every specific gap, grouped by failing criterion. Quote the problematic text from the ticket directly.

**Remediation Steps** -- Numbered checklist of what the team needs to do, in priority order. Be specific: don't say "add validation rules" -- say which fields need which rules. For example:

- Add validation for `title`: required, string, min 3 chars, max 255 chars
- Replace AC "Status is stored in the database" with: "When a user changes a task's status, the new status badge is visible immediately and persists after page refresh"
- Split this ticket into: (1) Status filtering, (2) Due date filtering, (3) Keyword search

**Remediated Example** -- Show a before/after for the most impactful section of the ticket. This teaches the team the pattern so they can apply it to other tickets. Format:

> **Before:**
> - User can create a task
> - Tasks persist in the database
>
> **After:**
> - When a user fills in the task title and clicks "Create", they are redirected to the task list and the new task appears at the top
> - When a user creates a task without a title, a validation error "Title is required" appears below the title field
> - When a user refreshes the task list page, all previously created tasks are still visible

## Judgment Calls

**Default to passing.** Your starting assumption should be that a criterion passes. Only fail it when you can point to a specific, concrete problem that would cause a developer to build the wrong thing or be unable to verify their work. "This could be more detailed" is an optional improvement, not a failure.

**Redundant implementation ACs**: If a ticket has a mix of user-facing ACs and one implementation-detail AC (like "saved to the database"), the ticket still passes criteria 4 (user-verifiable). Note the redundant AC as an optional cleanup in your assessment, but do not fail the criterion. Only fail criterion 4 when the ticket has NO user-verifiable ACs.

**Borderline ACs**: If an AC communicates the expected behavior clearly enough that a developer would know what to build, it passes criteria 1 and 3 -- even if the wording is informal or could be more precise. "Dragging changes order in the UI" is clear. "Results update correctly" is not (what does "correctly" mean?).

**Infrastructure + user value**: If a ticket combines infrastructure work with a user-facing deliverable, it passes criterion 5.

**Implied data models**: If the ticket doesn't explicitly say "create a new model" but the feature clearly requires one (e.g., "users can leave comments on tasks" implies a Comment model), flag the missing data model definition under criterion 6.

**Relationships vs. new models**: Adding a foreign key to establish a relationship between existing models (e.g., `user_id` on tasks) does NOT trigger criterion 6. The criterion is about new entities with user-facing fields that need form validation, not about database-level relationship plumbing.

**Artificial splits**: If a ticket references another ticket for essential details (e.g., "Status values are defined in TICKET-4"), flag this under criterion 2. The ticket should be self-contained or explicitly declare the dependency.

**Nearly Ready threshold**: Use this when the ticket fails exactly 1 criterion and the fix is small (< 30 minutes of refinement). Two or more failing criteria means Not Ready, even if each fix is individually small.

## Tone

Be direct and constructive. The goal is to help the team ship better tickets, not to gatekeep. Frame remediation as "here's what would make this ready" rather than "here's what's wrong." When a ticket is well-written, say so -- recognizing good practices helps establish patterns across the team.
