---
name: period-close
description: Plan and track month-end or quarter-end close tasks, timelines, dependencies, and process improvements.
---

## Close Activity Checklist

### Pre-Close Window (Final 2-3 Business Days of the Period)

- [ ] Distribute the close calendar with deadlines to every contributor
- [ ] Align cut-off procedures with AP, AR, payroll, and treasury teams
- [ ] Confirm all feeder systems (ERP modules, payroll platform, banking portals) are operating normally
- [ ] Perform a preliminary cash reconciliation covering all activity through the penultimate day
- [ ] Scan open purchase orders for items that may require an accrual
- [ ] Verify that the payroll processing schedule dovetails with the close timeline
- [ ] Gather details on any known non-routine transactions

### Day 1 After Period End (T+1)

- [ ] Verify that every subledger module has completed its period-end cycle
- [ ] Post AP accruals for received-not-invoiced goods and services
- [ ] Record payroll entries and any pay-period straddle accrual
- [ ] Capture all cash receipts and disbursements through the final day
- [ ] Post intercompany entries and obtain counterparty acknowledgment
- [ ] Finalize the bank reconciliation using the official month-end statement
- [ ] Execute the fixed-asset depreciation run
- [ ] Post the prepaid expense amortization schedule

### Day 2 (T+2)

- [ ] Complete revenue recognition entries and adjust contract liabilities
- [ ] Post all outstanding accrual journal entries
- [ ] Reconcile the AR subledger to the GL control account
- [ ] Reconcile the AP subledger to the GL control account
- [ ] Process inventory valuation adjustments (where applicable)
- [ ] Run foreign-currency remeasurement entries
- [ ] Begin balance-sheet account reconciliations

### Day 3 (T+3)

- [ ] Finish all balance-sheet reconciliations
- [ ] Post corrective entries surfaced during reconciliation
- [ ] Complete intercompany reconciliation and record elimination entries
- [ ] Produce a preliminary trial balance and income statement
- [ ] Conduct an initial comparative review of the income statement
- [ ] Research and resolve significant movements

### Day 4 (T+4)

- [ ] Record the income tax provision (current and deferred)
- [ ] Update the equity roll-forward (stock compensation, buybacks, dividends)
- [ ] Finalize every journal entry — declare soft close
- [ ] Generate draft financial statements (income statement, balance sheet, cash flow)
- [ ] Prepare detailed comparative commentary on all material line items
- [ ] Submit drafts for management review

### Day 5 (T+5)

- [ ] Incorporate any adjustments arising from management review
- [ ] Lock the financial statements — declare hard close
- [ ] Restrict the period in the ERP / general ledger
- [ ] Assemble and distribute the financial reporting package
- [ ] Refresh rolling forecasts and projections with actual results
- [ ] Conduct a close retrospective to capture improvement opportunities

## Dependency Architecture

### Layered Execution Model

Tasks are grouped into tiers where each tier's inputs depend on the prior tier's outputs:

```
TIER 1 — Independent (begin immediately at T+1):
  Cash transaction recording
  Bank statement retrieval
  Payroll processing & accrual
  Depreciation calculation
  Prepaid amortization
  AP accrual assembly
  Intercompany entry posting

TIER 2 — Requires Tier 1 outputs:
  Bank reconciliation (needs: cash entries + bank data)
  Revenue recognition (needs: billing & delivery data finalized)
  AR subledger reconciliation (needs: all revenue & cash postings)
  AP subledger reconciliation (needs: all AP activity & accruals)
  FX remeasurement (needs: all foreign-currency entries on the books)
  Remaining accrual entries (needs: complete source-data review)

TIER 3 — Requires Tier 2 outputs:
  Full balance-sheet reconciliations (needs: all entries posted)
  Intercompany reconciliation & eliminations (needs: both sides recorded)
  Corrective entries from reconciliation findings
  Preliminary trial balance extraction

TIER 4 — Requires Tier 3 outputs:
  Tax provision (needs: pre-tax income determined)
  Equity roll-forward
  Consolidation processing
  Draft financial statement generation
  Initial comparative analysis

TIER 5 — Requires Tier 4 outputs:
  Management review cycle
  Post-review corrections
  Hard close & period lock
  Reporting package assembly
  Forecast refresh
```

### Identifying the Critical Path

The longest dependent chain dictates minimum close duration. A representative critical path:

```
Cash/AP/AR posting -> Subledger reconciliations -> Balance-sheet recs ->
  Tax provision -> Draft statements -> Management review -> Hard close
```

**Strategies to compress the critical path:**
- Automate Tier 1 entries (depreciation, amortization, template accruals)
- Reconcile accounts continuously throughout the month instead of waiting for period end
- Execute independent reconciliations in parallel across team members
- Enforce firm submission deadlines with accountability for late items
- Standardize reconciliation templates to eliminate setup time each period

## Progress Tracking

### Close Dashboard Structure

| Task | Owner | Target Day | Current State | Blocker (if any) | Remarks |
|---|---|---|---|---|---|
| [Task name] | [Person] | T+N | Not Started / Active / Done / Blocked | [Description] | [Notes] |

### State Definitions

- **Not Started:** Awaiting prerequisite completion or scheduled start time
- **Active:** Work is underway
- **Done:** Completed and reviewed/approved
- **Blocked:** Cannot proceed — dependency unmet, data unavailable, or issue encountered
- **At Risk:** In progress but unlikely to meet its target date

### Daily Stand-Up Protocol (Recommended During Close)

Hold a focused 15-minute sync each day of the close window:

1. Walk the dashboard — call out any task not tracking to plan
2. Surface blockers and assign owners to resolve them
3. Redistribute work or escalate as needed
4. Reassess the overall timeline if any task slips

### Performance Metrics (Track Period Over Period)

| Metric | What It Measures | Goal |
|---|---|---|
| Total close duration | Business days from period end to hard close | Shorten over time |
| Post-soft-close adjustments | Entries added after the initial freeze | Drive toward zero |
| Missed deadlines | Tasks completed after their assigned day | Eliminate |
| Reconciliation exceptions | Items requiring investigation | Reduce over time |
| Post-close corrections | Errors discovered after the books are locked | Zero |

## Condensed Close Calendar (Standard 5-Day)

| Day | Primary Activities | Key Participants |
|---|---|---|
| T+1 | Cash postings, payroll, AP accruals, depreciation, prepaid amortization, intercompany entries | Staff accountants, payroll team |
| T+2 | Revenue entries, remaining accruals, AR/AP/FA subledger recs, FX remeasurement | Revenue accounting, AP/AR, treasury |
| T+3 | Balance-sheet recs, intercompany recs & eliminations, preliminary trial balance, initial variance review | Full accounting team, consolidation |
| T+4 | Tax provision, equity roll-forward, draft financials, detailed variance commentary, management review | Tax, controller, FP&A |
| T+5 | Final adjustments, hard close, period lock, reporting distribution, forecast update, retrospective | Controller, FP&A, finance leadership |

## Accelerated 3-Day Close

| Day | Activities |
|---|---|
| T+1 | All journal entries posted (automated + manual), all subledger recs, bank rec, intercompany rec, preliminary trial balance |
| T+2 | All balance-sheet recs, tax provision, consolidation, draft financials, comparative analysis, management review |
| T+3 | Final corrections, hard close, reporting package, forecast refresh |

**Enablers for a 3-day close:**
- Template-driven recurring entries fire automatically at period end
- Rolling reconciliation practices keep accounts current throughout the month
- Intercompany eliminations are system-generated
- Pre-close activities (accrual estimation, cut-off review) wrap up before the period ends
- Every task has a single accountable owner with minimal handoff
- Feeder systems integrate in real time or near-real time

## Continuous Improvement

### Diagnosing Common Bottlenecks

| Bottleneck | Underlying Cause | Countermeasure |
|---|---|---|
| Delayed AP accruals | Waiting on departmental spend confirmation | Move to continuous accrual estimation; enforce earlier cut-off deadlines |
| Manual recurring entries | Same entries rebuilt from scratch each month | Configure automated templates in the ERP |
| Protracted reconciliations | Full reconciliation attempted only at month end | Adopt rolling reconciliation during the period |
| Intercompany mismatches | Counterparty has not posted their side | Automate matching logic; impose tighter intercompany deadlines |
| Late management adjustments | Material issues surface only during final review | Strengthen preliminary review; empower the team to flag issues earlier |
| Missing documentation | Supporting files assembled after the fact | Collect evidence continuously, not just at close |

### Post-Close Retrospective Questions

After every close cycle, evaluate:
1. Which activities ran smoothly and should be preserved?
2. Where did elapsed time exceed expectations, and what caused the delay?
3. What impediments arose and how can they be prevented next period?
4. Were there unexpected results that could have been identified sooner?
5. What manual steps are candidates for automation before the next close?
