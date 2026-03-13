---
name: beancount-accounting
description: This skill should be used when the user asks to "add a transaction", "create a beancount entry", "record an expense", "balance my accounts", "query my finances", "check account balances", "categorize spending", "write beancount", "edit .beancount files", "run a BQL query", "reconcile accounts", or mentions beancount, double-entry accounting, or ledger files. Provides comprehensive beancount syntax, directives, and query language expertise.
---

# Beancount Accounting Skill

Beancount is a plain-text double-entry accounting system. This skill provides expertise for creating, editing, and querying beancount files.

## Core Concepts

### Double-Entry Accounting

Every transaction must balance to zero. Money flows between accounts:
- **Debits** increase Assets/Expenses, decrease Liabilities/Income/Equity
- **Credits** decrease Assets/Expenses, increase Liabilities/Income/Equity

### Five Account Types

| Type | Purpose | Normal Balance |
|------|---------|----------------|
| `Assets` | What you own (bank accounts, investments) | Positive |
| `Liabilities` | What you owe (credit cards, loans) | Negative |
| `Income` | Money coming in (salary, interest) | Negative |
| `Expenses` | Money going out (food, rent) | Positive |
| `Equity` | Net worth, opening balances | Negative |

### Account Naming

Use colon-separated hierarchical names starting with capital letters:
```
Type:Country:Institution:Account:SubAccount
```

Examples:
```
Assets:Checking:Centennial:Joint
Liabilities:Card:Chase:Sapphire
Expenses:Food:Groceries
Income:Salary:Employer
```

## Transaction Syntax

### Basic Format

```beancount
YYYY-MM-DD flag "Payee" "Narration"
  Account1    Amount Currency
  Account2    Amount Currency  ; optional comment
```

### Flags

- `*` - Cleared/completed transaction
- `!` - Pending/needs review

### Examples

Simple expense:
```beancount
2026-01-03 * "Starbucks" "Morning coffee"
  Expenses:Food:Coffee    5.75 USD
  Liabilities:Card:Chase:Sapphire
```

Paycheck with multiple postings:
```beancount
2026-01-15 * "Employer" "Bi-weekly salary"
  Assets:Checking:Main           3500.00 USD
  Expenses:Taxes:Federal          800.00 USD
  Expenses:Taxes:State            200.00 USD
  Expenses:Insurance:Health       150.00 USD
  Income:Salary                 -4650.00 USD
```

Transfer between accounts:
```beancount
2026-01-10 * "Transfer to savings"
  Assets:Savings:Ally     500.00 USD
  Assets:Checking:Main   -500.00 USD
```

### Amount Interpolation

One posting amount can be omitted - beancount calculates it:
```beancount
2026-01-03 * "Grocery Store" "Weekly groceries"
  Expenses:Food:Groceries    125.43 USD
  Assets:Checking:Main  ; Amount calculated as -125.43 USD
```

## Essential Directives

### open / close

Declare account lifecycle:
```beancount
2026-01-01 open Assets:Checking:Main USD
2028-12-31 close Assets:Checking:Main
```

### balance

Assert account balance at start of day (catches errors):
```beancount
2026-01-31 balance Assets:Checking:Main 4583.84 USD
```

### pad

Auto-generate balancing entry between two dates:
```beancount
2026-01-01 pad Assets:Checking:Main Equity:Opening-Balances
2026-01-02 balance Assets:Checking:Main 4583.84 USD
```

### include

Split files for organization:
```beancount
include "2026-01.beancount"
include "accounts.beancount"
```

### option

Configure beancount behavior:
```beancount
option "title" "Personal Finances"
option "operating_currency" "USD"
```

## Metadata and Tags

### Metadata

Attach key-value pairs to directives or postings:
```beancount
2026-01-03 * "Amazon" "Office supplies"
  order-id: "123-456-789"
  Expenses:Office    45.00 USD
    category: "equipment"
  Liabilities:Card:Chase
```

### Tags and Links

Group related transactions:
```beancount
2026-01-15 * "Hotel" "Conference lodging" #work-travel #conference-2026
  Expenses:Travel:Lodging    299.00 USD
  Liabilities:Card:Chase

2026-02-01 * "Expense Report" "Reimbursement" ^conference-2026
  Assets:Checking:Main    299.00 USD
  Income:Reimbursements
```

## BQL Queries

Beancount Query Language (BQL) provides SQL-like queries. Run with `bean-query`:

```bash
bean-query finances/2026.beancount "SELECT account, sum(position) WHERE account ~ 'Expenses' GROUP BY 1"
```

### Common Queries

Account balance:
```sql
SELECT account, sum(position)
WHERE account ~ 'Assets:Checking'
GROUP BY 1
```

Monthly expenses by category:
```sql
SELECT MONTH(date), account, sum(position)
WHERE account ~ 'Expenses' AND year = 2026
GROUP BY 1, 2
ORDER BY 1, 2
```

Transactions for an account:
```sql
SELECT date, narration, payee, position, balance
WHERE account = 'Assets:Checking:Centennial:Joint'
ORDER BY date
```

### Key BQL Functions

| Function | Purpose |
|----------|---------|
| `SUM(position)` | Aggregate amounts |
| `YEAR(date)`, `MONTH(date)` | Extract date parts |
| `COST(position)` | Get cost basis |
| `account ~ 'pattern'` | Regex match account |

## Working with Beancount Files

### Reading Files

Before editing, read the beancount file to understand:
- Existing account structure
- Naming conventions used
- Transaction patterns
- Include file organization

### Adding Transactions

1. Match existing account names exactly
2. Use consistent payee/narration style
3. Ensure transaction balances to zero
4. Add to chronologically appropriate location or include file

### Validation

Run `bean-check` to validate syntax:
```bash
bean-check finances/2026.beancount
```

### Common Patterns

Credit card payment:
```beancount
2026-01-25 * "Chase" "Credit card payment"
  Liabilities:Card:Chase:Sapphire    500.00 USD
  Assets:Checking:Main              -500.00 USD
```

Investment purchase with cost basis:
```beancount
2026-01-20 * "Fidelity" "Buy index fund"
  Assets:Investments:Fidelity:FXAIX    10 FXAIX {150.00 USD}
  Assets:Investments:Fidelity:Cash   -1500.00 USD
```

Mortgage payment breakdown:
```beancount
2026-01-01 * "Rocket Mortgage" "Monthly mortgage"
  Liabilities:Loan:RocketMortgage     800.00 USD  ; Principal
  Expenses:Housing:Interest           900.00 USD  ; Interest
  Expenses:Housing:Escrow             300.00 USD  ; Escrow
  Assets:Checking:Main              -2000.00 USD
```

## Best Practices

### File Organization

- Use `include` to split by month or category
- Keep account definitions in main file
- Add transactions to appropriate include files

### Account Hierarchy

- Be consistent with naming depth
- Use specific subcategories for visibility
- Group related accounts logically

### Balance Assertions

- Add monthly balance assertions for bank accounts
- Reconcile against actual statements
- Catches data entry errors early

### Error Prevention

- Always run `bean-check` after edits
- Use balance assertions frequently
- Keep transactions in chronological order

## Additional Resources

### Reference Files

For detailed syntax and patterns, consult:
- **`references/syntax.md`** - Complete directive reference with all options
- **`references/bql.md`** - Full BQL query language documentation
- **`references/examples.md`** - Common transaction patterns and workflows

### Command Line Tools

| Command | Purpose |
|---------|---------|
| `bean-check file.beancount` | Validate syntax |
| `bean-query file.beancount "QUERY"` | Run BQL query |
| `bean-report file.beancount balances` | Balance report |
| `bean-web file.beancount` | Web interface |
