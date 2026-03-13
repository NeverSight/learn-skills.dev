---
name: fund-wallet
description: Add funds to the wallet. Use when you or the user want to fund, deposit, top up, load, add funds, onramp, buy crypto, or get tokens into the wallet. Also use when the wallet has insufficient balance for a send, swap, or DeFi operation, or when someone asks "how do I get funds?" or "how do I add money?".
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(fdx status*)", "Bash(fdx call getWalletOverview*)", "Bash(fdx call getMyInfo*)"]
---

# Funding the Wallet

The Finance District wallet can be funded in two ways: through the web interface (credit card / onramp) or by direct token transfer to the wallet address from another wallet or exchange.

## Confirm wallet is authenticated

```bash
fdx status
```

If the wallet is not authenticated, refer to the `authenticate` skill.

## Get the Wallet Address

First, retrieve the wallet address that funds should be sent to:

```bash
fdx call getWalletOverview
```

This returns wallet addresses for all supported chains. Share the appropriate address with the human based on which chain they want to fund.

For a specific chain:

```bash
fdx call getWalletOverview --chainKey ethereum
```

## Funding Methods

### Method 1: Web Interface (Credit Card / Onramp)

The Finance District platform provides a web-based onramp where users can purchase crypto with credit cards or other payment methods.

**Tell your human:** "You can fund your wallet through the Finance District web interface at the platform dashboard. You'll be able to use a credit card or other payment methods to purchase tokens directly into your wallet."

### Method 2: Direct Transfer

The human can send tokens from any other wallet or exchange directly to their Finance District wallet address.

**Tell your human:** "You can send tokens from any wallet or exchange to your Finance District wallet address. Here's your address on [chain]: [address]."

Provide the correct wallet address for the chain they want to fund. Remind them to double-check the chain matches — sending tokens on the wrong chain may result in lost funds.

## Checking Balance After Funding

Once the human confirms they have sent funds:

```bash
fdx call getWalletOverview --chainKey <chain>
```

Note that transaction confirmation times vary by chain:

- **Ethereum**: ~12 seconds per block, but may take a few minutes for finality
- **Polygon/Base/Arbitrum**: Typically faster, a few seconds
- **Solana**: Near-instant
- **Exchange withdrawals**: May take additional time due to exchange processing

## Flow

1. Check authentication with `fdx status`
2. Get wallet addresses with `fdx call getWalletOverview`
3. Share the appropriate address with the human
4. Guide them to use the web onramp or direct transfer
5. After they confirm funding, verify balance with `fdx call getWalletOverview --chainKey <chain>`

## Prerequisites

- Must be authenticated (`fdx status` to check, see `authenticate` skill)

## Notes

- The wallet supports all EVM chains and Solana — make sure the human sends tokens on the correct chain
- There is no CLI command for direct onramp; funding requires the human to take action outside the CLI
- If the human wants to move funds between chains within their wallet, that's a transfer operation — see the `send-tokens` skill
