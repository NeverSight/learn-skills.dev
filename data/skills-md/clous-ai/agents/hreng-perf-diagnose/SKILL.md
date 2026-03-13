---
name: hreng-perf-diagnose
description: Use when the user wants to diagnose engineering performance issues (individual or team), distinguish systemic vs. individual patterns, and design data-driven interventions.
version: 1.0.0
license: MIT
---

# HR Engineering Performance Diagnose

## Overview

Systematically diagnose team and individual performance issues using quantitative and qualitative signals, separate systemic problems from individual gaps, and generate concrete, fair interventions.

## When to Use

Use this skill when:
- You’re seeing **missed commitments, low velocity, or quality issues** and want to understand why.
- You need a **structured performance diagnosis** for a specific person or team.
- You want to differentiate **systemic constraints** (scope, process, leadership) from **individual performance**.
- You’re preparing for a **performance conversation, PIP, or team health review**.

Do **not** use this skill when:
- The primary concern is **burnout risk** → start with `hreng-burnout` (then come back here if needed).
- You’re designing **career ladders or promotion criteria** → use `hreng-ladder`.
- You’re doing a **skills inventory vs. roadmap** → use `hreng-skills`.

## Inputs Required

- Time window to analyze (e.g., last 1–3 quarters).
- Performance signals (both **quantitative** and **qualitative**).
- Role expectations and level definitions (ideally from your ladder).
- Any recent org or product changes that could affect performance.

## Outputs Produced

- A structured **diagnostic JSON** capturing patterns, root causes, and recommended actions.
- A **manager/HR-friendly narrative report** summarizing findings and risks.

## Tooling Rule

- If MCP tools are available, prefer them for performance data sources (issue tracker, CI, incidents, HRIS).
- Use the templates in this repo for **all structured outputs** instead of ad hoc formats.

## Core Pattern

1. **Collect multi-source data** (velocity, quality, reviews, feedback, attendance).
2. **Cluster patterns** into individual vs. systemic findings.
3. **Identify root causes** across skills, expectations, context, and leadership.
4. **Map causes to interventions** with owners, timelines, and success metrics.
5. **Document clearly** for managers/HR, including risks of inaction and fairness checks.

## Data Collection

### Quantitative Signals

Look across:
- **Velocity/throughput:** stories per sprint, PRs/month, throughput trends.
- **Quality:** bug rates, incident frequency, regressions, escaped defects.
- **Code review:** time to review, review depth, number of rework cycles.
- **On-time delivery:** % of work delivered on time vs. re-scoped or delayed.
- **Availability:** attendance patterns, responsiveness to critical comms.

Important:
- Compare individuals to **team baselines**, not arbitrary expectations.
- Use **trends over time**, not single bad sprints.

### Qualitative Signals

Gather:
- Peer feedback (360, ad hoc comments).
- Stakeholder satisfaction (PM, design, support, GTM).
- 1:1 notes from the manager (with themes, not private details).
- Code review comments (patterns: “needs more tests”, “unclear design”, etc.).
- Meeting participation and cross-functional collaboration patterns.

## Pattern Analysis

### Individual Underperformance

Indicators:
- Performance concerns are **isolated** to one person vs. the whole team.
- Peer/stakeholder feedback repeatedly mentions **specific behaviors**.
- Clear gaps vs. documented level expectations (from career ladder).
- Issues persist **even when constraints are removed** (e.g., others succeed under same conditions).

Sanity checks:
- Has the person had **clear expectations** and feedback?
- Are they working on problems **appropriate for their level**?
- Are there signals of **burnout or wellbeing** issues that should be addressed first?

### Systemic Issues

Indicators:
- Multiple team members showing **similar performance symptoms**.
- External factors: org reshuffle, unstable roadmap, shifting priorities.
- Resource constraints: missing tooling, unclear ownership, under-staffing.
- Process problems: constant interruptions, context switching, broken workflows.

Rule of thumb:
- If **3+ people** show the same pattern, treat it as **systemic until proven otherwise**.

## Root Cause Identification

Common categories:

1. **Skill gaps**
   - Missing technical skills, design skills, or communication skills.
   - Often fixable via training, pairing, and targeted work.
2. **Unclear expectations**
   - No concrete level expectations, vague goals, shifting targets.
   - People “underperform” against expectations **they never actually received**.
3. **Personal/wellbeing issues**
   - Health, family, mental health, burnout (see `hreng-burnout`).
   - Requires **supportive, confidential handling**, not just performance framing.
4. **Management gaps**
   - Irregular feedback, poor prioritization, unclear strategy, weak sponsorship.
   - Team-level issues are often **management performance** problems.
5. **Role misfit**
   - Wrong level, wrong role (IC vs. manager), or misaligned strengths.
   - May call for role redesign, level correction, or transfers.
6. **External blockers**
   - Dependencies, cross-team bottlenecks, unowned work, flaky infra.

For each finding, explicitly identify:
- **Primary root cause category** (from list above).
- **Contributing factors** (other categories that matter).

## Diagnostic Output Structure

Use `templates/metrics-template.json` and `templates/performance-diagnosis-report.md` as baselines. A typical JSON summary:

```json
{
  "team": "Platform",
  "period": "Q4 2025",
  "findings": [
    {
      "type": "individual",
      "employee": "Name",
      "pattern": "Consistently missing sprint commitments",
      "evidence": [
        "Missed 4 of last 6 sprint goals while peers hit 80%+",
        "Peer feedback: unclear communication about blockers"
      ],
      "root_cause": "Skill gap in task estimation and reluctance to surface blockers early",
      "recommendation": "Mentorship on estimation, explicit expectations about raising risks, smaller scoped tickets for next 2 sprints",
      "urgency": "medium"
    },
    {
      "type": "systemic",
      "pattern": "Team velocity down 30% this quarter",
      "evidence": [
        "Average velocity: 45 → 32 story points",
        "Incident load doubled (2.1 → 4.3 incidents/week)"
      ],
      "root_cause": "Increased on-call burden and unclear Q4 priorities",
      "recommendation": "Reduce scope, clarify top 3 priorities, run incident postmortems to reduce repeat pages",
      "urgency": "high"
    }
  ]
}
```

## Interventions & Fairness Checks

For each individual finding, specify:
- **Concrete interventions:** coaching, mentorship, training, project rotation, or PIP (as last resort).
- **Timeline:** when you’ll re-evaluate (e.g., 4–8 weeks).
- **Success metrics:** what “improved” concretely looks like.

For each systemic finding, specify:
- **Process or structure changes:** clarify priorities, fix ownership, improve tooling.
- **Leadership actions:** manager training, clearer strategy, reducing WIP.
- **Risk of inaction:** impact on attrition, quality, or roadmap.

Fairness checklist before labeling someone “underperforming”:
- [ ] Are expectations documented and shared?
- [ ] Has the person received **specific, recent feedback**?
- [ ] Are peers with similar conditions performing better (evidence)?
- [ ] Have systemic constraints and burnout been evaluated?
- [ ] Is there any bias risk (location, identity, communication style, etc.)?

## Using Supporting Resources

### Templates
- **`templates/metrics-template.json`** – Structured performance metrics to track consistently.
- **`templates/performance-diagnosis-report.md`** – Narrative diagnosis report for managers/HR.
- **`templates/diagnostic-framework.md`** – Checklist-style root cause analysis guide.

### References
- **`references/overview.md`**, **`references/checklist.md`**, **`references/pitfalls.md`** – Process and pitfalls.
- **`references/intervention-library.md`** – Intervention options and fairness checks.
- **`references/output-schema.md`** – Diagnostic output structure.

### Scripts
- **`scripts/check-hreng-perf-diagnose.sh`** – Pre-run checks for the skill.
- **`scripts/validate-hreng-perf-diagnose.py`** – Validate diagnostic JSON and report structure.

## Common Mistakes

- Jumping straight to **PIP or “low performer” labels** without checking systemic factors.
- Treating **a few bad sprints** as a verdict instead of a signal.
- Overweighting **communication style** over actual outcomes (especially across cultures).
- Ignoring **burnout indicators** and reading them purely as poor performance.
- Producing diagnoses with **no explicit owner or follow-up date**.

Your goal is to produce a diagnosis that a reasonable third party would consider **fair, evidence-based, and actionable** if they read it six months later.