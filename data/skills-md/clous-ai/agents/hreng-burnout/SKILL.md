---
name: hreng-burnout
description: Use when the user wants to detect or assess engineering burnout risk (after-hours work, on-call load, unsustainable pace, team health checks) for an individual or team.
version: 1.0.0
license: MIT
---

# HR Engineering Burnout Diagnose

## Overview

Detect and diagnose engineering burnout risk using data across workload patterns, after-hours activity, on-call load, and team context, then turn it into a concrete mitigation plan.

## When to Use

Use this skill when:
- You see **sustained after-hours/weekend work** and want to know if it indicates burnout.
- You need a **structured burnout risk assessment** for a specific engineer or team.
- You want to **review on-call load** for fairness and sustainability.
- You’re preparing a **manager/HR discussion** about potential burnout or attrition risk.
- You want a **pre-mortem** before pushing the team harder (big launch, incident spike).

Do **not** use this skill when:
- The primary question is **performance quality or underperformance** → use `hreng-perf-diagnose`.
- You’re designing **career progression or promotion cases** → use `hreng-ladder`.
- You’re assessing **skills coverage vs. roadmap** → use `hreng-skills`.

## Inputs Required

- Time window to analyze (e.g., last 3 / 6 / 12 months).
- Workload and incident signals you can access (git, incidents, on-call, calendars, tickets).
- On-call rotation details (if applicable).
- Team context (org changes, big launches, layoffs, restructurings).

## Outputs Produced

- A **structured burnout indicators JSON** for the person/team.
- A **manager-ready risk assessment report**.
- A **prioritized mitigation and monitoring plan**.

## Tooling Rule

- If MCP tools are available, prefer them for incident/workload data (PagerDuty, Jira, calendars, git, HRIS).
- If scripts/templates exist in this repo, **always** base your output on them instead of inventing new formats.

## Core Pattern

1. **Collect signals** across code, incidents, on-call, meetings, and qualitative feedback.
2. **Score each indicator** (low/medium/high) using quantitative thresholds plus context.
3. **Determine risk level** (low/medium/high/critical) and what’s systemic vs. individual.
4. **Generate artifacts** using templates (indicators JSON, manager report, recommendations).
5. **Highlight trade-offs** (burnout vs. short-term delivery pressure) and concrete next steps.

## Quick Reference

| Dimension           | Example Metrics                                    | Typical Red Flags (guidance, not hard rules)                         |
|---------------------|----------------------------------------------------|-----------------------------------------------------------------------|
| After-hours work    | Commits/emails by hour, weekend activity          | \>20–30% work outside 9–6; regular weekend pushes; late-night spikes |
| On-call load        | Incidents/shift, pages/night, time to resolve     | \>3 incidents/week; \>5 pages/shift; same person paged repeatedly    |
| Workload & focus    | PRs to review, projects per person, context areas | \>10 PRs/week; \>3 parallel projects; 5+ distinct domains in a week  |
| Meetings            | Hours/week, fragmentation                         | \>20 hours/week; 4+ context switches/day due to meetings             |
| Trend & trajectory  | Last 3–6 months                                   | Clear upward trend in load + downward trend in engagement/output     |

## Data Collection & Indicators

### 1. Git & After-Hours Activity

**Goal:** Detect sustained, not one-off, patterns of after-hours and weekend work.

**Example commands (adapt author filters as needed):**

```bash
# Commits by hour (detect after-hours work)
git log --author="Name" --date=format:'%H' --pretty=format:'%ad' | sort | uniq -c

# Commits by day of week (weekend work)
git log --author="Name" --date=format:'%u' --pretty=format:'%ad' | sort | uniq -c

# Commit velocity trend by week
git log --author="Name" --since="6 months ago" --pretty=format:'%ad' --date=short | uniq -c
```

**Interpretation guidance:**
- Look for **multi-week patterns**, not single crunch weeks.
- Correlate spikes with **launches or incidents** before labeling as burnout.
- Account for **time zones and personal preference** (some engineers prefer evenings).

**Typical warning signs:**
- \>20–30% of commits outside local 9am–6pm for 6+ consecutive weeks.
- Regular weekend commits (\>10% of total) that aren’t tied to agreed launches.
- Late-night activity spikes (after 10pm) in multiple weeks.
- Declining commit velocity paired with increasing after-hours work.

### 2. On-Call & Incident Analysis

**Metrics to assemble:**
- Incidents per on-call shift/week.
- After-hours pages per shift.
- Time to acknowledge / resolve.
- Rotation fairness (how often each person is on-call).

**Typical warning signs:**
- \>3 incidents per on-call week for multiple weeks.
- \>5 after-hours pages per shift (people woken up multiple nights).
- Uneven rotation (same person carries outsized share, even if “volunteered”).
- Long incident resolution times (\>4 hours) due to exhaustion or overload.

### 3. Workload, Meetings, and Context Switching

**Signals to gather:**
- PR review load per engineer (opened vs. reviewed PRs).
- Number of concurrent projects/initiatives.
- Meeting hours per week, especially fragmented across days.
- Distinct repos/domains touched per week.

**Typical warning signs:**
- \>10 PRs to review per week for multiple weeks.
- Working on \>3 significant projects simultaneously.
- \>20 hours of recurring meetings per week.
- Frequent context switches (5+ different domains in a week).

### 4. Qualitative Indicators

Pull in:
- Recent 1:1 notes (energy, frustration, disengagement).
- Peer feedback about responsiveness, tone, and reliability.
- Self-reported stress, sleep, or health clues (without over-interpreting).
- Changes in participation (silent in meetings, cameras off, less proactive).

## Risk Assessment Structure

Always normalize your output to the JSON structure in `templates/burnout-indicators.json`. A typical filled-out structure looks like:

```json
{
  "employee": "Name",
  "assessment_date": "2026-01-22",
  "risk_level": "high",
  "indicators": [
    {
      "category": "after_hours_work",
      "severity": "high",
      "evidence": "35% of commits between 8pm-1am over last 8 weeks (team avg: 9%)",
      "trend": "increasing"
    },
    {
      "category": "on_call_load",
      "severity": "medium",
      "evidence": "4.2 incidents per on-call week (team avg: 2.1)",
      "trend": "stable"
    }
  ],
  "overall_drivers": [
    "Incident spike since Q4",
    "Understaffed platform team"
  ]
}
```

Map your indicator severities to an overall risk level:

- **Low:** Mostly healthy patterns, occasional spikes with clear context.
- **Medium:** Several medium indicators or one high indicator; risk if trend continues.
- **High:** Multiple high indicators or one critical (e.g., repeated all-nighters).
- **Critical:** Clear harm signals (health, medical leave, meltdown, attrition risk).

## Intervention Strategies

Anchor your recommendations in `templates/recommendations.md` and produce a **short, prioritized list** (3–7 items) with owners and timelines.

**Immediate actions (high/critical risk):**
- Reduce workload (remove lower-priority projects, stop scope creep).
- Pause or soften on-call rotation for the individual.
- Encourage real rest (PTO, no-slack expectation, explicit manager support).
- Manager to run a **non-judgmental 1:1** focused on support, not blame.

**Medium-term (systemic fixes):**
- Redistribute work and **fix unfair rotations**.
- Address systemic sources of load (incident reduction, tech debt, broken process).
- Add automation and tooling to reduce toil.
- Plan headcount or scope cuts explicitly instead of “heroics”.

**Long-term (culture & norms):**
- Make “sustainable pace” an explicit team norm.
- Clarify expectations about after-hours work and responses.
- Invest in on-call quality (runbooks, SLOs, better escalation).
- Cross-train team to reduce single points of failure.

## Manager-Facing Report

Use `templates/burnout-risk-assessment-report-manager.md` as the base and populate:
- **Context:** Time period, team, role, data sources used.
- **Summary:** One paragraph: current risk level and main drivers.
- **Evidence:** 3–7 bullet points tying indicators to specific data.
- **Recommended actions:** Ordered by urgency and impact.
- **Follow-up plan:** How and when you’ll re-check indicators.

## Using Supporting Resources

### Templates
- **`templates/burnout-indicators.json`** – Canonical indicators JSON schema.
- **`templates/burnout-risk-assessment-report-manager.md`** – Manager-facing narrative assessment template.
- **`templates/recommendations.md`** – Mitigation and intervention plan structure.

### Scripts
- **`scripts/check-hreng-burnout.sh`** – Pre-run checks for the skill.
- **`scripts/validate-hreng-burnout.py`** – Validate indicators JSON and report structure.

## Common Mistakes

- Treating **single crunch weeks** as burnout without trend/context.
- Ignoring **self-reported signals** because “metrics look fine”.
- Focusing only on an individual when **patterns are clearly systemic**.
- Confusing **high engagement** (voluntary extra work) with unmanaged burnout.
- Producing vague recommendations like “improve work-life balance” without owners or timelines.

Aim for **specific, data-backed, and humane** recommendations that a manager can act on within the next 1–3 sprints.