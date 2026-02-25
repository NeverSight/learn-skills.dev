---
name: deploying-contracts-on-base
description: Deploys smart contracts to Base using Foundry. Covers forge create commands, contract verification, testnet faucet setup via CDP, and BaseScan API key configuration. Use when deploying Solidity contracts to Base Mainnet or Sepolia testnet. Covers phrases like "deploy contract to Base", "forge create on Base", "verify contract on BaseScan", "get testnet ETH", "Base Sepolia faucet", "how do I deploy to Base", or "publish my contract".
---

# Deploying Contracts on Base

## Prerequisites

1. Configure RPC endpoint (testnet: `sepolia.base.org`, mainnet: `mainnet.base.org`)
2. Store private keys in Foundry's encrypted keystore — **never commit keys**
3. [Obtain testnet ETH](#obtaining-testnet-eth-via-cdp-faucet) from CDP faucet (testnet only)
4. [Get a BaseScan API key](#obtaining-a-basescan-api-key) for contract verification

## Security

- **Never commit private keys** to version control — use Foundry's encrypted keystore (`cast wallet import`)
- **Never hardcode API keys** in source files — use environment variables or `foundry.toml` with `${ENV_VAR}` references
- **Never expose `.env` files** — add `.env` to `.gitignore`
- **Use production RPC providers** (not public endpoints) for mainnet deployments to avoid rate limits and data leaks
- **Verify contracts on BaseScan** to enable public audit of deployed code

## Input Validation

Before constructing shell commands, validate all user-provided values:

- **contract-path**: Must match `^[a-zA-Z0-9_/.-]+\.sol:[a-zA-Z0-9_]+$`. Reject paths with spaces, semicolons, pipes, or backticks.
- **rpc-url**: Must be a valid HTTPS URL (`^https://[^\s;|&]+$`). Reject non-HTTPS or malformed URLs.
- **keystore-account**: Must be alphanumeric with hyphens/underscores (`^[a-zA-Z0-9_-]+$`).
- **etherscan-api-key**: Must be alphanumeric (`^[a-zA-Z0-9]+$`).

Do not pass unvalidated user input into shell commands.

## Obtaining Testnet ETH via CDP Faucet

Testnet ETH is required to pay gas on Base Sepolia. Use the [CDP Faucet](https://portal.cdp.coinbase.com/products/faucet) to claim it. Supported tokens: ETH, USDC, EURC, cbBTC. ETH claims are capped at 0.0001 ETH per claim, 1000 claims per 24 hours.

### Option A: CDP Portal UI (recommended for quick setup)

> **Agent behavior:** If you have browser access, navigate to the portal and claim directly. Otherwise, ask the user to complete these steps and provide the funded wallet address.

1. Sign in to [CDP Portal](https://portal.cdp.coinbase.com/signin) (create an account at [portal.cdp.coinbase.com/create-account](https://portal.cdp.coinbase.com/create-account) if needed)
2. Go to [Faucets](https://portal.cdp.coinbase.com/products/faucet)
3. Select **Base Sepolia** network
4. Select **ETH** token
5. Enter the wallet address and click **Claim**
6. Verify on [sepolia.basescan.org](https://sepolia.basescan.org) that the funds arrived

### Option B: Programmatic via CDP SDK

Requires a [CDP API key](https://portal.cdp.coinbase.com/projects/api-keys) and [Wallet Secret](https://portal.cdp.coinbase.com/products/server-wallets).

```bash
npm install @coinbase/cdp-sdk dotenv
```

```typescript
import { CdpClient } from "@coinbase/cdp-sdk";
import dotenv from "dotenv";
dotenv.config();

const cdp = new CdpClient();
const account = await cdp.evm.createAccount();

const faucetResponse = await cdp.evm.requestFaucet({
  address: account.address,
  network: "base-sepolia",
  token: "eth",
});

console.log(`Funded: https://sepolia.basescan.org/tx/${faucetResponse.transactionHash}`);
```

Environment variables needed in `.env`:

```
CDP_API_KEY_ID=your-api-key-id
CDP_API_KEY_SECRET=your-api-key-secret
CDP_WALLET_SECRET=your-wallet-secret
```

To fund an **existing** wallet instead of creating a new one, pass its address directly to `requestFaucet`.

## Obtaining a BaseScan API Key

A BaseScan API key is required for the `--verify` flag to auto-verify contracts on BaseScan. BaseScan uses the same account system as Etherscan.

> **Agent behavior:** If you have browser access, navigate to the BaseScan site and create the key. Otherwise, ask the user to complete these steps and provide the API key.

1. Go to [basescan.org/myapikey](https://basescan.org/apidashboard) (or [etherscan.io/myapikey](https://etherscan.io/apidashboard) — same account works)
2. Sign in or create a free account
3. Click **Add** to create a new API key
4. Copy the key and set it in your environment:

```bash
export ETHERSCAN_API_KEY=your-basescan-api-key
```

Alternatively, pass it directly to forge:

```bash
forge create ... --etherscan-api-key <your-key>
```

Or add it to `foundry.toml`:

```toml
[etherscan]
base-sepolia = { key = "${ETHERSCAN_API_KEY}", url = "https://api-sepolia.basescan.org/api" }
base = { key = "${ETHERSCAN_API_KEY}", url = "https://api.basescan.org/api" }
```

## Deployment Commands

### Testnet

```bash
forge create src/MyContract.sol:MyContract \
  --rpc-url https://sepolia.base.org \
  --account <keystore-account> \
  --verify \
  --etherscan-api-key $ETHERSCAN_API_KEY
```

### Mainnet

```bash
forge create src/MyContract.sol:MyContract \
  --rpc-url https://mainnet.base.org \
  --account <keystore-account> \
  --verify \
  --etherscan-api-key $ETHERSCAN_API_KEY
```

## Key Notes

- Contract format: `<contract-path>:<contract-name>`
- `--verify` flag auto-verifies on BaseScan (requires API key)
- Explorers: basescan.org (mainnet), sepolia.basescan.org (testnet)
- CDP Faucet docs: [docs.cdp.coinbase.com/faucets](https://docs.cdp.coinbase.com/faucets/introduction/quickstart)

## Common Issues

| Error | Cause |
|-------|-------|
| `nonce has already been used` | Node sync incomplete |
| Transaction fails | Insufficient ETH for gas — [claim from faucet](#obtaining-testnet-eth-via-cdp-faucet) |
| Verification fails | Wrong RPC endpoint for target network |
| Verification 403/unauthorized | Missing or invalid BaseScan API key |
