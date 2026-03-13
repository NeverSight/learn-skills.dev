---
name: agentbudget
description: Run an agent-first, YNAB-like zero-based envelope budgeting workflow using the agentbudget CLI. Prefer --json for automation.
---

# agentbudget

Use `agentbudget` as the **single interface** to the budget database (local SQLite or Turso/libSQL remote).

## Core conventions

- **Internal storage:** money is stored as **integer minor units** (e.g. cents).
- **CLI input:** commands accept **major units** for convenience:
  - `319` = RM319.00
  - `3.19` = RM3.19
  - **Do not multiply by 100** when calling the CLI.
- **Transaction sign convention:** outflow = negative, inflow = positive.
- **Inflow must be explicitly assigned to TBB** using `--envelope "To Be Budgeted"`.
- For agent calls, use `--json`.
  - success: `{ "ok": true, "data": ... }`
  - error: `{ "ok": false, "error": { "message": "...", "code"?: "..." } }`

### JSON output units (IMPORTANT)

Most numeric money fields returned in `--json` responses are **minor units** (integer cents).

- Example: `balance: 123456` means **1234.56** in the budget currency.
- To display to humans: divide by 100 and format to 2 decimals, using the returned `currency` (or the account currency).
- When comparing values, comparisons are safe in minor units (no float drift).

If unsure: when a number ends with `..00` suspiciously often or is 100× too big, treat it as minor units.

### Major vs minor units (common failure mode)

If an amount looks off by exactly **100×**, you mixed units.

- When a user says **"23.50"** (in the budget currency) → CLI amount is **`-23.50`** (major units)
- If you see **`-2350`**, that is **minor units** (cents) and should usually be **formatted as -23.50** (major units).

Rule of thumb for automation:
- Treat **CLI flags** like `--amount`, `--statement-balance`, targets, and moves as **major units**.
- Treat **`--json` outputs** (balances, budgeted/activity/available, cashflow, topSpending, etc.) as **minor units** unless the field name explicitly says otherwise.
- Treat **database storage** and any explicitly-named `minor`, `minorUnits`, `*_minor` fields as **minor units**.
- Exception: `budget allocate --from-json allocations.json` currently expects **minor units** in the JSON file (see note in Budget actions).

Output hygiene (so you don't lie to the user):
- When you quote money to the user, always render as **major units with 2 decimals** (e.g. `23.50`) and include/derive the **currency** from data (`currency` field or account currency).
- Sanity check: if an envelope "spent" is `2350`, you should display it as **23.50** (major units), not 2350.

## Workflow (recommended)

### 1) Initialize database config (choose one)

Local:
```bash
agentbudget init --local
```

Remote (Turso):
```bash
export TURSO_DATABASE_URL="libsql://..."
export TURSO_AUTH_TOKEN="..."
agentbudget init --remote
```

### 2) Bootstrap required system entities

Create the required system envelope **To Be Budgeted** (TBB):
```bash
agentbudget system init
```

### 3) Set budget currency (DB-backed)

`agentbudget` uses a **single budget currency** stored in the database (table: `settings`).

- Set it once per DB:
```bash
agentbudget currency set "RM" --json
```

- View it:
```bash
agentbudget currency show --json
```

Notes:
- You may store a **symbol** (e.g. `RM`, `$`) or a **code** (e.g. `MYR`, `USD`).
- This is **DB-backed**: if another machine points at the same DB, it will see the same currency.

### 4) Create reference data

Accounts:
```bash
agentbudget account create "Maybank" --type checking --json
agentbudget account list --json
```

Envelopes:
```bash
agentbudget envelope create "Groceries" --group "Living" --json
agentbudget envelope list --json
```

Payees (canonical list; transactions store both `payeeId` + `payeeName`):
```bash
agentbudget payee create "Grab" --json
agentbudget payee list --json

# Rename a payee (also updates linked transactions' payeeName)
agentbudget payee rename "GrabFood" "Grab" --json

# Merge variants into a canonical payee (updates tx.payeeId, then deletes source)
agentbudget payee merge "GRAB*FOOD" --into "Grab" --json
```

Payee rules (pattern matching → canonical payee; best for imports):
```bash
# When payee string contains "GRAB*FOOD", map it to canonical "Grab"
agentbudget payee rule add --match contains --pattern "GRAB*FOOD" --to "Grab" --json

agentbudget payee rule list --json

# Disable a rule
agentbudget payee rule archive payrule_... --json
```

Notes:
- Payee rules are applied when resolving `--payee` (tx add/import/update and schedules).
- When a rule matches, we store `payeeName` as the canonical payee name.

### 4) Ingest transactions

Transfers (between accounts; does not touch envelopes):
```bash
agentbudget tx transfer \
  --from-account "Checking" \
  --to-account "Savings" \
  --amount 250 \
  --date 2026-02-05 \
  --memo "move money" \
  --json
```

Single envelope:
```bash
agentbudget tx add \
  --account "Maybank" \
  --amount -23.50 \
  --date 2026-02-08 \
  --payee "Grab" \
  --memo "Food" \
  --envelope "Groceries" \
  --json
```

Notes:
- `--payee "..."` will **resolve or auto-create** a canonical payee and store both `payeeId` and `payeeName` on the transaction.

Split a transaction across envelopes:
```bash
agentbudget tx add \
  --account "Maybank" \
  --amount -120.00 \
  --date 2026-02-08 \
  --splits-json '[{"envelope":"Groceries","amount":-80.00},{"envelope":"Household","amount":-40.00}]' \
  --json
```

Batch import JSONL (one JSON object per line; each record can use `envelope` or `splits`):
```bash
agentbudget tx import --from-jsonl ./tx.jsonl --json
agentbudget tx import --from-jsonl ./tx.jsonl --dry-run --json
```

Query:
```bash
agentbudget tx list --from 2026-02-01 --to 2026-02-29 --json
agentbudget tx list --envelope "Groceries" --json
```

Update (basic patch + optional split replacement):
```bash
agentbudget tx update tx_... --memo "new memo" --json
agentbudget tx update tx_... \
  --amount -25.00 \
  --json
agentbudget tx update tx_... \
  --splits-json '[{"envelope":"Groceries","amount":-25.00,"note":"splitnote"}]' \
  --json
```

Delete (hard delete):
```bash
agentbudget tx delete tx_... --json
```

### 5) Budget actions

Targets/goals (major units):
```bash
agentbudget target set "Groceries" --type monthly --amount 800 --json
agentbudget target set "Groceries" --type needed-for-spending --amount 800 --json
agentbudget target set "Insurance" --type by-date --target-amount 1200 --target-month 2026-12 --start-month 2026-02 --json
agentbudget target list --json
agentbudget target clear "Groceries" --json
```

Underfunded (recommended funding amounts from targets):
```bash
agentbudget budget underfunded 2026-02 --json
```

Allocate (writes a matching TBB offset allocation automatically).

Note: allocation amounts in `allocations.json` are still **minor units** for now.
(We can upgrade this later with a `--major` mode.)

```bash
agentbudget budget allocate 2026-02 --from-json allocations.json --json
```

Move budget between envelopes (major units):
```bash
agentbudget budget move 2026-02 --from "Groceries" --to "Fun" --amount 100 --json
```

### 6) Scheduled transactions (recurring templates)

Use schedules to represent recurring future transactions. Work flow:
- `schedule create` creates the template
- `schedule due` generates a list of un-posted occurrences in a date range
- `schedule post <occurrenceId>` converts an occurrence into a real transaction

Create (typed flags):

Monthly:
```bash
agentbudget schedule create "Rent" \
  --account "Checking" \
  --amount -2000 \
  --payee "Landlord" \
  --envelope "Rent" \
  --freq monthly \
  --interval 1 \
  --month-day 1 \
  --start 2026-03-01 \
  --json
```

Daily:
```bash
agentbudget schedule create "Coffee" \
  --account "Checking" \
  --amount -15 \
  --payee "Starbucks" \
  --envelope "Coffee" \
  --freq daily \
  --interval 1 \
  --start 2026-03-02 \
  --json
```

Weekly (single weekday or comma-separated list):
```bash
agentbudget schedule create "Gym" \
  --account "Checking" \
  --amount -50 \
  --payee "Gym" \
  --envelope "Gym" \
  --freq weekly \
  --interval 1 \
  --weekday mon,thu \
  --start 2026-03-02 \
  --json
```

Yearly:
```bash
agentbudget schedule create "Insurance" \
  --account "Checking" \
  --amount -1200 \
  --payee "Insurer" \
  --envelope "Insurance" \
  --freq yearly \
  --interval 1 \
  --month 2 \
  --month-day last \
  --start 2026-02-01 \
  --json
```

List schedules:
```bash
agentbudget schedule list --json
```

Update a schedule (by id or name; unspecified fields unchanged):
```bash
agentbudget schedule update sched_... \
  --freq weekly \
  --interval 1 \
  --weekday mon,thu \
  --end 2026-03-31 \
  --json
```

Archive a schedule (hides it from list/due):
```bash
agentbudget schedule archive sched_... --json
```

See what’s due (occurrences not yet posted):
```bash
agentbudget schedule due --from 2026-03-01 --to 2026-03-31 --json
```

End date (optional; inclusive):
```bash
agentbudget schedule create "Trial" \
  --account "Checking" \
  --amount -999 \
  --payee "Service" \
  --envelope "Subscriptions" \
  --freq daily \
  --interval 1 \
  --start 2026-03-01 \
  --end 2026-03-07 \
  --json
```

Post an occurrence (creates a real tx + split; marks as posted):
```bash
agentbudget schedule post occ_sched_..._2026-03-01 --json
```

### 7) Read current state

Month summary (includes rollover):
```bash
agentbudget month summary 2026-02 --json
```

Overview (dashboard: budget health, goals/underfunded, cashflow, net worth, accounts):
```bash
agentbudget overview --month 2026-02 --json
```

JSON shape highlights:
- `budget.toBeBudgeted` (renamed from older `tbb`)
- `goals.underfundedTotal`, `goals.topUnderfunded[]`
- `schedules` summary (local date window, next 7 days):
  - `schedules.window.{from,to}`
  - `schedules.counts.{overdue,dueSoon}`
  - `schedules.topDue[]`
- `reports.cashflow` uses LLM-friendly numbers: `{ income, expense, net }` (income/expense positive)
- `reports.topSpending[]` grouped by envelope
- `reports.topSpendingByPayee[]` grouped by payee (outflows; excludes transfers)
- `netWorth`: `{ liquid, tracking, total }`
- `accounts.list[]`

Account detail (balances, counts, recent tx; optional statement delta):
```bash
agentbudget account detail "Checking" --limit 10 --json
agentbudget account detail "Checking" --statement-balance 1234.56 --json
```

Reconcile (creates TBB adjustment if needed; marks cleared tx as reconciled):
```bash
agentbudget account reconcile "Checking" --statement-balance 1234.56 --date 2026-02-28 --json
```

## Troubleshooting

- SQLite/libSQL error like `Unable to open connection ... : 14` usually means the local DB path is not writable.
  - Fix by running: `agentbudget init --local`
  - Or override: `agentbudget --db "file:/absolute/path.db" ...`
