---
name: token-lifecycle
description: Reference for Doppler token creation, vesting, inflation, and factory selection across DERC20, DERC2080, CloneERC20, and CloneDERC20VotesV2 paths.
metadata:
  author: doppler
  version: "2.0"
---

> **Source References**: Code citations link to raw GitHub files pinned to commit `46bad16d`.

# Token Lifecycle

## When to use
- You are choosing a token factory for a launch
- You need vesting/inflation semantics for Doppler asset tokens
- You are debugging vesting release, pool lock behavior, or mint-rate logic

## Prerequisites
- Determine required token capabilities (votes, permit, clone vs full deployment)
- Confirm Airlock-compatible factory interface (`ITokenFactory`)

## Core workflow
1. Pick factory path:
   - `TokenFactory` / `DERC20`
   - `TokenFactory80` / `DERC2080`
   - `CloneERC20Factory` / `CloneERC20`
   - `CloneERC20VotesFactory` / `CloneERC20Votes`
   - `CloneDERC20VotesV2Factory` / `CloneDERC20VotesV2` (multi-schedule vesting)
2. Validate token data encoding expected by selected factory.
3. Validate vesting schedule constraints and per-address/global premint caps.
4. Verify pool lock/unlock timing relative to migration and inflation mint start.

## Quick facts
| Family | Votes | Vesting model | Deployment style |
|---|---|---|---|
| `DERC20` / `DERC2080` | Yes | Single-schedule style | Full deployment |
| `CloneERC20` | No | Single-schedule style | ERC1167 clone |
| `CloneERC20Votes` | Yes | Single-schedule style | ERC1167 clone |
| `CloneDERC20VotesV2` | Yes | Multi-schedule vesting | ERC1167 clone |

## Failure modes
- Mismatched encoded token data vs selected factory ABI
- Invalid vesting schedule arrays or lengths
- Premint caps exceeded per address or globally
- Attempting inflation mint before unlock/initial mint window

## References
- [FACTORIES.md](references/FACTORIES.md)
- [VESTING.md](references/VESTING.md)
- Source: `doppler/src/tokens/*.sol` (especially `CloneDERC20VotesV2.sol`, `CloneDERC20VotesV2Factory.sol`)

## Related skills
- [v3-static-auction](../v3-static-auction/SKILL.md)
- [v4-dynamic-auction](../v4-dynamic-auction/SKILL.md)
- [v4-multicurve-auction](../v4-multicurve-auction/SKILL.md)
