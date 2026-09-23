---
name: sui-networks-gas
description: >
  Sui network environments and gas economics. Use when the user asks about
  Mainnet, Testnet, Devnet, or Localnet differences, gas cost calculations
  (computation + storage - rebate), gas budgets, epochs, or how the Sui network
  operates at a high level. This skill covers network concepts, not CLI commands.

  For CLI client setup, address management, faucets, and explorers, see the
  `sui-client` skill. For installing the Sui CLI, see the `sui-install` skill.
---

# Sui Networks and Gas

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

> **Source constraint:** All information in this skill is sourced exclusively from [docs.sui.io](https://docs.sui.io). When extending or updating this skill, only pull from this source. Do not use third-party blogs, tutorials, or unofficial documentation.

---

## Related skills

| Topic | Skill |
|-------|-------|
| CLI client configuration, addresses, faucets, explorers | `sui-client/` |
| Installing the Sui CLI (suiup) | `sui-install/` |
| Move project setup and Move.toml | `sui-move-project/` |
| Publishing and upgrading packages | `sui-publish/` |

---

## Sui networks

Sui operates four network environments:

- **Mainnet:** Production network. SUI tokens have real monetary value. Use for final deployments.
- **Testnet:** Mirrors Mainnet features. Free SUI tokens from faucets. Use for integration testing and staging.
- **Devnet:** Development network. Free SUI tokens. Use for early-stage development and experimentation.
- **Localnet:** Runs locally on your machine. Use for offline development and unit testing.

## Gas cost model

Every transaction on Sui requires SUI tokens to pay gas. The total gas cost is:

**gas cost = computation cost + storage cost - storage rebate**

- **Computation cost:** Proportional to the computational effort of executing the transaction.
- **Storage cost:** The cost of storing new or expanded objects onchain. You pay for the bytes your objects occupy.
- **Storage rebate:** When a transaction deletes objects or reduces their size, you receive a rebate for the storage freed. This incentivizes cleaning up unused state.

The gas budget (`--gas-budget`) sets the maximum you are willing to pay. If the transaction exceeds the budget, it fails and a portion of the gas budget is still charged. On Testnet and Devnet, tokens are free through faucets (see the `sui-client` skill for faucet methods). Gas prices can vary per epoch; query the current gas price through the RPC.

## Epochs

An epoch is a fixed time period during which the validator set and gas price remain constant. On Mainnet, one epoch is approximately 24 hours. At the epoch boundary, the network processes staking rewards, rotates validators, and updates the gas price. Use `ctx.epoch()` to read the current epoch number in Move and `ctx.epoch_timestamp_ms()` for the epoch start time.

## Rules

- Always specify `--gas-budget` when submitting transactions from the CLI.
- Use `sui client switch --env <ENV>` to change networks. Do not edit `client.yaml` manually.

## Common mistakes

- **Forgetting to switch networks.** Publishing to Mainnet when you meant Testnet. Always verify with `sui client active-env`.
- **Running out of gas on Testnet/Devnet.** Use the faucet (see `sui-client` skill) to get free tokens.
