---
name: uniswap-v4
description: Uniswap v4 core pool logic — singleton PoolManager, unlock/callback, pool actions, hooks, and types.
metadata:
  author: Hairy
  version: "2026.2.9"
  source: Generated from https://github.com/Uniswap/v4-core, scripts at https://github.com/antfu/skills
---

> Skill based on Uniswap v4 Core (Uniswap/v4-core), generated at 2026-02-09.

Uniswap v4 is an AMM with a singleton PoolManager: all pool state lives in one contract. Interactions go through `unlock` → `unlockCallback`, where callers perform swaps, liquidity changes, and donations, then settle balance deltas before the callback returns. Pools can attach hooks for lifecycle callbacks (initialize, add/remove liquidity, swap, donate).

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Architecture | Singleton, unlock/callback flow, delta settlement | [core-architecture](references/core-architecture.md) |
| Unlock callback | IUnlockCallback, when to use unlock, security | [core-unlock-callback](references/core-unlock-callback.md) |
| Pool actions | initialize, swap, modifyLiquidity, donate, take, settle, sync, mint, burn, clear | [core-pool-actions](references/core-pool-actions.md) |
| Types | PoolKey, PoolId, Currency, BalanceDelta, ModifyLiquidityParams, SwapParams | [core-types](references/core-types.md) |

## Features

### Hooks

| Topic | Description | Reference |
|-------|-------------|-----------|
| Hooks | IHooks lifecycle, address-based flags, before/after callbacks | [features-hooks](references/features-hooks.md) |
