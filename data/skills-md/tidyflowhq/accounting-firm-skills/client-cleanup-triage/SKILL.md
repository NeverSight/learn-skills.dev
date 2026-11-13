---
name: client-cleanup-triage
description: Assesses a messy new or prospective client's books, scores how bad the cleanup really is, and drafts a scoped cleanup proposal; use for messy books, QuickBooks or Xero cleanup, catch-up or rescue bookkeeping, unreconciled accounts, undeposited funds problems, taking over from a previous bookkeeper, or pricing a cleanup job.
---
# Client Cleanup Triage

## When to use this
- A prospect says their books are "a little behind" (they are usually more than a little behind).
- You are taking over from a previous bookkeeper and need to know what you are inheriting.
- Tax prep revealed a balance sheet that does not tie to anything.
- You need to price a catch-up or cleanup engagement without guessing.

## What to gather first
Ask the user for:
1. Country (US/AU/NZ/UK/CA) and accounting software (QuickBooks Online, Xero, MYOB, desktop file, spreadsheets).
2. What access exists: read-only login, or exported reports. The most useful reports: Balance Sheet (all dates and as of last year-end), A/R and A/P aging, reconciliation reports per account, and the audit log/history.
3. The period involved (when were the books last known to be right, usually the last filed tax return).
4. Why the client thinks they need help, in their words.
5. Who kept the books before (owner, family member, prior bookkeeper) and whether that person is still reachable.
6. Whether a tax deadline is driving the timeline.

Do not proceed to scoring on vibes alone; if reports are not available, the first deliverable is the request list for them.

## Workflow
1. Run the diagnostic question list. Answer from reports where possible and ask the client for the rest:
   - Last reconciled date for every bank account and credit card. "Never" is an answer and it matters.
   - Count of uncategorized transactions (Uncategorized Income/Expense, Ask My Accountant, suspense accounts).
   - Undeposited funds (or payments clearing account) balance, and how old it is.
   - Negative balances anywhere on the balance sheet: negative cash, negative AR or AP, negative loan balances, negative payroll liabilities.
   - Payroll liabilities reasonableness: the balance should look like roughly one pay period's withholdings, not months of buildup or a negative.
   - Sales tax / GST filings status: are filings current, and does the liability account roughly agree with what was filed (BAS lodgments in AU).
   - Loan balances in the GL vs lender statements.
   - AR/AP aging quality: stale invoices nobody will collect, unapplied credits, junk balances.
   - Opening Balance Equity: a nonzero balance means a conversion or setup was never finished.
   - Retained earnings for closed years changed since the last tax return? Someone has been editing closed periods.
2. Score severity with this rubric (worst area drags the whole file up a tier):
   - **Light tidy-up**: reconciliations 1-2 months behind, under ~100 uncategorized transactions, undeposited funds near zero, no negative balances, payroll and sales tax current. Days of work.
   - **Standard cleanup**: 3-12 months unreconciled, hundreds of uncategorized transactions, aged undeposited funds, one or two negative balances, a filing behind. Weeks of work with a defined end.
   - **Forensic-level**: over a year unreconciled or never reconciled, balance sheet unreliable (multiple negatives, Opening Balance Equity abuse, edited closed periods), payroll or sales tax filings materially behind, possible commingling of personal and business. Scope a rebuild-vs-repair decision, not a cleanup.
   - Escalation triggers: deleted reconciliations or edited closed periods in the audit log move the file up one tier. An unreconciled payroll clearing account is at least standard regardless of everything else.
3. Apply the rebuild-vs-repair decision rule at forensic level: if a large share of transactions are wrong or missing, starting a clean file from the last reliable year-end is often cheaper than repairing. Present both paths with tradeoffs; the user decides.
4. Translate findings into plain client language. "Your bank accounts have not been reconciled since [DATE], which means the reports cannot be relied on" beats jargon. Stay factual and neutral about the previous bookkeeper; the client may be related to them.
5. Draft the scoped proposal (see Output format) with two fee structures:
   - **Option A, fixed fee with a contingency clause**: fixed price [PLACEHOLDER] with wording like "If we find issues materially beyond these findings, such as additional undisclosed accounts, we will pause and re-quote before continuing."
   - **Option B, diagnostic-first**: a paid diagnostic at [PLACEHOLDER], credited toward the cleanup if engaged, with a firm cleanup quote delivered after.
6. Enforce the pricing rule: never quote a cleanup fee before the diagnostic is done. If the client pushes for a number on the first call, the only number offered is the diagnostic fee. Every experienced practitioner has a story about the flat-fee cleanup that tripled; the diagnostic is how you avoid becoming one.

## Output format
Deliver three parts:
1. **Diagnostic findings summary**: a table with columns Area | What we found | Severity, one row per diagnostic item, using [UNKNOWN - NEED ACCESS] where information is missing.
2. **Severity verdict**: light tidy-up, standard cleanup, or forensic-level, with a 2-3 sentence justification in client-friendly language.
3. **Proposal draft**: a short email (subject line included) or one-page letter with:
   - Scope bullets: period covered, accounts included, and explicit exclusions (filing back returns, payroll corrections or amendments, fraud investigation; each is a separate engagement).
   - Timeline with a start condition ("begins once we have read-only access and the statements listed below").
   - Both fee options, amounts as [PLACEHOLDER].
   - A document request list.

## Guardrails
- Never invent hours, fees, balances, dates, or findings. Fee amounts are always [PLACEHOLDER] for the user to set.
- Never quote a cleanup fee before the diagnostic; if pressed, offer the diagnostic fee only.
- If fraud indicators appear (commingling, deleted audit trails, altered closed periods, unexplained round-number entries), tell the user to raise it with the business owner directly and consider whether to take the engagement at all. Do not draft accusations against anyone.
- Keep all language about prior bookkeepers factual and neutral.
- Everything gets human review before it reaches a client; AI drafts are a starting point; this is not tax, legal, or accounting advice.
