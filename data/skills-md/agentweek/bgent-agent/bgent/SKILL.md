---
name: bgent
description: Run BGENT rounds on BNB Smart Chain with a Binance Agentic Wallet that holds a Binance Wallet Agent ID (.ai). Instant results, unlimited rounds with dynamic difficulty, claim any time. Use when the user wants to explore for BGENT, check or claim BGENT, or list, open or transfer a BGENT Sealed Block.
---

# Bgent (Binance Agents only)

BGENT rewards can only be earned by Binance Agents. The BgentWorld contract checks on chain that the calling wallet owns a
**Binance Wallet Agent ID (.ai)**, the soulbound SPACE ID Agent ID NFT `0x60B9262456dE011F7d15a54CdD8c48bAaa8B022F`
claimed in the Binance App's Agentic Wallet. Every transaction is signed by the user's Binance Agentic Wallet through the
official `baw` CLI. Any other wallet is rejected by the contract.

All logic is in `bgent.mjs` (Node.js 18+, no npm packages; reads use Foundry's `cast`). Addresses: `deployments.json`.

## Who can take part (enforced by the contract)

- The caller must be the current owner of an Agent ID (`ownerOf(agentId) == caller`).
- An Agent ID binds permanently to the first wallet that uses it, and a wallet binds to only one Agent ID.
  Agent IDs are non-transferable; even if one moved, the new holder could not use it here.
- Rewards are credited to the Agent ID and paid only to its bound wallet.

## Requirements (check in this order; stop and tell the user what is missing)

1. Binance Agentic Wallet skill installed: `npx skills add binance/binance-skills-hub/skills/binance-web3/binance-agentic-wallet`
   (provides `baw`). Signed in: `baw auth signin` and scan the QR code in the Binance App.
2. Developer Mode enabled in the Binance App (Agentic Wallet settings), required for custom contract calls.
3. An Agent ID (.ai) claimed from the Agentic Wallet banner in the Binance App.
4. A little BNB on the Agentic Wallet's BSC address for gas (about 0.00001 BNB per round, two transactions).
5. Foundry `cast` for reads: `curl -L https://foundry.paradigm.xyz | bash && ~/.foundry/bin/foundryup`.

Run `node bgent.mjs setup --name <their .ai name without .ai>`. It checks all of the above and remembers the Agent ID.

## Commands

- `node bgent.mjs explore` runs one round. The result is decided two blocks later from a block hash nobody knew when the
  round was sent, and is credited at once.
- `node bgent.mjs auto --interval <minutes>` keeps running rounds. Before starting, tell the user the interval and the
  expected daily gas (about 0.00001 BNB per round).
- `node bgent.mjs status` shows claimable BGENT, today's rounds, active days and current difficulty.
- `node bgent.mjs claim` pays all earned BGENT to the Agentic Wallet.
- `node bgent.mjs blocks` lists the Sealed Blocks this wallet holds, with tier and value range.
- `node bgent.mjs open --id <id>` opens a Sealed Block the wallet owns (two transactions, about 2 seconds apart).
- `node bgent.mjs send --id <id> --to <address>` moves an unopened Sealed Block to another BNB Chain wallet, for example
  the user's own wallet to keep or sell it. Always confirm the exact destination address with the user first; transfers
  cannot be undone. Any wallet can open a block with the `open.html` page in this repository.
- `--risk 0|1|2` selects steady (always x1), balanced (50% x1.96) or aggressive (20% x4.75). Default 0.

When a round finds a Sealed Block, tell the user its tier and value range; they may open it, or keep, transfer or sell
it as an NFT. Whoever owns it when it is opened receives the BGENT.

## Rules for the agent

- Every transaction goes through `baw contract-call preview` then `execute`. Show the user what is being signed when
  they ask; if the Binance App requires confirmation, tell them to confirm there.
- Never ask for seed phrases or private keys. The Agentic Wallet is keyless (MPC); nothing secret is stored by this skill.
- There is no guaranteed return. Difficulty rises as more Agents take part, and a daily emission cap applies.
