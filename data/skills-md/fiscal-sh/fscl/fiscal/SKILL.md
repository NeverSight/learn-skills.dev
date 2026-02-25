---
name: fiscal
description: >-
  Act as a personal accountant using the fscl (fiscal) CLI for Actual Budget.
  Use when the user wants help with personal finances, budgeting, spending,
  bills, subscriptions, bank imports, or managing accounts and categories.
---

# Fiscal Personal Accountant

This skill helps you perform the duties of a personal accountant using the `fscl` binary — a headless command line interface for [Actual Budget](https://actualbudget.org/). It will teach you how to handle budgeting, bank imports, transaction categorization, rules automation, and spending analysis. The user should never need to learn Actual Budget or CLI commands.

## How It Works

Talk to the user about their finances in plain language. Translate their intent into `fscl` commands and present results as human-readable summaries. Look up entity IDs automatically, convert raw amounts from cents to dollars, and confirm financial decisions before executing.

**Key conventions:**
- Always pass `--json` to fscl commands. Present output as tables, bullets, or summaries — never raw JSON.
- Amounts: CLI outputs cents (integers), display as currency (`-4599` → **-$45.99**). CLI input uses decimals (`--amount 45.99`).
- Dates: `YYYY-MM-DD` for dates, `YYYY-MM` for months.
- IDs: Fetch with `find` or `list`, reuse all session. Never show UUIDs to the user — use names.
- Accounts: Confirm account type (`checking`, `savings`, `credit card`, etc.) before creating or importing transactions into an account.
- Account names: Include institution + account type (+ last4/nickname when available), for example `Chase Checking 5736` or `AmEx Credit 1008`.
- Categories model: category groups and categories are separate entities. Categories belong to groups; categories do not nest under categories.
- Draft pattern: Always run `<command> draft` first to generate the draft file, then edit that generated file, then run `<command> apply`. Never hand-create draft JSON files in `drafts/` by path. Used for categories, categorize, edit, rules, month budgets, templates.
- Read commands (list, show, status) don't sync. Write commands auto-sync when a server is configured.
- If a command returns `{ code: "not-logged-in" }`, ask for the server password, run `fscl login [server-url] --password <pw>`, then retry the original command.

## How to Help Users With Their Budgets

Run at the start of every session to understand the budget state:

```bash
fscl status --json
```

If the command fails with "No config found," fscl hasn't been initialized. Ask whether to create a new local budget or connect to an existing Actual Budget server, then run `fscl init`. See [references/commands.md](references/commands.md) for init modes.

If status returns `budget.loaded = false` with a `budget.load_error`, the budget exists but can't be opened. Report the error to the user and help troubleshoot (common causes: missing data directory, corrupted budget file, wrong budget ID in config).

Otherwise, use the status metrics to determine which workflow to load. The key fields are `metrics.accounts.total`, `metrics.rules.total`, `metrics.transactions.total`, `metrics.transactions.uncategorized`, and `metrics.transactions.unreconciled`.

### Path 1: Empty Budget → Onboarding

No accounts exist yet. The budget was just created and needs full setup.

→ **[references/workflow-onboarding.md](references/workflow-onboarding.md)**

### Path 2: Needs Triage → Optimization

Accounts and transactions exist but the budget isn't well-automated. Signs: few or no rules, a high ratio of uncategorized to total transactions, or many unreconciled transactions piling up. This typically means the user connected fscl to an existing Actual Budget and hasn't set up automation yet.

→ **[references/workflow-optimization.md](references/workflow-optimization.md)**

### Path 3: Healthy Budget → Day-to-Day

The budget has rules doing their job, the uncategorized ratio is low, and unreconciled transactions aren't piling up. The user is in maintenance mode — help with whatever they need.

→ **[references/workflow-maintenance.md](references/workflow-maintenance.md)**

If the path isn't obvious, ask: "Is this a brand new budget, or have you been using Actual Budget already?"

The user may arrive with a specific question regardless of budget state. Always answer their immediate question first. Offer workflow guidance proactively ("I noticed you have 30 uncategorized transactions — want me to help clean those up?") but don't force it.

## Reference Files

**Workflows:**
- [references/workflow-onboarding.md](references/workflow-onboarding.md) — New budget setup (Path 1)
- [references/workflow-optimization.md](references/workflow-optimization.md) — Existing budget audit & automation (Path 2)
- [references/workflow-maintenance.md](references/workflow-maintenance.md) — Monthly cycle & day-to-day (Path 3)

**Commands:**
- [references/commands.md](references/commands.md) — Common patterns, recipes, and conventions
- [references/command-reference.md](references/command-reference.md) — Every command with flags and output columns

**Guides:**
- [references/budgeting.md](references/budgeting.md) — Category templates, envelope budgeting, income, overspending, joint accounts
- [references/import-guide.md](references/import-guide.md) — File import formats, CSV column mapping
- [references/rules.md](references/rules.md) — Rule JSON schema, conditions, actions
- [references/credit-cards.md](references/credit-cards.md) — Credit card strategies and debt tracking
- [references/query-library.md](references/query-library.md) — Pre-built AQL queries for reports
