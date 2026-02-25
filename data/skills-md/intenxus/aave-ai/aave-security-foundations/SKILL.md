---
name: aave-security-foundations
description: Security baseline for AAVE integration and execution scripts. Use when user asks for AAVE security review, pre-trade checks, liquidation safety, allowance minimization, or execution hardening.
license: MIT
metadata:
  author: AAVE AI Contributors
  version: 1.0.0
---

# AAVE Security Foundations

Security-first checklist for AAVE script development and operations.

## Threat Areas

- Over-approval risk: unlimited ERC20 approvals can expose wallet funds.
- Health factor drift: market volatility can liquidate leveraged positions quickly.
- Interest rate mode mismatch: stable mode assumptions can fail per asset.
- RPC/data inconsistency: stale or failing RPC can produce bad decisions.
- Execution race conditions: quote-time assumptions may be invalid at execution.

## Required Pre-Execution Checks

1. Validate chain/token/account/amount format.
2. Read reserve status (`isActive`, `isFrozen`, `borrowingEnabled`).
3. Read account health (`healthFactor`, `availableBorrowsBase`).
4. Enforce HF safety threshold before `withdraw` and aggressive `borrow`.
5. Reject execution if allowance/balance preconditions fail.

## References

- `references/audit-checklist.md`
- `references/common-failures.md`
