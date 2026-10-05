---
name: meteora
description: "Do anything on Meteora, Solana's liquidity layer: launch tokens on Dynamic Bonding Curves (DBC), create and manage DAMM v1/v2 and DLMM pools, add or remove liquidity, swap, place DLMM limit orders, claim fees, migrate DBC pools to DAMM, run alpha and presale vaults, lock tokens on vesting schedules, stake for fees (M3M3) or into LP farms, zap single tokens into and out of positions, split fees across wallets, and write TypeScript against Meteora SDKs. Use for any Meteora, meteora-invent, DBC, DLMM, DAMM, alpha vault, presale, token vesting, fee sharing, staking, farming, zap, or Solana liquidity/LP task — including building launchpads, trading bots, and integrations."
license: MIT
compatibility: "Requires Node.js 22.12+ and pnpm 10+ for the studio CLI path (repo enforces engine-strict), or Node.js 18+ with npm for standalone SDK code; network access to a Solana RPC; a funded keypair for on-chain writes."
metadata: {"version": "2.0.0", "author": "MeteoraAg", "openclaw": {"emoji": "🌊", "homepage": "https://github.com/MeteoraAg/meteora-invent", "requires": {"anyBins": ["pnpm", "npm"]}}, "hermes": {"category": "defi", "tags": ["solana", "meteora", "defi", "liquidity", "token-launch"]}}
---

# Meteora

Meteora is Solana's liquidity layer: bonding-curve token launches (DBC), constant-product AMMs
(DAMM v1/v2), bin-based concentrated liquidity with limit orders (DLMM), plus launch vaults.
This skill covers **doing actions on-chain** and **writing code against the SDKs**.

## Product Map

| Protocol | What it is | Choose when | SDK (pinned version) | Program ID (mainnet + devnet) |
|---|---|---|---|---|
| **DBC** | Virtual-liquidity bonding curve; token launches that graduate to an AMM | Launching a new token | `@meteora-ag/dynamic-bonding-curve-sdk@1.5.11` | `dbcij3LWUppWqq96dh6gJWwBifmcGfLSB5D4DuSMaqN` |
| **DAMM v2** | Constant-product AMM with position NFTs, fee schedulers, locks, farming | Pools for existing tokens; DBC graduation target (default) | `@meteora-ag/cp-amm-sdk@1.4.5` | `cpamdpZCGKUy5JxQXB4dcpGPiikHawvSWAd6mEn1sGG` |
| **DLMM** | Bin-based concentrated liquidity, dynamic fees, limit orders | Active LP strategies, capital efficiency, limit orders | `@meteora-ag/dlmm@1.9.14` | `LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo` |
| **DAMM v1** | Legacy dynamic AMM; LP tokens, lock escrows, Stake2Earn farms | Only for existing v1 pools or Stake2Earn/memecoin-v1 flows | `@meteora-ag/dynamic-amm-sdk@1.4.1` | `Eo7WjKq67rjJQSZxS6z3YkapzY3eMj6Xy8X5EQVn5UaB` |
| **Alpha Vault** | Anti-sniper launch deposit vault (FCFS/prorata) on DLMM/DAMM | Fair-launch allocation on a new pool | `@meteora-ag/alpha-vault@1.1.16` | `vaU6kP7iNEGkbmPkLmZfGwiGxd4Mob24QQCie5R9kd2` |
| **Presale Vault** | Generic presale with vesting | Presale before pool creation | `@meteora-ag/presale@0.1.1` | `presSVxnf9UU8jMxhgSMqaRwNiT36qeBdNeTRKjTdbj` |
| **Met Lock** | Standalone vesting/token-lock escrows (any SPL/Token-2022 mint) | Lock a team/creator allocation with a cliff + vesting schedule | `@meteora-ag/met-lock-sdk@1.0.1` | `LocpQgucEQHbqNABEYvBvwoxCPsSbG91A1QaQhQQqjn` |
| **Pool Farms** | DAMM v1 LP staking/reward farms | Stake DAMM v1 LP tokens to earn a separate reward token | `@meteora-ag/farming-sdk@1.0.18` | `FarmuwXPWXvefWUeqFAa5w6rifLkq5X6E8bimYvrhCB1` |

Compact SDK surfaces for the remaining products — Alpha Vault, Presale, Stake2Earn
(M3M3), Zap, Dynamic Vault, Dynamic Fee Sharing, Met Lock, Pool Farms — live in
`references/other-products.md` (deep docs: https://docs.meteora.ag/llms.txt).

## Decide the Path: ACT vs BUILD

**ACT — the user wants an outcome on-chain now** → use the **meteora-invent studio CLI**
(config-driven JSONC, `dryRun` simulation, devnet parity). Covers launches, migrations,
pool creation, seeding, vaults, locks — and swaps, position/status reads, and DLMM fee
claims on every protocol.

**BUILD — the user wants code, or a flow the studio doesn't have** → use the **SDKs
directly** with the pinned versions above. Required for: bots, backends, UIs, DLMM
add/remove/rebalance on existing positions, CP-AMM position ops on arbitrary pools, and
anything else not exposed as a studio action.

| Intent | Path | First action → then read |
|---|---|---|
| Wallet setup / get devnet SOL | ACT | `generate-keypair` → `airdrop-sol` (`references/studio-actions.md`) |
| Launch token on bonding curve | ACT | Run intake in `references/dbc.md` → `dbc-create-config` → `dbc-create-pool` (`references/studio-actions.md`) |
| Migrate graduated DBC pool | ACT | Check progress (`dbc-get-status`) → `dbc-migrate-to-damm-v2` (`references/studio-actions.md`) |
| Create DLMM/DAMM pool, seed liquidity | ACT | Edit the protocol config → `<protocol>-create-pool` → seed action (`references/studio-actions.md`) |
| Create an alpha/presale vault, a DAMM v1 lock escrow, or a Stake2Earn farm | ACT | `alpha-vault-create` / `presale-vault-create` / `damm-v1-lock-liquidity` / `damm-v1-create-stake2earn-farm` (`references/studio-actions.md`) |
| Participate in a launch vault (deposit / claim / refund) | ACT | `alpha-vault-deposit` → `alpha-vault-claim` (`references/studio-actions.md`) |
| Join / claim a presale (deposit, claim, refunds) | ACT | `presale-vault-deposit` → `presale-vault-claim` (`references/studio-actions.md`) |
| Lock/vest tokens for a recipient (cliff + vesting) | ACT | `lock-create-vesting-escrow` (`references/studio-actions.md`) |
| Stake for fees on a DAMM v1 memecoin pool (M3M3) | ACT | `stake2earn-stake` → `stake2earn-claim-fee` (`references/studio-actions.md`) |
| Stake DAMM v1 LP into a reward farm | ACT | `farm-stake` (`references/studio-actions.md`) |
| Earn lending yield on idle tokens (Dynamic Vault) | ACT | `vault-deposit` (`references/studio-actions.md`) |
| Split a fee stream between wallets (create/fund/claim fee vault) | ACT | `fee-sharing-create-vault` (`references/studio-actions.md`) |
| Enter/exit an LP position with a single token (zap) | ACT | `zap-in-damm-v2` / `zap-in-dlmm` / `zap-out` (`references/studio-actions.md` — DAMM v2 zap-in is direct-route only; DLMM zap-in is Jupiter-quoted, needs `JUPITER_API_KEY`/`JUPITER_API_URL` setup) |
| Swap / quote on any pool | ACT | Set the `<protocol>Swap` config block → `pnpm studio <protocol>-swap --poolAddress <POOL>` (dbc: `dbc-swap --baseMint`) |
| List positions, pool state, fees owed | ACT | `dlmm-get-positions` / `damm-v2-get-positions` / `dbc-get-status`, or REST (`references/data-and-apis.md`) |
| Claim DLMM fees + rewards | ACT | `pnpm studio dlmm-claim-fees --poolAddress <POOL>` |
| DLMM add/remove/rebalance an existing position | BUILD | Read `references/dlmm.md`, write against `@meteora-ag/dlmm@1.9.14` |
| Trading bot, backend, integration | BUILD | Read the protocol reference pack, then code against the pinned SDK |
| Launchpad / token UI | BUILD | `references/scaffolds.md` (fun-launch or custom via `references/dbc.md`) |
| Aggregated multi-DEX swap routing, DCA across venues | **Defer** | Jupiter APIs — not this skill |
| pump.fun launches, Raydium/Orca pools, generic wallet ops | **Defer** | Other tools/skills — not this skill |

## Protocol Decision Tree

```
New token to launch?
├─ Yes → DBC (bonding curve → auto-graduates to DAMM v2 by default)
│        Fair-launch allocation needed on the post-launch pool? → + Alpha Vault
│        Raise before any pool exists? → Presale Vault
└─ No, token already exists
   ├─ Passive/simple pool, position NFTs, fee scheduler → DAMM v2
   ├─ Concentrated liquidity, active strategy, limit orders → DLMM
   └─ Existing DAMM v1 pool / Stake2Earn farm → DAMM v1 (do not start new projects here)
```

## Intake: Collect Before Any On-Chain Write

Never guess these. Ask the owner (or read from an existing config) and restate what you will
do before doing it:

| Item | Rule |
|---|---|
| Network | Ask. Default **devnet** for first runs. Mainnet requires the gate below. |
| RPC URL | Default public endpoint for the chosen network; recommend Helius/QuickNode/Triton for mainnet. Config `rpcUrl`, never hardcoded in code. |
| Wallet | Ask: new wallet or existing? Either way the studio needs `PRIVATE_KEY` (base58) in `studio/.env` — `generate-keypair` only CONVERTS it to `studio/keypair.json` (+ optional devnet `--airdrop`); it does not create keys. New-wallet recipe: `studio-actions.md` §generate-keypair. Never print, log, or commit a private key. |
| Funding | Pool creation ~0.05 SOL, launches ~0.1 SOL recommended. Check first (`solana balance <PUBKEY> -u devnet`, or `connection.getBalance`); on devnet airdrop, on mainnet ask the owner to fund and confirm. |
| Amounts & units | Confirm token units vs lamports for every amount (studio configs use human units — except the presale-vault block, where supply and caps are raw base/quote units; SDKs use lamports/BN. This is the #1 footgun — trust each config field's comment). |
| Addresses | Any pubkey the owner must control (feeClaimer, leftoverReceiver, creator, recipient): ask, don't default silently. |
| Protocol params | Use the flow's intake contract in its reference file (e.g. DBC launch contract in `references/dbc.md`), applying documented defaults for anything unstated. |

**Gates (non-negotiable):**
1. First execution of any state-changing flow runs with `"dryRun": true` (ACT) or a
   simulation/quote (BUILD); show the owner the result. For actions that generate a fresh
   keypair (lock escrow, fee-sharing vault, stake2earn unstake account, zap position), the
   address a dry run prints is a throwaway placeholder — only save the address the real
   (`dryRun: false`) run prints.
2. Mainnet + real execution only after the owner explicitly confirms in this conversation.
3. After executing, verify on-chain (see Verification) and report addresses, costs, and
   next steps. Never claim success without verifying.

## ACT Quick Start (studio CLI)

```bash
# 0. Bootstrap: the toolkit is the meteora-invent repo
git clone https://github.com/MeteoraAg/meteora-invent && cd meteora-invent  # skip if present
pnpm install

# 1. Wallet: put PRIVATE_KEY (base58) in studio/.env — generate-keypair CONVERTS it
#    to studio/keypair.json (it does not create keys; new-wallet recipe in
#    references/studio-actions.md §generate-keypair)
pnpm studio generate-keypair --network devnet --airdrop

# 2. Configure by EDITING the protocol's fixed config file:
#    studio/config/<protocol>_config.jsonc (rpcUrl, dryRun, keypairFilePath,
#    computeUnitPriceMicroLamports, + protocol blocks). There is NO flag to pass a
#    different config file — flags only select targets (--baseMint / --poolAddress).
#    Commented templates identical to the real files: references/configs/*.jsonc

# 3. Dry-run (dryRun: true), review, flip to false, execute
pnpm studio <action> [--baseMint <MINT> | --poolAddress <POOL>]
```

All 81 actions with their real flags, config blocks, and outputs:
`references/studio-actions.md`. Environment details and wallet import:
`references/studio-setup.md`.

## BUILD Quick Start (SDKs)

Read the protocol reference pack first, then write code against the pinned SDK versions in
the Product Map (`npm install <pkg>@<pinned>` in a fresh project OUTSIDE the monorepo; run
TypeScript with `npx ts-node`, not tsx). Universal rules — all four SDKs:

1. **web3.js v1 only** (`Connection`, `Transaction`, `PublicKey`, `Keypair`). Never
   `@solana/kit` / web3.js v2 types.
2. **Anchor split:** DBC, DAMM v2, DLMM use Anchor **0.31**; DAMM v1 uses Anchor **0.29**.
   Don't mix DAMM v1 with the others in one package without dependency isolation.
3. **Everything returns unsigned transactions** — you attach blockhash, fee payer, and
   signers, then send. Some methods return `Transaction[]` or `{ transaction, keypairs }`
   (extra signers!) — check the reference before assuming a single `Transaction`.
4. **`CollectFeeMode` is a different enum in each SDK.** Never carry enums across packages.
5. **Amounts are `BN` in base units (lamports).** Convert with the token's decimals.
6. **Refresh before quoting:** DLMM `refetchStates()`, DAMM v1 `updateState()`; fetch fresh
   pool state in DBC/DAMM v2.
7. Pin the versions from the Product Map; the references document those exact APIs and the
   breaking changes around them ("version fences"). If installed versions are newer, check
   the SDK's CHANGELOG before trusting a snippet.

## Safety Invariants

- Devnet first; dry-run/simulate first; smallest viable amounts on first mainnet run.
- Verify every address the owner gives you on the explorer before using it.
- Secrets only in `.env` / keypair files; never in code, output, or commits.
- Set `computeUnitPriceMicroLamports` (studio) or a compute-budget instruction (SDK) —
  unprioritized transactions fail on busy mainnet.
- Slippage: set explicit `slippageBps`/min-out on every swap; never 0 or unlimited.

## Operating Rules

1. **Never fabricate progress.** Don't claim a transaction was sent, a pool was created,
   or fees were claimed unless you have a real signature or re-read on-chain state. If the
   runtime has no network/execution access, stop and hand the owner the exact commands to
   run locally instead.
2. **Key hygiene.** Never ask the owner to paste a raw private key or seed phrase into
   chat; never print secret values; refer to wallets by public address and to keys by file
   path or env-var name only.
3. **Fresh context policy.** The reference packs track the pinned SDK versions in the
   Product Map. If the installed version is newer, read the SDK's
   CHANGELOG/`docs.md` before trusting a snippet; fetched source beats this skill — follow
   it and note the mismatch. Deep, always-current reference: every docs.meteora.ag page
   serves raw markdown (index: https://docs.meteora.ag/llms.txt), and the docs are also
   exposed as a live MCP server at `https://docs.meteora.ag/mcp` — connect it when your
   runtime supports MCP for searchable, current documentation.
4. **Reuse what the owner already said.** Fill intake from their message first; ask only
   for missing required fields; confirm any normalization (addresses, amounts, units)
   before executing.

## Routing Table — read next

| Need | File |
|---|---|
| Any studio CLI action (flags, config fields, outputs) | `references/studio-actions.md` |
| Toolkit install, wallet setup, localnet | `references/studio-setup.md` |
| DBC: launch intake contract, curve modes, SDK surface, migration | `references/dbc.md` |
| DAMM v2: pools, positions, swaps, locks, fee modes | `references/damm-v2.md` |
| DLMM: bins/strategies, positions, swaps, limit orders, rebalance | `references/dlmm.md` |
| DAMM v1: pools, deposits, lock escrow, Stake2Earn | `references/damm-v1.md` |
| Keypairs, RPC, priority fees, send/confirm patterns | `references/wallets-and-txs.md` |
| Read-only data: REST APIs vs SDK state fetchers | `references/data-and-apis.md` |
| Errors → causes → fixes (all protocols) | `references/troubleshooting.md` |
| Launchpad UI / frontend templates | `references/scaffolds.md` |
| Ready-to-fill config templates | `references/configs/*.jsonc` |
| Alpha Vault / Presale / Stake2Earn / Zap / Dynamic Vault / Fee Sharing / Met Lock / Pool Farms SDK surfaces | `references/other-products.md` |

## Verification

After every state-changing action:

1. Confirm the transaction signature landed: explorer link `https://solscan.io/tx/<SIG>`
   (append `?cluster=devnet` on devnet) or `connection.confirmTransaction`.
2. Re-read state and check the expected change:
   - DBC: `pnpm studio dbc-get-status --baseMint <MINT>` (progress, migrated, reserves,
     fees) or `client.state.getPoolByBaseMint(mint)`.
   - DAMM v2: `cpAmm.fetchPoolState(pool)` / `getUserPositionByPool(pool, user)`.
   - DLMM: `dlmm.refetchStates()` → `getActiveBin()`, `getPositionsByUserAndLbPair(user)`.
   - DAMM v1: `pool.updateState()` → `poolInfo`, `getUserBalance(owner)`.
3. Report to the owner: what executed, tx signature(s), created addresses (mint, pool,
   position, config), cost in SOL, and the next step in the flow.

## Troubleshooting (top 5)

| Error | Fix |
|---|---|
| `Configuration validation failed` | JSONC syntax; all required fields for the chosen action; correct nesting (see `references/configs/`) |
| `Insufficient SOL balance` | Fund wallet / devnet airdrop; see min-SOL table in `references/studio-actions.md` |
| `Transaction simulation failed` | Read the program log lines below the error; usually wrong network, missing account, or slippage — see `references/troubleshooting.md` |
| Blockhash/timeout errors | Raise priority fee; use a premium RPC; re-send with fresh blockhash |
| TypeScript won't compile against an SDK | You're likely using a pre-2026 API from model memory — check the version fences in the protocol reference |

Full table: `references/troubleshooting.md`.
