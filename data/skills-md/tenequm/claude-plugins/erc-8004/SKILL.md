---
name: erc-8004
description: Build with ERC-8004 Trustless Agents - on-chain agent identity, reputation, validation, and discovery on EVM chains. Use when registering AI agents on-chain, building agent reputation systems, searching/discovering agents, working with the Agent0 SDK (agent0-sdk), or implementing the ERC-8004 standard. Triggers on ERC-8004, Agent0, agent identity, agent registry, agent reputation, trustless agents, agent discovery.
metadata:
  version: "0.1.0"
---

# ERC-8004: Trustless Agents

ERC-8004 is a Draft EIP for discovering, choosing, and interacting with AI agents across organizational boundaries without pre-existing trust. It defines three on-chain registries deployed as per-chain singletons on any EVM chain.

**Authors:** Marco De Rossi (MetaMask), Davide Crapis (EF), Jordan Ellis (Google), Erik Reppel (Coinbase)

**Full spec:** [references/spec.md](references/spec.md)

## When to Use This Skill

- Registering AI agents on-chain (ERC-721 identity)
- Building or querying agent reputation/feedback systems
- Searching and discovering agents by capabilities, trust models, or endpoints
- Working with the Agent0 TypeScript SDK (`agent0-sdk`)
- Implementing ERC-8004 smart contract integrations
- Setting up agent wallets, MCP/A2A endpoints, or OASF taxonomies

## Core Architecture

Three lightweight registries, each deployed as a UUPS-upgradeable singleton:

| Registry | Purpose | Contract |
|----------|---------|----------|
| **Identity** | ERC-721 NFTs for agent identities + registration files | `IdentityRegistryUpgradeable` |
| **Reputation** | Signed fixed-point feedback signals + off-chain detail files | `ReputationRegistryUpgradeable` |
| **Validation** | Third-party validator attestations (stake, zkML, TEE) | `ValidationRegistryUpgradeable` |

**Agent identity** = `agentRegistry` (string `eip155:{chainId}:{contractAddress}`) + `agentId` (ERC-721 tokenId).

Each agent's `agentURI` points to a JSON registration file (IPFS or HTTPS) advertising name, description, endpoints (MCP, A2A, ENS, DID, wallet), OASF skills/domains, trust models, and x402 support.

**See:** [references/contracts.md](references/contracts.md) for full contract interfaces and addresses.

## Quick Start with Agent0 SDK (TypeScript)

```bash
npm install agent0-sdk
```

### Register an Agent

```typescript
import { SDK } from 'agent0-sdk';

const sdk = new SDK({
  chainId: 84532,  // Base Sepolia
  rpcUrl: process.env.RPC_URL,
  privateKey: process.env.PRIVATE_KEY,
  ipfs: 'pinata',
  pinataJwt: process.env.PINATA_JWT,
});

const agent = sdk.createAgent(
  'MyAgent',
  'An AI agent that analyzes crypto markets',
  'https://example.com/agent-image.png'
);

// Configure endpoints and capabilities
await agent.setMCP('https://mcp.example.com', '2025-06-18', true);  // auto-fetches tools
await agent.setA2A('https://example.com/.well-known/agent-card.json', '0.3.0', true);
agent.setENS('myagent.eth');
agent.setActive(true);
agent.setX402Support(true);
agent.setTrust(true, false, false);  // reputation only

// Add OASF taxonomy
agent.addSkill('natural_language_processing/natural_language_generation/summarization', true);
agent.addDomain('finance_and_business/investment_services', true);

// Register on-chain (mints NFT + uploads to IPFS)
const tx = await agent.registerIPFS();
const { result } = await tx.waitConfirmed();
console.log(`Registered: ${result.agentId}`);  // e.g. "84532:42"
```

### Search for Agents

```typescript
const sdk = new SDK({ chainId: 84532, rpcUrl: process.env.RPC_URL });

// Search by capabilities
const agents = await sdk.searchAgents({
  hasMCP: true,
  active: true,
  x402support: true,
  mcpTools: ['financial_analyzer'],
  supportedTrust: ['reputation'],
});

// Get a specific agent
const agent = await sdk.getAgent('84532:42');

// Semantic search
const results = await sdk.searchAgents(
  { keyword: 'crypto market analysis' },
  { sort: ['semanticScore:desc'] }
);
```

### Give Feedback

```typescript
// Prepare optional off-chain feedback file
const feedbackFile = await sdk.prepareFeedbackFile({
  text: 'Accurate market analysis',
  capability: 'tools',
  name: 'financial_analyzer',
  proofOfPayment: { txHash: '0x...', chainId: '8453', fromAddress: '0x...', toAddress: '0x...' },
});

// Submit feedback (value=85 out of 100)
const tx = await sdk.giveFeedback('84532:42', 85, 'starred', '', '', feedbackFile);
await tx.waitConfirmed();

// Read reputation summary
const summary = await sdk.getReputationSummary('84532:42');
console.log(`Average: ${summary.averageValue}, Count: ${summary.count}`);
```

**See:** [references/sdk-typescript.md](references/sdk-typescript.md) for full SDK API reference.

## Registration File Format

Every agent's `agentURI` resolves to this JSON structure:

```json
{
  "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  "name": "MyAgent",
  "description": "What it does, pricing, interaction methods",
  "image": "https://example.com/agent.png",
  "services": [
    { "name": "MCP", "endpoint": "https://mcp.example.com", "version": "2025-06-18", "mcpTools": ["tool1"] },
    { "name": "A2A", "endpoint": "https://example.com/.well-known/agent-card.json", "version": "0.3.0" },
    { "name": "OASF", "endpoint": "https://github.com/agntcy/oasf/", "version": "v0.8.0",
      "skills": ["natural_language_processing/summarization"],
      "domains": ["finance_and_business/investment_services"] },
    { "name": "ENS", "endpoint": "myagent.eth", "version": "v1" },
    { "name": "agentWallet", "endpoint": "eip155:8453:0x..." }
  ],
  "registrations": [
    { "agentId": 42, "agentRegistry": "eip155:84532:0x8004A818BFB912233c491871b3d84c89A494BD9e" }
  ],
  "supportedTrust": ["reputation", "crypto-economic", "tee-attestation"],
  "active": true,
  "x402Support": true
}
```

The `registrations` field creates a bidirectional cryptographic link: the NFT points to this file, and this file points back to the NFT. This enables endpoint domain verification via `/.well-known/agent-registration.json`.

**See:** [references/registration.md](references/registration.md) for best practices (Four Golden Rules) and complete field reference.

## Contract Addresses

All registries deploy to deterministic vanity addresses via CREATE2 (SAFE Singleton Factory):

### Mainnet (Ethereum, Base, Polygon, Arbitrum, Optimism, etc.)

| Registry | Address |
|----------|---------|
| Identity | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |
| Reputation | `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63` |
| Validation | `0x8004Cb1BF31DAf7788923b405b754f57acEB4272` |

### Testnet (Sepolia, Base Sepolia, etc.)

| Registry | Address |
|----------|---------|
| Identity | `0x8004A818BFB912233c491871b3d84c89A494BD9e` |
| Reputation | `0x8004B663056A597Dffe9eCcC1965A193B7388713` |
| Validation | `0x8004Cb1BF31DAf7788923b405b754f57acEB4272` |

Same proxy addresses on: Ethereum, Base, Arbitrum, Avalanche, Celo, Gnosis, Linea, Mantle, MegaETH, Optimism, Polygon, Scroll, Taiko, Monad, BSC + testnets.

## Reputation System

Feedback uses signed fixed-point numbers: `value` (int128) + `valueDecimals` (uint8, 0-18).

| tag1 | Measures | Example | value | valueDecimals |
|------|----------|---------|-------|---------------|
| `starred` | Quality 0-100 | 87/100 | 87 | 0 |
| `reachable` | Endpoint up (binary) | true | 1 | 0 |
| `uptime` | Uptime % | 99.77% | 9977 | 2 |
| `successRate` | Success % | 89% | 89 | 0 |
| `responseTime` | Latency ms | 560ms | 560 | 0 |

Anti-Sybil: `getSummary()` requires a non-empty `clientAddresses` array (caller must supply trusted reviewer list). Self-feedback is rejected (agent owner/operators cannot submit feedback on their own agent).

**See:** [references/reputation.md](references/reputation.md) for full feedback system, off-chain file format, and aggregation details.

## OASF Taxonomy (v0.8.0)

Open Agentic Schema Framework provides standardized skills (136) and domains (204) for agent classification.

**Top-level skill categories:** `natural_language_processing`, `images_computer_vision`, `audio`, `analytical_skills`, `multi_modal`, `agent_orchestration`, `advanced_reasoning_planning`, `data_engineering`, `security_privacy`, `evaluation_monitoring`, `devops_mlops`, `governance_compliance`, `tool_interaction`, `retrieval_augmented_generation`, `tabular_text`

**Top-level domain categories:** `technology`, `finance_and_business`, `healthcare`, `legal`, `education`, `life_science`, `agriculture`, `energy`, `environmental_science`, `government`, `manufacturing`, `transportation`, and more.

Use slash-separated paths: `agent.addSkill('natural_language_processing/natural_language_generation/summarization', true)`.

## Key Concepts

| Term | Meaning |
|------|---------|
| `agentRegistry` | `eip155:{chainId}:{contractAddress}` - globally unique registry identifier |
| `agentId` | ERC-721 tokenId - numeric on-chain identifier (format in SDK: `"chainId:tokenId"`) |
| `agentURI` | URI (IPFS/HTTPS) pointing to agent registration file |
| `agentWallet` | Reserved on-chain metadata key for verified payment address (EIP-712/ERC-1271) |
| `feedbackIndex` | 1-indexed counter of feedback a clientAddress has given to an agentId |
| `supportedTrust` | Array: `"reputation"`, `"crypto-economic"`, `"tee-attestation"` |
| `x402Support` | Boolean flag for Coinbase x402 HTTP payment protocol support |
| OASF | Open Agentic Schema Framework - standardized agent skills/domains taxonomy |
| MCP | Model Context Protocol - tools, prompts, resources, completions |
| A2A | Agent2Agent - authentication, skills via AgentCards, task orchestration |

## Reference Index

| Reference | Content |
|-----------|---------|
| [spec.md](references/spec.md) | Complete ERC-8004 specification (EIP text) |
| [contracts.md](references/contracts.md) | Smart contract interfaces, storage layout, deployment |
| [sdk-typescript.md](references/sdk-typescript.md) | Agent0 TypeScript SDK full API |
| [registration.md](references/registration.md) | Registration file format, Four Golden Rules, domain verification |
| [reputation.md](references/reputation.md) | Feedback system, off-chain files, value encoding, aggregation |
| [search-discovery.md](references/search-discovery.md) | Agent search, subgraph queries, multi-chain discovery |
| [oasf-taxonomy.md](references/oasf-taxonomy.md) | Complete OASF v0.8.0 taxonomy: all 136 skills and 204 domains with slugs |

## Official Resources

- EIP Discussion: https://ethereum-magicians.org/t/erc-8004-trustless-agents/25098
- Contracts: https://github.com/erc-8004/erc-8004-contracts
- Best Practices: https://github.com/erc-8004/best-practices
- SDK Docs: https://sdk.ag0.xyz
- SDK Docs Source: https://github.com/agent0lab/agent0-sdk-docs
- TypeScript SDK: https://github.com/agent0lab/agent0-ts
- Python SDK: https://github.com/agent0lab/agent0-py
- Subgraph: https://github.com/agent0lab/subgraph
- OASF: https://github.com/agntcy/oasf
