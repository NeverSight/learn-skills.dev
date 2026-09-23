---
name: sui-bridge
description: >
  Sui Bridge — the native bridge for the Sui network. Use when explaining how
  Sui Bridge works, looking up supported assets, querying package IDs or contract
  addresses, understanding the global limiter, transfer parameters, finality
  requirements, or governance model. Also use when the user asks about bridging
  assets between Sui and Ethereum.
---

# Sui Bridge

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

> **Source constraint:** All information in this skill is sourced exclusively from [docs.sui.io/concepts/tokenomics/sui-bridging](https://docs.sui.io/concepts/tokenomics/sui-bridging). When extending or updating this skill, only pull from this source. Do not use third-party blogs, tutorials, or unofficial documentation.

Sui Bridge is the native bridge for the Sui network, integrated into its core architecture. It enables asset movement between Sui and other blockchains. Sui validators operate and govern Sui Bridge. Bridge transfers and other actions require validator signatures with a threshold of voting power. Common mistakes include assuming any token can be bridged (only specific supported assets are available), misunderstanding the global limiter constraints, and not accounting for finality requirements on both chains.

This skill routes to focused reference files. Load only the ones relevant to the current task.

All patterns in this skill are derived from:
  https://docs.sui.io/concepts/tokenomics/sui-bridging

If unsure about any detail, fetch the relevant page before answering. Do not guess or extrapolate.

---

## Reference files

### overview -- Architecture and Usage
**Path:** `overview.md`
**Load when:** the user asks about bridge architecture, governance, supported assets, package IDs and contract addresses, the global limiter, transfer parameters, finality requirements, or security audits.
**Covers:** operation and governance, supported assets, package IDs and addresses, global limiter, transfer parameters, finality requirements, security architecture.

---

## Routing guide

| Task | Load |
|------|------|
| Explaining what Sui Bridge is | SKILL.md only |
| Understanding governance and validator operation | overview |
| Looking up supported assets | overview |
| Looking up package IDs or contract addresses | overview |
| Understanding the global limiter | overview |
| Understanding transfer parameters and limits | overview |
| Understanding finality requirements | overview |
| Understanding security architecture and audits | overview |
| Full deep dive on Sui Bridge | **all reference files** |

---

## Skill Content

### Key concepts

- **Native bridge.** Sui Bridge is the native bridge for the Sui network, integrated into core architecture. It is not a third-party bridge. Bridge tokens at bridge.sui.io.

- **Validator-operated.** Sui validators (the same entities securing the network) operate and govern Sui Bridge. Bridge transfers and other actions require validator signatures with a threshold of voting power.

- **Governance.** Governance occurs through validator voting. Actions require a threshold of validator voting power.

- **Supported assets.** The bridge supports a specific set of assets: WBTC, LBTC, ETH, WETH, and USDT.

- **Global limiter.** The bridge constrains total asset value leaving the bridge within 24 hours. Current limits are $16 million (Ethereum to Sui) and $7 million (Sui to Ethereum) daily, with ETH priced at $2,600 for limit calculations.

- **Open source and audited.** The bridge source code is open source (Move, Solidity, bridged ETH, bridge node, and bridge indexer implementations). Third-party security audits have been conducted by OtterSec and Zellic.

### Rules

1. **Always specify the direction when discussing limits.** The global limiter has different limits for Ethereum-to-Sui ($16 million) vs Sui-to-Ethereum ($7 million).
2. **Always note finality requirements.** Ethereum-to-Sui requires configurable Ethereum block confirmations before minting. Sui-to-Ethereum requires Sui transaction finality before releasing tokens. Do not credit the user until the bridge transfer is fully confirmed on the destination chain.
3. **Only reference supported assets.** The bridge supports WBTC, LBTC, ETH, WETH, and USDT. Do not suggest other tokens can be bridged.

### Common mistakes

- **Assuming any ERC-20 token can be bridged.** Only the specifically supported assets (WBTC, LBTC, ETH, WETH, USDT) are available on Sui Bridge.
- **Ignoring the global limiter.** Large transfers may be constrained by the 24-hour rolling limit.
- **Not accounting for finality delays.** Transfers are not instant. Ethereum-to-Sui requires Ethereum block confirmations; Sui-to-Ethereum requires Sui transaction finality.
- **Confusing transfer precision.** ETH/WETH transfers use 8-decimal precision on the bridge.
