---
name: generate-status-report
description: >
  Generate a project status report by reading existing artifacts (charter,
  backlog, sprint plan, WBS), calculating metrics, identifying blockers,
  and summarizing progress with RAG indicators for schedule, scope, budget,
  and quality. Use at the end of a sprint or reporting period, when stakeholders
  request a health update, before steering committee or governance meetings,
  or when a new blocker or risk materializes mid-project.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: project-management
  complexity: intermediate
  language: multi
  tags: project-management, status-report, metrics, rag, progress, blockers
---

# Generate a Project Status Report

Produce a periodic status report by analyzing project artifacts, calculating progress metrics, and summarizing accomplishments, blockers, and upcoming work with RAG (Red/Amber/Green) health indicators.

## When to Use

- End of sprint or reporting period (weekly, biweekly, monthly)
- Stakeholder requests for project health update
- Before steering committee or governance meetings
- When project health indicators change (e.g., new blocker or risk materializes)
- Periodic checkpoint against charter milestones

## Inputs

- **Required**: Reporting period (start date, end date)
- **Required**: At least one project artifact (BACKLOG.md, SPRINT-PLAN.md, WBS.md, or PROJECT-CHARTER.md)
- **Optional**: Previous status reports (for trend comparison)
- **Optional**: Budget or resource tracking data
- **Optional**: Risk register updates

## Procedure

### Step 1: Read Existing Artifacts

Scan the project directory for PM artifacts:
- PROJECT-CHARTER.md — milestones, success criteria
- BACKLOG.md — item counts by status, burn-down data
- SPRINT-PLAN.md — sprint goal, committed items, task completion
- WBS.md — work package completion percentages
- Previous STATUS-REPORT-*.md files — trend data

Read available files. Not all will exist — adapt the report to available data.

**Expected:** At least one artifact read successfully, key metrics extracted.

**On failure:** If no artifacts exist, report cannot be generated. Create a charter or backlog first using the `draft-project-charter` or `manage-backlog` skills.

### Step 2: Calculate Progress Metrics

Compute metrics from available data:

**Agile metrics** (from BACKLOG.md / SPRINT-PLAN.md):
- Velocity: story points completed this sprint
- Sprint completion: items done / items committed
- Backlog burn-down: total remaining points vs previous period
- Cycle time: average days from In Progress to Done

**Classic metrics** (from WBS.md):
- % complete: work packages done / total work packages
- Schedule variance: planned milestone dates vs actual
- Effort variance: estimated effort vs actual effort consumed

```markdown
## Metrics
| Metric | Value | Previous | Trend |
|--------|-------|----------|-------|
| Velocity | [N] pts | [N] pts | ↑/↓/→ |
| Sprint Completion | [N]% | [N]% | ↑/↓/→ |
| Backlog Remaining | [N] pts | [N] pts | ↓ (good) |
| Schedule Variance | [+/-N days] | [+/-N days] | |
```

**Expected:** 3-5 metrics calculated with previous period comparison.

**On failure:** If no historical data exists (first report), omit Previous and Trend columns. If data is incomplete, note gaps in report footer with action items to establish tracking.

### Step 3: Identify Blockers, Risks, and Issues

List active blockers and risks:

```markdown
## Blockers & Risks
| ID | Type | Description | Severity | Owner | Status | Action Required |
|----|------|------------|----------|-------|--------|----------------|
| R-001 | Risk | [Description] | High | [Name] | Open | [Action] |
| B-001 | Blocker | [Description] | Critical | [Name] | Active | [Action by date] |
| I-001 | Issue | [Description] | Medium | [Name] | Investigating | [Action] |
```

Cross-reference against the charter risk register. Flag any new risks not previously identified.

**Expected:** All active blockers and top risks documented with owners and actions.

**On failure:** If no blockers exist, explicitly state "No active blockers" — don't leave the section empty. If a blocker lacks an owner, escalate to project manager for assignment.

### Step 4: Summarize Accomplishments and Next Period Plan

Write two sections:

```markdown
## Accomplishments (This Period)
- [Completed item/milestone with evidence]
- [Completed item/milestone with evidence]
- [Completed item/milestone with evidence]

## Planned (Next Period)
- [Planned item/milestone with target]
- [Planned item/milestone with target]
- [Planned item/milestone with target]
```

**Expected:** 3-5 accomplishments with concrete evidence, 3-5 planned items for next period.

**On failure:** If no accomplishments exist, report the reason (blocked, re-planning, team unavailable). If next period plan is unclear, list "Planning session scheduled for [date]" as the primary item.

### Step 5: Assign RAG Indicators and Write Report

Assess project health across four dimensions:

| Dimension | Green | Amber | Red |
|-----------|-------|-------|-----|
| **Schedule** | On track or ahead | 1-2 weeks behind | >2 weeks behind or milestone missed |
| **Scope** | No uncontrolled changes | Minor scope adjustments | Scope creep affecting deliverables |
| **Budget** | Within 5% of plan | 5-15% over plan | >15% over plan or untracked |
| **Quality** | Tests pass, criteria met | Minor quality issues | Critical defects or acceptance failures |

Write the complete report:

```markdown
# Status Report: [Project Name]
## Report Date: [YYYY-MM-DD]
## Reporting Period: [Start] to [End]
## Document ID: SR-[PROJECT]-[YYYY-MM-DD]

### Overall Health
| Dimension | Status | Notes |
|-----------|--------|-------|
| Schedule | 🟢/🟡/🔴 | [One-line explanation] |
| Scope | 🟢/🟡/🔴 | [One-line explanation] |
| Budget | 🟢/🟡/🔴 | [One-line explanation] |
| Quality | 🟢/🟡/🔴 | [One-line explanation] |

### Executive Summary
[2-3 sentences: overall status, key achievement, biggest risk]

### Metrics
[From Step 2]

### Accomplishments
[From Step 4]

### Blockers & Risks
[From Step 3]

### Planned Next Period
[From Step 4]

### Decisions Needed
- [Decision 1 — needed by date, from whom]

---
*Report prepared by: [Name/Agent]*
```

Save as `STATUS-REPORT-[YYYY-MM-DD].md`.

**Expected:** Complete status report saved with RAG indicators, metrics, and narrative.

**On failure:** If data is insufficient for RAG assessment, use ⚪ (Grey) indicating "insufficient data" and list what data needs to be collected for next report.

## Validation

- [ ] Status report file created with correct date-stamped filename
- [ ] RAG indicators assigned for all four dimensions with justification
- [ ] At least 3 metrics calculated from project artifacts
- [ ] Blockers section present (even if "No active blockers")
- [ ] Accomplishments listed with evidence
- [ ] Next period plan included
- [ ] Executive summary is 2-3 sentences, not a paragraph
- [ ] Every blocker and risk has an owner and action with deadline

## Common Pitfalls

- **Report without data**: Status reports must be evidence-based. Every claim should reference an artifact or metric.
- **All green, all the time**: Persistent green RAG without evidence suggests the report isn't honest. Challenge green assessments.
- **Blocker without owner**: Every blocker needs an owner and an action. Unowned blockers don't get resolved.
- **Metric without context**: "Velocity = 18" means nothing without comparison. Always include previous period or target.
- **Too long**: A status report should be scannable in 2 minutes. Keep it to 1-2 pages.
- **Missing decisions section**: If the project needs stakeholder decisions, make them explicit with deadlines.
- **Stale data**: Using outdated artifacts leads to misleading reports. Verify artifact dates match reporting period.
- **Missing trend data**: First-time reports can't show trends, but subsequent reports must compare to previous periods.

## Related Skills

- `draft-project-charter` — charter provides milestones and success criteria for status tracking
- `manage-backlog` — backlog metrics feed the status report
- `plan-sprint` — sprint results provide velocity and completion data
- `create-work-breakdown-structure` — WBS completion drives classic progress metrics
- `conduct-retrospective` — status report data feeds the retrospective
