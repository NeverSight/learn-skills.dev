---
name: walletconnect-staking
description: Manages the walletconnect-staking CLI for WCT token staking on Optimism. Use when the user wants to stake WCT, unstake, claim rewards, check staking status, or view WCT balance.
---

# WalletConnect Staking CLI

## Goal

Operate the `walletconnect-staking` CLI to stake/unstake WCT tokens, claim staking rewards, and check positions on Optimism (chain ID 10).

## When to use

- User asks to stake WCT tokens
- User asks to unstake or withdraw staked WCT
- User asks to claim staking rewards
- User asks about their staking position, APY, or rewards
- User asks about their WCT token balance
- User mentions `walletconnect-staking` or WCT staking

## When not to use

- User wants basic wallet connection without staking (use `walletconnect` skill)
- User is working on the staking-cli source code (just edit normally)
- User wants to interact with WCT on a chain other than Optimism

## Prerequisites

- Project ID must be configured for write commands (stake, unstake, claim). Set globally with `walletconnect config set project-id <id>` or override per-command with `WALLETCONNECT_PROJECT_ID` env var.
- Binary is at `packages/staking-cli/dist/cli.js` (or globally linked as `walletconnect-staking`)
- Build first if needed: `npm run build -w @walletconnect/staking-cli`

## Commands

```bash
# Stake WCT — locks tokens for N weeks
walletconnect-staking stake <amount> <weeks>

# Unstake — withdraw all (only after lock expires)
walletconnect-staking unstake

# Claim staking rewards
walletconnect-staking claim

# Check staking position, rewards, APY (read-only)
walletconnect-staking status --address=0x...

# Check WCT balance (read-only)
walletconnect-staking balance --address=0x...
```

## Default workflow

### For write commands (stake, unstake, claim)
1. Ensure project ID is configured (`walletconnect config get project-id`)
2. Run the command — CLI auto-restores session or prompts QR connection
3. The session must include Optimism (eip155:10). If the existing session doesn't, the CLI disconnects and requests a new one
4. Inform the user to confirm the transaction in their wallet app
5. Use 60s+ timeout for all wallet interaction commands

### For read-only commands (status, balance)
1. Use `--address=0x...` to skip wallet connection entirely
2. Or let the CLI restore an existing session for the address
3. No project ID needed when using `--address`

## Important notes

- **Optimism only**: All transactions happen on Optimism (chain ID 10)
- **Lock duration**: Stake lock time is rounded down to the nearest week boundary
- **Approve flow**: `stake` automatically checks allowance and sends an approve tx first if needed
- **Existing position**: `stake` detects existing positions and calls `updateLock` instead of `createLock`
- **Unlock check**: `unstake` refuses to run if the lock hasn't expired yet
- **Read-only shortcut**: `status` and `balance` work with just `--address=0x...`, no wallet connection needed
- **APY formula**: `APY = max((stakeWeight / 1M) * -0.06464 + 12.0808, 0)`, adjusted by `min(weeks, 104) / 52`

## Validation checklist

- [ ] Project ID is configured (`walletconnect config get project-id`) for write commands
- [ ] Binary is built and linked (`walletconnect-staking --help` works)
- [ ] Wallet session includes Optimism chain approval
- [ ] Transaction output (tx hash) is shown to the user
- [ ] Timeouts are 60s+ for wallet interaction commands
- [ ] For read-only queries, `--address` is used when no session is needed

## Examples

### Stake 100 WCT for 4 weeks
```
User: "Stake 100 WCT for a month"
Action: Run `walletconnect-staking stake 100 4`
Note: May send 2 transactions (approve + createLock/updateLock). Inform user to confirm each.
```

### Check staking status
```
User: "What's my staking position for 0xABC...?"
Action: Run `walletconnect-staking status --address=0xABC...`
Note: No project ID or wallet connection needed.
```

### Check WCT balance
```
User: "How much WCT do I have?"
Action: Run `walletconnect-staking balance --address=0x...`
Note: If no address provided, ask the user for one or use an existing session.
```
