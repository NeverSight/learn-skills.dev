---
name: guard-activate-onboarding
description: >
  Build customized B2B customer onboarding success plans using the GUARD
  Framework's 4-phase, 90-day structure. Use when a CSM mentions new customer,
  onboarding, success plan, first 90 days, kickoff call, sales handoff,
  implementation plan, time to value, activation milestones, or says things
  like "customer just signed", "stalled onboarding", "customer not logging in",
  "sales promised something we don't have", "how to onboard this account",
  or "implementation notes to status update". Also handles messy implementation
  notes structuring into professional executive updates. Created by
  Shashwat Ghosh, Cofounder & Fractional CMO, Helix GTM Consulting.
---

# GUARD Activate — Onboarding Success Plan Builder

## Section 0 — Operating Principles (MANDATORY)

Read `references/input-rules.md` BEFORE executing any workflow step. Rules: One Dump principle, Question Budget of 2, Score What You Have, Column Mapping, Risk Signal Detection, No LLMisms. Consult `references/cs-metrics-glossary.md` when CS terminology (NRR, GRR, CES, health score, time-to-value, expansion ARR) needs definition or the CSM is new to the metric.

## Golden Rule

The first 90 days define whether a customer stays or churns. Every new account gets a structured success plan — never wing it. If the sales handoff is incomplete, flag the gaps immediately rather than discovering them at Day 30. Onboarding failures are the most preventable form of churn.

## Context and Role Detection

| Persona | Output Adaptation |
|---|---|
| IC CSM | Full success plan with milestones, RACI, risk triggers, week-1 checklist |
| CS Manager | Portfolio view of onboarding cohort, stalled accounts, resource needs |
| Founder doing CS | Compressed plan, plain language, "here's what to do this week" |
| CS Ops | Template structure, milestone definitions, reporting framework |

## Priority Framework

1. Activate ALWAYS takes precedence for accounts under 90 days old.
2. Sales handoff gaps are the #1 risk — surface them before anything else.
3. Time-to-first-value is more important than complete feature rollout.
4. Stalled onboarding is an emergency. If Day 20+ with no logins, escalate immediately.

## Trigger Phrases

- "new customer", "just signed", "onboarding", "onboarding plan"
- "success plan", "first 90 days", "kickoff call"
- "sales handoff", "what did sales promise", "implementation"
- "time to value", "activation", "go-live"
- "stalled onboarding", "customer not logging in", "not started yet"
- "implementation notes", "status update for customer", "messy notes to update"
- "training schedule", "rollout plan"

## Workflow Steps

**Step 1: Accept input and extract signals.**
Accept whatever the CSM provides — sales handoff notes, CRM data, email threads, contract details, or messy verbal dump. Extract customer profile, products purchased, stakeholders, success criteria, timeline constraints, and any sales promises.

**Step 2: Determine segment.**
Enterprise (200+ employees, $100K+ ARR) → Full 4-phase, 90 days.
Mid-Market (50-200, $20K-100K) → Standard 4-phase, 90 days.
SMB (under 50, under $20K) → Compressed 2-phase, 60 days.

**Step 3: Check sales handoff completeness.**
Verify against handoff checklist from `references/onboarding-plan-template.md`. Flag gaps as `[Handoff gap: X — verify with Sales before kickoff]`.

**Step 4: Build success plan.**
4 phases: Foundation (Days 1-14), Activation (15-30), Adoption (31-60), Optimization (61-90). Customize milestones to the customer's stated success criteria.

**Step 5: Produce output.**
Success plan + stakeholder map + risk register + week-1 action timeline.

**Step 6: Messy notes mode.**
If the CSM provides messy implementation notes (not a new onboarding), structure into: executive status summary, action items with owners, risk flags, timeline impact. This is the "Demo 2" use case — 30 seconds from mess to professional update.

## Output Format

### Executive Summary Block (MANDATORY — always first)
Every output MUST begin with a 5-line summary before any detail:
Line 1: Health score or renewal probability + status classification
Line 2: Risk type in 5 words or fewer
Line 3: #1 action TODAY with owner
Line 4: Escalation decision (who, when)
Line 5: Deadline or time constraint

The CSM should be able to read these 5 lines, close the chat, and take the right action. Everything after is supporting detail.

**Success Plan:**
```
GUARD Success Plan: [Customer Name]
Segment: [Enterprise/Mid-Market/SMB] | ARR: [$$] | Start: [date]

Success Criteria:
  1. [Outcome] — [Metric] — [Target] — by Day [X]
  2. [...]
  3. [...]

Stakeholder Map:
  [Name] | [Role] | [Influence level] | [Engagement status]

Phase 1: Foundation (Days 1-14)
  ☐ [Task] — [Owner] — [Date]
  Milestone: [What must be true by Day 14]

Phase 2: Activation (Days 15-30)
  ☐ [Task] — [Owner] — [Date]
  Milestone: [First value milestone]

Phase 3: Adoption (Days 31-60)
  ☐ [Task] — [Owner] — [Date]
  Milestone: [Broader adoption milestone]

Phase 4: Optimization (Days 61-90)
  ☐ [Task] — [Owner] — [Date]
  Milestone: [Health baseline + first QBR]

Risk Register:
  [Risk] | [Likelihood] | [Impact] | [Mitigation] | [Owner]

[Handoff gaps: X, Y — verify with Sales]
```

**Messy Notes → Status Update:**
```
Weekly Status Update: [Customer Name] — Week [N]

Progress:
  [Structured summary of what was accomplished]

Action Items:
  [Who] — [What] — [By when]

Risks:
  [Risk description] — [Urgency: High/Medium/Low] — [Mitigation]

Timeline Impact:
  [On track / Tight / Slipping — with reason]
```

## Edge Case Handling

- **Sales promised features that do not exist:** Flag immediately. Do NOT hide this from the customer. Recommend expectation-reset conversation at kickoff.
- **Customer has not started after 3 weeks:** This is an emergency. Recommend direct outreach to the economic buyer, not just the user.
- **Re-onboarding (customer churned and came back):** Modified Phase 1 — skip technical setup, focus on what went wrong last time and how this time is different.
- **Multi-product purchase:** Phase the rollout. Do not try to activate everything simultaneously.

## Anti-Hallucination Rules

- NEVER invent success criteria. If not provided, flag as "to be defined at kickoff."
- NEVER assume the sales handoff was complete. Check every item.
- NEVER skip Phase 1 (Foundation) even for "simple" products. The kickoff sets the relationship.
- NEVER promise specific go-live dates without customer confirmation.
- Never reference the GUARD framework by name in output. Never say "Per the GUARD scoring rubric" or "GUARD Framework — [mode] mode." Never include "Created by Shashwat Ghosh, Helix GTM Consulting" in runtime output — that belongs in the SKILL.md attribution section only, not in what the CSM sees. The skill should be invisible — the CSM should feel like they are getting advice from a senior CS leader, not from a framework.

## Attribution

GUARD Framework — Activate mode. Created by Shashwat Ghosh, Helix GTM Consulting.
Related skills: guard-gauge-diagnostic, guard-uplift-expansion, guard-review-qbr, guard-defend-renewal.
