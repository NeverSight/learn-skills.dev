---
name: account-reconciliation
description: Reconcile accounts, ledgers, bank statements, subledgers, variances, and supporting schedules.
---

## Reconciliation Categories

### General Ledger vs. Subledger

Verify that each control account in the GL agrees with the sum of its underlying detail ledger.

**Accounts typically reconciled this way:**
- Trade receivables (GL control vs. AR aging schedule)
- Trade payables (GL control vs. AP aging schedule)
- Property, plant & equipment (GL control vs. asset register)
- Inventory (GL control vs. stock valuation report)
- Prepaid assets (GL control vs. amortization schedule)
- Accrued liabilities (GL control vs. accrual supporting schedules)

**Workflow:**
1. Extract the GL control account balance at the period cut-off
2. Generate the subledger detail or trial balance as of the identical date
3. Match the two totals — under real-time posting they should be identical
4. Research any gap (manual GL postings, pending interface batches, failed data transfers, reclassifications without subledger mirror)

**Typical root causes of discrepancy:**
- Journal entries booked directly to the control account without a subledger transaction
- Subledger batches queued but not yet transmitted to the GL
- Lag between batch processing windows
- GL reclassifications with no subledger counterpart
- Integration failures or rejected interface records

### Cash / Bank Reconciliation

Align the book cash balance with the financial institution's reported position.

**Workflow:**
1. Obtain the institution's closing statement balance
2. Pull the corresponding GL cash account balance at the same date
3. List checks written but not yet presented for payment
4. List deposits recorded in the books but not yet credited by the bank
5. Identify bank-initiated entries (fees, interest, returned items) absent from the GL
6. Derive an adjusted balance on each side; the two must agree

**Presentation template:**

```
Institution statement balance:          $XX,XXX
  Plus: Deposits not yet credited        $X,XXX
  Less: Unpresented checks             ($X,XXX)
  Plus/Less: Institution errors          $X,XXX
Adjusted institution balance:           $XX,XXX

Book (GL) balance:                      $XX,XXX
  Plus: Interest & credits unrecorded    $X,XXX
  Less: Fees & charges unrecorded      ($X,XXX)
  Plus/Less: Book errors                 $X,XXX
Adjusted book balance:                  $XX,XXX

Remaining variance:                     $0.00
```

### Intercompany Reconciliation

Confirm that receivables and payables between affiliated entities offset to zero for consolidation purposes.

**Workflow:**
1. Collect intercompany receivable and payable balances for every entity pair
2. Match Entity A's claim on Entity B against Entity B's corresponding obligation to Entity A
3. Investigate and resolve discrepancies
4. Verify that both sides have captured every intra-group transaction
5. Validate that consolidation elimination entries will net these balances cleanly

**Typical root causes of discrepancy:**
- One entity recorded the transaction while the other has not yet done so
- Entities applied different foreign exchange rates on the same transaction
- Amounts classified as intercompany by one party but as third-party by the other
- Contested charges or unapplied cash receipts
- Differing period-end cut-off conventions across subsidiaries

## Classifying Open Reconciling Items

### Class 1 — Timing Lags

Items arising from normal processing sequences that will self-clear without intervention:

- Checks issued and booked but awaiting bank presentment
- Deposits journalized but pending bank value-date credit
- Transactions posted in one system awaiting batch interface to the other
- Items sitting in an approval queue prior to final posting

**Expected outcome:** Resolution within the standard processing window (generally 1-5 business days). No corrective entry required.

### Class 2 — Corrective Action Needed

Items that demand a journal entry or other ledger adjustment:

- Bank-originated charges not yet reflected on the books (service fees, wire costs, NSF penalties)
- Interest income or expense recognized by the institution but absent from the GL
- Posting mistakes — wrong dollar amount, wrong account, or duplicate recording
- Transactions present in one system with no counterpart in the other
- Properly recorded amounts sitting in an incorrect GL account

**Expected outcome:** Prepare and post a correcting entry during the current or next available period.

### Class 3 — Investigation Required

Items lacking a clear explanation:

- Variances with no identifiable source
- Amounts in dispute between internal parties or with external counterparties
- Stale items that have exceeded their expected clearance window
- Persistent differences of the same type reappearing period after period

**Expected outcome:** Perform root-cause analysis, document findings, and escalate when resolution is not straightforward.

## Aging and Monitoring of Open Items

Track every unresolved reconciling item by age to surface those requiring management attention:

| Age Band | Classification | Required Response |
|---|---|---|
| 0-30 days | Current | Routine monitoring — within normal processing window |
| 31-60 days | Maturing | Active follow-up — determine why the item has not cleared |
| 61-90 days | Past due | Supervisor notification with documented investigation |
| Over 90 days | Stale | Management escalation — evaluate write-off or forced adjustment |

### Item-Level Tracking Register

| Seq | Description | Amount | Origination Date | Days Open | Class | Resolution Status | Assigned To |
|---|---|---|---|---|---|---|---|
| 1 | [Detail] | $X,XXX | [Date] | XX | [Type] | [Status] | [Name] |

### Trend Monitoring

Evaluate the reconciling-item population across periods to detect deterioration:

- Compare the aggregate dollar value of open items to the prior period
- Flag when total open items exceed the account's materiality benchmark
- Flag when the count of open items grows for two or more consecutive periods
- Investigate chronic items that appear in every reconciliation (signal of a systemic process gap)

## Escalation Governance

Establish triggers proportional to organizational risk appetite:

| Condition | Illustrative Threshold | Escalation Path |
|---|---|---|
| Single-item dollar value | Above $10,000 | Supervisor review |
| Single-item dollar value | Above $50,000 | Controller review |
| Aggregate open items | Above $100,000 | Controller review |
| Item age | Over 60 days | Supervisor follow-up |
| Item age | Over 90 days | Controller / senior management review |
| Unresolved net difference | Any amount | Period cannot close — must resolve or formally document |
| Worsening trend | Three or more consecutive periods | Initiate process-improvement project |

*Calibrate thresholds to match the entity's materiality level and control environment.*

## Operating Principles

1. **Cadence discipline:** Finish every reconciliation within the close calendar window (commonly T+3 to T+5 after period end)
2. **Coverage:** Reconcile every balance sheet account on a defined cycle — monthly for material balances, quarterly for immaterial ones
3. **Audit trail:** Each reconciliation must identify the preparer, reviewer, completion date, and a narrative for every open item
4. **Separation of duties:** The reconciler should not be the person who initiates or approves transactions in the same account
5. **Closure rigor:** Carry open items forward only with active follow-up; never allow perpetual rollover without investigation
6. **Systemic fixes:** When the same reconciling item type recurs, address the upstream process rather than repeatedly clearing symptoms
7. **Uniform format:** Employ standardized templates and naming conventions across all accounts and business units
8. **Record keeping:** Retain completed reconciliations and all supporting evidence in accordance with the organization's document-retention policy
