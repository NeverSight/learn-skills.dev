---
name: taiko
description: Deploy, test, and interact with smart contracts on Taiko networks (Type-1 ZK-EVM rollup on Ethereum). Use when "Taiko", "Hoodi", "L2 deployment", "bridge", "forge", or "Taikoscan" is mentioned. For x402 payment APIs use the taiko-x402 skill instead.
---

# Taiko Development

Build, deploy, and verify smart contracts on Taiko — a Type-1 ZK-EVM based rollup on Ethereum. Taiko targets 2-second block times powered by based preconfirmations.

> **Network Selection:** If the user has not specified "hoodi" or "mainnet", always ask which network to use before proceeding.

## Networks

See [Networks Reference](./references/networks.md) for chain IDs, RPCs, contract addresses, explorers, and API endpoints.

## Quick Decision Guide

| Task | Command/Resource |
|------|------------------|
| Deploy contract | `FOUNDRY_PROFILE=layer2 forge create ...` |
| Verify (Taikoscan) | `forge verify-contract --verifier-url $TAIKOSCAN_API_URL ...` |
| Verify (Blockscout) | `forge verify-contract --verifier blockscout ...` |
| Verify (Etherscan V2) | `forge verify-contract --verifier-url "https://api.etherscan.io/v2/api?chainid=$CHAIN_ID" ...` |
| Fork testing | `FOUNDRY_PROFILE=layer2 forge test --fork-url $TAIKO_RPC` |
| Contract addresses | `MainnetL1Addrs.sol` / `MainnetL2Addrs.sol` / `HoodiL1Addrs.sol` / `HoodiL2Addrs.sol` in [`assets/foundry-template/src/`](./assets/foundry-template/src/) |

## Protocol Knowledge

- [Networks Reference](./references/networks.md) - Chain IDs, RPCs, contract addresses
- [Protocol Overview](./references/protocol-overview.md) - Based rollup architecture
- [EVM Compatibility](./references/evm-compatibility.md) - Shanghai EVM details
- [Foundry Guide](./references/foundry-guide.md) - Complete Foundry setup
- [Security Checklist](./references/security-checklist.md) - Taiko-specific security checks
- [Bridge Interface](./references/bridge-interface.md) - Cross-chain messaging
- [Cross-Chain Patterns](./references/cross-chain-patterns.md) - L1↔L2 patterns
- [Anchor Contract](./references/anchor-contract.md) - L1 data access from L2

## Foundry Setup

Use `assets/foundry-template/` as a starting point.

**Critical:** Always use `FOUNDRY_PROFILE=layer2` for Taiko L2:

```bash
FOUNDRY_PROFILE=layer2 forge build
FOUNDRY_PROFILE=layer2 forge test --fork-url $TAIKO_RPC
```

### foundry.toml (both networks)

```toml
[profile.default]
solc_version = "0.8.30"
evm_version = "prague"

[profile.layer2]
evm_version = "shanghai"
```

See [Networks Reference](./references/networks.md#foundry-config) for RPC and Etherscan config.

## Deploy

```bash
FOUNDRY_PROFILE=layer2 forge create src/MyContract.sol:MyContract \
  --rpc-url $TAIKO_RPC --private-key $PRIVATE_KEY

# With constructor args
FOUNDRY_PROFILE=layer2 forge create src/Token.sol:Token \
  --rpc-url $TAIKO_RPC --private-key $PRIVATE_KEY \
  --constructor-args "TokenName" "TKN" 1000000000000000000000000

# Via script
FOUNDRY_PROFILE=layer2 forge script script/Deploy.s.sol:DeployScript \
  --rpc-url $TAIKO_RPC --private-key $PRIVATE_KEY --broadcast
```

## Verify

### Taikoscan

```bash
# Mainnet
forge verify-contract <ADDRESS> src/MyContract.sol:MyContract \
  --watch --verifier-url https://api.taikoscan.io/api \
  --etherscan-api-key $TAIKOSCAN_API_KEY

# Hoodi
forge verify-contract <ADDRESS> src/MyContract.sol:MyContract \
  --watch --verifier-url https://api-hoodi.taikoscan.io/api \
  --etherscan-api-key $TAIKOSCAN_API_KEY
```

### Blockscout

```bash
# Mainnet
forge verify-contract <ADDRESS> src/MyContract.sol:MyContract \
  --chain-id 167000 --verifier blockscout \
  --verifier-url "https://blockscoutapi.mainnet.taiko.xyz/api?"

# Hoodi
forge verify-contract <ADDRESS> src/MyContract.sol:MyContract \
  --chain-id 167013 --verifier blockscout \
  --verifier-url https://blockscout.hoodi.taiko.xyz/api
```

## Cast CLI

```bash
cast balance <ADDRESS> --rpc-url $TAIKO_RPC
cast chain-id --rpc-url $TAIKO_RPC
cast block-number --rpc-url $TAIKO_RPC
cast gas-price --rpc-url $TAIKO_RPC
cast send <TO> "functionName(args)" --rpc-url $TAIKO_RPC --private-key $PRIVATE_KEY
```

## Getting ETH

**Mainnet:** Bridge from Ethereum via https://bridge.taiko.xyz (24h cooldown for L2→L1)

**Hoodi:** Get test ETH from L1 faucets (see [Networks Reference](./references/networks.md#hoodi-faucets-ethereum-hoodi-l1)), then bridge via https://bridge.hoodi.taiko.xyz

## x402 Payments

Taiko runs live x402 facilitators for HTTP-native USDC payments on Mainnet and Hoodi. For building payment-protected APIs or AI agent clients, use the dedicated **[taiko-x402 skill](../taiko-x402/SKILL.md)** — it covers seller middleware, buyer client setup, and full facilitator configuration.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Invalid EVM version" | Use `FOUNDRY_PROFILE=layer2` |
| "Contract not verified" | Check API endpoint URL and key |
| "Insufficient funds" | Bridge ETH from L1 |
| "Transaction reverted" | Use `cast run <TX_HASH>` to debug |

## Examples

See `examples/` for Python (signal verification, block hash) and Solidity (bridge receiver, cross-chain counter).

## CLI Quick Reference

Use `taiko --json` for structured output parseable by agents:

```bash
taiko network status --json                              # verify network reachability before any operation
taiko network info --json                                # chain ID, contract addresses, gas price
taiko contract verify <ADDR> <id> --network hoodi        # preferred verify method (wraps forge with Taiko config)
taiko bridge status <TX_HASH> --json                     # check bridge relay status
```

All commands return: `{ schema_version, command, status, network, data, errors, warnings, metrics }`

## Related Skills

- **Node setup & L1 requirements:** [taiko-node skill](../taiko-node/SKILL.md)
- **x402 HTTP payments:** [taiko-x402 skill](../taiko-x402/SKILL.md)
- **Private ETH transfers:** [taiko-shadow skill](../taiko-shadow/SKILL.md)

## Resources

- **Docs**: https://docs.taiko.xyz
- **Status**: https://status.taiko.xyz
- **Proofs**: https://proofs.taiko.xyz
- **Code Diff**: https://codediff.taiko.xyz
- **Protocol Source**: https://github.com/taikoxyz/taiko-mono/tree/main/packages/protocol
- **Releases**: https://github.com/taikoxyz/taiko-mono/releases?q=alethia-protocol
