---
name: stacking
description: "STX stacking operations on Stacks — query PoX cycle info, check stacking status, lock STX to earn BTC rewards (stack-stx), and extend an existing stacking lock period. Write operations require an unlocked wallet."
metadata:
  author: "whoabuddy"
  author-agent: "Trustless Indra"
  user-invocable: "false"
  arguments: "get-pox-info | get-stacking-status | stack-stx | extend-stacking"
  entry: "stacking/stacking.ts"
  mcp-tools: "get_pox_info, get_stacking_status, stack_stx, extend_stacking"
  requires: "wallet"
  tags: "l2, write, requires-funds"
---

# Stacking Skill

Provides Proof of Transfer (PoX) stacking operations on the Stacks blockchain. Stacking locks STX tokens for a specified number of reward cycles to earn Bitcoin rewards.

- **get-pox-info** and **get-stacking-status** — Read-only, no wallet required.
- **stack-stx** and **extend-stacking** — Write operations, require an unlocked wallet.

## Usage

```
bun run stacking/stacking.ts <subcommand> [options]
```

## Subcommands

### get-pox-info

Get current Proof of Transfer (PoX) cycle information, including current and next cycle details, minimum stacking amount, and cycle lengths.

```
bun run stacking/stacking.ts get-pox-info
```

Output:
```json
{
  "network": "testnet",
  "currentCycle": {
    "id": 88,
    "min_threshold_ustx": 50000000000,
    "stacked_ustx": 1200000000000,
    "is_pox_active": true
  },
  "nextCycle": {
    "id": 89,
    "min_threshold_ustx": 50000000000,
    "min_increment_ustx": 5000000000,
    "stacked_ustx": 0,
    "prepare_phase_start_block_height": 3450,
    "blocks_until_prepare_phase": 25,
    "reward_phase_start_block_height": 3500,
    "blocks_until_reward_phase": 75,
    "ustx_until_pox_rejection": 0
  },
  "minAmountUstx": 50000000000,
  "rewardCycleLength": 2100,
  "prepareCycleLength": 100,
  "currentBurnchainBlockHeight": 3425,
  "totalLiquidSupplyUstx": 1400000000000000
}
```

### get-stacking-status

Check if an address is currently stacking STX.

```
bun run stacking/stacking.ts get-stacking-status [--address <addr>]
```

Options:
- `--address` (optional) — Stacks address to check (uses active wallet if omitted)

Output:
```json
{
  "address": "SP2...",
  "network": "testnet",
  "stacked": true,
  "amountMicroStx": "100000000000",
  "amountStx": "100000",
  "firstRewardCycle": 85,
  "lockPeriod": 3,
  "unlockHeight": 6300
}
```

### stack-stx

Lock STX tokens to earn Bitcoin rewards via Proof of Transfer. Requires an unlocked wallet with sufficient STX.

The Bitcoin reward address must be provided as a version byte and hash. For P2PKH (legacy Bitcoin address), version is `0`. For P2SH, version is `1`. For P2WPKH (native SegWit), version is `4`.

```
bun run stacking/stacking.ts stack-stx \
  --amount <microStx> \
  --pox-address-version <version> \
  --pox-address-hashbytes <hex> \
  --start-burn-height <btcBlockHeight> \
  --lock-period <cycles>
```

Options:
- `--amount` (required) — Amount of STX to stack in micro-STX (1 STX = 1,000,000 micro-STX). Must meet the minimum stacking threshold.
- `--pox-address-version` (required) — Bitcoin address version byte: `0` (P2PKH), `1` (P2SH), `4` (P2WPKH), `5` (P2WSH), `6` (P2TR)
- `--pox-address-hashbytes` (required) — Bitcoin address hash bytes as a hex string (20 bytes for P2PKH/P2SH/P2WPKH, 32 bytes for P2WSH/P2TR)
- `--start-burn-height` (required) — Bitcoin block height at which stacking begins (must be in a prepare phase or the first block of a reward phase)
- `--lock-period` (required) — Number of reward cycles to lock STX (1–12)

Output:
```json
{
  "success": true,
  "txid": "abc123...",
  "stacker": "SP2...",
  "amount": "100000000000",
  "lockPeriod": 3,
  "startBurnHeight": 850000,
  "network": "testnet",
  "explorerUrl": "https://explorer.hiro.so/txid/abc123...?chain=testnet"
}
```

### extend-stacking

Extend an existing stacking lock period by additional reward cycles. Must already be stacking. Requires an unlocked wallet.

```
bun run stacking/stacking.ts extend-stacking \
  --extend-count <cycles> \
  --pox-address-version <version> \
  --pox-address-hashbytes <hex>
```

Options:
- `--extend-count` (required) — Number of additional reward cycles to lock (1–12)
- `--pox-address-version` (required) — Bitcoin address version byte (same as used when initially stacking)
- `--pox-address-hashbytes` (required) — Bitcoin address hash bytes as a hex string (same as used when initially stacking)

Output:
```json
{
  "success": true,
  "txid": "abc123...",
  "stacker": "SP2...",
  "extendCount": 2,
  "network": "testnet",
  "explorerUrl": "https://explorer.hiro.so/txid/abc123...?chain=testnet"
}
```

## Notes

- The minimum stacking amount varies by cycle. Use `get-pox-info` to check `minAmountUstx` before calling `stack-stx`.
- Bitcoin reward addresses are specified as version + hashbytes (raw hash, not base58check encoded). To derive these from a Bitcoin address, use a library or the `wallet` skill's `get-taproot-address` for Taproot addresses.
- `lock-period` of 1–12 cycles is valid. Each cycle is typically ~2 weeks on mainnet.
- `start-burn-height` must fall within the prepare phase of the current PoX cycle. Check `nextCycle.prepare_phase_start_block_height` from `get-pox-info`.
- Wallet operations require an unlocked wallet (use `bun run wallet/wallet.ts unlock` first).
