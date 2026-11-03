---
name: system-design
description: Writes a system design with requirements, interfaces, data model, and explicit tradeoffs. Use when the user asks for a system design, architecture proposal, design doc, technical design, or to compare approaches before implementation.
---

# System Design

Produce a design the team can implement or reject. Stay at the depth of the question: a single service change does not need a full platform essay.

## Before writing

Collect only what changes the design:

- Users and the job to be done
- Hard constraints (latency, consistency, compliance, existing systems, deadline)
- Scale that is real today, and the next order of magnitude that must still work
- What is explicitly out of scope
- Use SOLID principale, DRY, KISS etc

If a missing fact would change the architecture, ask one question and stop. Otherwise state the assumption and continue.

## Document

```markdown
# [Design title]

## Problem
One paragraph. Who is blocked, and what “done” means.

## Requirements
- Functional: observable behaviors
- Non-functional: latency, availability, consistency, security, scale
- Out of scope

## Proposed design
The chosen approach in a few paragraphs. Name the components and how a request or job moves through them.

## Interfaces
- APIs or events, with the important request and response fields
- Failure behavior callers can rely on

## Data
- Entities and ownership (who writes the source of truth)
- Retention, migration, and backfill if existing data changes

## Tradeoffs
| Option | Why it was not chosen |
| --- | --- |
| [Rejected option] | [Concrete cost] |

## Risks
- Risk, how we would notice it, and the mitigation

## Rollout
- First slice that proves the design
- What is deferred
- How to roll back
```

## Rules

1. Recommend one option. List alternatives only in the tradeoff table, each with the reason it lost.
2. Tie every component to a requirement. Drop components that do not serve one.
3. Prefer extending an existing service, table, or queue in the repo over introducing a new one.
4. Call out consistency boundaries: what can be stale, and for how long.
5. Security and tenancy are requirements when the system handles user data or more than one tenant.
6. The rollout slice must be shippable on its own. Do not hide the first milestone inside a full rewrite.
7. Do not invent traffic numbers, SLAs, or vendor limits. Mark unknown numbers as assumptions.
