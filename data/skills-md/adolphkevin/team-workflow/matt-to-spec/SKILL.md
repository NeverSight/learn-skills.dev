---
name: matt-to-spec
description: "Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you've already discussed."
disable-model-invocation: true
---

Before using this method, read the [knowledge and team rules](../team-workflow/references/matt-integration.md): project knowledge comes from team-knowledge (`tw brief`).


This skill takes the current conversation context and codebase understanding and produces a spec. Do NOT interview the user; just synthesize what you already know.

Use the project tracker and labels already configured. If absent, retain a local task draft.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

2. Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better - the ideal number is one.

Use already agreed interfaces and acceptance criteria. Ask only about a material unresolved testing choice.

3. Write the spec using the template below, sized to the actual task. Publish it and apply project labels only when that external action is authorized; otherwise retain a reviewable local draft.

For a team task, use the [versioned section format](../team-workflow/references/designs.md) as the shared plan: define the real starting state, actor, business steps, observable outcome, negative cases and acceptance owner before splitting work; investigate affected operations and cross-service data producers/consumers. Then assess complexity and risk separately, give acceptance and tasks stable IDs, and declare their actual dependencies. Record unresolved business choices with their affected sections. Parent and child assessments are separate; simple tasks need a short plan before implementation and may use combined plan/code review. Record each unresolved question with a stable ID, affected sections and a responsible person; scope changes and constraints remain pending until actually resolved. Carry forward existing approval and publish only within authorization. Standalone use keeps the prose template below. Name the entry-level API, RPC or UI seam the acceptance tests will drive.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A numbered list of the user stories needed to explain this change. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

Cover the requested behavior and material risks; avoid inventing unrelated scope.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
