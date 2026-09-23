---
name: pace-plan
description: >-
  Build, coordinate, operate, troubleshoot, exercise, and improve an authorized
  Primary, Alternate, Contingency, and Emergency communications plan. Use for
  resilient emergency-communications paths and their ownership, triggers,
  check-ins, tests, and corrective actions. Do not use for generic incident
  status messaging, frequency or channel planning, radio programming, or
  unauthorized transmission and activation.
license: MIT
compatibility: No runtime dependency. Local procedures, authorities, regulations, and communication details must be supplied by the user.
---

# PACE Plan

PACE means Primary, Alternate, Contingency, and Emergency. Use this skill to make a group's communications fallbacks operable, testable, and reviewable without inventing local facts or authority.

## Safety And Authority

This skill can support live activation, transmission, or tests that change external state. Read-only discovery and document drafting may proceed without confirmation.

Before the first real transmission, activation, live-system test, or other external mutation:

> Confirm the target, scope, and rollback path before acting. Read-only discovery may proceed without confirmation.

Also confirm the named activation authority permits the operational action under the applicable procedure. Plan approval by a decision-maker does not by itself authorize activation. Never infer authority from urgency, role labels, access to equipment, or possession of plan details. Destructive actions and irreversible cleanup require an explicit user directive.

Do not invent frequencies, channels, talkgroups, call signs, contacts, infrastructure, regulatory permission, medical or public-safety instructions, or authority to transmit or activate. Defer to authorized operating procedures, applicable regulation, and incident leadership.

## Core Workflow

```text
PLAN -> COORDINATE -> OPERATE -> TROUBLESHOOT -> EXERCISE -> IMPROVE
```

1. **PLAN:** Define the mission or essential function and every sender/receiver pair that must communicate. Inventory only authorized and available capabilities.
2. **COORDINATE:** Assign owners, participants, decision authority, activation authority, and handoffs. Validate that both ends can use each path.
3. **OPERATE:** Define contact, check-in, escalation, fallback, activation, and abandonment procedures with observable criteria.
4. **TROUBLESHOOT:** Check the expected tier, endpoint readiness, dependencies, and evidence before recommending a transition or handoff.
5. **EXERCISE:** Design an authorized, bounded test with objectives, safety limits, expected evidence, and a stop condition. Exercise paths only to the available and authorized extent.
6. **IMPROVE:** Record findings, corrective actions, owners, due dates, validation actions, plan changes, unresolved gaps, and the next review.

## Path Quality Gate

Evaluate every proposed P/A/C/E path against these CISA-derived questions:

- **Feasible:** Are working systems and trained users available at both ends?
- **Acceptable:** Can the path be established without interfering with concurrent operations?
- **Suitable:** Can it carry the operationally required information?
- **Distinguishable:** Does it avoid the failed method and shared dependencies that would fail with it?
- **Complete:** Are the method and transition triggers explicit?

Different applications are not demonstrably independent merely because their names differ. When paths share a device, network, power source, provider, site, or other critical dependency, identify whether the anticipated failure would disable both and record the owner's risk decision. Do not declare independence from technology names alone.

If four feasible paths do not exist, preserve missing tiers as explicit gaps. A truthful incomplete plan is safer than invented redundancy.

## Unknowns Contract

Never fill a missing plan-local fact with a plausible value. Record:

```text
VALUE: UNKNOWN
OWNER: [person or role responsible for resolving it]
VALIDATION ACTION: [observable check that will establish the value]
```

An unknown authority, trigger, endpoint capability, or required contact blocks approval of the affected path. It does not block documenting the rest of the plan.

## Loading Guide

| Need | Load | File |
|---|---|---|
| Design a plan or audit path completeness and independence | Plan design method | `references/plan-design.md` |
| Assign authority, align endpoints, or define activation and handoff | Coordination and operation | `references/coordination-and-operation.md` |
| Diagnose a failed or degraded path | Troubleshooting method | `references/troubleshooting.md` |
| Design a drill, after-action review, or improvement cycle | Exercise and improvement | `references/exercise-and-improvement.md` |
| Audit the domain claims or source limitations behind this skill | Evidence base | `references/evidence-base.md` |
| Test description boundaries outside portable output evals | Trigger probes | `references/trigger-probes.md` |

## Templates

| Artifact | Use when | File |
|---|---|---|
| PACE plan worksheet | Creating or auditing all four paths for one mission or function | `templates/pace-plan-worksheet.md` |
| Communications check-in card | Giving participants a concise, approved operating aid | `templates/communications-check-in-card.md` |
| Exercise and after-action review | Planning a bounded test and converting observations into corrective actions | `templates/exercise-and-after-action-review.md` |
| Troubleshooting decision log | Diagnosing a failure and preserving evidence, decisions, and handoffs | `templates/troubleshooting-decision-log.md` |

## Operating Rules

- Progress through tiers according to the approved plan's triggers, not by improvising a preferred method.
- Verify sender and receiver readiness; a one-sided path is not feasible.
- Use the plan-local review and exercise cadence. Do not invent a universal cadence.
- Keep operational identifiers in the group's protected plan, not in generic examples or public artifacts.
- When immediate danger exists, route to emergency services and authorized incident procedures rather than improvising operational instructions.
- If no communication path remains, record the condition and use only preauthorized no-communications procedures.

## Completion Gate

The work is complete only when:

- [ ] The named owner and authorized decision-maker approved the plan.
- [ ] Every required communication pair has P/A/C/E entries or explicitly owned gaps.
- [ ] Every path has documented dependencies, triggers, check-ins, abandonment criteria, and recovery or handoff.
- [ ] Sender and receiver capability was validated to the available extent.
- [ ] Intended paths were exercised to the available and authorized extent, with evidence recorded.
- [ ] Findings and corrective actions have owners, validation actions, and review dates.
- [ ] Unresolved gaps remain visible; none were replaced with assumptions.
- [ ] The change record identifies what changed, why, who approved it, and when it will be reviewed.

## When Not To Use

- Use an incident-communications or stakeholder-communications workflow for status updates, audience messaging, and notification copy that do not concern redundant communication paths.
- Use the group's authorized radio, frequency, channel, spectrum, or deployment procedure for technical programming and allocation details.
- Use emergency services and incident leadership for immediate life-safety decisions.
- Do not use this skill as authority to operate equipment, transmit, activate a system, bypass regulation, or override an incident command structure.

## Portability

This skill is technology-neutral and host-neutral. It organizes plan-local facts and decisions; it does not replace local procedures, licenses, regulations, equipment manuals, or incident authority.
