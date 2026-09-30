---
name: finicity
description: Use the platform-managed banking gateway backed by Finicity to list enabled bank accounts, balances, and transactions. Use when the user mentions Finicity, connected bank accounts, banking balances, or bank transactions.
---

## Prerequisites

1. Authenticate Okou CLI with `OKOU_TOKEN` carrying the `banking:read` capability.
2. A platform administrator must enable the relevant Finicity-backed accounts for the current agent.
3. Finicity credentials and app tokens remain server-side; do not request them from the user.

## List Accounts

```bash
okou banking accounts --json | jq '{provider, accounts}'
```

Use the returned account `id` for balance and transaction requests.

## Get an Account Balance

```bash
okou banking balances --account-id <account-id> --json | jq '{provider, balance}'
```

## List Transactions

Dates must use `YYYY-MM-DD`. Limits must be between 1 and 1000.

```bash
okou banking transactions --account-id <account-id> --from 2026-07-01 --to 2026-07-31 --limit 100 --json | jq '{provider, transactions}'
```

## Guidelines

1. Use `okou banking`; do not call Finicity APIs directly or ask for Finicity partner credentials.
2. Access is limited to accounts enabled for the current agent.
3. Treat account identifiers, balances, and transactions as sensitive financial data.
4. Use the narrowest date range needed and avoid retaining raw banking responses.
5. Banking commands are read-only; do not imply that transfers or account changes are supported.

## Troubleshooting

If a banking command is unavailable or returns an authorization error, verify the current Okou authentication and ask an administrator to confirm the `banking:read` capability and enabled account access.
