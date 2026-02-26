---
name: token-distribution
description: "For token distribution on Solana 5000x cheaper than SPL (rewards, airdrops, depins, ...). @lightprotocol/compressed-token (TypeScript). Reference examples for custom claim support."
metadata:
  source: https://github.com/Lightprotocol/skills
  documentation: https://www.zkcompression.com
  openclaw:
    requires:
      env: ["HELIUS_API_KEY"]
      bins: ["node"]
---

# Airdrop

Distribute compressed tokens to multiple recipients using TypeScript client.

> **Disclaimer:** This guide demonstrates efficient token distribution on Solana using ZK compression. It does not constitute financial advice and does not endorse any specific token or project.

## Workflow

1. **Clarify intent**
   - Recommend plan mode, if it's not activated
   - Use `AskUserQuestion` to resolve blind spots
   - All questions must be resolved before execution
2. **Identify references and skills**
   - Match task to [distribution approaches](#distribution-via-client) below
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

## Distribution via Client

| Scale | Approach |
|-------|----------|
| <10,000 recipients | Single transaction - see [simple-airdrop.md](references/simple-airdrop.md) |
| 10,000+ recipients | Batched with retry - see [batched-airdrop.md](references/batched-airdrop.md) |
| No-code | [Airship by Helius](https://airship.helius.dev/) (up to 200k) |

### Cost Comparison

| Creation          | Solana              | Compressed         |
| :---------------- | :------------------ | :----------------- |
| **Token Account** | ~2,000,000 lamports | **5,000** lamports |

## Claim Program Reference Implementations

Customize token distribution and let users claim.

Simple Implementation: [simple-claim](https://github.com/Lightprotocol/program-examples/tree/main/airdrop-implementations/simple-claim) - Distributes compressed tokens that get decompressed on claim.

Advanced Implementation: [distributor](https://github.com/Lightprotocol/distributor/tree/master) - Distributes SPL tokens, uses compressed PDAs to track claims. Based on jito Merkle distributor.



|  | distributor | simple-claim |
|--|-------------|--------------|
| Vesting | Linear Vesting | Cliff at Slot X |
| Partial claims | Yes | No |
| Clawback | Yes | No |
| Frontend | REST API + CLI | None |

The programs are reference implementations and not audited. The Light Protocol Programs are audited and live on Solana Mainnet.

### Cost

|                          |    Per-claim | 100k claims |
|--------------------------|-------------:|------------:|
| simple-claim             | ~0.00001 SOL |      ~1 SOL |
| distributor (compressed) | ~0.00005 SOL |      ~5 SOL |
| distributor (original)   |   ~0.002 SOL |    ~200 SOL |

## Core Pattern

```typescript
import { CompressedTokenProgram, getTokenPoolInfos, selectTokenPoolInfo } from "@lightprotocol/compressed-token";
import { bn, createRpc, selectStateTreeInfo, buildAndSignTx, sendAndConfirmTx } from "@lightprotocol/stateless.js";
import { ComputeBudgetProgram } from "@solana/web3.js";

const rpc = createRpc(RPC_ENDPOINT);

// 1. Get infrastructure
const treeInfo = selectStateTreeInfo(await rpc.getStateTreeInfos());
const tokenPoolInfo = selectTokenPoolInfo(await getTokenPoolInfos(rpc, mint));

// 2. Build compress instruction (SPL → compressed to multiple recipients)
const ix = await CompressedTokenProgram.compress({
  payer: payer.publicKey,
  owner: payer.publicKey,
  source: sourceAta.address,           // SPL associated token account holding tokens
  toAddress: recipients,                // PublicKey[]
  amount: recipients.map(() => bn(amount)),
  mint,
  tokenPoolInfo,
  outputStateTreeInfo: treeInfo,
});

// 3. Send with compute budget (120k CU per recipient)
const instructions = [
  ComputeBudgetProgram.setComputeUnitLimit({ units: 120_000 * recipients.length }),
  ix,
];
const { blockhash } = await rpc.getLatestBlockhash();
const tx = buildAndSignTx(instructions, payer, blockhash, []);
await sendAndConfirmTx(rpc, tx);
```

## Setup: Create Mint

```typescript
import { createMint } from "@lightprotocol/compressed-token";
import { getOrCreateAssociatedTokenAccount, mintTo } from "@solana/spl-token";

const { mint } = await createMint(rpc, payer, payer.publicKey, 9);
const ata = await getOrCreateAssociatedTokenAccount(rpc, payer, mint, payer.publicKey);
await mintTo(rpc, payer, mint, ata.address, payer.publicKey, 100_000_000_000);
```

## Compute Units

| Recipients/instruction | CU |
|----------------------|-----|
| 1 | 120,000 |
| 5 | 170,000 |
| Batched tx | 500,000 |

## Lookup Tables

Reduce transaction size:

| Network | Address |
|---------|---------|
| Mainnet | `9NYFyEqPkyXUhkerbGHXUXkvb4qpzeEdHuGpgbgpH1NJ` |
| Devnet | `qAJZMgnQJ8G6vA3WRcjD9Jan1wtKkaCFWLWskxJrR5V` |

## Advanced: Claim-Based

For vesting, clawback, or user-initiated claims:

| Implementation | Features |
|---------------|----------|
| [Merkle Distributor](https://github.com/Lightprotocol/distributor) | Linear vesting, partial claims, clawback, REST API |
| [Simple Claim](https://github.com/Lightprotocol/program-examples/tree/main/airdrop-implementations/simple-claim) | Cliff vesting at slot X |

## Resources

- **Docs**: [Airdrop Guide](https://www.zkcompression.com/compressed-tokens/airdrop)
- **Code**: [examples-light-token](https://github.com/Lightprotocol/examples-light-token)
- **Tool**: [Airship by Helius](https://airship.helius.dev/)

## SDK references

| Package | Link |
|---------|------|
| `@lightprotocol/stateless.js` | [API docs](https://lightprotocol.github.io/light-protocol/stateless.js/index.html) |
| `@lightprotocol/compressed-token` | [API docs](https://lightprotocol.github.io/light-protocol/compressed-token/index.html) |


## Security

This skill provides code patterns and documentation references only.

- **Declared dependencies.** Reference examples require `HELIUS_API_KEY` (RPC provider key) and a payer keypair for signing transactions. Neither is needed for read-only or localnet testing. In production, load both from a secrets manager — never hard-code private keys.
- **Filesystem scope.** `Read`, `Glob`, and `Grep` must be limited to the current project directory and skill references. Do not read outside these paths.
- **Subagent scope.** When stuck, the skill asks to spawn a read-only subagent with `Read`, `Glob`, `Grep` scoped to skill references, example repos, and docs.
- **Install source.** `npx skills add Lightprotocol/skills` from [Lightprotocol/skills](https://github.com/Lightprotocol/skills).
- **Audited protocol.** Light Protocol smart contracts are independently audited. Reports are published at [github.com/Lightprotocol/light-protocol/tree/main/audits](https://github.com/Lightprotocol/light-protocol/tree/main/audits).
