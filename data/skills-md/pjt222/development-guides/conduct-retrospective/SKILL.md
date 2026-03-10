---
name: conduct-retrospective
description: >
  Conduct a project or sprint retrospective by gathering data from status
  reports and velocity metrics, structuring what went well and what needs
  improvement, and generating actionable improvement items with owners and
  due dates. Use at the end of a sprint, after a project phase or milestone,
  following a significant incident or success, at a quarterly review of
  ongoing processes, or before starting a similar project to capture lessons
  learned.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: project-management
  complexity: basic
  language: multi
  tags: project-management, retrospective, continuous-improvement, agile, lessons-learned
---

# Conduct a Retrospective

Facilitate a structured retrospective that reviews recent project execution, identifies what worked and what didn't, and produces actionable improvement items that feed back into project processes. This skill transforms raw project data into evidence-backed learnings with specific actions, owners, and due dates.

## When to Use

- End of a sprint (sprint retrospective)
- End of a project phase or milestone
- After a significant incident, failure, or success
- Quarterly review of ongoing project processes
- Before starting a similar project (lessons learned review)

## Inputs

- **Required**: Period under review (sprint number, date range, or milestone)
- **Optional**: Status reports from the review period
- **Optional**: Sprint velocity and completion data
- **Optional**: Previous retrospective actions (to check closure)
- **Optional**: Team feedback or survey results

## Procedure

### Step 1: Gather Retrospective Data

Read available artifacts from the review period:
- STATUS-REPORT-*.md files for the period
- SPRINT-PLAN.md for planned vs actual
- BACKLOG.md for item flow and cycle times
- Previous RETRO-*.md for open action items

Extract key facts:
- Items planned vs completed
- Velocity trend
- Blockers encountered and resolution time
- Unplanned work that entered the sprint
- Open action items from previous retrospectives

**Expected:** Data summary with quantitative metrics (velocity, completion %, blocker count).

**On failure:** If no artifacts exist, base the retrospective on qualitative observations.

### Step 2: Structure "What Went Well"

List 3-5 things that worked well, with evidence:

```markdown
## What Went Well
| # | Observation | Evidence |
|---|------------|---------|
| 1 | [Specific positive observation] | [Metric, example, or artifact reference] |
| 2 | [Specific positive observation] | [Metric, example, or artifact reference] |
| 3 | [Specific positive observation] | [Metric, example, or artifact reference] |
```

Focus on practices to continue, not just outcomes. "Daily standups kept blockers visible" is more actionable than "We delivered on time."

**Expected:** 3-5 evidence-backed positive observations.

**On failure:** If nothing went well, look harder — even small wins matter. At minimum, the team completed the period.

### Step 3: Structure "What Needs Improvement"

List 3-5 things that need improvement, with evidence:

```markdown
## What Needs Improvement
| # | Observation | Evidence | Impact |
|---|------------|---------|--------|
| 1 | [Specific issue] | [Metric, example, or incident] | [Effect on delivery] |
| 2 | [Specific issue] | [Metric, example, or incident] | [Effect on delivery] |
| 3 | [Specific issue] | [Metric, example, or incident] | [Effect on delivery] |
```

Be specific and factual. "Estimation was off" is vague. "3 of 5 items exceeded estimates by >50%, adding 8 unplanned days" is actionable.

**Expected:** 3-5 evidence-backed improvement areas with stated impact.

**On failure:** If the team claims everything is fine, compare planned vs actual metrics — gaps reveal issues.

### Step 4: Generate Improvement Actions

For each improvement area, create an actionable item:

```markdown
## Improvement Actions
| ID | Action | Owner | Due Date | Success Criteria | Source |
|----|--------|-------|----------|-----------------|--------|
| A-001 | [Specific action] | [Name] | [Date] | [How to verify success] | Improvement #1 |
| A-002 | [Specific action] | [Name] | [Date] | [How to verify success] | Improvement #2 |
| A-003 | [Specific action] | [Name] | [Date] | [How to verify success] | Improvement #3 |
```

Each action must be:
- Specific (not "improve estimation" but "add estimation review step to grooming")
- Owned (one person accountable)
- Time-bound (due date within next 1-2 sprints)
- Verifiable (success criteria defined)

**Expected:** 2-4 improvement actions with owners and due dates.

**On failure:** If actions are too vague, apply the "how would you verify this was done?" test.

### Step 5: Review Previous Actions and Write Report

Check previous retrospective actions for closure:

```markdown
## Previous Action Review
| ID | Action | Owner | Status | Notes |
|----|--------|-------|--------|-------|
| A-prev-001 | [Action from last retro] | [Name] | Closed / Open / Recurring | [Outcome] |
| A-prev-002 | [Action from last retro] | [Name] | Closed / Open / Recurring | [Outcome] |
```

Flag recurring items (same issue appearing in 3+ retrospectives) — these need escalation or a different approach.

Write the complete retrospective:

```markdown
# Retrospective: [Sprint N / Phase Name / Date Range]
## Date: [YYYY-MM-DD]
## Document ID: RETRO-[PROJECT]-[YYYY-MM-DD]

### Period Summary
- **Period**: [Sprint N / dates]
- **Planned**: [N items / N points]
- **Completed**: [N items / N points]
- **Velocity**: [N] (previous: [N])
- **Unplanned Work**: [N items]

### What Went Well
[From Step 2]

### What Needs Improvement
[From Step 3]

### Improvement Actions
[From Step 4]

### Previous Action Review
[From Step 5]

---
*Retrospective facilitated by: [Name/Agent]*
```

Save as `RETRO-[YYYY-MM-DD].md`.

**Expected:** Complete retrospective document saved with actions, evidence, and previous action review.

**On failure:** If the retrospective has no improvement actions, it's not driving change — revisit Step 3.

## Validation

- [ ] Retrospective file created with date-stamped filename
- [ ] Period summary includes quantitative metrics
- [ ] "What Went Well" has 3-5 evidence-backed items
- [ ] "What Needs Improvement" has 3-5 evidence-backed items
- [ ] Improvement actions have owners, due dates, and success criteria
- [ ] Previous retrospective actions reviewed for closure
- [ ] Recurring issues flagged

## Common Pitfalls

- **Blame game**: Retrospectives review processes and practices, not people. Frame issues as systemic, not personal.
- **Actions without follow-through**: The biggest retrospective failure. Always review previous actions before creating new ones.
- **Too many actions**: 2-4 focused actions are better than 10 vague ones. The team can only absorb so many changes.
- **No evidence**: "We feel estimation is bad" is opinion. "3 of 5 items exceeded estimates by 50%" is data. Always attach evidence.
- **Skipping the positives**: Only discussing problems is demoralizing. Celebrating wins reinforces good practices.

## Related Skills

- `generate-status-report` — status reports provide the data for retrospectives
- `manage-backlog` — improvement actions feed back into the backlog
- `plan-sprint` — retrospective learnings improve sprint planning accuracy
- `draft-project-charter` — review charter assumptions and risk accuracy
- `create-work-breakdown-structure` — review estimation accuracy against WBS
