---
name: planning-blueprinting
description: In-repo planning and specification system for software projects. Use when asked to "create a plan", "write a spec", "document a proposal", "blueprint a feature", or when doing architectural planning work.
compatibility: any project, markdown
metadata:
  author: constructive-io
  version: "1.0.0"
---

# Planning and Blueprinting System

A minimal, enforceable system for doing planning, blueprinting, and specification inside a codebase using two core concepts: **plans** (proposals) and **specs** (contracts).

## When to Apply

Use this skill when:
- Creating a proposal or blueprint for new work
- Documenting accepted specifications
- Doing architectural planning
- Tracking decision and implementation status
- Promoting a plan to a formal specification

## Core Concepts

**Plan** — A proposal, blueprint, or work-in-progress design. Plans are iterative, may contain open questions, and are not authoritative contracts.

**Spec** — An accepted contract and source of truth. Specs define reference behavior that reviewers and tests enforce. They must remain accurate over time.

## Folder Structure

Create this structure in the repository when needed:

```
docs/
├── README.md              # Overview and rules
├── plan/
│   ├── README.md          # Plan guidelines
│   └── template.plan.md   # Plan template
└── spec/
    ├── README.md          # Spec guidelines
    └── template.spec.md   # Spec template
```

## Promotion Flow

```
plan (Draft) → plan (In Review) → plan (Accepted) → spec
```

When a plan reaches **Accepted** status, promote it into `docs/spec/` as a formal specification.

## Two-Axis Status Tracking for Specs

Specs must track two independent dimensions:

### Decision Status (contract lifecycle)

| Status | Meaning |
|--------|---------|
| Draft | Under development, not yet accepted |
| Accepted | Approved as the authoritative contract |
| Deprecated | No longer recommended, superseded or obsolete |
| Superseded | Replaced by a newer spec |

### Implementation Status (delivery lifecycle)

| Status | Meaning |
|--------|---------|
| Not Implemented | Work has not started |
| In Progress | Active development |
| Partial | Some parts implemented |
| Implemented | Fully complete |
| Blocked | Cannot proceed due to dependencies |

## Rules

1. **Plans are not contracts.** They may be messy, incomplete, or exploratory.

2. **Specs are contracts.** They must remain accurate and are the authoritative reference for implementation and testing.

3. **Specs may describe future behavior** only when Decision Status = Accepted. This allows specs to document planned work before implementation begins.

4. **Status fields are authoritative.** Update them as work progresses.

5. **Architecture uses Constructive tooling.** Designs should leverage constructive-skills and interoperable Constructive patterns where applicable.

## Plan Template

```markdown
# [Plan Title]

| Field | Value |
|-------|-------|
| Status | Draft / In Review / Accepted / Rejected |
| Owner | @username |
| Created | YYYY-MM-DD |
| Related | #issue, #pr |

## Problem Statement

What problem does this solve? Why does it matter?

## Goals

What this plan aims to achieve.

## Non-Goals

What is explicitly out of scope.

## Proposal

High-level approach to solving the problem.

## Detailed Design

Technical blueprint: architecture, data flow, component interactions.

## Milestones

| Milestone | Description | Target |
|-----------|-------------|--------|
| M1 | ... | ... |

## Rollout Plan

How this will be deployed/released. Phasing, feature flags, migration steps.

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| ... | ... | ... | ... |

## Alternatives Considered

Other approaches evaluated and why they were not chosen.

## Open Questions

- [ ] Question 1
- [ ] Question 2
```

## Spec Template

```markdown
# [Spec Title]

| Field | Value |
|-------|-------|
| Decision Status | Draft / Accepted / Deprecated / Superseded |
| Implementation Status | Not Implemented / In Progress / Partial / Implemented / Blocked |
| Last Updated | YYYY-MM-DD |
| Plan | [link to plan] |
| Issues | #issue |
| PRs | #pr |

## Summary

Brief description of what this spec defines.

## Definitions

Key terms and their meanings within this spec.

## Requirements

### Functional

What the system must do.

### Non-Functional

Performance, security, reliability, and other quality attributes.

## Behavior

Expected system behavior under normal and edge conditions.

## Interfaces

### API

Endpoints, methods, request/response formats.

### Data Model

Schemas, entities, relationships.

## Edge Cases

How the system handles boundary conditions and error states.

## Observability

Logging, metrics, alerts, and debugging support.

## Test Plan

How compliance with this spec is verified.

## Implementation Notes

Links to PRs, technical decisions made during implementation.

## Changelog

| Date | Change | Author |
|------|--------|--------|
| YYYY-MM-DD | Initial spec | @username |
```

## docs/README.md Template

```markdown
# Documentation System

This directory contains the in-repo planning and specification system.

## Concepts

**Plan** — A proposal, blueprint, or work-in-progress design. Plans live in `docs/plan/`.

**Spec** — An accepted contract and source of truth. Specs live in `docs/spec/`.

## Promotion Flow

plan (Draft) → plan (In Review) → plan (Accepted) → spec

## Rules

1. Plans are not contracts. They may be messy or exploratory.
2. Specs are contracts. They must remain accurate.
3. Specs may describe future behavior only when Decision Status = Accepted.
4. Status fields are authoritative. Update them as work progresses.
```

## docs/plan/README.md Template

```markdown
# Plans

Plans are blueprints and proposals. They are allowed to be messy and iterative, may contain open questions, and are not authoritative contracts.

When a plan is accepted, it is promoted into `docs/spec/`.

## Creating a Plan

1. Copy `template.plan.md` to a new file
2. Fill in the sections
3. Set Status to Draft
4. Submit for review when ready
```

## docs/spec/README.md Template

```markdown
# Specifications

Specs are accepted contracts and reference behavior. They are the source of truth for implementation and tests. Specs must remain accurate over time.

Specs may describe not-yet-implemented behavior only when explicitly marked with Decision Status = Accepted.

## Status Tracking

Specs track two independent dimensions:

**Decision Status**: Draft, Accepted, Deprecated, Superseded

**Implementation Status**: Not Implemented, In Progress, Partial, Implemented, Blocked
```

## Best Practices

1. **Keep plans focused**: One plan per feature or change
2. **Update status promptly**: Status fields should reflect current reality
3. **Link related artifacts**: Connect plans to issues, PRs, and specs
4. **Prune deprecated specs**: Mark old specs as Deprecated or Superseded
5. **Dense content**: Be succinct yet descriptive, avoid verbose cruft
