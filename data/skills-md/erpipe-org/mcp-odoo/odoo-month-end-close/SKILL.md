---
name: odoo-month-end-close
description: Drive a month-end accounting close on Odoo through odoo-mcp — AR/AP aging, open-item and draft-invoice review, reconciliation checklists, and chatter documentation — with human sign-off at every posting step. Use when the user asks to "close the month", "review receivables/payables", "check aging", or prepare finance reports from Odoo.
---

# Odoo month-end close

You are running a month-end close review against a live Odoo database
through odoo-mcp. Finance data is the last place an agent should guess:
every number you present must come from a tool result, and every posting
action needs the human's explicit approval.

## Prerequisites

- odoo-mcp connected; `account` module installed (verify via
  `business_pack_report(pack="accounting")` or `get_odoo_profile`).
- The `accounting_close_checklist` MCP prompt is the compact in-server
  version of this playbook; this skill adds pacing and judgment.

## Playbook

1. **Baseline:** `accounting_health_summary` — open AR/AP item counts and
   the draft-invoice backlog. This is your before-photo; show it.
2. **Aging deep-dive:** `receivable_payable_aging(direction="receivable")`
   then `"payable"`. Present the bucket table (not due / 1-30 / 31-60 /
   61-90 / 90+) with per-partner totals; flag partners with >60d balances.
3. **Draft backlog:** `search_records(model="account.move",
   domain=[["state","=","draft"],["move_type","in",["out_invoice","in_invoice"]]])`
   — list drafts with amounts and dates; ask which should be posted,
   which deleted (deletion = human decision, never yours).
4. **Unreconciled sweep:** search `account.move.line` for open items on
   receivable/payable accounts older than the period; summarize by
   account. Use `aggregate_records` (groupby `account_id`) instead of
   paging raw lines.
5. **Anomaly pass:** run `data_quality_report(model="account.move")` —
   missing required values and format anomalies on invoices are close
   blockers.
6. **Actions through the gate.** Posting a draft, correcting a field, or
   any state change: `preview_write` → human reviews the diff →
   `validate_write` → `execute_approved_write(confirm=true)`. One document
   batch at a time.
7. **Document the close:** with approval, `chatter_post` a close summary on
   the relevant records (or the human's designated close journal entry) —
   what was reviewed, what was posted, what is carried over.
8. **After-photo:** re-run `accounting_health_summary`; report the delta.

## Output format

Close report with: baseline vs final summary, aging tables, actions taken
(each with its approval token event), and a carried-over list with owners.

## Hard rules

- Never post, reconcile, or delete without a fresh per-batch approval.
- `as_of` on aging shifts the bucketing reference only — say so if the
  human asks for a "historical snapshot"; do not fake one.
- If multi-company is active, confirm the company scope first
  (`diagnose_access` explains company-based invisibility).
