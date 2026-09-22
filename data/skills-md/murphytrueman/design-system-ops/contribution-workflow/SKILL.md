---
name: contribution-workflow
description: "Create or document a contribution workflow for a design system — the multi-stage process for evaluating, accepting, and shepherding new contributions through to publication. Trigger when someone says: how should someone contribute, contribution process, adding a new component, contribution guidelines, what's the process for adding something, how do we handle contributions, or anything about the process of bringing new work into the design system. Do NOT trigger for converting audit findings into backlog tickets — use backlog-generator for that."
references:
  - ../../knowledge-notes/component-governance.md
  - ../../knowledge-notes/design-to-code-contract.md
---

# Contribution workflow

A skill for creating a structured contribution workflow covering the full journey from proposal to release. Output is a document teams can actually follow — not a policy statement, but a process with named stages, decision criteria, and clear ownership at each gate.

## Context

Most design systems have one of two contribution problems. Either there is no process, so contributions arrive inconsistently and the design systems team becomes a bottleneck because every request is a negotiation. Or there is a process that is so heavy it discourages contribution entirely, and teams build locally rather than bother.

The goal here is a workflow that is lightweight enough to not be a burden, structured enough to produce consistent quality, and honest enough to tell contributors what will and will not make it into the system.

The six-stage structure below reflects the full lifecycle of a contribution. Not every contribution needs all six stages at the same depth — a small enhancement to an existing component is lighter than a new foundational component. The workflow should scale accordingly, and the output should note where the path diverges by contribution type.

---

## Step 1: Understand the current state

Ask for or confirm:
- Does a contribution process already exist? If so, what is working and what is not?
- Who is responsible for design system maintenance — a dedicated team, shared responsibility, or a single person?
- What types of contributions are most common? (New components, enhancements, token changes, documentation, bug fixes)
- What is the team's capacity for reviewing and integrating contributions?

Capacity is the variable most contribution processes ignore. A six-stage review process designed for a four-person dedicated team will break immediately if there is only one part-time maintainer.

**Small-system note (fewer than 5 components):** For systems this size, the full six-stage workflow is almost certainly too heavy. Produce a lightweight three-stage workflow instead: Propose (async, one paragraph) → Build (with review from the maintainer) → Ship (documentation + release note). The community review stage and the detailed assessment stage add overhead that small teams cannot absorb. The contribution criteria should still be documented — but they can be a short checklist, not a policy document. Ask: "Is there one person maintaining this, or is it shared?" If one person, the workflow is essentially "talk to them first."

## Step 2: Write the contribution workflow

---

### Design system contribution workflow

**Version:** [version number or date]
**Owner:** [who maintains this document]
**Last reviewed:** [date]

---

#### Contribution types

Before the stages, establish the contribution types. Different types move through the process at different speeds.

**Type A: Bug fix or small enhancement**
Scope: Correcting a documented error, adding a missing state, fixing a token reference.
Path: Lightweight — skips proposal and community review, moves directly to build.

**Type B: Component enhancement**
Scope: Adding a new variant, prop, or behaviour to an existing component.
Path: Standard — proposal, design review, build, documentation, release.

**Type C: New component**
Scope: A component that does not currently exist in the system.
Path: Full — all six stages.

**Type D: System-level change**
Scope: Token architecture changes, naming convention updates, governance policy changes.
Path: Full, with extended community review. These changes have the widest blast radius.

---

#### Stage 1: Proposal

**Purpose:** Establish whether a contribution is worth building before anyone builds it.

**What the contributor submits:**
- What they want to add or change, in one sentence
- The problem it solves and for which product contexts
- Evidence of the need: two or more distinct product use cases, not just a single team's request
- Whether they are aware of anything in the current system that partially addresses this need

**Proposal template:**

```
## Contribution proposal

**What:** [One sentence — what you want to add or change]
**Why:** [The problem this solves, in business or user terms]
**Evidence:** [Two or more distinct product use cases demonstrating the need]
**Existing awareness:** [What currently exists in the system that partially addresses this? Why is it insufficient?]
**Contributor commitment:** [Are you willing to own the build phase? Y/N]
```

**What happens next:**
The design systems team reviews the proposal within [SLA — e.g. five working days]. Three outcomes are possible:
- Accepted: proceed to Stage 2
- Deferred: the need is real but the timing or scope is wrong — include a reason and a re-evaluation date
- Declined: the need is better served by a local solution or does not meet the contribution criteria — include a reason

**Deferred proposals:** Proposals marked as "deferred" are real needs with wrong timing. To prevent them from being forgotten:
- Assign a re-evaluation date (typically next quarter or next planning cycle)
- Log the proposal in the system's backlog with the original evidence
- Notify the contributor when the re-evaluation date arrives
- If the same need surfaces from a second team before the re-evaluation date, escalate to "accepted" — repeated need is strong evidence

**Contribution criteria checklist:**
A proposal meets the criteria if it satisfies all of the following:
- [ ] Addresses a problem shared by at least two distinct product teams
- [ ] Does not duplicate something already in the system or in another active proposal
- [ ] Can be implemented accessibly without significant design compromise
- [ ] The contributor is willing to own the build phase

Document why each declined proposal was declined. This creates a record that protects the team from re-litigating the same decisions and gives contributors an honest answer.

---

#### Stage 2: Design

**Purpose:** Establish the design direction and component API before any build work begins.

**What the contributor produces:**
- Design exploration covering the primary use case and at least two edge cases
- Proposed component API: props, types, defaults, and states
- Accessibility considerations: keyboard interaction, ARIA role, focus behaviour
- Token usage: which existing tokens will be used, and whether any new tokens are needed

**Review:**
Design review with the design systems team and, where possible, a representative from each product team that raised the original need. One round of structured feedback, then sign-off.

Sign-off criteria:
- Component API is stable enough to build against
- No known accessibility blockers
- Token usage is consistent with existing patterns or new tokens are justified
- Edge cases have been considered and handled, not deferred

If new tokens are needed, the token decision runs in parallel and must be resolved before Stage 3 begins.

---

#### Stage 3: Build

**Purpose:** Implement the component to the agreed spec.

**What the contributor produces:**
- Component implementation against the agreed API
- Unit tests covering all props, states, and interactive behaviour
- Accessibility tests: keyboard navigation, screen reader, colour contrast
- Storybook or equivalent — one story per documented state

**Handshake points:**
Mid-build check with the design systems team when the happy path is functional but before edge cases and tests are complete. Catch misalignments early.

Build is considered complete when:
- All agreed states are implemented and tested
- Accessibility tests pass at WCAG 2.1 AA
- Design-to-code alignment has been reviewed by the original designer

---

#### Stage 4: Documentation

**Purpose:** Make the component usable by teams who were not in the room when it was designed.

**What must be documented before release:**
- Usage guidelines: when to use, when not to use, and two to three common anti-patterns
- Props reference: every prop with type, default, and one-sentence description
- Accessibility: the specific keyboard and screen reader behaviour for this component
- Examples: at least the primary use case and one edge case

The `ai-component-description` skill should also be run at this stage to produce the Figma MCP-optimised description.

Documentation is not complete until someone who was not involved in the build can follow the guidelines to use the component correctly. Consider a brief documentation review with a designer from a consuming team.

---

#### Stage 5: Community review

**Purpose:** A final check before release, giving consuming teams visibility before the component ships.

For Type A and B contributions, this stage can be abbreviated to a release note preview.

For Type C (new components) and Type D (system-level changes): share the component and documentation with consuming teams at least [SLA — e.g. one week] before release. Invite feedback. Document any significant responses. Make the rationale for any changes or non-changes explicit.

This stage is not a veto mechanism. It is a courtesy that reduces post-release surprises and builds contributor trust.

---

#### Stage 6: Release

**Purpose:** Ship the contribution with enough communication that consuming teams know it exists and can use it.

**What ships:**
- Component in the system at its documented version
- Release notes covering what is new, any migration considerations, and links to documentation
- Announcement through the team's standard channels

Release notes for a new component should name the contributor. Contribution is a social act as much as a technical one.

After release: log the contribution in the system's change history and update the proposal record with the outcome.

---

#### What does not go into the system

As important as the stages above: be explicit about what the contribution process is not for.

The system does not accept:
- Components that solve a single team's specific problem without broader applicability
- Components that duplicate existing functionality without a clear migration path for the old version
- Components that cannot be implemented accessibly
- Work that the contributor is not willing to document

Saying no clearly is part of a healthy contribution process. A system that accepts everything eventually becomes a system no one trusts.

#### Rejection decision record

When a proposal is declined, document the decision using the `decision-record` skill. The record should include:
- The proposal that was declined
- The specific criteria it did not meet
- The alternative recommended to the contributor
- Under what conditions the decision might be revisited

Rejection records serve two purposes: they give the contributor a clear, written explanation, and they prevent the same proposal from being re-litigated without new evidence. A healthy contribution process produces rejection records as often as it produces new components.

---

#### API versioning contract (staff-level)

At the staff level, the contribution workflow must account for the component's API as a versioned contract:

**For Type B (enhancements):**
- New props and variants are additive — they must not change existing prop behaviour or defaults
- This is a minor version increment. Consuming teams should not need to change anything.
- If the enhancement requires changing an existing prop's type, default, or accepted values, it is a breaking change and must follow the Type D path

**For Type C (new components):**
- The component ships at v1.0.0 with a documented API
- All props, their types, defaults, and accepted values are part of the public contract
- Internal implementation details (helper components, internal state) are explicitly not part of the contract
- The release notes should state what is public API and what is internal

**For Type D (system-level changes):**
- Blast radius must be assessed before approval: how many components, how many consuming applications, what is the estimated migration effort?
- If the blast radius exceeds a defined threshold (e.g., affects 50%+ of components or 3+ consuming teams), the change requires a migration plan and extended timeline
- Breaking token changes should include a codemod or find-and-replace instructions

Include the versioning contract in the contribution workflow document as a section that contributors and reviewers reference at the Build and Release stages.

#### Consumer contract testing (staff-level)

For new components (Type C) and system-level changes (Type D), the workflow should include a consumer contract validation step:

- Before release, verify that consuming applications use the component's public API correctly
- For breaking changes, run the consuming applications' test suites against the new version to detect breakage
- If consuming teams have snapshot tests or visual regression tests, coordinate a pre-release validation

This step sits between Stage 5 (Community review) and Stage 6 (Release). It converts "we told them about the change" into "we verified the change works for them."

## Step 3: Calibrate for team capacity

After writing the workflow, add a note on how to calibrate the SLAs and review stages for the team's actual capacity. A part-time maintainer cannot run the same process as a four-person dedicated team. Name where the process can be compressed without compromising quality, and where it cannot.

## Quality checks

- Contribution types are defined before the stages — different types have different paths
- Every stage has a clear output and a clear sign-off condition
- SLA placeholders are flagged and must be filled in before the document is used
- Decline criteria exist and are documented — the process can say no
- Capacity note is included
- The document is written for contributors, not for the design systems team to hide behind
