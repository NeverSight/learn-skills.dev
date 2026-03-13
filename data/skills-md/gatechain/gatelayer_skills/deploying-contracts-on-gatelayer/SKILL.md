---
name: deploying-contracts-on-gatelayer
description: Deploys smart contracts to GateLayer using Foundry. Covers forge create commands, contract verification, and GateScan API key configuration. Use when deploying Solidity contracts to GateLayer Mainnet or Testnet. Covers phrases like "deploy contract to GateLayer", "forge create on GateLayer", "verify contract on GateScan", "get testnet GT", "GateLayer faucet", "how do I deploy to GateLayer", or "publish my contract".
---

# Deploying Contracts on GateLayer

## Prerequisites

1. Configure RPC endpoint (testnet: `https://gatelayer-testnet.gatenode.cc`, mainnet: `https://gatelayer-mainnet.gatenode.cc`)
2. Store private keys in Foundry's encrypted keystore — **never commit keys**
3. [Obtain testnet GT](#obtaining-testnet-GT) from faucet (testnet only)

## Security

- **Never commit private keys** to version control — use Foundry's encrypted keystore (`cast wallet import`)
- **Never hardcode API keys** in source files — use environment variables or `foundry.toml` with `${ENV_VAR}` references
- **Never expose `.env` files** — add `.env` to `.gitignore`
- **Use production RPC providers** (not public endpoints) for mainnet deployments to avoid rate limits and data leaks
- **Verify contracts on GateScan** to enable public audit of deployed code

## Input Validation

Before constructing shell commands, validate all user-provided values:

- **contract-path**: Must match `^[a-zA-Z0-9_/.-]+\.sol:[a-zA-Z0-9_]+$`. Reject paths with spaces, semicolons, pipes, or backticks.
- **rpc-url**: Must be a valid HTTPS URL (`^https://[^\s;|&]+$`). Reject non-HTTPS or malformed URLs.
- **keystore-account**: Must be alphanumeric with hyphens/underscores (`^[a-zA-Z0-9_-]+$`).


Do not pass unvalidated user input into shell commands.

## Obtaining Testnet GT

Testnet GT is required to pay gas on GateLayer Testnet. 
Use the [Gatelayer Faucet](https://www.gatescan.org/gatechain-testnet/en/faucet) to claim it. Supported token :GT  claims are capped at 0.1 GT per claim, 1 claims per 24 hours.

### Gatelayer UI (recommended for quick setup)

> **Agent behavior:** If you have browser access, navigate to the portal and claim directly. Otherwise, ask the user to complete these steps and provide the funded wallet address.



1. Go to [ Gatelayer Faucets](https://www.gatescan.org/gatechain-testnet/en/faucet)
2. Select **Gatelayer** network
3. Enter the wallet address and click **Claim**
4. Verify on [Gatelayer Testnet Scan](https://www.gatescan.org/gatelayer-testnet) that the funds arrived




## Deployment and Verify Commands

### Testnet

```bash
forge create src/MyContract.sol:MyContract \
  --rpc-url https://gatelayer-testnet.gatenode.cc \
  --account <keystore-account> \
  --verify \
  --verifier-url 'https://www.gatescan.org/gatelayer-testnet/api' \
  --verifier blockscout

```

### Mainnet

```bash
forge create src/MyContract.sol:MyContract \
  --rpc-url https://gatelayer-mainnet.gatenode.cc \
  --account <keystore-account> \
  --verify \
  --verifier-url 'https://www.gatescan.org/gatelayer/api' \
  --verifier blockscout
```

## Key Notes

- Contract format: `<contract-path>:<contract-name>`
- Explorers: www.gatescan.org/gatelayer (mainnet), www.gatescan.org/gatelayer-testnet (testnet)

## Common Issues

| Error | Cause |
|-------|-------|
| `nonce has already been used` | Node sync incomplete |
| Transaction fails | Insufficient GT for gas — obtain from faucet |
| Verification fails | Wrong RPC endpoint for target network |

