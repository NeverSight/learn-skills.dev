---
name: web3-audit
description: Smart contract security audit — 10 DeFi bug classes (accounting desync, access control, incomplete path, off-by-one, oracle, ERC4626, reentrancy, flash loan, signature replay, proxy), pre-dive kill signals (TVL < $500K etc), Foundry PoC template, grep patterns for each class, and real Immunefi paid examples. Use for any Solidity/Rust contract audit or when deciding whether a DeFi target is worth hunting.
---

# WEB3 SMART CONTRACT AUDIT

## Overview

10 bug classes. Pre-dive kill signals. Foundry PoC template. Real paid examples.
This skill supports static source review of Solidity/Rust contracts (passive)
and, with explicit scope, on-chain interaction (intrusive). Workflows run the
static scanners; manual deep dives follow the per-class methodology.

> Safety: local/static analysis is `passive`. Anything touching a live chain
> (fork tests, on-chain authority checks, PoC execution) is `intrusive` and
> requires program authorization + scope confirmation.

## Quick Reference

### Pre-dive kill signals (check BEFORE any code review)

1. **TVL < $500K** → max payout capped too low for effort
2. **2+ top-tier audits** (Halborn, ToB, Cyfrin, OpenZeppelin) on simple protocol → bugs already found
3. **Protocol < 500 lines, single A→B→C flow** → minimal attack surface
4. **Formula**: `max_realistic_payout = min(10% × TVL, program_cap)` — if < $10K, skip

**Soft kill:** OZ/ToB/Cyfrin audit on current version + codebase > 500K LOC → expect 40+ hours for maybe 1 finding. Only proceed if bounty floor > $50K AND you have protocol-specific expertise.

**Target scoring (go if >= 6/10):**
- TVL > $10M: +2
- Immunefi program with Critical >= $50K: +2
- No top-tier audit on current version: +2
- < 30 days since deploy: +1
- Protocol you've hunted before: +1
- Source code + natspec comments: +1
- Upgradeable proxies: +1

### The one rule

> "Read ALL sibling functions. If `vote()` has a modifier, check `poke()`, `reset()`, `harvest()`. The missing modifier on the sibling IS the bug."

### Bug classes (with share of Criticals on Immunefi)

| # | Class | Share |
|---|---|---|
| 1 | Accounting state desynchronization | 28% of Criticals |
| 2 | Access control | 19% of Criticals |
| 3 | Incomplete code path | 17% of Criticals |
| 4 | Off-by-one / boundary | 22% of Highs |
| 5 | Oracle / price manipulation | 12% of all reports |
| 6 | ERC4626 vault attacks | — |
| 7 | Reentrancy | since 2016 |
| 8 | Flash loan attacks | — |
| 9 | Signature replay | — |
| 10 | Proxy / upgrade issues | — |

## Workflow Selection

| Situation | Workflow |
|---|---|
| Static review of a contracts directory | `audit-contract` |
| Token-specific rug-vector scan (EVM + Solana) | `token-scan` |
| Foundry PoC template | `runbooks/foundry-poc.md` |
| Deep dive per bug class | `runbooks/bug-classes.md` (grep patterns) |

## Available Workflows

### audit-contract
Runs the class-pattern grep audit over a Solidity contracts directory
(accounting desync, access control, incomplete path, off-by-one, oracle,
ERC4626, reentrancy, signature replay, proxy). Passive — local files only.

```
python3 .claude/skills/web3-audit/scripts/sol_pattern_scan.py \
  --dir "${CONTRACTS_DIR:?Set CONTRACTS_DIR}" > $OUTDIR/web3/contract_scan.txt
```

### token-scan
Runs the token red-flag scanner (8 meme-coin bug classes) over Solidity or
Rust/Anchor token sources. Passive — regex analysis of local files only.

```
python3 .claude/skills/web3-audit/scripts/token_scanner.py \
  "${CONTRACTS_DIR:?Set CONTRACTS_DIR}" --recursive > $OUTDIR/web3/token_scan.txt
```

## Evidence Required

| Artifact | File |
|---|---|
| Pattern-scan output grouped by bug class | `$OUTDIR/web3/contract_scan.txt` |
| Token scanner report | `$OUTDIR/web3/token_scan.txt` |
| Vulnerable code snippet with line numbers | in finding report |
| Foundry PoC (chain interaction = intrusive) | `evidence/<finding>/poc.sol` |

## References

- Grep patterns per class: `runbooks/bug-classes.md`
- Foundry PoC template + cheatcodes: `runbooks/foundry-poc.md`
- Immunefi report format: `reporting/platform-templates/immunefi.md`
- Real paid examples: Wormhole $10M (uninitialized UUPS proxy), Parity $150M frozen (no access control on initWallet)
- Redaction policy: scan output stays local-only under `$OUTDIR`; redact any
  RPC URLs, keys, or addresses you consider sensitive before committing.
