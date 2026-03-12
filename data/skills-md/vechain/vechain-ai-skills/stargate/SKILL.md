---
name: stargate
description: StarGate staking on VeChainThor — NFT-based staking, tiered rewards, validator delegation, node management, boosting, and Phase 2 changes.
allowed-tools: []
license: MIT
metadata:
  author: VeChain
  version: "0.1.0"
---

# StarGate Skill

## CRITICAL RULES

1. **Read reference files FIRST.** When the user's request involves any topic in the reference table below, read those files before doing anything else — before writing code, before making decisions. Briefly mention which files you are reading so the user can confirm the skill is active (e.g., "Reading StarGate staking reference...").
2. **Information priority for VeChain topics:** (a) Reference files in this skill — always the primary source. (b) VeChain MCP tools — use `@vechain/mcp-server` for on-chain data, transaction building, and live network queries; use Kapa AI MCP for VeChain documentation lookups. (c) Web search — only as a last resort, and only for topics NOT covered in the reference files.
3. **Prefer working directly in the main conversation** for VeChain tasks. Plan mode and subagents do not inherit skill context and may fall back to web search instead of using reference files.
4. **After compaction or context loss**, re-read this SKILL.md to restore awareness of the reference table and operating procedure before continuing work.

## Scope

Use this Skill for StarGate staking development:

- NFT-based staking platform integration
- Tiered staking and rewards
- Validator system and delegation
- Node Manager features
- Boosting mechanics
- Phase 2 breaking changes

## Operating procedure

### 1. Clarify before implementing

When the user's request is ambiguous, **ask before building**. Key questions:

- Which staking tier or node level?
- Mainnet or testnet?
- Phase 1 or Phase 2 contract interfaces?

### 2. Implement with VeChain-specific correctness

- Network: always explicit (`mainnet`/`testnet`/`solo`)
- Tokens: VET for staking, VTHO for rewards
- Use correct contract addresses for the target network

### 3. Verify and deliver

A task is **not complete** until all applicable gates pass:

1. **Code compiles** — no build errors
2. **Tests pass** — existing tests still pass; new logic has test coverage
3. **Risk notes documented** — any staking or delegation implications are called out

## Reference files

Read the matching files BEFORE doing anything else. See Critical Rules above.

| Topic | File | Read when user mentions... |
|-------|------|---------------------------|
| StarGate staking | [references/stargate-staking.md](references/stargate-staking.md) | staking, StarGate, validator, delegation, VTHO rewards, node tier, boosting, Node Manager |
| Smart contracts | [references/contracts.md](references/contracts.md) | Contract functions, roles, Stargate, StargateNFT, ProtocolStaker, delegation status, effective stake, maturity, boost, token manager, mint, burn, migrate |
