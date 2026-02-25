---
name: fund-wallet
description: Get instructions for funding your AgnicPay wallet with USDC. Use when you or the user want to add funds, deposit USDC, top up the wallet, or need more balance. Covers phrases like "add funds", "deposit", "top up", "fund my wallet", "how do I get USDC", "need more balance".
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx agnic@latest status*)", "Bash(npx agnic@latest address*)", "Bash(npx agnic@latest balance*)"]
---

# Funding the AgnicPay Wallet

Provide instructions for adding USDC to the user's AgnicPay wallet on Base.

## Confirm wallet is initialized and authed

```bash
npx agnic@latest status
```

If the wallet is not authenticated, refer to the `authenticate-wallet` skill.

## Get Wallet Address

```bash
npx agnic@latest address
```

This displays the user's wallet address on each supported network.

## Funding Options

### Option 1: AgnicPay Dashboard (Recommended)

1. Go to [pay.agnic.ai](https://pay.agnic.ai)
2. Sign in with the same account used in the CLI
3. Navigate to the dashboard
4. Use the **"Add Funds"** button to deposit USDC via card, bank transfer, or crypto

### Option 2: Direct USDC Transfer

Send USDC directly to the wallet address on **Base network**:

1. Get the address: `npx agnic@latest address`
2. From any wallet (MetaMask, Coinbase, Phantom, etc.), send USDC on **Base** to that address
3. Verify arrival: `npx agnic@latest balance --network base`

**Important**: Send USDC on **Base network** only. USDC on other chains (Ethereum mainnet, Arbitrum, etc.) will not appear in the AgnicPay balance.

### Option 3: Bridge from Another Chain

If the user has USDC on Ethereum, Arbitrum, or Optimism, they can bridge to Base using:
- [bridge.base.org](https://bridge.base.org) (official Base bridge)
- Any cross-chain bridge that supports Base

## Verify Balance

After funding, confirm the deposit arrived:

```bash
npx agnic@latest balance --network base
```

## Important Notes

- AgnicPay wallets use **USDC** (not ETH) for payments and trading
- **Base network** is the primary chain
- Minimum recommended balance: **$1.00 USDC** for testing
- Small amounts of ETH on Base may be needed for gas (auto-handled in most cases)

## Prerequisites

- Must be authenticated (`npx agnic@latest status` to check)

## Error Handling

Common errors:

- "Not authenticated" — Run `npx agnic@latest auth login` first
- Balance shows 0 after transfer — Verify the transfer was on Base network (not Ethereum mainnet)
- Transfer pending — Base transactions typically confirm in 2-3 seconds
