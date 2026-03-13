---
name: hreng-onboard-306090
description: Use when the user wants to create or refine 30/60/90 day onboarding plans for new engineering hires, with clear milestones, stakeholders, and risk mitigation.
version: 1.0.0
license: MIT
---

# HR Engineering Onboarding 30/60/90

## Overview

Create structured onboarding plans that set new engineers up for success through clear milestones, measurable outcomes, stakeholder engagement, and early feedback loops.

## When to Use

Use this skill when:
- A **new hire has accepted an offer** and you’re planning their first 90 days.
- Redesigning or **standardizing onboarding** for a team/org.
- Onboarding a **contractor-to-FTE conversion**.
- Creating **role- or level-specific** onboarding tracks.

Do **not** use this skill when:
- You’re defining **headcount needs and intake** → use `hreng-hire-intake`.
- You’re diagnosing **performance or burnout** for an existing employee → use `hreng-perf-diagnose` or `hreng-burnout`.
- The focus is **1:1 prep** for an existing report → use `hreng-1-1-prep`.
- The focus is **exit or handoff** for a departing person → use `hreng-offboard`.

## Inputs Required

- Role title and level.
- Team goals and near-term roadmap.
- Start date and any constraints (time zones, part-time, parental leave, etc.).
- Onboarding resources (buddy availability, documentation, training).

## Outputs Produced

- A structured **30/60/90 onboarding plan JSON** (`templates/30-60-90-template.json`).
- A **manager-facing narrative plan** (`templates/onboarding-30-60-90-plan-manager.md`).
- A **stakeholder map** and **checkpoint agendas** (`templates/stakeholder-map.md`, `templates/checkpoint-agenda.md`).

## Tooling Rule

- If MCP tools are available, prefer them for employee/team context (HRIS, calendar, org chart).
- Use repository templates for all artifacts, then customize to the specific hire.

## Core Plan Structure

### 30-Day Plan: Foundation

**Goals:**
- Understand codebase, architecture, and development workflow.
- Complete environment setup and access provisioning.
- Ship the first small contribution.
- Meet key stakeholders and understand team mission.

**Measurable Outcomes:**
- [ ] Development environment fully configured.
- [ ] 1–2 small PRs merged (bug fixes, docs, low-risk tasks).
- [ ] Completed codebase overview / architecture walkthrough.
- [ ] 1:1s with manager, onboarding buddy, and 3–5 teammates.
- [ ] Participation in team rituals (standups, planning, retro).

**Activities (example by week):**
- Week 1: Setup, documentation, shadowing, intro meetings.
- Week 2: First contributions with heavy pairing/review.
- Week 3: Domain deep-dive, product context, stakeholder meetings.
- Week 4: 30-day checkpoint with manager, including feedback both ways.

**Stakeholders:**
- Onboarding buddy (day-to-day help).
- Hiring manager (expectations, feedback).
- Tech lead (architecture, technical decisions).
- Cross-functional partners (PM, design, data, support).

**Risks & Mitigations:**
- Environment setup blockers → Pre-provision access, clear setup docs.
- Slow ramp due to complexity → Pair programming, “tour of systems”.
- Isolation (especially remote) → Scheduled social time, regular check-ins.

### 60-Day Plan: Contribution

**Goals:**
- Own end-to-end features with guidance.
- Demonstrate technical competency for their level.
- Build relationships beyond immediate team.
- Understand roadmap and business context in depth.

**Measurable Outcomes:**
- [ ] Shipped 1–2 medium-sized features end-to-end.
- [ ] Participated in on-call rotation (or completed shadowing), if applicable.
- [ ] Presented a technical topic at a team meeting.
- [ ] Received peer feedback (formal or informal).
- [ ] Contributed to team processes (docs, tooling, test improvements).

**Activities:**
- Week 5–6: Increase feature ownership, reduce pairing intensity.
- Week 7: On-call shadowing or first light on-call, if your org uses it.
- Week 8: Midpoint review with manager focusing on strengths and gaps.

**Risks & Mitigations:**
- Overconfidence → rushing changes → Maintain strong code review norms.
- Underconfidence → not asking for help → Normalize “ask early” and visible support.
- Misaligned expectations → Lack of explicit success criteria → Use ladder + clear 60-day goals.

### 90-Day Plan: Impact

**Goals:**
- Operate autonomously at level expectations.
- Drive initiatives beyond assigned tasks.
- Demonstrate ownership and early leadership (relative to level).
- Successfully complete probation/trial period.

**Measurable Outcomes:**
- [ ] Led design and implementation of a significant feature or project slice.
- [ ] Proactively identified and solved at least one meaningful problem.
- [ ] Positive feedback from peers and key stakeholders.
- [ ] Meets or exceeds competency expectations for level (technical, collaboration, ownership).
- [ ] Manager recommends continuation and integration into regular performance cycle.

**Activities:**
- Week 9–11: Full autonomy on larger projects, including design input.
- Week 12: 90-day structured review with manager (strengths, gaps, next 6–12 months).
- Week 13+: Transition to standard performance and growth cadence.

**Risks & Mitigations:**
- Not meeting bar → Mitigation: Early flagging by week 4 and 8, targeted support plan.
- Burnout from over-achievement → Mitigation: Align pace expectations, avoid hero culture.
- Lack of feedback → Mitigation: Scheduled written and verbal feedback at 30/60/90.

## Level-Specific Customization (Examples)

### Junior Engineer (L3)
- **30 days:** Setup, learning codebase, small tickets with pairing.
- **60 days:** Ship one feature with heavy guidance; focus on fundamentals.
- **90 days:** Independently ship features with standard code review.

### Mid Engineer (L4)
- **30 days:** Setup + small features independently.
- **60 days:** Own medium features, some tech lead support.
- **90 days:** Fully autonomous, begins mentoring juniors.

### Senior Engineer (L5)
- **30 days:** Quick ramp; meaningful contributions within first month.
- **60 days:** Leads features and shapes technical direction.
- **90 days:** Drives initiatives, mentors, and improves team processes.

### Staff+ Engineer (L6+)
- **30 days:** Context gathering, relationship building, understanding strategy.
- **60 days:** Proposes strategic initiatives, influences across teams.
- **90 days:** Executes on strategic work with org-level impact.

## Output Template

Base your JSON output on `templates/30-60-90-template.json`:

```json
{
  "new_hire": {
    "name": "string",
    "role": "string",
    "level": "string",
    "start_date": "YYYY-MM-DD",
    "manager": "string",
    "onboarding_buddy": "string"
  },
  "plan_30_days": {
    "goals": ["array of strings"],
    "outcomes": ["array of measurable outcomes"],
    "activities": [
      {
        "week": 1,
        "focus": "string",
        "deliverables": ["array"]
      }
    ],
    "stakeholders": [
      {
        "name": "string",
        "role": "string",
        "interaction": "1:1|meeting|shadowing"
      }
    ],
    "risks": [
      {
        "risk": "string",
        "mitigation": "string"
      }
    ]
  },
  "plan_60_days": { /* similar structure */ },
  "plan_90_days": { /* similar structure */ },
  "checkpoints": [
    {
      "day": 7,
      "type": "informal",
      "focus": "Setup complete? Blockers?"
    },
    {
      "day": 30,
      "type": "formal",
      "focus": "Foundation laid? Ready for more ownership?"
    },
    {
      "day": 60,
      "type": "formal",
      "focus": "Contributing well? Feedback?"
    },
    {
      "day": 90,
      "type": "formal",
      "focus": "Performance review, probation decision"
    }
  ],
  "success_criteria": {
    "technical": "string - level-appropriate technical performance",
    "collaboration": "string - working well with team",
    "ownership": "string - taking initiative",
    "growth": "string - learning and adapting"
  }
}
```

## Using Supporting Resources

### Templates
- **`templates/30-60-90-template.json`** – Complete plan schema by level (JSON).
- **`templates/onboarding-30-60-90-plan-manager.md`** – Manager-facing onboarding plan.
- **`templates/stakeholder-map.md`** – Key relationships to build.
- **`templates/checkpoint-agenda.md`** – Checkpoint meeting template.

### References
- **`references/onboarding-best-practices.md`** – Research-backed onboarding approaches (stub: add your playbook).
- **`references/remote-onboarding.md`** – Remote-specific strategies and pitfalls (stub: expand as needed).
- **`references/checklist.md`**, **`references/overview.md`**, **`references/risk-library.md`**, **`references/manager-notes.md`** – Process and risk guidance.

### Scripts
- **`scripts/check-hreng-onboard-306090.sh`** – Pre-run checks for the skill.
- **`scripts/validate-hreng-onboard-306090.py`** – Check plan completeness and measurability.

## Common Mistakes

- Treating onboarding as **“ship as fast as possible”** instead of learning + relationships.
- Failing to schedule **regular feedback** and waiting until day 90 to flag issues.
- Underestimating the impact of **remote/async constraints** on ramp-up.
- Copy-pasting a generic plan that ignores **level and role**.

The 30/60/90 plan should make it obvious what “good” looks like for this hire and give the manager a concrete way to track progress and intervene early if needed.