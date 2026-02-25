---
name: status-report-generator
description: Project status report generation from git history, task context, and milestone tracking. Use when creating weekly updates, sprint reviews, stakeholder reports, or project dashboards.
---

# Status Report Generator

Structured frameworks for generating project status reports from code activity, task systems, and milestone tracking.

## Status Report Structure

### Standard Report Sections

```
STATUS REPORT OUTLINE:

1. TL;DR (3-5 bullets)
   - What was accomplished
   - What's in progress
   - What's blocked or at risk
   - Key decision needed (if any)

2. STATUS INDICATOR
   - Overall: GREEN / YELLOW / RED
   - Schedule: on track / at risk / behind
   - Scope: stable / expanding / contracting
   - Budget: on track / at risk / over (if applicable)

3. ACCOMPLISHMENTS (completed this period)
   - Bullet list with links to PRs/tickets
   - Grouped by workstream or milestone
   - Include metrics where possible

4. IN PROGRESS (active work)
   - Current tasks and expected completion
   - Progress indicators (% or status)
   - Owner for each item

5. BLOCKERS AND RISKS
   - Active blockers with escalation status
   - Emerging risks with mitigation plans
   - Dependencies on other teams

6. UPCOMING (next period)
   - Planned work for next sprint/week
   - Key milestones approaching
   - Decisions needed

7. METRICS (if applicable)
   - Velocity / throughput
   - Quality indicators (bugs, incidents)
   - Business metrics impact
```

## Data Extraction Methods

### From Git History

```
GIT DATA FOR STATUS REPORTS:

COMMITS THIS PERIOD:
git log --since="1 week ago" --oneline --no-merges

COMMITS BY AUTHOR:
git shortlog --since="1 week ago" -sn --no-merges

FILES CHANGED:
git diff --stat HEAD~{n}..HEAD

MERGED PRs (GitHub):
gh pr list --state merged --search "merged:>=2025-01-01"

PR SUMMARY:
gh pr list --state merged --json title,author,mergedAt,url \
  --jq '.[] | "- \(.title) (@\(.author.login)) \(.url)"'

OPEN PRs:
gh pr list --state open --json title,author,url \
  --jq '.[] | "- \(.title) (@\(.author.login)) \(.url)"'

RELEASE NOTES:
git log --since="1 week ago" --pretty=format:"- %s" --no-merges \
  | grep -E "^- (feat|fix|refactor|perf):"
```

### From Task Systems

```
TASK DATA EXTRACTION:

JIRA (via API or CLI):
- Tickets moved to "Done" this sprint
- Tickets currently "In Progress"
- Tickets in "Blocked" status
- Story points completed vs planned

GITHUB ISSUES:
gh issue list --state closed --search "closed:>=2025-01-01"
gh issue list --state open --label "in-progress"
gh issue list --state open --label "blocked"

LINEAR (via API):
- Completed issues this cycle
- In-progress issues
- Blocked issues with reason
- Cycle velocity metrics

GENERIC EXTRACTION TEMPLATE:
| Ticket | Title | Status | Owner | Notes |
|--------|-------|--------|-------|-------|
|        |       |        |       |       |
```

### Automated Report Generation

```
REPORT GENERATION SCRIPT APPROACH:

1. PULL DATA
   - Git log for the period
   - PR merge data
   - Issue/ticket status
   - CI/CD metrics (build success rate, deploy count)

2. CATEGORIZE
   - Group commits by type (feat, fix, refactor, etc.)
   - Group issues by milestone or epic
   - Identify blockers from issue labels

3. SUMMARIZE
   - Count: X features shipped, Y bugs fixed, Z PRs merged
   - Highlight: biggest wins and remaining risks
   - Metrics: velocity, cycle time, throughput

4. FORMAT
   - Apply template for audience (exec, team, detailed)
   - Add status indicators (RAG)
   - Include links to source data

OUTPUT FORMATS:
- Markdown (for Slack, GitHub, internal docs)
- HTML (for email)
- PDF (for stakeholder presentations)
```

## RAG Status Framework

### Status Definitions

| Color | Meaning | Criteria | Action Required |
| --- | --- | --- | --- |
| **GREEN** | On Track | Milestones on schedule, no blockers, metrics healthy | Continue as planned |
| **YELLOW** | At Risk | Minor delays, emerging risks, metrics declining | Monitor closely, mitigation plan |
| **RED** | Off Track | Milestones missed, active blockers, critical metrics failing | Immediate escalation, intervention |

### RAG Assessment Matrix

```
ASSESS EACH DIMENSION:

SCHEDULE:
  GREEN:  All milestones on track or ahead
  YELLOW: 1-2 items slipping, recoverable within sprint
  RED:    Major milestone at risk, recovery plan needed

SCOPE:
  GREEN:  Scope stable, requirements clear
  YELLOW: Minor scope additions, managed through backlog
  RED:    Significant scope creep, re-prioritization needed

QUALITY:
  GREEN:  Bug rate normal, test coverage stable, no incidents
  YELLOW: Bug rate elevated, test gaps identified
  RED:    Critical bugs in production, quality declining

TEAM:
  GREEN:  Team capacity sufficient, morale good
  YELLOW: Key person risk or capacity constraints
  RED:    Critical staffing gap, team burnout risk

OVERALL STATUS = worst dimension status
(If any dimension is RED, overall is RED)
```

### Status Change Triggers

```
GREEN → YELLOW TRIGGERS:
- Sprint velocity drops > 20% from average
- Blocker unresolved for > 2 business days
- Unplanned work exceeds 30% of sprint capacity
- Key dependency delayed by partner team
- New risk identified without mitigation plan

YELLOW → RED TRIGGERS:
- Milestone will be missed by > 1 week
- Critical path blocked with no workaround
- Stakeholder escalation required
- Team capacity < 70% of planned
- Quality metrics below acceptable threshold
```

## Stakeholder-Appropriate Detail Levels

### Executive Summary (C-Level / VP)

```
EXECUTIVE STATUS REPORT:

Format: 1 page max, bullet points, RAG indicators
Frequency: Weekly or biweekly
Audience: VP+, C-suite, board

TEMPLATE:

PROJECT: [Name]
PERIOD:  [Date Range]
STATUS:  [GREEN / YELLOW / RED]

HIGHLIGHTS:
- [Biggest win / accomplishment]
- [Key metric improvement]
- [Important milestone reached]

RISKS:
- [Top risk + mitigation status]
- [Second risk if applicable]

DECISIONS NEEDED:
- [Specific ask with options and recommendation]

NEXT MILESTONE: [What] by [When]
CONFIDENCE: [High / Medium / Low]
```

### Team Status (Engineering / Product)

```
TEAM STATUS REPORT:

Format: 1-2 pages, moderate detail, links to tickets
Frequency: Weekly (or per sprint)
Audience: Engineering team, product managers, designers

TEMPLATE:

SPRINT: [Number] | [Date Range]
VELOCITY: [X] points / [Y] planned ([Z]%)

COMPLETED:
- [Feature/Fix] - [PR #link] (@owner)
- [Feature/Fix] - [PR #link] (@owner)
- [Feature/Fix] - [PR #link] (@owner)

IN PROGRESS:
- [Task] - [X]% complete - ETA [date] (@owner)
- [Task] - [X]% complete - ETA [date] (@owner)

BLOCKED:
- [Task] - Blocked by [reason] - Escalated to [who]

BUGS:
- [X] new bugs filed
- [Y] bugs fixed
- [Z] bugs remaining (P0: _, P1: _, P2: _)

CARRY-OVER:
- [Task not completed] - Reason: [why] - New ETA: [date]

NEXT SPRINT PLAN:
- [Planned item 1]
- [Planned item 2]
- [Planned item 3]

RETRO NOTES:
- What went well: [brief]
- What to improve: [brief]
```

### Detailed Technical Report

```
DETAILED STATUS REPORT:

Format: 2-4 pages, full technical detail
Frequency: Per sprint or biweekly
Audience: Tech leads, architects, senior engineers

TEMPLATE:

ARCHITECTURE / INFRASTRUCTURE:
- Changes deployed: [list]
- Performance impact: [metrics]
- Incidents: [count, severity, resolution]

CODE METRICS:
- PRs merged: [count]
- Avg review time: [hours]
- Test coverage: [current] (delta: [+/-X%])
- Build success rate: [%]
- Deploy frequency: [count this period]
- Mean time to recovery: [hours/minutes]

TECHNICAL DEBT:
- Debt added: [items]
- Debt resolved: [items]
- Net debt trend: [increasing/decreasing/stable]

DEPENDENCY UPDATES:
- [Package] updated from [v1] to [v2] - [reason]
- [Security patch] applied - [CVE reference]

PERFORMANCE:
- p50 latency: [Xms] (target: [Yms])
- p95 latency: [Xms] (target: [Yms])
- Error rate: [X%] (target: < [Y%])
- Uptime: [X%] (target: [Y%])
```

## Sprint Review Template

```
SPRINT REVIEW:

SPRINT: [Number]
DATES:  [Start] - [End]
GOAL:   [Sprint goal statement]

GOAL ACHIEVED: [Yes / Partially / No]

DEMO ITEMS:
1. [Feature] - Demonstrated by [@person]
   - What it does: [brief description]
   - Why it matters: [user/business impact]
   - Status: [shipped / ready to ship / needs polish]

2. [Feature] - Demonstrated by [@person]
   - What it does: [brief description]
   - Why it matters: [user/business impact]
   - Status: [shipped / ready to ship / needs polish]

METRICS:
- Planned: [X] points across [Y] tickets
- Completed: [X] points across [Y] tickets
- Completion rate: [Z%]
- Carry-over: [X] tickets ([reason])

STAKEHOLDER FEEDBACK:
- [Feedback item 1]
- [Feedback item 2]

SPRINT HEALTH:
| Dimension | Status | Notes |
|-----------|--------|-------|
| Velocity  |  /  / |       |
| Quality   |  /  / |       |
| Scope     |  /  / |       |
| Morale    |  /  / |       |
```

## Milestone Tracking

### Milestone Dashboard Template

```
PROJECT MILESTONES:

Milestone           Target Date   Status    Confidence
────────────────────────────────────────────────────────
Alpha release        [date]        [RAG]     [H/M/L]
Beta release         [date]        [RAG]     [H/M/L]
Feature freeze       [date]        [RAG]     [H/M/L]
QA complete          [date]        [RAG]     [H/M/L]
Launch               [date]        [RAG]     [H/M/L]

KEY DEPENDENCIES:
- [Milestone X] depends on [Team Y] completing [Task Z] by [Date]
- [Milestone A] depends on [External vendor] delivering [Thing] by [Date]

CRITICAL PATH:
[Task 1] → [Task 2] → [Task 3] → [Launch]
         ↗ [Task 4] ↗
```

### Burn-Down Narrative

```
BURN-DOWN SUMMARY:

PLANNED: [X] story points for this milestone
COMPLETED: [Y] story points ([Z]% of planned)
REMAINING: [W] story points
DAYS LEFT: [N] days

VELOCITY (last 3 sprints): [A], [B], [C] = avg [D] points/sprint
SPRINTS REMAINING: [M]
PROJECTED COMPLETION: [points remaining / avg velocity] = [N] sprints

AT CURRENT VELOCITY:
- Will complete [on time / X days early / X days late]
- Confidence: [HIGH / MEDIUM / LOW]

IF BEHIND:
- Option A: Reduce scope by [X] points (cut [features])
- Option B: Add [X] capacity (hire/borrow)
- Option C: Extend deadline by [X] days
- Recommendation: [which option and why]
```

## Risk and Blocker Escalation

### Blocker Escalation Format

```
BLOCKER REPORT:

BLOCKER: [Clear description of what is blocked]
IMPACT:  [What work cannot proceed]
OWNER:   [Who is responsible for resolving]
STATUS:  [New / Escalated / In Progress / Resolved]
AGE:     [Days since identified]

ROOT CAUSE: [Why this is blocked]
ATTEMPTED: [What has been tried]
NEEDED:    [Specific action or decision needed]
FROM:      [Who needs to act]
BY:        [Date needed to avoid milestone impact]

ESCALATION PATH:
Day 1:   Raised with team lead
Day 2:   Escalated to manager
Day 3+:  Escalated to director/VP
Day 5+:  Executive escalation
```

### Risk Register Template

| Risk | Likelihood | Impact | Severity | Mitigation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| [Description] | H/M/L | H/M/L | [LxI] | [Plan] | [Name] | [Open/Mitigated] |

```
SEVERITY MATRIX:

              LOW Impact   MED Impact   HIGH Impact
HIGH Likely:  MEDIUM       HIGH         CRITICAL
MED Likely:   LOW          MEDIUM       HIGH
LOW Likely:   LOW          LOW          MEDIUM

CRITICAL: Immediate action, executive visibility
HIGH:     Active mitigation required this sprint
MEDIUM:   Monitor, mitigation plan documented
LOW:      Accept, review quarterly
```

## Status Report Quality Checklist

| Check | Status |
| --- | --- |
| TL;DR section is standalone and actionable | [ ] |
| RAG status is honest (not optimistic) | [ ] |
| Accomplishments link to PRs/tickets (verifiable) | [ ] |
| Blockers include escalation status and owner | [ ] |
| Risks have mitigation plans | [ ] |
| Metrics are compared to targets (not just reported) | [ ] |
| Next steps are specific with owners and dates | [ ] |
| Detail level matches audience | [ ] |
| Report is concise (executive: 1 page, team: 2 pages) | [ ] |
| Decisions needed are clearly framed with options | [ ] |

## Status Report Anti-Patterns

```
COMMON STATUS REPORT FAILURES:

1. ALL GREEN SYNDROME
   Problem: Everything is green until it's suddenly red
   Fix: Be honest about yellow early; it builds trust

2. ACTIVITY OVER OUTCOMES
   Problem: "We merged 47 PRs" (so what?)
   Fix: "Shipped checkout v2, reducing cart abandonment 12%"

3. BURIED BAD NEWS
   Problem: Blockers mentioned in paragraph 4 of page 3
   Fix: TL;DR section with clear blocker callout

4. NO DECISIONS SECTION
   Problem: Report is informational but doesn't drive action
   Fix: Always include "Decisions Needed" if any exist

5. STALE RISKS
   Problem: Same risks listed for 6 months with no updates
   Fix: Update risk status every report; close resolved ones

6. INCONSISTENT FORMAT
   Problem: Different format each week, hard to compare
   Fix: Use the same template; consistency enables trend spotting
```

## See Also

- [Codebase Documenter](../codebase-documenter/SKILL.md)
- [Document Skills: DOCX](../document-skills/docx/SKILL.md)
- [Product Management](../product-management/SKILL.md)
- [Finance](../finance/SKILL.md)
