---
name: pipeline-review
description: "Use this skill when a manager or founder needs to review the sales pipeline and forecast: \"review my pipeline\", \"prep for the forecast call\", \"which deals are at risk\", \"is our quarter going to land\". Checks pipeline coverage, stage health, deal aging, slipped close dates, missing next steps and single-threaded deals, scores every deal's risk with evidence, and produces a forecast (commit, best case, upside) with the actions that change the outcome this week."
license: MIT
metadata:
  title: Pipeline review
  category: deals
  tags: "Sales Leaders, Founders, RevOps"
  author: prosyo
  version: "1.0.0"
  keywords: "sales pipeline review template, forecast call prep, deal risk analysis, claude pipeline review skill, pipeline coverage"
  inputs: "Pipeline export with stages amounts and dates, Activity history, Quota"
  outputs: "Coverage and health summary, Deal risk table, Forecast, Actions this week"
---

Use this weekly or before a forecast call. It turns a pipeline export into an honest forecast and a short list of actions that move the number.

## Inputs

- Pipeline export: deal, owner, stage, amount, close date, created date, last activity, next step, contacts.
- Quota or target for the period and what has closed so far.
- Historical stage conversion rates if available.

## The play

### 1. Check coverage
Open pipeline due this period ÷ remaining target. Healthy coverage depends on win rate; at a 25% win rate, 3-4x is typical. Read [references/pipeline-health.md](references/pipeline-health.md) for the health checks, thresholds and the risk scoring table.

### 2. Run the health checks
- **Aging**: deals in a stage longer than 1.5x the average for that stage.
- **Slips**: close date moved 2+ times.
- **No next step**: no future activity scheduled.
- **Stale**: no activity in 14+ days.
- **Single-threaded**: one contact engaged.
- **Close date in the past**.
- **Stage mismatch**: proposal stage without an economic buyer met.

### 3. Score deal risk
Each failing check adds risk points. High-risk deals in commit move to best case or out, with the reason.

### 4. Build the forecast
| Category | Rule |
| --- | --- |
| Commit | Low risk, verbal yes or clear paper process, close date backed by a plan |
| Best case | Medium risk, strong engagement, one open gap |
| Upside | Early or high risk |
| Remove | Dead, past due with no response, or no next step for 30 days |

Weighted forecast = commit + (best case × historical conversion).

### 5. Choose the actions
Three to five actions that change the quarter: a deal that needs an executive call, a stalled proposal, a missing champion, pipeline generation if coverage is short.

## Output format

```
Target: X | Closed: X | Gap: X | Coverage: Nx (healthy / thin)
Forecast: Commit X | Best case X | Upside X | Weighted X
Risks: <deal - risk score - failing checks - recommendation>
Actions this week: <action - owner - expected impact>
Pipeline hygiene: N deals with past close dates, N without next steps
```

## What good looks like

- Every deal moved out of commit has a stated reason.
- The forecast says what would need to be true for best case to land.
- Actions are specific, owned and dated.
- The common mistake is reviewing deals by amount only; a small deal with a signed order form matters more for the forecast than a big deal with no economic buyer.

## Rules

- MUST base risk on evidence (activity, dates, contacts), not on rep confidence.
- MUST flag past-due close dates and missing next steps.
- NEVER change records in the CRM without approval; propose updates instead.

## Example prompts

- "Here's our pipeline export. Prep me for Monday's forecast call."
- "Which of my 30 open deals are most at risk this quarter?"
- "We need $400k more this quarter. Is the pipeline enough, and what should we do?"
