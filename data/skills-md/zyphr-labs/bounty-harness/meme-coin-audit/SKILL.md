---
name: meme-coin-audit
description: Meme coin and token security audit — rug pull detection (honeypot, hidden mint, fee manipulation, LP lock bypass), Solana SPL token analysis (freeze authority, mint authority, metadata mutability), Token-2022 extension risks (transfer hooks, permanent delegate), DEX liquidity pool attacks (sandwich amplification, LP drain, bonding curve exploits), pump.fun/Raydium/Jupiter integration risks, token_scanner.py automation, and real exploit examples from 2024-2025. Use for any token audit, rug pull assessment, meme coin security review, or pre-investment due diligence.
---

# MEME COIN & TOKEN SECURITY AUDIT

## Overview

Fast-kill rug pull detection and deep token security analysis for EVM and
Solana meme coins. The one rule: **"Check ALL authorities and owner functions.
The retained authority IS the rug vector."** Every rug pull requires a
privileged operation: mint, blacklist, fee change, LP removal, or authority
abuse. Find the privilege, find the bug.

> Safety: static source analysis is `passive`. On-chain verification
> (Solscan/Etherscan authority checks, DEX pool inspection, PoC execution)
> is `intrusive` — require explicit authorization.

## Quick Reference

### Hard kills (skip immediately)

- Contract not verified on Etherscan/Solscan → cannot audit source
- Deployer wallet has a history of rug pulls
- Token age < 1 hour AND no known team
- Mint authority retained (Solana) AND no cap → infinite mint = certain rug
- Freeze authority retained (Solana) on a meme coin → honeypot confirmed
- Transfer hook present (Token-2022) with mutable hook program → honeypot vector
- Permanent delegate extension (Token-2022) → can steal all holder tokens

### Soft kills (proceed with extreme caution)

- Top holder > 20% of supply (excluding DEX pools)
- LP not burned or locked in a verified contract
- Contract is upgradeable / proxy with retained admin
- Less than $5K liquidity in the pool
- No social presence / anonymous deployer with no history

### Bug classes

| # | Class | Share of rugs |
|---|---|---|
| 1 | Hidden mint / unlimited supply | 35% |
| 2 | Honeypot / transfer restriction | 25% |
| 3 | Fee manipulation | 20% |
| 4 | Liquidity pool drain | — |
| 5 | Bonding curve manipulation | — |
| 6 | Authority retention (Solana) | — |
| 7 | Fake renounce / hidden ownership | — |
| 8 | Sandwich amplification by design | — |

## Workflow Selection

| Situation | Workflow |
|---|---|
| Static token source review (EVM or Solana) | `token-scan` |
| Retained-authority grep across sources | `scripts/authority_check.py` |
| On-chain authority / LP / holder verification | manual (intrusive — `runbooks/onchain-checks.md`) |

## Available Workflows

### token-scan
Runs the token red-flag scanner (8 bug classes via regex) over Solidity or
Rust/Anchor token sources. Passive — local files only, no API calls.

```
python3 .claude/skills/meme-coin-audit/scripts/token_scanner.py \
  "${CONTRACTS_DIR:?Set CONTRACTS_DIR}" --recursive > $OUTDIR/web3/token_scan.txt
```

Outputs: `$OUTDIR/web3/token_scan.txt`. Safety tier: passive.

## Evidence Required

| Artifact | File |
|---|---|
| Token scanner report | `$OUTDIR/web3/token_scan.txt` |
| Authority grep output | `$OUTDIR/web3/authority_check.txt` |
| On-chain state (intrusive): mint/freeze authority, LP lock, holder dist | `evidence/<finding>/onchain.json` |

## References

- Scanner limitations: it does NOT check on-chain state, holder distribution,
  LP lock status, or deployer history — those are manual (intrusive) checks
- Solana quick checks: `runbooks/onchain-checks.md`
- Token exploits Foundry template: `runbooks/token-exploit-poc.md`
- Pre-dive kills: `runbooks/kill-signals.md`
- Scanner usage: `runbooks/token-scan.md`
- Redaction policy: evidence stays local-only under `$OUTDIR`; redact wallet
  addresses, RPC endpoints, and any private keys before committing.
