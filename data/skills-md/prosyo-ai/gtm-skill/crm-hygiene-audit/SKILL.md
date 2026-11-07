---
name: crm-hygiene-audit
description: "Use this skill when CRM data is messy and reports cannot be trusted: \"audit our CRM\", \"clean up our CRM data\", \"duplicates and missing fields\", \"why is our pipeline report wrong\". Checks duplicates, missing required fields, stale and past-due opportunities, ownership gaps, lifecycle stage errors, bad picklist values and unlinked records, quantifies each issue, ranks them by impact on reporting and selling, and produces a cleanup plan plus the rules that stop the mess coming back. Proposes changes for approval, never bulk-edits on its own."
license: MIT
metadata:
  title: CRM hygiene audit
  category: revops
  tags: "RevOps, Sales Leaders, Founders"
  author: prosyo
  version: "1.0.0"
  keywords: "crm data hygiene, crm cleanup checklist, crm audit, claude crm hygiene skill, duplicate records crm"
  inputs: "CRM exports of accounts contacts and deals, Required fields and stages, Reporting that matters"
  outputs: "Issue inventory with counts, Impact ranking, Cleanup plan, Prevention rules"
---

Use this when the pipeline report and reality disagree. It produces a ranked list of data problems, a cleanup plan and the rules that keep data clean afterwards.

## Inputs

- Exports of accounts, contacts and opportunities (or read access).
- The fields and stages the business relies on.
- The reports leadership uses, so impact can be judged.

## The play

### 1. Inventory issues
| Area | Check |
| --- | --- |
| Duplicates | Accounts by domain; contacts by email; similar names |
| Completeness | Required fields empty: industry, size, owner, lifecycle stage, source |
| Opportunities | Past close dates, no next step, no activity in 30 days, amount empty or zero, stage without required fields |
| Ownership | Records owned by former employees or unassigned |
| Lifecycle | Customers without closed-won deals; leads with won deals |
| Picklists | Free-text values where picklists should be; outdated values |
| Relationships | Contacts not linked to accounts; deals without contacts |
| Compliance | Opted-out contacts still in active sequences |

### 2. Quantify and rank
Count each issue and score impact: does it break forecasting, routing, outreach or compliance? Compliance and forecast issues come first.

### 3. Plan the cleanup
For each issue: the fix, who decides (some merges need a human), whether it can be done in bulk safely, and the order. Merges and deletions are proposed with a sample for approval, then run in batches with a backup export first.

### 4. Prevent recurrence
Required fields at stage changes, validation rules, duplicate checks on create, ownership reassignment when people leave, a monthly hygiene report.

## Output format

```
Health score: X/100
Issues (ranked): <issue - count - % of records - impact - fix - bulk-safe? - owner>
Cleanup plan: <week by week, with approval points>
Prevention: <rules to add>
Monthly report: <metrics to track>
```

## What good looks like

- Every issue has a count and an impact, not just "data is messy".
- Opt-out compliance issues are fixed first.
- The prevention rules are light enough that reps follow them.
- The common mistake is a one-time cleanup sprint with no rules, so the data is dirty again in a quarter.

## Rules

- MUST export a backup before any bulk change.
- MUST get approval with a sample before merges, deletions or bulk updates.
- MUST fix opted-out contacts in active sequences immediately.
- NEVER permanently delete records without explicit approval.

## Example prompts

- "Audit these CRM exports and tell me what's wrong, ranked by impact."
- "Our forecast is off every month. Check our opportunity data."
- "Write the hygiene rules and monthly report for our CRM."
