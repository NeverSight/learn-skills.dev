---
name: feature-brief-document
description: Preserve agreed feature behaviour in a Feature Brief as Shape develops enough understanding to record it.
---

# Feature Brief document

Shape owns one Feature Brief for each substantial feature. The brief records
useful behavioural understanding that survives discussion. It is working memory
while Draft and the behavioural contract for Design while Ready. Writing the
brief does not drive the discussion. Design may correct non-material wording
or links, with those changes included in Design acceptance. Material changes
return to Shape.

## Create and locate

Create a brief when Shape has enough useful behavioural understanding to
preserve. Do not create one merely because Shape has started. Require an
existing Backlog item with `Status: Ready for Shape`. If no item exists, return
the work to Direction. If its status is `Needs Direction`, return to the
unresolved question in Direction. Return any other status besides
`Ready for Shape` to Direction for review. Do not create or promote an item from
this skill. Read the Ready item, nearby briefs, and applicable main or topic
Direction, Context, PDR, and ADR material. Use the item's stable ID as the
feature ID. Store the brief at
`.workflow/features/<feature-id>/brief.md`, such as
`.workflow/features/B-0001/brief.md`. Link it from the Backlog item through
`backlog-document`.

Before creating the file, check whether a brief for the feature exists elsewhere. Do not create a duplicate or migrate it in this skill. Ask for a separate migration when an existing brief is outside the canonical location.

Use this structure as the brief gains content. A Draft can have empty or
incomplete sections. Omit optional sections when they add no value:

```markdown
# Feature title

Status: Draft
Feature ID: B-0001

## Goal

## Stories and acceptance

### S1: Short name

Story: Actor, situation, intent or action, and observable result.

Acceptance:

- Observable criterion.

## Feature-wide constraints and acceptance

## Scope

## Non-goals

## Related records

## Open questions and assumptions
```

Keep `Status: Draft` or `Status: Ready` near the title. Create a brief as Draft.
Shape changes it to Ready only after explicit user agreement and a readiness
review. If later evidence requires a material contract change, return it to
Shape. Set Draft before changing behaviour, scope, stories, or acceptance
criteria. Do not present a Draft brief as accepted behaviour.

## Content and acceptance

State the goal and intended value. Use stories and failure cases to test
behaviour in the discussion. Record stories and acceptance criteria as the user
and model agree on them. Each story identifies an actor, situation, intent or
action, and observable result. Put criteria under each story so their trace is
clear. Put criteria that span stories under a named feature-wide constraint.
Before Ready, give every story acceptance coverage. Cover relevant failure and
boundary behaviour, permissions, persistence, lifecycle, and compatibility
where observable.

State scope and non-goals. Link neighbouring features and shared Direction,
Context, PDR, or ADR material when they constrain this feature. Record unresolved
feature-behaviour questions and unverified assumptions in Draft. Keep unresolved
end-state questions in Direction and link to them instead of copying them.
Remove resolved questions and superseded wording instead of retaining a
discussion history.

Ready requires one coherent vertical slice, agreed behaviour and boundaries,
acceptance coverage, intentional scope and non-goals, and linked shared
decisions. Design must be able to proceed without making product decisions.
No open question may materially change the feature. A safely deferred
assumption must leave the feature contract clear. The user must explicitly
agree that the brief is Ready.

Do not include internal APIs, modules, schemas, classes, libraries, implementation plans, test code, copied shared rules, or speculative future behaviour.

## Size and validation

Keep a Draft only as long as its current understanding needs. The hard limit
is 1,000 words per brief. Near that limit, remove copied decisions, history,
and implementation detail. Question whether separate features are hidden in
the brief. Split unrelated behaviour and update the Backlog relationship.

Invoke `concise-prose` before writing or revising the Feature Brief. Follow its
STE100 and Vale repair loop until `prose-check` passes. Install
`workflow-document-check` alongside this skill and run it after edits. Check
status, feature identity, and links after edits. Check story coverage, criterion
trace, and unresolved material questions when reviewing readiness.
