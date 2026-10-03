---
name: to-spec
description: Create and publish an implementation-ready spec from the current conversation. Use when a discussed feature or change is settled enough to write up and publish to the issue tracker.
license: MIT
disable-model-invocation: true
metadata:
  author: "Sascha Grau"
  version: "1.0.0"
  category: "engineering"
---

# To spec

Turn the established conversation and repository evidence into a publishable spec. Synthesize; do not conduct a feature interview. State gaps that block implementation as open questions in the spec.

Before publishing, read `docs/agents/issue-tracker.md`. When `docs/agents/triage-labels.md` exists, read it before assigning its mapped roles. If the tracker contract is absent or does not describe publication, report that repository setup blocks publication and direct the user to the `setup-software-engineering-skills` skill.

## Process

### 1. Ground the spec

Read the established conversation, every user-provided source, and the repository-specific domain-documentation contract. Use its selected glossary and applicable ADRs while exploring the relevant code only as far as needed to establish current behavior, conventions, and comparable tests.

**Complete when:** the spec's terminology, affected behavior, prior architectural decisions, and relevant test prior art are evidenced or explicitly absent.

### 2. Choose the test seams

For every intended externally observable behavior, select the highest existing test seam that can prove it. Prefer one seam; when no existing seam is sufficient, propose the minimal new seam at the highest viable boundary. Record the proposed seams and the behavior each proves in the spec's testing decisions.

**Complete when:** every intended behavior has a testable seam, each proposed new seam is justified, and no lower-level seam is included without a distinct behavior it alone proves.

### 3. Write and publish

Write the spec using the template below. Distinguish decisions established by the conversation from repository-aligned proposals. Classify the issue as `enhancement` unless the conversation establishes a defect. Apply the configured category role: use `docs/agents/triage-labels.md` when it exists, otherwise use the tracker contract's native category field when it defines one.

When **Open questions** has no implementation blocker, apply the configured ready-for-agent state: use its mapped role when the mapping exists, otherwise the tracker contract's native ready state when it defines one. When a blocker remains, publish the spec with the tracker contract's unresolved state, or without readiness metadata when the contract has no state model; state the promotion condition in the returned result.

**Complete when:** the tracker confirms the issue exists; its configured category and readiness or unresolved state accurately reflect whether implementation is blocked; and its stable locator (identifier, URL, or configured local spec path) is returned to the user.

<spec-template>

## Problem Statement

The problem the user faces, from the user's perspective.

## Solution

The intended outcome, from the user's perspective.

## User Stories

A numbered list of distinct user stories covering every established actor, lifecycle state, permission boundary, failure or recovery path, and externally observable outcome. Omit duplicate restatements.

1. As an <actor>, I want a <feature>, so that <benefit>.

## Acceptance Criteria

A checkable list of observable outcomes that prove the solution works, including relevant negative cases and boundary conditions.

- [ ] Criterion 1
- [ ] Criterion 2

## Implementation Decisions

### Confirmed decisions

Decisions established by the conversation, including affected modules, interfaces, architectural choices, schema changes, API contracts, and specific interactions.

### Repository-aligned proposals

Necessary implementation details inferred from established repository conventions or code evidence. State the evidence for each proposal.

### Open questions

Only decisions whose absence blocks implementation. State the decision needed and its impact.

Avoid file paths and ordinary code snippets. When a prototype produced a decision-rich artifact, include the decision-rich excerpt marked as prototype-derived and link the executable prototype as its primary source.

## Testing Decisions

For each acceptance criterion, state the externally observable behavior, the selected test seam, and comparable test prior art. A good test proves behavior rather than implementation detail.

## Out of Scope

Things the spec intentionally excludes.

## Further Notes

Relevant context that does not alter the implementation contract.

</spec-template>
