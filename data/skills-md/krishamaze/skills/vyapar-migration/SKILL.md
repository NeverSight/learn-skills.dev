---
name: vyapar-migration
description: >
  Authoritative Vyapar schema knowledge. Use when the user mentions Vyapar, .vyb files,
  .vyp SQLite databases, reading Vyapar data, or any task that requires understanding
  Vyapar's internal structure. Triggers on: "vyapar", "vyb file", "vyp file", "vyapar backup",
  "vyapar schema", "vyapar sqlite", "vyapar data". This skill contains only verified facts
  about Vyapar's internals — zero assumptions, zero hallucination. Use it regardless of
  the target system (Odoo, Tally, custom ERP, CSV export, or anything else).
license: MIT
metadata:
  author: NexaraTech
  version: "1.0.0"
  vyapar-version: "5.x Android"
  evidence: "Live .vyp SQLite backups + APK DEX decompilation (strings classes*.dex)"
---

# Vyapar Schema Skill

This skill contains only verified facts about Vyapar's internal database.
It has no opinions about what to migrate to. The agent using this skill
decides what to do with the data — this skill ensures they start with
accurate source knowledge.

---

## File Format

- Vyapar backup extension: **`.vyb`** — a standard ZIP archive
- Inside the ZIP: a single **`.vyp`** file — a SQLite 3 database
- Extract: `unzip backup.vyb` → produces `<name>.vyp`
- Open: `sqlite3 <name>.vyp` or DB Browser for SQLite
- There is always exactly one `.vyp` per `.vyb`

---

## Architecture

- Single-company, single-user accounting + inventory app
- One SQLite file = one company's complete data
- No multi-tenancy, no foreign server, no hidden tables
- All financial data lives in `kb_transactions` + `kb_lineitems`
- All party data lives in `kb_names`
- All product data lives in `kb_items`

---

## Reference Files

Load on demand — not all at once:

| File | Load when |
|---|---|
| `references/schema.md` | Need column-level detail for any table |
| `references/enums.md` | Interpreting any INTEGER flag or status field |
| `references/data-rules.md` | Validating or transforming Vyapar data |

---

## Core Tables — Quick Reference

```
kb_firms              — company profile, GSTIN, address
kb_names              — all parties (customers + vendors)
kb_items              — products and services
kb_item_categories    — product categories
kb_item_units         — units of measure
kb_transactions       — every transaction header
kb_lineitems          — line items for each transaction
kb_tax_code           — GST and other tax definitions
kb_paymentTypes       — payment methods (Cash, Cheque, UPI, Bank)
kb_payment_terms      — payment term definitions
txn_payment_mapping   — links payment methods to transactions
kb_txn_links          — links payments to invoices (optional, settings-driven)
kb_linked_transactions— links converted documents (e.g. estimate → invoice)
journal_entry         — manual journal entries
journal_entry_line_items — lines for manual journals
kb_item_stock_tracking— stock movement history
other_accounts        — chart of accounts (non-party accounts)
party_to_party_transfer — inter-party transfers (separate from kb_transactions)
```

---

## Transaction Types — Critical Mapping

Always read `references/enums.md` for the full table. Key types:

| txn_type | Label | Has lineitems | Financial |
|---|---|---|---|
| 1 | Sale Invoice | Yes | Yes |
| 2 | Purchase Invoice | Yes | Yes |
| 3 | Payment-In | No | Yes |
| 4 | Payment-Out | No | Yes |
| 5 | Opening Balance — Receivable | No | Yes |
| 6 | Opening Balance — Payable | No | Yes |
| 7 | Expense | No | Yes |
| 21 | Credit Note / Sale Return | Yes | Yes |
| 23 | Debit Note / Purchase Return | Yes | Yes |
| 24 | Sale Order | Yes | No (until converted) |
| 27 | Delivery Challan | Yes | No |
| 28 | Purchase Order | Yes | No |
| 30 | Estimate / Quotation | Yes | No |
| 65 | Proforma Invoice | Yes | No |
| 83 | Job Work Challan | Yes | No |
| 60 | Sale — Fixed Asset | Yes | Yes |
| 61 | Purchase — Fixed Asset | Yes | Yes |

Non-financial types (24, 27, 28, 30, 65, 83) do not affect balances unless
`txn_status=4` (converted). Confirmed by SQL: `WHERE txn_type NOT IN (24,28,30,27,83,70)`.

---

## Amount Fields — Exact Meaning

```
txn_cash_amount       — amount already collected/paid
txn_balance_amount    — amount still outstanding
txn_total_amount      — gross before tax (lineitems sum)
txn_tax_amount        — total tax
txn_discount_amount   — transaction-level discount
```

**Invoice total = `txn_cash_amount + txn_balance_amount`**
Never use `txn_total_amount` alone as the invoice value.

---

## Tax Logic

- `txn_tax_inclusive=1` → price INCLUDES tax
- `txn_tax_inclusive=2` → price EXCLUDES tax (most common)
- GST components stored as separate rows in `kb_lineitems` joined to `kb_tax_code`
- `txn_place_of_supply` determines inter-state (IGST) vs intra-state (CGST+SGST)
- If `txn_place_of_supply` is empty → default to intra-state

---

## Party Rules

- `name_type=1` = Customer, `name_type=2` = Vendor
- A single `name_id` can appear in both types — same entity, dual role
- Unique key for deduplication: `name_id` (internal) or `full_name` + `phone_number`
- GSTIN stored in `name_gstin_number` — may be blank for unregistered parties

---

## Payment Linking

- `txn_payment_mapping.payment_id` → `kb_paymentTypes.paymentType_id`
  This is the payment **METHOD** (Cash=1, Cheque=2) — NOT a linked payment transaction
- `kb_txn_links` — optionally links payment transactions to invoices
  This link is user-controlled via a settings toggle — NOT guaranteed to exist
- `kb_linked_transactions` — links converted documents (estimate → invoice, order → invoice)

---

## Stock

- `kb_items.item_stock_quantity` = current snapshot quantity
- For historical opening quantity: use `kb_item_stock_tracking.ist_opening_quantity`
- Negative stock is possible — Vyapar allows sales without stock enforcement

---

## Data Quality — Known Issues

Read `references/data-rules.md` for the full SQL validation suite. Key issues:

- Lineitems can exist without a matching transaction (orphaned rows)
- Parties can exist without GSTIN or phone (minimal required fields)
- `txn_balance_amount` can be negative on overpayments
- Duplicate GSTIN across parties is possible (data entry error)
- `txn_place_of_supply` is frequently blank
