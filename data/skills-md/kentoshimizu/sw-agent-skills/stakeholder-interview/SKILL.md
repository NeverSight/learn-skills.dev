---
name: stakeholder-interview
description: "Internal stakeholder interview workflow for capturing constraints, decision authority, and policy requirements. Use when delivery is blocked by unresolved business, engineering, legal, security, or operations decisions; do not use for end-user behavior research."
---

# Stakeholder Interview

## Overview
Use this skill to extract authoritative decisions from internal stakeholders and convert them into traceable engineering constraints.

## Scope Boundaries
- Requirements or architecture choices are blocked by missing policy or ownership decisions.
- Teams disagree about constraints and need documented decision authority.
- Cross-functional alignment is required before implementation commitments.

## Templates And Assets
- Interview note template:
  - `assets/stakeholder-interview-template.md`
- Decision conflict log:
  - `assets/decision-conflict-log-template.md`

## Inputs To Gather
- Decision questions and why each question is blocking progress.
- Stakeholder map with authority boundaries and fallback approvers.
- Existing assumptions, unresolved conflicts, and time constraints.

## Deliverables
- Interview records with source, date, authority level, and explicit decision statement.
- Constraint catalog (policy, compliance, operational, budget, timeline).
- Conflict log with owner, escalation route, and required resolution date.

## Workflow
1. Define interview goals as decision questions, not open brainstorming topics.
2. Prioritize stakeholders by decision authority and delivery criticality.
3. Conduct structured interviews and separate facts from preferences.
4. Confirm decisions in writing with explicit scope and expiry assumptions.
5. Record conflicts and escalate unresolved items with options and impacts.
6. Publish an auditable summary that downstream requirement skills can consume.

## Quality Standard
- Every key claim has a named source and explicit authority level.
- Ambiguous statements are converted into verifiable constraints.
- Conflicts are visible with an assigned owner and deadline.
- Outputs are specific enough to drive requirement and implementation decisions.

## Failure Conditions
- Stop when no stakeholder with decision authority is available.
- Stop when interview outputs mix assumptions and approved policy.
- Escalate when blocking conflicts remain unresolved past agreed deadlines.
