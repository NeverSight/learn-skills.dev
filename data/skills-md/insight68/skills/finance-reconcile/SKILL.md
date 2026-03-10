---
name: finance-reconcile
description: Comprehensive financial audit tool for balance sheets and income statements. Use when Claude needs to verify balance sheet equilibrium, validate income statement items against detail records, track account changes with opening/closing balance reconciliation, verify cross-statement relationships, or generate audit reports with account analysis and transaction tracing.
---

# Finance Audit

## Overview

Comprehensive financial audit tool that validates balance sheets and income statements. Performs four core audits: balance sheet equilibrium, income statement verification, account change tracking, and cross-statement relationship validation.

## Quick Start

### Basic Balance Sheet Audit

Verify balance sheet with account changes:

```bash
scripts/reconcile.py \
    --balance-sheet balance_sheet.xlsx \
    --account-changes account_changes.xlsx \
    --output audit_report.xlsx
```

### Complete Financial Audit (Balance Sheet + Income Statement)

Full audit including profit statement:

```bash
scripts/reconcile.py \
    --balance-sheet balance_sheet.xlsx \
    --account-changes account_changes.xlsx \
    --income-statement income_statement.xlsx \
    --income-details income_details.xlsx \
    --transactions transactions.xlsx \
    --output complete_audit.xlsx \
    --period "2024年1月"
```

### Using Custom Column Names

Use JSON config file for custom column names:

```bash
scripts/reconcile.py \
    --balance-sheet bs.xlsx \
    --account-changes ac.xlsx \
    --config my_config.json
```

## Command Parameters

| Parameter | Short | Required | Description |
|-----------|-------|----------|-------------|
| `--balance-sheet` | `-b` | Yes | Balance sheet file path |
| `--account-changes` | `-a` | Yes | Account change details file path |
| `--income-statement` | `-i` | No | Income statement file path |
| `--income-details` | `-d` | No | Income statement details file path |
| `--transactions` | `-t` | No | Transaction details file path |
| `--output` | `-o` | No | Output Excel audit report path |
| `--period` | `-p` | No | Audit period (default: 本期) |
| `--tolerance` | - | No | Tolerance for acceptable difference (default: 0.01) |
| `--config` | `-c` | No | JSON config file for column names |
| `--bs-sheet` | - | No | Balance sheet sheet name or index |
| `--ac-sheet` | - | No | Account changes sheet name or index |
| `--is-sheet` | - | No | Income statement sheet name or index |
| `--id-sheet` | - | No | Income details sheet name or index |
| `--trans-sheet` | - | No | Transaction details sheet name or index |

## Required File Formats

### 1. Balance Sheet (资产负债表) - Required

| Column | Description |
|--------|-------------|
| 科目 | Account name |
| 期初余额 | Opening balance |
| 期末余额 | Closing balance |
| 类型 | Account type (资产/负债/所有者权益) |
| 金额 | Amount for totals |

### 2. Account Changes (科目变动明细表) - Required

| Column | Description |
|--------|-------------|
| 科目 | Account name |
| 借方 | Debit amount |
| 贷方 | Credit amount |

### 3. Income Statement (利润表) - Optional

| Column | Description |
|--------|-------------|
| 项目 | Income statement item |
| 金额 | Amount |

### 4. Income Details (利润明细表) - Optional

| Column | Description |
|--------|-------------|
| 项目 | Item name (must match income statement) |
| 金额 | Detail amount |

### 5. Transactions (交易明细表) - Optional

| Column | Description |
|--------|-------------|
| 科目 | Affected account |
| 借方 | Debit amount |
| 贷方 | Credit amount |
| 日期 (optional) | Transaction date |
| 凭证号 (optional) | Voucher number |

See `references/file_formats.md` for detailed format specifications and custom column configuration.

## Audit Objectives

The script performs four core audit objectives:

### 1. Balance Sheet Equilibrium Verification

**Formula**: 资产总计 = 负债总计 + 所有者权益总计

Verifies that the balance sheet is balanced overall.

### 2. Income Statement Verification

**Logic**: Income statement items = Corresponding detail summary

Validates each income statement item (revenue, expenses, etc.) against detail records.

### 3. Account Change Tracking

**Logic**: Opening Balance + Changes = Closing Balance

For each account:
- Asset accounts: Closing = Opening + Debit - Credit
- Liability/Equity accounts: Closing = Opening + Credit - Debit

### 4. Cross-Statement Relationship Validation

**Logic**: Retained earnings change ≈ Net profit

Validates relationships between balance sheet and income statement.

See `references/verification_rules.md` for detailed audit logic and troubleshooting.

## Audit Outputs

### Console Report

```
================================================================================
                              财务审计报告 - 本期
================================================================================

一、审计概述
--------------------------------------------------------------------------------
审计结果: 通过 ✓

二、资产负债表审计
--------------------------------------------------------------------------------
资产总计: ¥1,000,000.00
负债总计: ¥600,000.00
所有者权益总计: ¥400,000.00
资产负债平衡: 是 ✓

三、利润表审计
--------------------------------------------------------------------------------
利润项目匹配: 5/5

四、报表勾稽关系
--------------------------------------------------------------------------------
净利润: ¥100,000.00
未分配利润变动: ¥100,000.00
勾稽关系验证: 通过 ✓

五、不平衡项目清单
--------------------------------------------------------------------------------
  无不平衡项目
```

### Excel Audit Report

When `--output` is specified, generates an Excel file with these sheets:

| Sheet | Content |
|-------|---------|
| 审计报告 | Full audit report text |
| 科目变动分析 | Account analysis with opening/closing balances |
| 交易影响追踪 | Transaction impact tracking |
| 利润表核对 | Income statement verification results |
| 不平衡项 | List of unbalanced items |

### Account Change Analysis Table

| 科目 | 科目类型 | 期初余额 | 借方变动 | 贷方变动 | 净变动 | 期末余额 | 是否平衡 | 差异 |
|------|----------|----------|----------|----------|--------|----------|----------|------|
| 货币资金 | 资产 | 100000 | 20000 | 0 | 20000 | 120000 | 是 | 0 |

## Using the Script as a Module

```python
from scripts.reconcile import (
    audit_financial_statements,
    generate_audit_report,
    export_audit_report
)

result, accounts = audit_financial_statements(
    balance_sheet_file='balance_sheet.xlsx',
    account_changes_file='account_changes.xlsx',
    income_statement_file='income_statement.xlsx',
    income_details_file='income_details.xlsx',
    transactions_file='transactions.xlsx',
    tolerance=0.01,
    period='2024年1月'
)

# Print console report
print(generate_audit_report(result, period='2024年1月'))

# Export Excel report
export_audit_report(result, 'audit_report.xlsx', accounts, period='2024年1月')

# Check audit result
if result.is_passed:
    print("Audit passed!")
else:
    print(f"Found {len(result.unbalanced_items)} unbalanced items")
```

## Tolerance Setting

Default tolerance is ±0.01 yuan. Adjust with `--tolerance`:

```bash
scripts/reconcile.py \
    --balance-sheet bs.xlsx \
    --account-changes ac.xlsx \
    --tolerance 1.0
```

Consider these factors when setting tolerance:
- Exchange rate fluctuations (for foreign currency)
- System precision differences
- Rounding errors

## Troubleshooting

### Balance Sheet Not Balanced

**Possible causes**:
- Incorrect balance entries
- Incorrect totals calculation
- Opening/closing mismatch

**Solutions**:
1. Check balance sheet total rows
2. Verify account balances
3. Check account type classification

### Account Changes Unbalanced

**Possible causes**:
- Missing change records
- Incorrect debit/credit direction
- Account name mismatch

**Solutions**:
1. Ensure account names match exactly
2. Verify debit/credit records
3. Check for missing change records

### Income Statement Not Matching

**Possible causes**:
- Missing detail items
- Inconsistent item names
- Incorrect summary calculation

**Solutions**:
1. Ensure detail table includes all items
2. Check item name consistency
3. Verify summary calculations

### Cross-Statement Relationship Failed

**Possible causes**:
- Profit distribution (dividends, retained earnings)
- Mismatched accounting periods
- Incorrect net profit calculation

**Solutions**:
1. Consider profit distribution events
2. Verify income statement net profit
3. Confirm period consistency

## Resources

### scripts/reconcile.py
Core audit script supporting:
- Balance sheet equilibrium verification
- Income statement validation
- Account change tracking
- Cross-statement relationship validation
- Transaction impact tracing
- Comprehensive audit report generation

### references/file_formats.md
Detailed file format specifications, column name mapping, and configuration options.

### references/verification_rules.md
Comprehensive audit rules, validation logic, output examples, and troubleshooting guide.
