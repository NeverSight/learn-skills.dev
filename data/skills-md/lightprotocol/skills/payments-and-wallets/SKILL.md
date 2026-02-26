---
name: payments-and-wallets
description: "For stablecoin payment flows and wallet integrations on Solana 200x cheaper token accounts. Receive, send, balance, history, and client-side signing with Privy and Solana wallet adapters. Optional guide to add nullifiers to prevent payments from being executed more than once."
metadata:
  source: https://github.com/Lightprotocol/skills
  documentation: https://www.zkcompression.com
  openclaw:
    requires:
      env: ["HELIUS_RPC_URL"]  # Required for all examples
      # Privy signing flow only (sign-with-privy.md): PRIVY_APP_ID, PRIVY_APP_SECRET, TREASURY_WALLET_ID, TREASURY_AUTHORIZATION_KEY — get these at privy.io
      bins: ["node", "cargo"] # node for TS client, cargo for Rust nullifier example
---

# Payments and wallets

Build payment flows and wallet integrations using light-token on Solana. The light-token API matches SPL-token and extends it to include the light token program.

| Creation cost     | SPL                 | light-token          |
| :---------------- | :------------------ | :------------------- |
| **Token Account** | ~2,000,000 lamports | ~**11,000** lamports |

## Workflow

1. **Clarify intent**
   - Recommend plan mode, if it's not activated
   - Use `AskUserQuestion` to resolve blind spots
   - All questions must be resolved before execution
2. **Identify references and skills**
   - Match task to [domain references](#domain-references) below
   - Locate relevant documentation and examples
3. **Write plan file** (YAML task format)
   - Use `AskUserQuestion` for anything unclear — never guess or assume
   - Identify blockers: permissions, dependencies, unknowns
   - Plan must be complete before execution begins
4. **Execute**
   - Use `Task` tool with subagents for parallel research
   - Subagents load skills via `Skill` tool
   - Track progress with `TodoWrite`
5. **When stuck**: ask to spawn a read-only subagent with `Read`, `Glob`, `Grep`, and DeepWiki MCP access, loading `skills/ask-mcp`. Scope reads to skill references, example repos, and docs.

## API overview

| Operation | SPL | light-token (action / instruction) |
|-----------|-----|-------------------------------------|
| Receive | `getOrCreateAssociatedTokenAccount()` | `loadAta()` / `createLoadAtaInstructions()` |
| Transfer | `createTransferInstruction()` | `transferInterface()` / `createTransferInterfaceInstructions()` |
| Get balance | `getAccount()` | `getAtaInterface()` |
| Tx history | `getSignaturesForAddress()` | `rpc.getSignaturesForOwnerInterface()` |
| Wrap from SPL | N/A | `wrap()` / `createWrapInstruction()` |
| Unwrap to SPL | N/A | `unwrap()` / `createUnwrapInstructions()` |
| Register SPL mint | N/A | `createSplInterface()` / `LightTokenProgram.createSplInterface()` |
| Create mint | `createMint()` | `createMintInterface()` |

Plural functions (`createTransferInterfaceInstructions`, `createUnwrapInstructions`) return `TransactionInstruction[][]` — each inner array is one transaction. They handle loading cold accounts automatically.

## Domain references

| Task | Reference |
|------|-----------|
| Build payment flows (receive, send, balance, history, wrap/unwrap) | [payments.md](references/payments.md) |
| Build wallet UI (display tokens, transfer, wrap/unwrap) | [wallets.md](references/wallets.md) |
| Sign with Wallet Adapter or Mobile Wallet Adapter | [sign-with-adapter.md](references/sign-with-adapter.md) |
| Sign with Privy (embedded wallet provider) | [sign-with-privy.md](references/sign-with-privy.md) |
| Prevent duplicate actions (double-spend prevention) | [nullifiers.md](references/nullifiers.md) |

## Setup

```bash
npm install @lightprotocol/compressed-token@beta @lightprotocol/stateless.js@beta @solana/web3.js @solana/spl-token
```

```typescript
import { createRpc } from "@lightprotocol/stateless.js";
import {
  createLoadAtaInstructions,
  loadAta,
  createTransferInterfaceInstructions,
  transferInterface,
  createUnwrapInstructions,
  unwrap,
  getAssociatedTokenAddressInterface,
  getAtaInterface,
  wrap,
} from "@lightprotocol/compressed-token/unified";

const rpc = createRpc(RPC_ENDPOINT);
```

## Resources

- [Payments docs](https://zkcompression.com/light-token/toolkits/for-payments)
- [Wallets docs](https://zkcompression.com/light-token/toolkits/for-wallets)
- [GitHub examples](https://github.com/Lightprotocol/examples-light-token/tree/main/toolkits/payments-and-wallets)
- [Nullifier program](https://github.com/Lightprotocol/nullifier-program/)

## SDK references

| Package | Link |
|---------|------|
| `@lightprotocol/stateless.js` | [API docs](https://lightprotocol.github.io/light-protocol/stateless.js/index.html) |
| `@lightprotocol/compressed-token` | [API docs](https://lightprotocol.github.io/light-protocol/compressed-token/index.html) |
| `@lightprotocol/nullifier-program` | [npm](https://www.npmjs.com/package/@lightprotocol/nullifier-program) |

## Security

The Privy signing examples transmit secrets to an external API — review [sign-with-privy.md](references/sign-with-privy.md) before running.

- **Declared dependencies.** `HELIUS_RPC_URL` is required for all examples. The Privy signing flow additionally requires `PRIVY_APP_ID`, `PRIVY_APP_SECRET`, `TREASURY_WALLET_ID`, and `TREASURY_AUTHORIZATION_KEY` — get these at [privy.io](https://privy.io). Load secrets from a secrets manager, not agent-global environment.
- **Privy signing flow.** `PRIVY_APP_SECRET` and `TREASURY_AUTHORIZATION_KEY` are sent to Privy's signing API. Verify these only reach Privy's official endpoints. See [sign-with-privy.md](references/sign-with-privy.md).
- **Subagent scope.** When stuck, the skill asks to spawn a read-only subagent with `Read`, `Glob`, `Grep` scoped to skill references, example repos, and docs.
- **Install source.** `npx skills add Lightprotocol/skills` from [Lightprotocol/skills](https://github.com/Lightprotocol/skills).
- **Audited protocol.** Light Protocol smart contracts are independently audited. Reports are published at [github.com/Lightprotocol/light-protocol/tree/main/audits](https://github.com/Lightprotocol/light-protocol/tree/main/audits).
