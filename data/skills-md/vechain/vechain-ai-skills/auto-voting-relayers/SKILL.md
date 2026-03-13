---
name: auto-voting-relayers
description: "Complete domain knowledge for VeBetterDAO's auto-voting and relayer system. Use when working on relayer dashboard, relayer node, auto-voting contracts (XAllocationVoting, VoterRewards, RelayerRewardsPool), or anything related to relayers, auto-voting, gasless voting, or relayer rewards. Triggers on: relayer, auto-voting, autovoting, gasless voting, relayer rewards, RelayerRewardsPool, castVoteOnBehalfOf, relayer dashboard, relayer node, veDelegate comparison."
allowed-tools: []
license: MIT
metadata:
  author: VeChain
  version: "0.1.0"
---

# VeBetterDAO Auto-Voting & Relayer System

Complete domain knowledge for the auto-voting and relayer ecosystem. This skill provides context for working on any component of the system: smart contracts, relayer node, relayer dashboard, or documentation.

## System Overview

VeBetterDAO's auto-voting system lets users automate their weekly X Allocation voting. Users pick favorite apps once, toggle auto-voting on, and relayers (off-chain services) handle the rest: casting votes, claiming rewards, all gasless. Relayers earn a fee from the reward pool. Tokens never leave the user's wallet.

Auto-voting applies **only to X Allocation rounds**. Governance proposals remain manual-only.

## Architecture

```text
Users (toggle auto-voting, set preferences)
    |
    v
Smart Contracts (on-chain logic)
    - XAllocationVoting (v8): auto-voting state, vote execution
    - VoterRewards (v6): reward claiming, fee deduction
    - RelayerRewardsPool (v1): relayer registration, reward distribution
    |
    v
Relayer Nodes (off-chain execution)
    - relayer-node/ (standalone CLI, no monorepo dependency)
    - Monitor rounds, batch vote/claim, loop every 5 min
    |
    v
Relayer Dashboard (monitoring/analytics)
    - apps/relayer-dashboard/ (static Next.js, GitHub Pages)
    - Round analytics, relayer stats, ROI tracking
```

## How It Works (Non-Technical)

### For Users

1. Hold 1+ VOT3, complete 3+ sustainable actions, pass VeBetterPassport
2. Choose up to 15 apps, toggle auto-voting on
3. Takes effect next round (not current)
4. Each week: relayer votes for you, claims your rewards to your wallet
5. Fee: 10% of rewards (max 100 B3TR/week) - covers all gas costs
6. While active: no manual voting/claiming allowed
7. Manual claim fallback: available 5 days after round end if relayer hasn't processed

### Auto-Disable Triggers

- VOT3 drops below 1
- All selected apps become ineligible
- Sustainable action threshold not met
- Bot detection by app owner

### For Relayers

1. Register on-chain by calling registerRelayer() on RelayerRewardsPool (open to anyone)
2. Run relayer-node with wallet (MNEMONIC or RELAYER_PRIVATE_KEY)
3. Node auto-discovers users, batches votes + claims
4. Earn weighted points: vote = 3 pts, claim = 1 pt
5. After ALL users served, claim proportional share of reward pool
6. All-or-nothing: if any user missed, nobody gets paid

### Apps as Relayers

Apps can register as relayers, ask users to set them as preference, and run a node. They earn relayer fees instead of paying veDelegate for votes. Important: apps should ADD themselves to preference lists, not replace other apps.

## vs veDelegate

| Feature | veDelegate | VeBetterDAO Auto-Voting |
| --- | --- | --- |
| X Allocation voting | Yes | Yes |
| Governance voting | Yes (always "abstain") | No (manual only) |
| Compounding (B3TR->VOT3) | Auto | Manual |
| Token custody | Leaves wallet | Stays in wallet |
| Centralization | Single entity | Many relayers |
| Cost to apps | Apps pay veDelegate | Apps earn fees |

veDelegate: docs.vedelegate.vet / github.com/vechain-energy/vedelegate-for-dapps

## Smart Contracts Detail

### XAllocationVoting.sol (v8)

Auto-voting added in v8 via `AutoVotingLogicUpgradeable` module.

**Storage** (in AutoVotingLogic library):

- `_autoVotingEnabled`: Checkpointed per-user status (changes take effect next round)
- `_userVotingPreferences`: Array of app IDs per user (max 15, validated, no duplicates)
- `_totalAutoVotingUsers`: Checkpointed total count

**Key functions:**

```solidity
toggleAutoVoting(address user)                         // Enable/disable
setUserVotingPreferences(bytes32[] memory appIds)      // Set apps (1-15)
castVoteOnBehalfOf(address voter, uint256 roundId)     // Relayer executes vote
getUserVotingPreferences(address)                      // View preferences
isUserAutoVotingEnabled(address)                       // Current status
isUserAutoVotingEnabledForRound(address, uint256)      // Status at round snapshot
getTotalAutoVotingUsersAtRoundStart()                  // Count at last emission
getTotalAutoVotingUsersAtTimepoint(uint48)             // Historical count
```

**Vote execution** (`castVoteOnBehalfOf`):

1. Validate early access (registered relayer during window)
2. Get user preferences, filter eligible apps
3. Split voting power equally across eligible apps
4. Cast via internal `_countVote()`
5. Register VOTE action on RelayerRewardsPool (3 weight points)

### VoterRewards.sol (v6)

V6 added relayer fee integration. Fee deduction happens HERE during `claimReward()`.

**V6 storage:** `xAllocationVoting`, `relayerRewardsPool`

**Fee flow in `claimReward(uint256 cycle, address voter)`:**

1. Check user had auto-voting at round start (checkpointed)
2. Calculate raw rewards (voting + GM reward)
3. If auto-voting: `fee = min(totalReward * 10/100, 100 B3TR)`
4. Fee proportionally split between voting and GM reward
5. Fee approved + deposited to `RelayerRewardsPool.deposit(fee, cycle)`
6. `registerRelayerAction(msg.sender, voter, cycle, CLAIM)` - credits caller with 1 weight point
7. Net reward transferred to voter wallet

**Important:** `msg.sender` calling `claimReward()` IS the relayer credited for CLAIM action.

**Early access:** During window, `validateClaimDuringEarlyAccess()` reverts if caller is the voter or not a registered relayer.

### RelayerRewardsPool.sol (v1)

Manages registration, action tracking, reward distribution.

**Storage:**

```text
totalRewards[roundId]                    // Pool amount (funded by fees)
relayerWeightedActions[roundId][relayer] // Per-relayer weighted work
totalWeightedActions[roundId]            // Expected weighted total
completedWeightedActions[roundId]        // Completed weighted total
registeredRelayers[address]              // Registration mapping
relayerAddresses[]                       // All registered addresses
voteWeight = 3                           // Points per vote action
claimWeight = 1                          // Points per claim action
earlyAccessBlocks = 432,000              // ~5 days on VeChain
relayerFeePercentage = 10               // 10%
feeCap = 100 ether                       // 100 B3TR
```

**Reward formula:**

```text
relayerShare = (relayerWeightedActions / completedWeightedActions) * totalRewards
```

**Claimability:** `isRewardClaimable(roundId)` requires:

- Round ended (`emissions.isCycleEnded(roundId)`)
- All work done (`completedWeightedActions >= totalWeightedActions`)

**Registration (open to anyone):**

- `registerRelayer()` — self-registration, callable by anyone
- `unregisterRelayer(address)` — callable by admin or the relayer itself
- `setTotalActionsForRound(roundId, userCount)` - sets expected = userCount x 2 actions, userCount x 4 weighted
- `reduceExpectedActionsForRound(roundId, userCount)` - for ineligible users
- `registerRelayerAction(relayer, voter, roundId, action)` - record work
- `deposit(amount, roundId)` - fund pool

**Early access:**

- Vote window: `roundSnapshot + earlyAccessBlocks`
- Claim window: `roundDeadline + earlyAccessBlocks`
- During: only registered relayers, user can't self-act
- After: anyone can act

## Auto-Voting Lifecycle (Per Round)

```text
Round N: User enables auto-voting + sets preferences (checkpointed)
Round N+1:
  1. startNewRound() - snapshot locks auto-voting status
  2. setTotalActionsForRound(roundId, userCount)
  3. Relayers call castVoteOnBehalfOf() for each user
     - Ineligible users: reduceExpectedActionsForRound()
     - Each successful vote: +3 weighted points to relayer
  4. Round ends (deadline block)
  5. Relayers call VoterRewards.claimReward() for each user
     - Fee deducted and deposited to pool
     - Each successful claim: +1 weighted point to relayer
  6. All actions complete -> pool unlocked
  7. Relayers call RelayerRewardsPool.claimRewards()
```

## Relayer Node (relayer-node/)

Standalone CLI tool. No monorepo dependency.

**Deps:** `@vechain/sdk-core`, `@vechain/sdk-network`, `@vechain/vebetterdao-contracts`

```text
relayer-node/src/
  index.ts      # Entry, env parsing, main loop, SIGINT
  config.ts     # Mainnet + testnet-staging addresses
  contracts.ts  # 26 view functions + event pagination
  relayer.ts    # Batch vote/claim with isolation/retry
  display.ts    # Terminal UI (box drawing + chalk)
  types.ts      # Shared interfaces
```

**Env vars:** `MNEMONIC` / `RELAYER_PRIVATE_KEY`, `RELAYER_NETWORK`, `RUN_ONCE`, `DRY_RUN`

**Cycle:** Discover users from events -> filter voted -> batch castVoteOnBehalfOf -> batch claimReward -> loop 5min

## Relayer Dashboard (apps/relayer-dashboard/)

Static Next.js 14 (output: "export"), Chakra UI v3, VeChain Kit, Recharts. GitHub Pages under /b3tr.

**Data:** Static `report.json` (hourly GH Action, temporary) + on-chain reads via `useCallClause`

**Pages** (state-based nav, not file routing):

- Home: StatsCards (2x2), RoundsChart, RoundsList, info cards
- My Relayer: ConnectedWallet view
- Info: BecomeRelayer + AppsAsRelayers
- Round detail: `/round?roundId=X` - 2-col layout, summary/actions/financials

**Hooks:**

- `contracts.ts` - ABIs + addresses from `@repo/config`
- `useCurrentRoundId` - XAllocationVoting.currentRoundId()
- `useTotalAutoVotingUsers` - getTotalAutoVotingUsersAtTimepoint()
- `useRegisteredRelayers` - getRegisteredRelayers()
- `useRoundRewardStatus` - isRewardClaimable() + getTotalRewards()
- `useReportData` - fetches /data/report.json
- `useB3trToVthoRate` - oracle exchange rate

**Commands:** `yarn relayer:dev:staging`, `yarn relayer:dev:mainnet`, `yarn relayer:build:staging`, `yarn relayer:build:mainnet`

## Gas Cost Analysis

| Action | Gas | VTHO | B3TR equiv |
| --- | --- | --- | --- |
| Vote (5-8 apps) | ~441K | ~4.41 | ~0.075 |
| Claim | ~208K | ~2.08 | ~0.035 |
| **Total/user/round** | | **~6.49** | **~0.11** |

Average user: ~10.8k-22.6k VOT3, earns ~90-190 B3TR/round.
At 10% fee: ~9-19 B3TR per user into pool. Relayer cost: ~0.11 B3TR. Margin: ~8.9-18.9 B3TR/user.

## External Resources

- Docs: https://docs.vebetterdao.org/vebetter/automation
- Governance proposal: https://governance.vebetterdao.org/proposals/93450486232994296830196736391400835825360450263361422145364815974754963306849
- Discourse: https://vechain.discourse.group/t/vebetterdao-proposal-auto-voting-for-x-allocation-with-gasless-voting-and-relayer-rewards/559
- NPM: `@vechain/vebetterdao-contracts`
- Contracts source: https://github.com/vechain/vebetterdao-contracts
