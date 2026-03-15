---
name: hillchart
description: "Hillchart: visualize project progress by analyzing the codebase"
disable-model-invocation: true
---

# Hillchart: visualize project progress by analyzing the codebase

When the user types `/hillchart` and references a project, do the following:

## 1) Load the project artifacts (required)

- Read the plan at `projects/<domain-name>/<project-name>/plan.md`
- Read the shaping doc at `projects/<domain-name>/<project-name>/shaping.md` (if exists)
- Read all task files in `projects/<domain-name>/<project-name>/tasks/`
- Identify scopes and their expected deliverables
- **Check for open PRs** related to the project (see step 3a)

## 2) Extract expected artifacts from the plan

For each scope, extract:

- **Models**: class names mentioned (e.g., `StripePayout`, `StripePayoutItem`)
- **Migrations**: expected table names
- **Jobs**: Sidekiq/background job class names
- **Services**: service class names and paths
- **Controllers**: controller names and actions
- **GraphQL**: types, queries, mutations mentioned
- **Feature flags**: flag names (e.g., `payments_deposit_reconciliation_enabled`)
- **Views/UI**: view paths or React component names
- **Tests**: expected spec file paths

## 3) Search codebase for signals

For each expected artifact, search for existence and completeness:

### Uphill signals (0–50%: "Figuring it out")

| Signal | Search pattern | Weight |
|--------|----------------|--------|
| Spike exists | `projects/<domain>/<project>/spike/` has files | +10% |
| Migration drafted | `db/migrate/*<table_name>*` exists | +10% |
| Model file exists but minimal | Model file < 20 lines or no validations | +5% |
| Tests pending/skipped | `pending`, `skip`, `xit`, `xdescribe` in specs | -10% from 50% |
| TODOs in feature code | `TODO`, `FIXME`, `WIP` in feature paths | -5% per occurrence (max -15%) |
| Empty method bodies | `def.*\n\s*end` or `raise NotImplementedError` | -10% |
| Feature flag defined only | Flag in registry but no enforcement | +5% |
| **Draft PR exists** | Open PR with "Draft" status or WIP label | +10% (active exploration) |
| **PR with failing CI** | Open PR but CI checks failing | +5% (code exists but not working) |

### Downhill signals (50–100%: "Making it happen")

| Signal | Search pattern | Weight |
|--------|----------------|--------|
| Model implemented | Model exists with associations/validations | +10% |
| Service implemented | Service class with non-trivial logic | +10% |
| Job implemented | Job class with `perform` method | +10% |
| Controller actions exist | Expected actions defined | +10% |
| Feature flag enforced | Flag checked in controller/resolver/view | +10% |
| Tests exist and not pending | Spec files without `pending`/`skip` | +15% |
| Observability in place | `StatsD`, metrics, structured logging | +5% |
| No TODOs remaining | Zero `TODO`/`FIXME` in feature paths | +5% |
| Task checkboxes complete | `- [x]` count / total checkboxes | +10% × ratio |
| **PR approved and CI passing** | `gh pr view` shows approvals + green CI | +15% |
| **PR merged recently** | PR for scope merged in last 7 days | +10% (confirms completion) |

### Task file parsing (highest fidelity signal)

Parse `projects/<domain-name>/<project-name>/tasks/*.md` for:

```markdown
- [x] Completed item   → counts as done
- [ ] Incomplete item  → counts as remaining
```

Calculate: `scope_progress = completed_checkboxes / total_checkboxes × 100`

This is the primary signal when task files exist and are maintained.

### 3a) Check open Pull Requests for in-progress work

Use GitHub CLI to find open PRs related to the project:

```bash
# Search for open PRs by project name, scope names, or feature flag names
gh pr list --state open --search "<project_name> OR <scope_name> OR <feature_flag>"

# For each open PR, get details:
gh pr view <pr_number> --json title,body,labels,reviews,commits,additions,deletions,changedFiles,createdAt,updatedAt
```

#### PR signals to evaluate:

| Signal | Interpretation | Weight |
|--------|----------------|--------|
| Open PR exists for scope | Active work in progress | +10% toward 50% |
| PR has "WIP" or "Draft" label | Early stage, still figuring out | Caps progress at 45% |
| PR has passing CI checks | Code is functional | +10% |
| PR has failing CI checks | Work blocked or incomplete | -10% |
| PR has approving reviews | Ready to merge, nearly complete | +15% |
| PR has changes requested | Needs rework | -5% |
| PR is stale (no updates > 7 days) | Potentially stuck | ⚠ Flag for attention |
| PR linked to task file checkboxes | High-fidelity correlation | Use PR status for that checkbox |
| Multiple open PRs for same scope | Parallel work streams | Report all, don't double-count |

#### How to match PRs to scopes:

1. **Title/branch matching**: PR title or branch contains scope name (e.g., `stripe-sync`, `admin-ui`)
2. **File path matching**: PR changes files in expected paths from the plan
3. **Commit message matching**: Commits reference scope name or task file path
4. **Label matching**: PR has labels matching project or scope name
5. **Body matching**: PR description references the project plan or task file

#### PR summary in output:

```
Open PRs:
  🔄 #1234 "Add StripePayout model and migration" (Scope 1)
     Status: Draft, CI passing, 0 reviews
     Last updated: 2 days ago
     Files: app/models/stripe_payout.rb, db/migrate/...
  
  🔄 #1235 "Implement SyncStripePayoutsJob" (Scope 2)
     Status: Ready for review, CI passing, 1 approval
     Last updated: 4 hours ago
     Files: app/jobs/payments/sync_stripe_payouts_job.rb, spec/...
  
  ⚠️ #1230 "Add admin payout reconciliation UI" (Scope 3)
     Status: Changes requested, CI failing
     Last updated: 8 days ago (STALE)
     Files: app/frontend/src/views/payments/...
```

## 4) Calculate hill position for each scope

```
hill_position = base_position + uphill_signals + downhill_signals

where:
  base_position = 0% (no artifacts) or 25% (spike exists) or 50% (core implemented)
  
  Uphill (0–50%):
    - Spike/exploration only: 10–25%
    - Schema/models drafted: 25–40%
    - Core logic stubbed, tests failing: 40–50%
  
  Downhill (50–100%):
    - Core logic works, tests passing: 50–65%
    - Integration complete, UI functional: 65–80%
    - Polish, error handling, observability: 80–95%
    - All checkboxes complete, ready to ship: 95–100%
```

## 5) Render the hill chart

Output an ASCII hill chart with scope positions:

```
Hill Chart: bank-deposit-reconciliation
Generated: 2026-01-06 14:30 UTC

              .-------------------.
             /                     \
            /                       \
           /      ③                  \
          /                       ②   \
         /   ①                         \
        /                               \
       '--------------------------------'
       0%            50%            100%
       ← Figuring out | Making it happen →

┌─────┬──────────────────────────────┬──────────┬───────────┐
│ Pos │ Scope                        │ Progress │ Direction │
├─────┼──────────────────────────────┼──────────┼───────────┤
│  ①  │ Spike & data model           │    35%   │     ↗     │
│  ②  │ Stripe sync job              │    78%   │     ↘     │
│  ③  │ Admin UI                     │    55%   │     ↘     │
└─────┴──────────────────────────────┴──────────┴───────────┘

Key signals detected:
  ✓ Feature flag `payments_deposit_reconciliation_enabled` defined
  ✓ StripePayout model exists (45 lines, has associations)
  ✓ SyncStripePayoutsJob exists with perform method
  ⚠ 3 TODOs found in app/services/payments/stripe/
  ✗ No specs found for StripePayout model
  ✗ Feature flag not enforced in any controller

Open PRs (3):
  🔄 #1234 "Add StripePayout model" → Scope 1 (Draft, CI ✓)
  ✅ #1235 "Implement sync job" → Scope 2 (Approved, CI ✓, ready to merge)
  ⚠️ #1230 "Admin UI" → Scope 3 (Changes requested, stale 8d)
```

## 6) Provide actionable insights

After the chart, suggest:

- **Stuck uphill?** Identify blocking unknowns or missing decisions
- **Sliding back?** Flag new TODOs or failing tests since last check
- **Ready to ship?** Confirm all checkboxes complete, no blockers

Example:

```
Recommendations:
  
  Scope 1 (35% ↗): Uphill, still figuring it out
    → Missing: specs for StripePayout model
    → Blocker: Stripe API pagination strategy not decided (see rabbit hole #3)
    → PR #1234 is draft - consider marking ready for review once spike complete
  
  Scope 2 (78% ↘): Downhill, making progress
    → Remaining: 2 TODOs in sync_payouts.rb
    → Next: Add observability metrics
    → PR #1235 approved and ready - merge to complete scope
  
  Scope 3 (55% ↘): Just crossed the hill
    → Remaining: UI components not started
    → Dependencies: Blocked on Scope 2 completion
    → ⚠️ PR #1230 stale for 8 days - needs attention or should be closed
```

## 7) Optional: track progress over time

If the user wants historical tracking:

- Append a timestamped entry to `projects/<domain-name>/<project-name>/hillchart-history.md`
- Show trend arrows based on previous position
- Detect stalls (no movement in N days)

```markdown
## Hill Chart History

| Date       | Scope 1 | Scope 2 | Scope 3 |
|------------|---------|---------|---------|
| 2026-01-06 |   35%   |   78%   |   55%   |
| 2026-01-03 |   25%   |   65%   |   40%   |
| 2026-01-01 |   10%   |   50%   |   20%   |
```

## Configuration (optional)

Users can add a `projects/<domain-name>/<project-name>/hillchart.yml` to customize:

```yaml
# Override artifact detection
artifacts:
  models:
    - StripePayout
    - StripePayoutItem
  jobs:
    - SyncStripePayoutsJob
  feature_flags:
    - payments_deposit_reconciliation_enabled

# Override file paths to search
search_paths:
  - app/models/stripe_payout*.rb
  - app/jobs/payments/
  - app/services/payments/stripe/

# Weight adjustments
weights:
  task_checkboxes: 0.5    # Primary signal
  code_artifacts: 0.25    # Secondary signal
  code_quality: 0.1       # Tertiary signal
  pr_status: 0.15         # PR-based signals

# PR detection settings
pr_search:
  # Additional search terms for finding related PRs
  terms:
    - bank-deposit
    - stripe-payout
    - reconciliation
  # Labels that indicate project PRs
  labels:
    - payments
    - reconciliation
  # Authors to filter by (optional)
  authors: []
  # Consider PRs stale after N days without updates
  stale_threshold_days: 7
```

## Example usage

```
/hillchart bank-deposit-reconciliation
```

Or with options:

```
/hillchart bank-deposit-reconciliation --save-history --verbose
```
