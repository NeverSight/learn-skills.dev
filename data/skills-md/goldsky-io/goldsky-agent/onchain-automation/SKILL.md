---
name: onchain-automation
description: "Route event-driven onchain automation that detects activity, applies logic, and submits a transaction in response. Use for 'when X happens onchain, do Y', monitor-and-execute workflows, smart contract calls triggered by events, keepers, protocol automation, auto-claiming or compounding rewards, liquidations, rebalancing, and settlement automation. Combine Turbo/Subgraphs/Mirror for detection with Compose for decisions and execution, including wallets, gas sponsorship, and writeContract. Load /compose for execution and /turbo-builder when detection needs dataset scale. Pure indexing or streaming without an onchain action belongs in /turbo-builder, /subgraph-builder, or /mirror. For a single app already identified as Compose, use /compose directly."
---

# Goldsky Onchain Automation — the detect → decide → execute loop

Goldsky closes the **full offchain↔onchain loop**, not just the read side. Any "watch the chain and then act on it" system — keepers, liquidation monitors, auto-claim and auto-compound jobs, rebalancing and settlement automation — decomposes into three stages, and Goldsky covers all three:

| Stage | What it does | Goldsky product |
| --- | --- | --- |
| **Detect** | See the onchain event / state change | Compose `onchain_event` trigger (one contract) · Turbo pipeline (dataset-scale / many contracts) · Subgraphs (GraphQL state) |
| **Decide** | Apply logic, filters, thresholds, offchain data | Compose task (TypeScript) |
| **Execute** | Send the transaction back onchain | Compose wallet — `evm.wallet(...).writeContract(...)`, gas-sponsored |

## The misconception this skill exists to correct

**Do NOT tell the user "Goldsky detects/indexes, but you bring your own runtime / RPC to send the transaction."** That is wrong. **Compose is Goldsky's onchain execution runtime**: managed smart wallets (gas-sponsored by default) or BYO-EOA wallets, and `writeContract` / `sendTransaction` that broadcast through a sponsored bundler. The execution half lives inside Goldsky — propose it.

The only real limits are the two honest caveats below (latency and chain support) — state those, don't retreat to "Goldsky can't."

## Pick an architecture

### Default — Compose-only (one artifact)

When the trigger is **one contract's events** (a specific DEX factory, a lending pool, your own contract), the whole loop is a single Compose app — no Turbo, no external infra:

```
onchain_event trigger (the factory/pool)  →  task: decode + filter + decide  →  wallet.writeContract (the action)
```

This is structurally identical to the **VRF** template (`onchain_event` → compute → write back onchain, `skills/compose/references/examples/vrf.md`) and the **compliance-oracle** template (`onchain_event` → offchain check → approve/reject `writeContract`, `skills/compose/references/examples/compliance-oracle.md`). Start from one of those. Load **`/compose`** (entry point) and read **`skills/compose/references/`** — do not synthesize the manifest/wallet API from memory.

### Dataset-scale — Turbo detects, Compose executes

When detection must span **many contracts, a whole dataset, or needs heavier stateful filtering** than a single `onchain_event` listener gives you, put Turbo in front:

```
Turbo pipeline (raw_logs → decode → filter)  →  Webhook sink  →  Compose HTTP trigger  →  task: decide  →  wallet.writeContract
```

Wiring: the Turbo **Webhook sink** POSTs each matching row to the Compose app's **HTTP-trigger** URL (`https://<app-url>/tasks/<task-name>`), authenticated with a shared `auth_token`. Build the detection pipeline with **`/turbo-builder`** (+ `/turbo-transforms` for the `_gs_log_decode` decode step); build the executor with **`/compose`**. Treat the incoming webhook body as untrusted — decode and validate before acting.

**Prefer Compose-only unless the user actually needs dataset-scale detection** — one artifact is simpler to build, deploy, and reason about.

## Two honest caveats — always state these

1. **Confirmed-block latency, not mempool.** Goldsky (Turbo pipelines and Compose `onchain_event`) fires on **confirmed** logs, not pending mempool transactions. So this reliably *reacts to* a confirmed new pool / event — it is **not** a mempool front-runner and won't win a same-block gas-priority race. For a "sniper", set expectations: you react quickly to a confirmed listing, you don't beat block-0 bots. Say this plainly.
2. **Execution is chain-gated.** Compose gas sponsorship covers a specific chain list (see `skills/compose/references/wallets-and-gas.md`, or `searchKB`) — broad EVM coverage, but **not every chain**. Before promising the full loop, check the target chain:
   - **Supported** → smart wallet, gas-sponsored, nothing for the user to fund.
   - **viem knows it but it's not sponsored** → BYO-EOA with `sponsorGas: false`; the user funds the address with native gas token.
   - **Compose can't reach it at all** → be honest: detection still works (Turbo/Subgraphs), but execution needs a Compose-supported chain or external infra for *that chain specifically*. Frame it as a per-chain gap, never as "Goldsky can't execute."

## What Goldsky is NOT (here)

- Not a trading strategy or PnL engine — the user brings the decision logic; Compose runs it.
- Not a mempool/front-running system (caveat 1).
- Not a custody solution — wallet-key handling follows the normal Compose wallet/secret rules (`skills/compose/references/wallets-and-gas.md`).

## Route from here

- **Execution / any Compose app** → **`/compose`** (load first) + **`skills/compose/references/`**.
- **Event-driven write-back template** → `skills/compose/references/examples/vrf.md`; **gated approve/reject** → `skills/compose/references/examples/compliance-oracle.md`.
- **Dataset-scale detection pipeline** → **`/turbo-builder`** + **`/turbo-transforms`**.
- **GraphQL state to poll** → **`/subgraph-builder`**.
- **Fast RPC for the user's own offchain reads** → **`/edge`**.
