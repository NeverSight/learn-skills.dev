---
name: writing-issues
description: Use when writing or refining tracker items - epics, stories, tasks, bug reports, spikes, or acceptance criteria - or when turning a discussion, review finding, or plan into tickets. Encodes the survives-without-you test, the issue-type glossary, and the story and bug skeletons. Use whenever work is written into a tracker, even from a rough verbal dump.
---

# Writing issues

**REQUIRED BACKGROUND:** the `technical-writing` skill (hard rules, truth rules, style).

## Overview

Core principle: **write issues so they survive without you.** State the outcome, include the acceptance check that decides Done, link the evidence behind every decision, and name the owner of every open part.

## When to invoke, and not

Invoke when writing or editing tracker items, filing a bug, splitting work into tickets, or writing acceptance criteria. Do NOT invoke for weighing alternatives: when an issue needs a design argued, that is `writing-design-docs`; the issue links the design doc and never inlines it. This skill covers the writing only, not prioritization or workflow advice.

Read-first applies to the tracker: read up to two recent issues of the same type and match their conventions before filing. When the tracker holds fewer, read what exists and file anyway.

When the reporter is unavailable, file with named gaps rather than blocking. The `technical-writing` checkpoint (kind, audience, purpose, non-goals) is what you stop and ask about. Missing content details (a repro step, a log line, a prior-incident link) become explicitly owned open items inside the issue.

## The survives-without-you test

Every issue answers four questions a stranger will ask:

1. **What outcome?** The state of the world when this is done, not the steps to get there. Implementation belongs in the plan.
2. **What decides Done?** A concrete, independently testable acceptance check. "Handle errors appropriately" decides nothing; "a failed upload shows the retry banner and logs at WARN" does.
3. **What is the evidence?** Where a decision or constraint came from evidence, link the source: a repo path, a document, a URL.
4. **Who owns the open parts?** "Still needs investigation" without a name or role is a banned vague owner; name one or mark the field explicitly as unassigned.

## Issue types

One glossary per tracker, defined in one line each and used consistently:

| Type | Definition |
|---|---|
| Epic | A body of work; its description states the outcome and links the design doc |
| Story | Something with user-visible value, written from the user's seat |
| Task | Engineering work with no user-visible surface |
| Bug | A defect: current behavior contradicts intended behavior |
| Spike | A time-boxed investigation whose output is a decision, not code |

A spike's Done is the decision recorded (see `recording-decisions`), never "looked into it".

A decision followed by a body of work fits two shapes: a spike first with the epic filed after the decision, or an epic whose first acceptance item is the accepted design doc. Both are valid; pick one and say which.

## Story and task skeleton

The issue description is the spec for what and why:

```markdown
**Problem / Why:** [the observable problem, from the reader's seat, with numbers where they exist]

**Outcome:** [the state of the world when done; not the steps]

**Acceptance:**
- [ ] [independently testable check]
- [ ] [another]

**Out of scope:** [what this issue deliberately does not cover]

**Open items:** [each with a named owner or role, or an explicit "unassigned"]

**Sources:** [repo paths, documents, measurements behind the above]
```

Apply the five vagueness defects from `writing-design-docs` to the acceptance list: an acceptance check that fails "what without how" or "no verifiable output" is not testable.

Gherkin-style given/when/then is an accepted format for acceptance checks when the team uses it; the same testability bar applies either way. INVEST (independent, negotiable, valuable, estimable, small, testable) works as a sizing check for stories: a story failing "small" or "testable" splits before it is filed.

## Bug report skeleton

Symptom first: the next reader arrives searching for the error.

```markdown
**Symptom:** [verbatim error string or observable misbehavior, searchable]

**Reproduction:** [numbered steps, one action each, from a clean state]

**Expected:** [what should happen, with the source that says so, or an explicit "no written source found" rather than a fabricated reference]
**Actual:** [what happens]

**Environment:** [version, platform, config that matters]

**Open items:** [each with a named owner or role, or an explicit "unassigned"]

**Suspected cause:** [only if investigated; labeled as hypothesis, never stated as fact]
```

The title carries the symptom, not the diagnosis: "duplicate reminders at reminder time", not "race condition in scheduler", unless the cause is verified.

## Rules

- **One home.** The issue owns what and why; the plan in the repo owns how. Never maintain two live copies.
- **Ticket keys.** They live in commits and planning docs, never in code, comments, test names, or user-facing strings.
- **Trust code, not issue status.** Self-reported state goes stale fast; before building on an imported or old issue, verify against the repository (grep the symbols, check the history).
- **Append, do not rewrite.** Scope changes on an in-flight issue are dated appended notes, not silent edits. Follow-up work found after completion is a new issue, never an edit to a closed one.
- **Subtasks.** Coarse reviewable slices, not every micro-step; the micro-steps live in the plan.
- **Estimates.** Labeled as estimates, with what they depend on.
- **Closing an issue.** It records the reason, especially for won't-fix and duplicates.
