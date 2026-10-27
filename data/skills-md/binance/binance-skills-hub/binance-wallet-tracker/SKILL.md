---
name: binance-wallet-tracker
description: |
  Wallet tracking and monitoring on Binance Web3. Monitor token/trade activity for private groups
  or public Smart Money/KOL data. Four domains: (A) Discovery — consensus, pioneer,
  leaderboard diff, token buyer lookup, time-window summaries, similar wallets; (B) Evaluation —
  token risk (tokenRiskLevel ≥ 3), group rhythm, follow list assessment, token heat; (C) Replay —
  4h summary, Accumulation/Distribution, sector rotation, anomaly orders, round-trip, first-mover/leader-follower,
  wake-up, bot-like; (D) Management — group create/rename, batch import, label update, link, follow list;
  (E) Real-time — WebSocket push for Smart Money, KOL, wallet-level, and address-level trade events.
  Trigger on: wallet tracker, monitoring, consensus, pioneer, accumulation, Distribution, Sector Rotation, Anomaly Large Order,
  round-trip, first-mover, wake-up, bot-like, token risk, token heat, group profile, similar wallets,
  group management, address import, follow list, real-time push, WebSocket — even without "tracker" explicitly.
metadata:
  author: binance-web3-team
  version: "1.3"
  requiredCliVersion: '1.9.1'
  openclaw:
    requires:
      bins:
        - baw
    install:
      - kind: node
        package: '@binance/agentic-wallet'
        bins: [baw]
        label: Install Binance Agentic Wallet CLI (npm)
---

# Binance Wallet Tracker Skill

On-chain wallet tracking and monitoring. Monitor token-level and trade-level activity for private groups or public Smart Money / KOL data. Includes 9 built-in analysis scenarios for replay and pattern detection.

## Prerequisites

This skill requires the `baw` CLI (`@binance/agentic-wallet` npm package). If `baw` is not found:

```bash
npm install -g @binance/agentic-wallet
```

Verify: `baw --version` should print `1.6.2` or higher. If installation fails or the user doesn't have Node.js, inform them that Node.js >= 18 is required.

## When to Use

### Discovery

| User intent | Command |
|-------------|---------|
| Consensus tokens (many buyers) | `tracker token query` → sort by `consensusCount` |
| Pioneer tokens (≤2 traders) | `tracker token query` → filter `launchTime` + `consensusCount ≤ 2` |
| Leaderboard diff (untracked wallets) | `leaderboard query` (leaderboard skill) + `tracker address list` → diff |
| Token-based buyer lookup | `tracker tx query` → client-side filter by `ca` |
| Time-window summary | `tracker token query --period 4h` + `tracker tx query` |
| Similar wallet discovery | `leaderboard analyze` (leaderboard skill) → archetype matching |

### Evaluation

| User intent | Command |
|-------------|---------|
| Token risk screening | `tracker token query` → filter `tokenRiskLevel ≥ 3` + `consensusCount ≥ 3` |
| Group rhythm profiling | `tracker tx query` → per-address rhythm analysis |
| Follow list assessment | `tracker follow` + `leaderboard analyze` (cross-skill) |
| Token heat analysis | `tracker tx query` → aggregate by `ca` |

### Replay

| User intent | Command |
|-------------|---------|
| 4h comprehensive summary | `tracker token query --period 4h` + `tracker tx query` |
| Accumulation vs distribution (Accumulation/Distribution) | `tracker token query` → `buyCount`/`sellCount` per address |
| Sector rotation | `tracker tx query` → compare token top across time windows |
| Anomaly large orders | `tracker tx query` → `anomaly` detection |
| Round-trip (Round-Trip) | `tracker tx query` → `round-trip` detection |
| First-mover + leader-follower | `tracker tx query` → `first-mover` + `leader-follower` |
| Wake-up detection | `tracker tx query` → `wake-up` detection |
| Bot-like behavior | `tracker tx query` → `bot-like` detection |

Full 9-scenario analysis rules: [`references/analytics.md`](references/analytics.md)

### Management

| User intent | Command |
|-------------|---------|
| Create / rename group | `tracker group create/update` |
| Batch import addresses | `tracker address batch` |
| Add single address | `tracker address add` |
|| Update label / link to group | `tracker address update -l` + `tracker address link` |
| Delete addresses | `tracker address delete` |
| Follow / unfollow address | `tracker address follow/unfollow` |
| View follow list | `tracker follow` |
| Search address (fuzzy) | `tracker address search` |

## Supported Chains

| Chain | chainId |
|-------|---------|
| BSC | `56` |
| Solana | `CT_501` |
| Base | `8453` |
| Ethereum | `1` |
| Robinhood | `4663` |

This table lists chains verified for tracker use; it is a subset of `baw wallet chains` (which returns all wallet-supported chains, e.g. Arbitrum 42161, Polygon 137). Before treating a chain as unsupported for tracking, probe it first — the wallet chain list is dynamic.

## Command Tree

```
baw tracker
  token query                # Token dimension monitor (private + --tag-type for public)
  tx query                   # Trade dimension monitor (private + --tag-type for public)
  follow                     # Query current user follow list (read-only, chainId only)
  ws                         # WebSocket real-time push (--smy/--kol/--wallet/--address/--following)
  group
    list                     # Group list
    create                   # Create group
    update                   # Rename group
  address
    search                   # Fuzzy search address
    list                     # Paginated address list
    add                      # Add single address (wraps import)
    batch                    # Batch import
    update                   # Update label (label only)
    link                     # Link to group (group/link)
    delete                   # Delete (supports batch)
    follow                   # Follow address
    unfollow                 # Unfollow
```

All commands support `--json` for structured output.

**`token query` and `tx query` require either `--group-id` (private group) or `--tag-type` (public KOL/SMY). Calling without either returns an error.**

**`--tag-type` accepts: `kol` (KOL), `smy` (Smart Money).**

## Token Monitor (A2)

```bash
# Private — own group data (must specify --group-id or --tag-type)
baw tracker token query -c 56 --group-id 1 --json
baw tracker token query -c 56 --group-id 1 --period 4h --json

# Public — SMY/KOL data
baw tracker token query -c 56 --tag-type kol --json   # KOL
baw tracker token query -c CT_501 --tag-type smy --json  # Smart Money
```

Returns per-token aggregated data: token name, CA, price, market cap, volume, `addressList[]` (per-address buy/sell/inflow), `launchTime`, `tokenRiskLevel`, `tokenTag`.

**Consensus computation**: The API does NOT return top-level `traderNum` or `inFlow`. The CLI aggregates `consensusCount` = `addressList.length`, `netInflow` = Σ `addressList[].inflow`, `countBuy`/`countSell` = Σ buy/sell counts. Use these fields directly.

**Per-address fields**: `address`, `label`, `buyCount`, `sellCount`, `inflow`, `tokenQty`, `latestTxTime`, `lastTrade`, `addressLogoUrl`.

Full parameter and return field reference: [`references/cli.md`](references/cli.md)

## Tx Monitor (A3)

```bash
# Private — own group trade flow
baw tracker tx query -c 56 --group-id 1 --json

# Public — SMY/KOL trade flow
baw tracker tx query -c 56 --tag-type smy --json

# Filter by trade side (19=buy, 11=first-buy, 29=sell, 21=clear)
baw tracker tx query -c 56 --group-id 1 --trade-side 19 --json
```

Returns per-trade records: `txHash`, `logId`, `address`, `ts`, `tradeSideCategory`, `txUsdValue`, `tokenPrice`, `currentPrice`, `ca`, `tokenName`, `marketCap`, `tokenRiskLevel`, `tokenTag`, plus optional `toAddress`, `toLabel`, `nativePrice`, `txNativeTokenQty`, `tokenDecimals`, `tokenSupply`, `launchTime`, `rwaType`.

**⚠️ Critical: `ts` is in SECONDS (not milliseconds)** — 10-digit Unix timestamp. All time-window calculations (round-trip <1h, wake-up >72h, co-buy 10min window) must use seconds. A2's `latestTxTime`/`launchTime` ARE in milliseconds (13-digit).

**No pagination** — returns all matching records in one response.

**ca/address filtering (Skill responsibility)**: The A3 API does NOT accept `ca` or `address` as filter parameters. The Skill handles this filtering: fetch all records from `tx query`, then filter by matching `ca` (contract address) or `address` (wallet) in the results. This enables the core scenario "who in a group is buying a specific token" — fetch the group's full trade flow, then filter by `ca`.

## Follow Query (A4)

```bash
# Query current user's follow list (chainId only)
baw tracker follow -c 56 --json
```

Returns a map where key = followed address, value = `{label}`.

**Limitation**: Only queries the **current user's** follow list. You cannot query another user's follow list. For "evaluate follow list" scenarios, combine with `binance-leaderboard` skill's `leaderboard analyze` to score each followed address.

## Group Management (B1)

```bash
# List groups (displayOrder: All=-1, Default=0, others sequential)
baw tracker group list -c 56 --json

# Create group
baw tracker group create -c 56 -n "Base-Sniper" --json

# Rename group
baw tracker group update -c 56 -g 1 -n "NewName" --json

# Note: group delete is not available in the CLI. Groups can only be created and renamed.
```

**Group fields**: `groupId`, `groupName`, `addressCount`, `displayOrder`. Sort groups by `displayOrder`: All=-1, Default=0, others sequential.

## Address Management (B2)

```bash
# Fuzzy search
baw tracker address search -c 56 -g 1 -a 0xabc --json

# Paginated list
baw tracker address list -c 56 -g 1 --page 1 --size 20 --json

# Single add (wraps import with enforce=false)
baw tracker address add -c 56 -g 1 -a 0xabc --label "Whale1" --json

# Batch import (comma-separated addresses or JSON array of {address,label})
baw tracker address batch -c 56 -g 1 -a 0xabc,0xdef --json
# Or with labels: -a '[{"address":"0xabc","label":"Whale1"},{"address":"0xdef"}]'

# Update label only (groupId is deprecated for update)
baw tracker address update -c 56 -a 0xabc --label "NewLabel" --json

# Link to another group
baw tracker address link -c 56 -a 0xabc -g 2 --json

# Delete (comma-separated addresses)
baw tracker address delete -c 56 -g 1 -a 0xabc,0xdef -y --json

# Follow / unfollow
baw tracker address follow -c 56 -g 1 -a 0xabc --label "Follow1" --json
baw tracker address unfollow -c 56 -a 0xabc --json
```

**Import defaults**: `allowOverwrite` defaults to `true` (overwrites existing label). `enforce` defaults to `false`. Use `--no-overwrite` to disable overwrite.

**Follow response**: Returns `{address, followed: true}` — NO `groupId` field. `followed` is a boolean status flag.

**Address search/list fields**: Returns `address`, `label`, `emoji`, `color`, `groupId`, `groupName`, `isFollowed`, `addressLogoUrl`, `genericAddressTagList`, `lastActiveTime`, `nativeTokenQty`.

Full parameter and return field reference: [`references/cli.md`](references/cli.md)

## Core Rules

### Consensus & Inflow Computation (A2)

The API does NOT return top-level `traderNum`, `inFlow`, `countBuy`, or `countSell` fields. The CLI aggregates these from `addressList[]` and exposes them as:
- **`consensusCount`** (Consensus) = `addressList.length`
- **`netInflow`** (Net Inflow) = Σ `addressList[].inflow`
- **`countBuy`** (accumulation count) = Σ `addressList[].buyCount`
- **`countSell`** (distribution count) = Σ `addressList[].sellCount`

Use these CLI-aggregated fields directly — no need to re-compute from `addressList`.

### Accumulation vs Distribution

`buyCount` and `sellCount` are returned per-address directly. No need to aggregate `tradeSideCategory` — use these fields directly for Accumulation/Distribution analysis.

### Client-Side Filtering (Skill responsibility)

The A2/A3 APIs do NOT accept `ca` or `address` as filter parameters. The `caList` param on A2 token/query is accepted but silently ignored by the backend. The Skill handles this filtering:
1. Fetch all records via `token query` or `tx query` (no ca/address filter)
2. Filter by matching `ca` (contract address) or `address` (wallet) in the results

This enables core scenarios like "who in a group is buying a specific token" — fetch the group's full trade flow, then filter by `ca`.

This affects: Find Buyers by Token (co-buy), token-based buyer lookup, and any scenario requiring single-token or single-address focus.

### Follow List Limitation (A4)

`tracker follow` only queries the **current user's** follow list (chainId only, no address param). You cannot evaluate another user's follow list. For "evaluate follow list" scenarios, combine with `binance-leaderboard` skill's `analyze` command.

### Group Field Names

`group list` returns `displayOrder`. Sort groups by `displayOrder`: All=-1, Default=0, others sequential.

**Follow Response Fields**

`address follow` response returns `{address, followed: true}`. `followed` is a boolean status flag.

### Write-Back Confirmation

After any write operation (create/update/delete/import/follow/unfollow/link), re-fetch the affected resource to confirm the operation succeeded — this guards against `agentSessionId` silent expiry and backend silent failures.

**Readback failure handling**: If readback shows the operation didn't take effect (e.g. address still exists after delete, group not found after create), tell the user "Operation may not have taken effect, please try again later" — never mention backend bugs, silent failures, or error codes.

### Destructive Operation Safety

Delete, link, and unfollow operations require `-y` flag (or interactive confirmation) before execution. Always confirm with the user before executing destructive operations.

### EVM Address Case Normalization (delete only)

The backend stores EVM addresses as lowercase (import API lowercases them), but `address/delete` does case-sensitive matching. If the user provides an EIP-55 mixed-case address (e.g. `0x52908400098527886E0F7030069857D03E3248B4`), delete will silently fail — return `success:true` without actually deleting. The CLI does NOT normalize; it passes through as-is.

**Skill responsibility**: Before calling `baw tracker address delete`, normalize EVM addresses to lowercase:
- EVM (`0x` + 40 hex): `address.toLowerCase()`
- Solana (Base58, case-sensitive): pass through as-is — do NOT lowercase

This is verified against QA: import with mixed case stores as lowercase, delete with lowercase succeeds, delete with mixed case returns `success:true` but address remains.

### Batch Import Behavior

`address batch` / `address add`:
- `allowOverwrite` defaults to `true` — existing labels are overwritten
- `enforce` defaults to `false` — skips validation enforcement
- Chain is specified by `-c` — CLI does NOT auto-detect address format
- **Cross-chain auto-dispatch (Skill responsibility)**: When the user provides a mixed list of EVM + Solana addresses, the Skill must:
  1. Classify each address by format:
     - EVM: matches `^0x[a-fA-F0-9]{40}$` → chainId `56` (BSC) or `8453` (Base) — determine by user context or ask
     - Solana: Base58, 32-44 chars, no `0x` prefix → chainId `CT_501`
  2. Group addresses by chain
  3. Call `baw tracker address batch -c <chainId>` once per group
  4. Aggregate results (new/exist/overwrite counts) across all chains

### Real-Time Monitoring (WebSocket)

| User intent | Command |
|-------------|---------|
| Real-time Smart Money buy/sell signals | `tracker ws --smy --duration 15` |
| Real-time KOL activity on a chain | `tracker ws --kol -c <chainId> --duration 15` |
| Chain-level wallet activity (multi-chain) | `tracker ws --wallet BSC,SOL --duration 15` |
| Monitor specific address trades | `tracker ws --address <addr> -c <chainId> --duration 15` |
| Batch address monitoring (file) | `tracker ws --address-list <file> -c <chainId> --duration 15` |
| Monitor my followings' activity | `tracker ws --following -c <chainId> --duration 15` |

`tracker ws` subscribes to WSP WebSocket push events. It streams real-time trade data (buys, sells, price changes) for the selected scope. In `--json` mode, only push messages are written to stdout (no meta info), enabling pipeline processing with `| jq`.

**`--duration` is required unless the user explicitly asks for an unlimited stream.** Extract the duration from the user's instruction when available (e.g. "monitor for 60 seconds" → `--duration 60`). If no duration is specified, default to `--duration 15`.

> **`--following` tip**: When the followed address list is large, the CLI may fall back to a broader chain-level stream. If the user only wants events for their followed addresses, filter push messages by `address` against the follow list (`tracker follow -c <chainId> --json`).

### Limitations

- **Token price change**: `token/query` may not reliably return `priceChangeRate` for all tokens. For reliable price data, use marketCap + risk + pioneer timing as proxy.
- **Time window filtering**: `token/query` has a `period` param (1m/5m/1h/4h/24h), but granular time-window queries (e.g., "past 4h") rely on client-side aggregation of `tx/query` `ts` fields.
- **A4 Follow read-only**: `tracker follow` only queries the current user's own follow list. Follow/unfollow writes use `address follow`/`unfollow` commands (B2).

## 9 Analysis Scenarios (A3)

Built-in analysis patterns for `tracker tx query` data. Full rules and algorithms: [`references/analytics.md`](references/analytics.md)

| Scenario | Detection Rule |
|----------|----------------|
| rhythm | Per-address count/buys/sells/mean_usd/active hours |
| anomaly | `txUsdValue > 3×mean` and `> 500` |
| co-buy | Same `ca`, ≥3 buyers within 10min window |
| round-trip | Same address same `ca`, buy→sell < 1h |
| rotation | Token top diff across time windows |
| first-mover | Earliest buyer of a `ca` |
| leader-follower | Median delay after first-mover |
| wake-up | New activity after >72h gap |
| bot-like | Low interval variance + high night ratio + low amount dispersion |

## Error Codes

Error codes are for internal lookup only — never show numeric codes or internal names to users. Translate to natural-language messages.

| Code | Internal Name | User-Facing Message |
|------|---------------|---------------------|
| 70001001 | TRACKER_API_ERROR | Query failed, please try again later |
| 70002001 | TRACKER_GROUP_NOT_FOUND | Group not found |
| 70002002 | TRACKER_GROUP_EXISTS | Group already exists |
| 70002003 | TRACKER_GROUP_LIMIT | Group limit reached |
| 70003001 | TRACKER_ADDRESS_NOT_FOUND | Address not found |
| 70003002 | TRACKER_ADDRESS_EXISTS | Address already exists |
| 70003003 | TRACKER_ADDRESS_INVALID | Invalid address format |

## Display Templates

**Consensus token**:
```
📊 Consensus Tokens Top 5
{tokenName} | Consensus: {consensusCount} | Net Inflow: ${netInflow} | Accumulation: {countBuy} | Distribution: {countSell} | Liquidity: {volume} | Risk: {riskLevel}
```

**Trade flow entry**:
```
{ts} | {label} | {tradeSideLabel} {tokenName} | ${txUsdValue} | Price: {tokenPrice} → {currentPrice}
```

**Group info**:
```
{groupName} ({addressCount}addresses)
```

## User-Facing Presentation

This skill serves end users, not developers. Internal field names, error codes, and CLI internals must never appear in user-facing output.

**1. Term Mapping (internal → user-facing)**

| Internal value | User-facing term | Notes |
|----------------|-------------------|-------|
| `tradeSideCategory: 11` | First Buy | |
| `tradeSideCategory: 19` | Buy | |
| `tradeSideCategory: 21` | Clear Position | |
| `tradeSideCategory: 29` | Sell | |
| `tradeSideCategory: other` | Unknown Trade Type | May include undocumented values |
| `tokenRiskLevel: 0-2` | Low Risk | |
| `tokenRiskLevel: 3-5` | High Risk | ≥3 = high risk |
| `groupId` | (omit) | Never show in user-facing output |
| `displayOrder` | (omit) | Never show in user-facing output |
| `ca` (in display) | (omit unless asked) | Use `{tokenName}` as primary identifier |
| `address` (in display) | `{label}` | Use label, not raw address |

Raw enum values (`19`, `11`, etc.) may appear in CLI syntax examples and internal lookup tables, but never in user-facing replies.

**2. Never expose internal identifiers**

- `groupId`, `displayOrder` — internal IDs, never shown to users
- Error codes (`70001001`, etc.) — translate to natural-language messages only
- Backend behavior details (e.g. delete silently failing on case mismatch, preset save not persisting) — never mention "backend bug" or "silent failure"; handle gracefully with readback

**3. Display template hygiene**

Use user-facing terms in all output. The `tradeSideCategory` field should be translated to its display term (Buy, Sell, etc.) — never show the raw numeric value. `tokenRiskLevel` should be shown as Low Risk/High Risk, not as a number. `groupId` and `displayOrder` should not appear in display templates.

## Full CLI Reference

- [`references/cli.md`](references/cli.md) — All commands with parameter tables, return field tables, and examples
- [`references/analytics.md`](references/analytics.md) — 9 analysis scenarios with detection rules and algorithms
