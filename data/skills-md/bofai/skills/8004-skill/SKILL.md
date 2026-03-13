---
name: 8004-skill
description: ERC-8004 Trustless Agents - Register and manage AI agent identities on TRON and BSC blockchains with on-chain reputation tracking
---

# ERC-8004: Trustless Agents on TRON & BSC

On-chain identity, reputation, and validation for autonomous agents on TRON. **Now live on TRON Mainnet + BSC Mainnet!**

## Overview

ERC-8004 provides three registries on TRON and BSC blockchains:
- **Identity Registry** - TRC-721 agent identities with registration metadata
- **Reputation Registry** - Signed feedback scores between agents/clients
- **Validation Registry** - Independent verification (zkML, TEE, stakers)

**Multi-Chain:** Same protocol works on TRON and BSC (BNB Smart Chain) - both fully deployed!

## Quick Reference

### Register Agent
```bash
# TRON Mainnet
node scripts/register.js --uri "ipfs://..." --chain tron --network mainnet

# TRON Testnet
node scripts/register.js --uri "ipfs://..." --chain tron --network nile

# BSC Mainnet
node scripts/register.js --uri "ipfs://..." --chain bsc --network mainnet

# BSC Testnet
node scripts/register.js --uri "ipfs://..." --chain bsc --network testnet

# Register without URI (set later)
node scripts/register.js --chain tron --network nile
```

### Private Key Setup
```bash
# Set once, works for both TRON and BSC
export TRON_PRIVATE_KEY="your_64_character_hex_private_key"
```

## Networks

### TRON Networks

| Network | Status | Identity Registry | Reputation Registry | Validation Registry |
|---------|--------|-------------------|---------------------|---------------------|
| **Mainnet** | Live | `TFLvivMdKsk6v2GrwyD2apEr9dU1w7p7Fy` | `TFbvfLDa4eFqNR5vy24nTrhgZ74HmQ6yat` | `TLCWcW8Qmo7QMNoAKfBhGYfGpHkw1krUEm` |
| **Nile** | Live | `TDDk4vc69nzBCbsY4kfu7gw2jmvbinirj5` | `TBVaGd6mBuGuN5ebcvPvRaJo4rtEWqsW6Y` | `TGGkHDHhBzhFcLNcEogAWJkvfFYy4jyrSw` |
| **Shasta** | Live | `TH775ZzfJ5V25EZkFuX6SkbAP53ykXTcma` | `TTkds2ZZKBTChZHho4wcWAa7eWQTxh5TUT` | `TQBFHtKRiaQjc1xp4LtmmXKYdA7JLN89w3` |

**Note:** TRON deployments implement TRC-8004 (TRON version of ERC-8004). Query scripts use compatibility mode:
- ✅ Always available: `ownerOf`, `tokenURI` (ERC-721 standard)
- ⚠️ May vary: `agentURI`, `getAgentWallet`, `agentExists` (ERC-8004 extensions)

### BSC Networks

| Network | Status | Identity Registry | Reputation Registry | Validation Registry |
|---------|--------|-------------------|---------------------|---------------------|
| **BSC Mainnet** | Live | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` | `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63` | `0x8004Cc8439f36fd5F9F049D9fF86523Df6dAAB58` |
| **BSC Testnet** | Live | `0x8004A818BFB912233c491871b3d84c89A494BD9e` | `0x8004B663056A597Dffe9eCcC1965A193B7388713` | `0x8004Cb1BF31DAf7788923b405b754f57acEB4272` |

**Note:** BSC deployments use full ERC-8004 specification with all standard methods.

**Multi-Chain Usage:**
```bash
# TRON
node scripts/register.js --uri "ipfs://..." --chain tron --network mainnet

# BSC
node scripts/register.js --uri "ipfs://..." --chain bsc --network mainnet
```

Contract addresses and ABIs in `lib/contracts.json`. 

## Registration File Format

```json
{
  "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  "name": "your-agent-name",
  "description": "Agent description...",
  "image": "ipfs://...",
  "services": [
    { "name": "A2A", "endpoint": "https://agent.example/.well-known/agent-card.json", "version": "0.3.0" },
    { "name": "MCP", "endpoint": "https://mcp.agent.tron/", "version": "2025-06-18" }
  ],
  "registrations": [
    { "agentRegistry": "tron:728126428:TFLvivMdKsk6v2GrwyD2apEr9dU1w7p7Fy", "agentId": "1" }
  ],
  "supportedTrust": ["reputation", "crypto-economic", "tee-attestation"]
}
```

Template at `templates/registration.json`.

## Reputation Scores

The reputation system uses signed fixed-point numbers (`value` + `valueDecimals`):

| Tag | Meaning | Example | value | decimals |
|-----|---------|---------|-------|----------|
| quality | Quality (0-100) | 87/100 | 87 | 0 |
| uptime | Uptime % | 99.77% | 9977 | 2 |
| yield | Yield % | -3.2% | -32 | 1 |
| latency | Latency ms | 560ms | 560 | 0 |

## Trust Models

ERC-8004 supports three pluggable trust models:
- **Reputation-based** - Client feedback with scores, tags, and metadata
- **Crypto-economic** - Stake-secured validation with economic incentives
- **Crypto-verification** - TEE attestations and zkML proofs

## Dependencies

- `node` & `npm` - JavaScript runtime and package manager
- `tronweb` - TRON JavaScript SDK (`npm install tronweb`)
- Private key configuration (choose one):
  - Environment variable: `TRON_PRIVATE_KEY` or `PRIVATE_KEY`
  - File: `~/.clawdbot/wallets/.deployer_pk`
- IPFS: Set `PINATA_JWT` for uploads, or upload manually

## TRON-Specific Features

### Address Format
- TRON uses Base58 addresses starting with 'T' (e.g., `TFLvivMdKsk6v2GrwyD2apEr9dU1w7p7Fy`)
- Scripts automatically handle address conversion

### Network Identifiers
- Mainnet: `tron:728126428` (TRON chain ID)
- Use in registration files: `tron:728126428:TFLvivMdKsk6v2GrwyD2apEr9dU1w7p7Fy`

### Energy & Bandwidth
- TRON uses Energy and Bandwidth instead of gas
- Scripts set `feeLimit: 1000000000` (1000 TRX max)
- Actual costs are typically much lower

## Resources

### Official
- [EIP-8004 Spec](https://eips.ethereum.org/EIPS/eip-8004) - Full specification
- [8004.org](https://8004.org) - Official website
- [Telegram Community](https://t.me/ERC8004) - Builder chat
- [Builder Program](http://bit.ly/8004builderprogram) - Join the ecosystem

### TRON Resources
- [TRON Developers](https://developers.tron.network/) - Official documentation
- [TronScan](https://tronscan.org/) - Block explorer
- [TronWeb](https://github.com/tronprotocol/tronweb) - JavaScript SDK
- [TronGrid](https://www.trongrid.io/) - API service

### Ecosystem
- [Awesome ERC-8004](https://github.com/sudeepb02/awesome-erc8004) - Curated resource list
- [A2A Protocol](https://a2a-protocol.org/) - Agent-to-Agent protocol TRC-8004 extends

## Script Reference

All scripts support multi-chain (TRON + BSC):

- **register.js** - Register new agent on-chain
- **query.js** - Query agent info and reputation
- **search.js** - Semantic search agents via search-service API
- **feedback.js** - Submit feedback/reputation scores
- **set-uri.js** - Update agent metadata URI

Run any script without arguments to see detailed usage information.

## Examples

### Complete Agent Workflow
```bash
# 1. Set private key (works for both TRON and BSC)
export TRON_PRIVATE_KEY="your_private_key"

# 2. Register agent on TRON testnet
node scripts/register.js --uri "ipfs://QmYourHash" --chain tron --network nile

# 3. Query agent info (use ID from step 2)
node scripts/query.js agent 1 --chain tron --network nile

# 4. Submit feedback
node scripts/feedback.js --agent-id 1 --score 95 --tag1 "quality" --chain tron --network nile

# 5. Query reputation
node scripts/query.js reputation 1 --chain tron --network nile

# 6. Update URI if needed
node scripts/set-uri.js --agent-id 1 --uri "ipfs://QmNewHash" --chain tron --network nile

# 7. Semantic search by keyword
node scripts/search.js --query "market order" --url "https://tn-search-service.bankofai.io" --chain-id 3448148188

# 8. Multi-chain search (choose chain(s) based on user request)
node scripts/search.js --query "x402 a2a payment" --chains "56,3448148188"
```

### Multi-Chain Examples
```bash
# Register on BSC testnet
node scripts/register.js --uri "ipfs://..." --chain bsc --network testnet

# Query agent on BSC mainnet
node scripts/query.js agent 1 --chain bsc --network mainnet

# Submit feedback on TRON mainnet
node scripts/feedback.js --agent-id 1 --score 98 --tag1 "quality" --chain tron --network mainnet

# Search only BSC mainnet agents
node scripts/search.js --query "a2a x402" --chain-id 56

# Search all configured chains in search-service
node scripts/search.js --query "merchant recharge" --chains all
```

### Search Chain Selection Rule

- Always choose search chain(s) from user intent instead of hardcoding a default chain.
- Use `--chain-id <id>` for a single chain request.
- Use `--chains "<id1,id2>"` for cross-chain requests.
- Use `--chains all` when user asks to search all available networks.
- Common chain IDs:
  - TRON Nile: `3448148188`
  - BSC Mainnet: `56`

## Troubleshooting

### "TRON_PRIVATE_KEY not set"
```bash
# Option 1: Environment variable (recommended)
export TRON_PRIVATE_KEY="your_64_character_hex_private_key"

# Option 2: File storage
mkdir -p ~/.clawdbot/wallets
echo "your_private_key" > ~/.clawdbot/wallets/.deployer_pk
chmod 600 ~/.clawdbot/wallets/.deployer_pk
```

### "Insufficient balance"
- Ensure your wallet has TRX for transaction fees
- Get testnet TRX from [Nile Faucet](https://nileex.io/join/getJoinPage)

### "Not the owner"
- Only the agent owner can update URI or metadata
- Check ownership with `query.js agent <id>`

## Security Notes

- Never commit private keys to version control
- Use environment variables for sensitive data
- Test on Nile testnet before mainnet deployment
- Verify contract addresses in `lib/contracts.json`

---

*Compatible with ERC-8004 specification. TRON implementation is TRC-8004.*
