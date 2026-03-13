---
name: user-story-writing
description: "User story authoring workflow for turning prioritized requirements into implementable, testable delivery slices. Use when approved requirement work must be decomposed for sprint execution; do not use for initial requirement discovery or release-level prioritization."
---

# User Story Writing

## Overview
Use this skill to convert prioritized requirements into stories that are small, value-oriented, and verifiable.

## Scope Boundaries
- Requirements are approved and ranked, but execution slices are not defined.
- Teams need sprint-ready stories with explicit acceptance boundaries.
- Scope must be split to reduce risk and improve delivery predictability.

## Templates And Assets
- User story template:
  - `assets/user-story-template.md`
- Story slicing checklist:
  - `assets/story-splitting-checklist.md`

## Inputs To Gather
- Prioritized requirement items and acceptance context.
- Technical dependencies, compliance constraints, and non-functional expectations.
- Team delivery cadence and capacity boundaries.

## Deliverables
- Story set with actor/need/value statements and scope boundaries.
- Story-level acceptance mapping and explicit out-of-scope notes.
- Dependency and assumption log for planning and risk tracking.

## Workflow
1. Select the next highest-priority requirement and identify user-visible value.
2. Slice work vertically so each story produces testable user or operator value.
3. Write story statements and add concrete acceptance evidence expectations.
4. Mark non-functional, compliance, and operational constraints explicitly.
5. Split oversized stories until each can finish in one planning cycle.
6. Validate dependencies and sequencing assumptions with responsible owners.

## Quality Standard
- Each story has clear value, scope boundary, and acceptance evidence.
- Stories avoid hidden technical coupling that blocks independent completion.
- Compliance or safety work is represented as first-class deliverables.
- Assumptions and risks are visible before sprint commitment.

## Failure Conditions
- Stop when stories cannot be traced to approved requirements.
- Stop when acceptance evidence is undefined or non-testable.
- Escalate when critical dependencies make sprint sizing unreliable.
