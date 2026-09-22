---
name: decision-record
description: "Create a structured narrative record documenting why a design system decision was made — the context, options considered, trade-offs, and rationale. This produces a human-readable decision document, NOT machine-executable rules or constraint files. Trigger when someone says: document this decision, record why we chose, ADR, architecture decision record, capture this decision, why did we pick, what was the reasoning, or anything about preserving the narrative behind a specific design system choice. Do NOT trigger for encoding governance policies as machine-checkable rules — use governance-encoder for that."
references:
  - ../../knowledge-notes/component-governance.md
---

# Decision record

A skill for creating structured decision records for design system choices. Covers component decisions, token architecture choices, tooling selections, governance policies, and any other decision worth recording so future contributors do not have to reverse-engineer the reasoning.

## Context

Design systems accumulate decisions faster than they accumulate documentation. The result is a system where the current state is known but the reasoning is not — which means the same debates recur, constraints get ignored because their origin is forgotten, and new team members spend weeks learning by collision what a thirty-minute conversation would have covered.

A decision record does not need to be formal. It needs to be findable and honest. The format below is lightweight enough to write in under twenty minutes and structured enough to be useful when someone reads it twelve months later.

---

## Step 1: Clarify the decision

Ask for or confirm:
- What was decided? (One clear sentence)
- When was this decided?
- Who was involved in making the decision?
- Is this decision already made, or is it still in progress?

If the decision is in progress, the record still gets written — just with an open status. Decision records for in-progress decisions are often the most valuable, because they capture the thinking before it is lost in the gap between discussion and resolution.

## Step 0: Decision trigger checklist

Before writing a record, confirm this decision warrants one. Not every choice needs a formal record — but more decisions warrant records than teams typically capture. Use this checklist:

**Create a decision record if any of these are true:**
- [ ] The decision affects more than one consuming team
- [ ] The decision involves a trade-off where reasonable people could disagree
- [ ] The decision will be referenced during future contribution reviews
- [ ] The decision changes a naming convention, token architecture, or API contract
- [ ] The decision deprecates or removes something from the system
- [ ] Someone asked "why do we do it this way?" and the answer was not documented
- [ ] The same question has come up more than once

**Skip the decision record if all of these are true:**
- The decision affects only one component's internal implementation
- The decision is easily reversible with no consumer impact
- The decision follows an existing, documented convention without exception

When in doubt, write the record. A twenty-minute investment in documentation saves hours of re-discovery and re-debate.

## Step 2: Write the record

Use the following six-section structure.

---

### Decision record: [title]

**ID:** DR-[number or date-based ID, e.g. DR-2026-03]
**Date:** [when the decision was made or this record was created]
**Status:** Accepted / Proposed / Superseded / Deprecated
**Authors:** [who made or documented this decision]

---

#### Context

What was the situation that made this decision necessary? What problem was being solved, or what question needed an answer?

Write this as a factual description of the state of the world at the time of the decision. Include any constraints that shaped the decision space — technical, organisational, time-based, or otherwise. Do not frame the context to make the eventual decision look inevitable. Future readers need to understand the real landscape, including the pressures that influenced the outcome.

Two to four sentences is usually enough.

#### Options considered

List each option that was genuinely evaluated. For each option:
- Name or brief description
- Why it was a viable candidate
- Why it was not chosen (if it was not)

Do not list options that were not seriously considered — this section should reflect the actual decision space, not a post-hoc justification exercise. If only one option was considered, say so and explain why.

The option that was eventually chosen should also appear here, with a note that it was selected and a forward reference to the decision section.

#### Decision

State the decision in one sentence. Then explain the primary reasoning in two to four sentences.

Be honest about trade-offs. If the chosen option had weaknesses that were accepted, name them. If the decision was influenced by non-technical factors — timelines, team preferences, tooling constraints — include that. Decision records that paper over trade-offs are records of what was decided, not why, which makes them significantly less useful.

#### Impact assessment

Quantify the impact of this decision. Numbers make a decision record actionable instead of archival.

| Impact dimension | Measurement |
|---|---|
| Files affected | [count — from grep/search if available] |
| Components affected | [count and names] |
| Consuming teams affected | [count and names] |
| Estimated migration effort | [range in hours, with assumptions] |
| Token/API changes required | [count] |
| Breaking changes | [yes/no — if yes, list them] |
| Timeline to full adoption | [estimate] |

If codebase access is available, run searches to populate these numbers rather than estimating. For example, if the decision is to adopt DTCG token format, count how many token files need restructuring, how many consuming files reference tokens, and how many teams own those files.

If quantitative data is not available, state what would need to be measured and recommend running the appropriate audit skill before committing to a timeline.

#### Consequences

What changes as a result of this decision? What becomes easier, and what becomes harder?

This section should cover both intended outcomes and known risks. If the decision introduces a dependency, a constraint, or a new obligation for contributors, document it here. If it closes off a future option, name that too.

#### Supersedes / superseded by

If this decision replaces a previous decision, reference it here.
If this decision is later superseded, this field gets updated with the reference to the new record.

#### Related records

Any other decision records relevant to understanding this one. Links or IDs are sufficient.

#### Recommended follow-up skills

Based on the decision's consequences, recommend specific Design System Ops skills that should be run next. This turns a decision record from a static document into a trigger for action.

| If the decision involves... | Run this skill next | Why |
|---|---|---|
| Deprecating a component | `deprecation-process` | Produces the full deprecation plan with timeline, migration guidance, and communication |
| Changing token architecture | `token-audit` | Validates the new architecture and surfaces gaps before migration begins |
| Changing a component API | `change-communication` | Produces release notes and migration guide for consuming teams |
| Introducing a new convention | `governance-encoder` | Encodes the convention as a machine-checkable rule |
| Affecting multiple consumers | `codemod-generator` | Produces automated migration scripts for consuming codebases |
| Making a large investment | `stakeholder-brief` | Translates the decision into a business-language brief for leadership |

Include only the follow-up skills that are relevant to this specific decision. This cross-linking ensures that decisions lead to action rather than sitting in a decisions directory unacted upon.

---

## Step 3: Determine where it lives

Decision records should be stored somewhere contributors will actually look. If the team uses a documentation platform (Zeroheight, Notion, Confluence), the record belongs there alongside the relevant component or system section. If the team uses a code repository, a `/decisions` or `/adr` directory works.

Suggest the appropriate location based on what you know about the team's setup. If unknown, recommend the documentation platform as the default.

## Step 4: Suggest a review trigger

Decision records go stale. Suggest a condition that should prompt this record to be revisited — for example, a tooling change, a team size threshold, a specific dependency version, or a timeline milestone.

This does not need to be elaborate. One sentence is enough: "Revisit this decision if the team grows beyond ten active contributors or if the token tooling changes."

## Quality checks

- Context describes the actual situation, not a setup for the conclusion
- Options considered reflects the real decision space, not a post-hoc list
- Decision section names the trade-offs that were accepted, not just the benefits
- Consequences covers both intended outcomes and known risks
- Record is written for someone who was not in the room — no assumed context
- Status field is set correctly
- A review trigger is included
