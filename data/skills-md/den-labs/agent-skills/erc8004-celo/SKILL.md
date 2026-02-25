---
name: erc8004-celo
description: Register and manage AI agent identities on Celo using ERC-8004 (Trustless Agents). Use this skill when the user wants to register an AI agent on-chain, give or read reputation feedback, request validation, or interact with ERC-8004 identity/reputation/validation registries on Celo mainnet or Celo Sepolia testnet.
---

# ERC-8004: Trustless Agents on Celo

Register your AI agent on Celo with a verifiable on-chain identity, making it discoverable and enabling trust signals through reputation and validation.

## What is ERC-8004?

ERC-8004 is an Ethereum standard for trustless agent identity and reputation, deployed on Celo:

- **Identity Registry** - ERC-721 based agent IDs (your agent gets an NFT)
- **Reputation Registry** - Feedback and trust signals from other agents/users
- **Validation Registry** - Third-party verification of agent work

Website: https://www.8004.org | Spec: https://eips.ethereum.org/EIPS/eip-8004

## Contract Addresses

| Chain | Identity Registry | Reputation Registry |
|---|---|---|
| Celo Mainnet (42220) | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` | `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63` |
| Celo Sepolia (11142220) | `0x8004A818BFB912233c491871b3d84c89A494BD9e` | `0x8004B663056A597Dffe9eCcC1965A193B7388713` |

Explorer links:
- Mainnet: https://celoscan.io/address/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432
- Celo Sepolia: https://celo-sepolia.blockscout.com/address/0x8004A818BFB912233c491871b3d84c89A494BD9e

## Quick Start

### 1. Register Your Agent

```bash
# Set environment variables
export CELO_RPC_URL="https://forno.celo.org"
export PRIVATE_KEY="your-private-key"

# Register with a URI pointing to your agent's registration file
./scripts/register.sh "https://myagent.xyz/agent.json"

# Or register with IPFS (requires PINATA_JWT)
export PINATA_JWT="your-pinata-jwt"
./scripts/register.sh "ipfs"
```

### 2. Check Agent Registration

```bash
# Check if an agent is registered and get its info
./scripts/check-agent.sh <agent-id>
```

### 3. Give Feedback

```bash
# Give reputation feedback to an agent
./scripts/give-feedback.sh <agent-id> <value> <tag1> <tag2>
```

## Registration File Format

Your agent's registration file (see `assets/templates/registration.json`):

```json
{
  "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  "name": "My Celo Agent",
  "description": "An AI agent operating on Celo",
  "image": "https://example.com/avatar.png",
  "services": [
    { "name": "web", "endpoint": "https://myagent.xyz/" },
    { "name": "A2A", "endpoint": "https://myagent.xyz/.well-known/agent-card.json", "version": "0.3.0" },
    { "name": "MCP", "endpoint": "https://mcp.myagent.xyz/", "version": "2025-06-18" }
  ],
  "x402Support": false,
  "active": true,
  "registrations": [
    {
      "agentId": 1,
      "agentRegistry": "eip155:42220:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432"
    }
  ],
  "supportedTrust": ["reputation"]
}
```

## Key Concepts

### Agent Identity (ERC-721 NFT)
- Each agent gets a unique `agentId` (tokenId) on registration
- The NFT owner controls the agent's profile and metadata
- Agents are globally identified by `eip155:42220:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` + `agentId`

### Reputation System
- Anyone can give feedback (except the agent owner themselves)
- Feedback includes a value (int128) with decimals (0-18) plus optional tags
- Common tags: `starred` (quality 0-100), `reachable` (binary), `uptime` (percentage)
- Feedback can be revoked by the original submitter
- Agents can append responses to feedback

### Validation
- Agents request validation from validator contracts
- Validators respond with a score (0-100)
- Supports stake-secured re-execution, zkML, TEE attestation

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `CELO_RPC_URL` | Celo RPC endpoint | Yes (defaults to public RPC) |
| `PRIVATE_KEY` | Wallet private key for signing transactions | Yes |
| `PINATA_JWT` | Pinata API JWT for IPFS uploads | No (only for IPFS registration) |
| `AGENT_NAME` | Agent display name | No |
| `AGENT_DESCRIPTION` | Agent description | No |
| `AGENT_IMAGE` | Avatar URL | No |
| `CELOSCAN_API_KEY` | Celoscan API key for verification | No |

## Celo Network Details

| Parameter | Mainnet | Celo Sepolia Testnet |
|---|---|---|
| Chain ID | 42220 | 11142220 |
| RPC URL | `https://forno.celo.org` | `https://forno.celo-sepolia.celo-testnet.org` |
| Explorer | https://celoscan.io | https://celo-sepolia.blockscout.com |
| Currency | CELO | CELO (test) |
| Faucet | - | https://faucet.celo.org/celo-sepolia |

## Workflow

1. **Get CELO** - You need CELO for gas fees (very low on Celo, ~$0.001 per tx)
2. **Create Registration File** - Generate a JSON following the registration format
3. **Upload to IPFS** (optional) - Pin via Pinata or host at any URL
4. **Register On-Chain** - Call `register(agentURI)` on the Identity Registry
5. **Set Metadata** - Optionally set on-chain metadata and agent wallet
6. **Receive Feedback** - Other agents/users can give reputation signals
7. **Request Validation** - Optionally request third-party verification

## Using with cast (Foundry)

```bash
# Register an agent with a URI
cast send 0x8004A169FB4a3325136EB29fA0ceB6D2e539a432 \
  "register(string)" "https://myagent.xyz/agent.json" \
  --rpc-url https://forno.celo.org \
  --private-key $PRIVATE_KEY

# Read agent URI
cast call 0x8004A169FB4a3325136EB29fA0ceB6D2e539a432 \
  "tokenURI(uint256)" 1 \
  --rpc-url https://forno.celo.org

# Give feedback (value=85, decimals=0, tag1="starred")
cast send 0x8004BAa17C55a88189AE136b182e5fdA19dE9b63 \
  "giveFeedback(uint256,int128,uint8,string,string,string,string,bytes32)" \
  1 85 0 "starred" "" "" "" 0x0000000000000000000000000000000000000000000000000000000000000000 \
  --rpc-url https://forno.celo.org \
  --private-key $PRIVATE_KEY

# Get reputation summary
cast call 0x8004BAa17C55a88189AE136b182e5fdA19dE9b63 \
  "getSummary(uint256,address[],string,string)" \
  1 "[0xREVIEWER_ADDRESS]" "starred" "" \
  --rpc-url https://forno.celo.org
```

## Using with viem/ethers.js

See `references/api-reference.md` for complete TypeScript examples.

## Links

- [ERC-8004 Spec](https://eips.ethereum.org/EIPS/eip-8004)
- [8004.org](https://www.8004.org)
- [GitHub: erc-8004-contracts](https://github.com/agent0-labs/erc-8004-contracts)
- [Celoscan Explorer](https://celoscan.io)
